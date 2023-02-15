import subprocess
import os
import re
import random

class Solution:
    def __init__(self, olevel, simd, problem_size_x, problem_size_y, problem_size_z, nthreads, thrdblock_x, thrdblock_y, thrdblock_z) -> None:
        self.olevel = olevel
        self.simd = simd
        self.problem_size_x = problem_size_x
        self.problem_size_y = problem_size_y
        self.problem_size_z = problem_size_z
        self.nthreads = nthreads
        self.thrdblock_x = thrdblock_x
        self.thrdblock_y = thrdblock_y
        self.thrdblock_z = thrdblock_z

    def cost(self, verbose=False):
        result = subprocess.run(['make', f'Olevel={self.olevel}', f'simd={self.simd}', 'last'], stdout=subprocess.DEVNULL)
        if result.returncode != 0:
            raise Exception( f'Failed compiling: { result.returncode }' )
        
        result = subprocess.run(['bin/iso3dfd_dev13_cpu_avx2.exe', 
            self.problem_size_x, self.problem_size_y, self.problem_size_z,
            self.nthreads, '100', self.thrdblock_x, self.thrdblock_y, self.thrdblock_z], capture_output=True)
        if result.returncode != 0:
            raise Exception( f'Failed executing: { result.returncode }' )

        output = result.stdout
        m = re.search('throughput:\s+([\d\.]+)', str(output))
        throughput = m.group(1)
        try:
            throughput = float(throughput)
        except:
            raise ValueError('throughput not a float')
        if verbose:
            print(output)
        return throughput

    def get_neighbors(self):
        neigh = set()

        olevels = set(['-O2', '-O3', '-Ofast'])
        olevels.remove(self.olevel)
        for level in olevels:
            neigh.add((level, self.simd, self.problem_size_x, self.problem_size_y, self.problem_size_z, self.nthreads, self.thrdblock_x, self.thrdblock_y, self.thrdblock_z))
      
        simds = set(['avx', 'avx2', 'avx512'])
        simds.remove(self.simd)
        for simd in simds:
            neigh.add((self.olevel, simd, self.problem_size_x, self.problem_size_y, self.problem_size_z, self.nthreads, self.thrdblock_x, self.thrdblock_y, self.thrdblock_z))
             
        if int(self.thrdblock_x) > 16:
            neigh.add( (self.olevel, self.simd, self.problem_size_x, self.problem_size_y, self.problem_size_z, self.nthreads, str(int(self.thrdblock_x)//2), self.thrdblock_y, self.thrdblock_z) )
        if int(self.thrdblock_y) > 1:
            neigh.add( (self.olevel, self.simd, self.problem_size_x, self.problem_size_y, self.problem_size_z, self.nthreads,  self.thrdblock_x, str(int(self.thrdblock_y)//2), self.thrdblock_z) )
        if int(self.thrdblock_z) > 1:
            neigh.add( (self.olevel, self.simd, self.problem_size_x, self.problem_size_y, self.problem_size_z, self.nthreads, self.thrdblock_x, self.thrdblock_y, str(int(self.thrdblock_z)//2)) )
        if int(self.nthreads) > 1:
            neigh.add( (self.olevel, self.simd, self.problem_size_x, self.problem_size_y, self.problem_size_z, str(int(self.nthreads)//2), self.thrdblock_x, self.thrdblock_y, self.thrdblock_z))
        neigh.add( (self.olevel, self.simd, self.problem_size_x, self.problem_size_y, self.problem_size_z, self.nthreads, str(int(self.thrdblock_x)*2), self.thrdblock_y, self.thrdblock_z) )
        neigh.add( (self.olevel, self.simd, self.problem_size_x, self.problem_size_y, self.problem_size_z, self.nthreads, self.thrdblock_x, str(int(self.thrdblock_y)*2), self.thrdblock_z) )
        neigh.add( (self.olevel, self.simd, self.problem_size_x, self.problem_size_y, self.problem_size_z, self.nthreads, self.thrdblock_x, self.thrdblock_y, str(int(self.thrdblock_z)*2)) )
        if int(self.nthreads) <= 32:
            neigh.add( (self.olevel, self.simd, self.problem_size_x, self.problem_size_y, self.problem_size_z, str(int(self.nthreads)*2), self.thrdblock_x, self.thrdblock_y, self.thrdblock_z) )
        return [Solution(*n) for n in neigh]
    
    def display(self):
        print(self.olevel, self.simd, self.problem_size_x, self.problem_size_y, self.problem_size_z, self.nthreads, self.thrdblock_x, self.thrdblock_y, self.thrdblock_z)

def hill_climibing(kmax):
    Sbest = Solution('-O3', 'avx512', '256', '256', '256', '16', '32', '32', '32')
    Ebest = Sbest.cost()
    neighbors = Sbest.get_neighbors()
    k = 0
    print('Cost= ', Ebest, end=' ')
    path = [(Sbest, Ebest)]
    Sbest.display()
    while k < kmax and len(neighbors) > 0:
        selected_index = random.randint(0, len(neighbors)-1)
        S_new = neighbors[selected_index]
        neighbors.pop(selected_index)
        E_new = S_new.cost()
        print('Cost= ', E_new, end=' ')
        S_new.display()
        if E_new > Ebest:
            print('New best:', end=' ')
            Sbest.display()
            Ebest = E_new
            Sbest = S_new
            path.append((Sbest, Ebest))
            neighbors = Sbest.get_neighbors()
        k += 1
    return Sbest, path

if __name__ == "__main__":
    os.chdir('iso3dfd-st7')
    best_solution, path = hill_climibing(50)
    print('\n\nPath taken:')
    for sol in path:
        print(sol[1], end=' ')
        sol[0].display()

    print('\n\nBest soltuion found:', end=' ')
    best_solution.display()
    print(best_solution.cost(verbose=True))
