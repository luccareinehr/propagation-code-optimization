import os
from hill_climbing import hill_climibing
import sys

from mpi4py import MPI

comm = MPI.COMM_WORLD
NbP = comm.Get_size()
Me = comm.Get_rank()

if __name__ == "__main__":
    os.chdir('iso3dfd-st7')
    best_solution, path = hill_climibing(10)
    print('\n\nPath taken:')
    for sol in path:
        print(sol[1], end=' ')
        sol[0].display()

    print('\n\nBest solution found:', end=' ')
    best_solution.display()
    cost = best_solution.cost(verbose=True)
    print(cost)

    TabE = comm.gather(cost,root=0)
    TabS = comm.gather(best_solution,root=0)
    if (Me == 0):
        print('Best solutions:')
        for i in range(TabE):
            TabS[i].display()
            print(TabE[i])
        print('Best overall:')
        Eopt = min(TabE)
        idx = TabE.index(Eopt)
        Sopt = TabS[idx]
        print(Sopt)