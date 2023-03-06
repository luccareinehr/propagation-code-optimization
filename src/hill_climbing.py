import os
import sys
import subprocess
from solution import Solution
import random

from random_solution import get_random_solution
from algorithm import Algorithm

from mpi4py import MPI

PROBLEM_SIZE_X = '256'
PROBLEM_SIZE_Y = '256'
PROBLEM_SIZE_Z = '256'


class HillClimbing(Algorithm):
    def __init__(self, args, hparams) -> None:
        super().__init__(args, hparams)
        self.comm = MPI.COMM_WORLD

    def run(self, num_steps, evaluation_session):
        Me = self.comm.Get_rank()
        best_solution, path = self.single_run(num_steps, evaluation_session)
        print('\n\nPath taken:')
        for sol in path:
            print(sol[1], end=' ')
            sol[0].display()

        print('\n\nBest solution found:', end=' ')
        best_solution.display()
        # TODO: There is no need to recalculate this cost. Remove it
        cost = best_solution.cost()
        print(cost)

        TabE = self.comm.gather(cost, root=0)
        TabS = self.comm.gather(best_solution, root=0)
        if (Me == 0):
            print('\n\nBest solutions:')
            for i in range(len(TabE)):
                TabS[i].display()
                print(TabE[i])
            print('\nBest overall:')
            Eopt = max(TabE)
            idx = TabE.index(Eopt)
            Sopt = TabS[idx]
            Sopt.display()

            evaluation_session.display()

    def single_run(self, num_steps, evaluation_session):
        Sbest = get_random_solution(
            PROBLEM_SIZE_X, PROBLEM_SIZE_Y, PROBLEM_SIZE_Z, evaluation_session)
        Ebest = Sbest.cost()
        neighbors = Sbest.get_neighbors()
        k = 0
        print('Initial:', end=' ')
        Sbest.display()
        print('Cost= ', Ebest, end=' ')
        path = [(Sbest, Ebest)]
        Sbest.display()
        while k < num_steps and len(neighbors) > 0:
            selected_index = random.randint(0, len(neighbors)-1)
            S_new = neighbors[selected_index]
            neighbors.pop(selected_index)
            E_new = S_new.cost()
            print('Cost= ', E_new, end=' ')
            S_new.display()
            if E_new > Ebest:
                print('New best:', end=' ')
                Ebest = E_new
                Sbest = S_new
                Sbest.display()
                path.append((Sbest, Ebest))
                neighbors = Sbest.get_neighbors()
            k += 1
        return Sbest, path
