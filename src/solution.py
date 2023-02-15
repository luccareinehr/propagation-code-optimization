import subprocess
import re
import os
import threading

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

    def cost(self, verbose=False, delete_file=True):
        file_name = str(threading.get_ident())
        file_name_with_ext = f'{file_name}.exe'
        executable_path = f'bin/{file_name_with_ext}'

        result = subprocess.run(['make', f'Olevel={self.olevel}', f'simd={self.simd}', 'last'], 
            stdout=subprocess.DEVNULL,
            env=dict(os.environ, CONFIG_EXE_NAME=file_name_with_ext))
        if result.returncode != 0:
            raise Exception( f'Failed compiling: { result.returncode }' )
        
        result = subprocess.run([executable_path, 
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
        
        if delete_file:
            result = subprocess.run(['rm', executable_path])
            if result.returncode != 0:
                raise Exception( f'Failed deleting: { result.returncode }' )

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
