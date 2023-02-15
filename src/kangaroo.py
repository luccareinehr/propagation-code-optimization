from hill_climbing import hill_climbing
from solution import Solution
import math
import random

def kangaroo(n, func, *args, **kwargs):
    """
    Wrapper that runs a given optimization strategy using n initial states.
    
    n: number of initial states
    func: optimization strategy function (e.g. hill_climbing)
    *args, **kwargs: arguments of func (positional or named)

    returns: a tuple containing the best solution found, its cost and the path taken.
    """
    if 'Sinit' in kwargs:
        kwargs.pop('Sinit')

    best_sol_cost = 0 # this will be maximized
    Sinit_list = gen_initial_states(n)
    for i in range(n):
        print(f"=== Kangaroo [{i}] ===")
        Sinit = Sinit_list[i]
        solution, cost, path = func(Sinit=Sinit, *args, **kwargs)
        if cost > best_sol_cost:
            best_sol = solution
            best_sol_cost = cost
            best_sol_path = path

    return best_sol, best_sol_cost, best_sol_path
    
def gen_initial_states(n):
    """
    Automatically generates n random initial states.

    TODO: ensure the states are "far" from each other
    """
    problem_size_x = 256
    problem_size_y = 256
    problem_size_z = 256

    max_nthreads = 32
    
    all_olevels = ['-O2', '-O3', '-Ofast']
    all_simds = ['avx', 'avx2', 'avx512']
    all_nthreads = [2**n for n in range(math.floor(math.log(max_nthreads,2)) + 1)]
    all_thrdblock_x = [16 * 2**(n-1) for n in range(1, math.floor(math.log(problem_size_x,2) - 3) + 1)] # constraint: multiple of 16
    all_thrdblock_y = [2**n for n in range(math.floor(math.log(problem_size_y,2)) + 1)]
    all_thrdblock_z = [2**n for n in range(math.floor(math.log(problem_size_z,2)) + 1)]

    Sinit_list = []
    for i in range(n):
        olevel = random.choice(all_olevels)
        simd = random.choice(all_simds)
        nthreads = random.choice(all_nthreads)
        thrdblock_x = random.choice(all_thrdblock_x)
        thrdblock_y = random.choice(all_thrdblock_y)
        thrdblock_z = random.choice(all_thrdblock_z)
        solution = Solution(olevel, simd, str(problem_size_x), str(problem_size_y), str(problem_size_z), str(nthreads), str(thrdblock_x), str(thrdblock_y), str(thrdblock_z))
        Sinit_list.append(solution)
    return Sinit_list