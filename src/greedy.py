from solution import Solution
import math

import os
import sys
import subprocess
from algorithm import Algorithm
from random_solution import get_random_solution

class Greedy(Algorithm):
    def __init__(self, hparams, problem_size, logger) -> None:
        super().__init__(hparams, problem_size, logger)

    def run(self, kmax):
        self.logger.write_info('Starting greedy hill climbing')
        Sbest = get_random_solution(self.problem_size)
        Ebest = Sbest.cost()
        neighbors = Sbest.get_neighbors()
        k = 0
        newBetterS = True
        path = [(Sbest, Ebest)]
        self.logger.write_msg(
            k, Ebest, Sbest.get_compilation_flags(), flair='Initial'
        )

        while k < kmax and len(neighbors) > 0 and newBetterS:
            S1 = neighbors.pop()
            E1 = S1.cost()
            for S2 in neighbors:
                E2 = S2.cost()
                if E2 > E1:
                    S1 = S2
                    E1 = E2
            if E1 > Ebest:
                Sbest = S1
                Ebest = E1
                neighbors = Sbest.get_neighbors()
                path.append((Sbest, Ebest))
                self.logger.write_msg(
                    k+1, Ebest, Sbest.get_compilation_flags(),
                )
            else:
                newBetterS = False
                self.logger.write_info("No better element. End of the loop")

            k = k+1
        self.logger.write_info("End of the loop via number of iterations")
        return Sbest, Ebest, path    

class TabuGreedy(Algorithm):
    def __init__(self, hparams, problem_size, logger) -> None:
        super().__init__(hparams, problem_size, logger)

    def run(self, kmax):
        self.logger.write_info('Starting tabu_greedy hill climbing')
        N_Tabu = self.hparams['n_tabu']
        Sbest = get_random_solution(self.problem_size)
        Ebest = Sbest.cost()
        neighbors = Sbest.get_neighbors()
        k = 0
        path = [(Sbest, Ebest)]
        self.logger.write_msg(
            k, Ebest, Sbest.get_compilation_flags(), flair='Initial'
        )

        newBetterS = True
        visited = []

        while k < kmax and newBetterS:
            S1, E1 = TabuFindBest(neighbors, visited)
            if E1 > Ebest:
                Sbest = S1
                Ebest = E1
                visited = FifoAdd(self.logger, Sbest, visited, N_Tabu)

                path.append((Sbest, Ebest))

                self.logger.write_msg(
                    k+1, Ebest, Sbest.get_compilation_flags(),
                )

                neighbors = Sbest.get_neighbors()

            else:
                newBetterS = False
                self.logger.write_info("No better element. End of the loop")

            k = k+1

        print("End of the loop via number of iterations")
        return Sbest, Ebest, path


def FifoAdd(logger, Sbest, Ltabu, TabuSize=10):
    if len(Ltabu) == TabuSize:
        Ltabu.pop(0)
    Ltabu.append(Sbest)

    logger.write_info("Tabu List:")
    for i in Ltabu:
            logger.write_raw("\t" + i.get_compilation_flags())

    return Ltabu


def TabuFindBest(Lneigh, Ltabu):
    E1 = -math.inf
    S1 = None
    for S2 in Lneigh:
        if S2 not in Ltabu:
            E2 = S2.cost()
            if E2 > E1:
                S1 = S2
                E1 = E2
    return S1, E1
