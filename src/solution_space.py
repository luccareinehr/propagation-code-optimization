import numpy as np
from evaluator import Simulator
from solution import Solution

class SolutionSpace:
    o_levels = ['-O2', '-O3', '-Ofast']
    simds = ['avx', 'avx2', 'avx512']
    n_threads = [8, 16, 32]
    threadblocks = [2, 4, 8, 16, 32, 64, 128, 256, 512]

def get_random_solution(problem_size, simulator):
    return Solution(
        olevel=np.random.choice(SolutionSpace.o_levels),
        simd=np.random.choice(SolutionSpace.simds),
        problem_size_x=problem_size[0],
        problem_size_y=problem_size[1],
        problem_size_z=problem_size[2],
        nthreads=np.random.choice(SolutionSpace.n_threads),
        thrdblock_x=np.random.choice(
            SolutionSpace.threadblocks[3:]),  # must be multiple of 16
        thrdblock_y=np.random.choice(SolutionSpace.threadblocks),
        thrdblock_z=np.random.choice(SolutionSpace.threadblocks),
        simulator=simulator
    )
