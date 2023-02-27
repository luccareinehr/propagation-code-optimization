import os
from hill_climbing import hill_climibing
import sys

from mpi4py import MPI

comm = MPI.COMM_WORLD
NbP = comm.Get_size()
Me = comm.Get_rank()

if __name__ == "__main__":
    os.chdir('iso3dfd-st7')
    best_solution, path = hill_climibing(100)
    print('\n\nPath taken:')
    for sol in path:
        print(sol[1], end=' ')
        sol[0].display()

    print('\n\nBest solution found:', end=' ')
    best_solution.display()
    cost = best_solution.cost()
    print(cost)

    TabE = comm.gather(cost,root=0)
    TabS = comm.gather(best_solution,root=0)
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