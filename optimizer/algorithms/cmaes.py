import cma
import numpy as np

from optimizer.solution import Solution
from optimizer.evaluator import Simulator
from optimizer.random_solution import get_random_solution
from optimizer.solution_space import SolutionSpace
from optimizer.algorithms import Algorithm

class CMAESAlgorithm(Algorithm):
    def __init__(self, hparams, problem_size) -> None:
        super().__init__(hparams, problem_size)

    def run(self, kmax, evaluation_session):
        self.evaluation_session = evaluation_session
        initial_solution = get_random_solution(self.problem_size, evaluation_session)
        x0 = self.solution_to_x(initial_solution)
        sigma0 = 1   # initial standard deviation to sample new solutions
        options = {
            'bounds': self.get_bounds(),
            'integer_variables': [0, 1, 2, 3, 4, 5],
            'maxiter': kmax,
        }
        # TODO: pass parallel_objective instead of cost_function
        x, es = cma.fmin2(
            lambda x : self.cost_function(x), 
            x0, 
            sigma0, 
            options,
        )
        Sbest = self.x_to_solution(x)
        # TODO: how to manage path for CMAES?
        path = [ ]
        return Sbest, Sbest.cost(), path

    def cost_function(self, x):
        solution = self.x_to_solution(x)
        cost = solution.cost()
        print('Evaluating:', end=' ')
        solution.display()
        print('Cost: ', cost)
        return -cost

    def x_to_solution(self, x):
        x_parsed = [int(np.floor(xi)) for xi in x]
        return Solution(
            olevel=SolutionSpace.o_levels[x_parsed[0]],
            simd=SolutionSpace.simds[x_parsed[1]],
            problem_size_x=self.problem_size[0],
            problem_size_y=self.problem_size[1],
            problem_size_z=self.problem_size[2],
            nthreads=SolutionSpace.n_threads[x_parsed[2]],
            thrdblock_x=SolutionSpace.threadblocks[3:][x_parsed[3]],  # must be multiple of 16
            thrdblock_y=SolutionSpace.threadblocks[x_parsed[4]],
            thrdblock_z=SolutionSpace.threadblocks[x_parsed[5]],
            simulator=self.evaluation_session
        )
    
    def solution_to_x(self, solution):
        return [
            SolutionSpace.o_levels.index(solution.olevel),
            SolutionSpace.simds.index(solution.simd),
            SolutionSpace.n_threads.index(solution.nthreads),
            SolutionSpace.threadblocks.index(solution.thrdblock_x)-3,
            SolutionSpace.threadblocks.index(solution.thrdblock_y),
            SolutionSpace.threadblocks.index(solution.thrdblock_z),
        ]
    
    def get_bounds(self):
        return [0, [
            len(SolutionSpace.o_levels)-1e-3, 
            len(SolutionSpace.simds)-1e-3, 
            len(SolutionSpace.n_threads)-1e-3, 
            len(SolutionSpace.threadblocks[3:])-1e-3, 
            len(SolutionSpace.threadblocks)-1e-3, 
            len(SolutionSpace.threadblocks)-1e-3, 
        ]]