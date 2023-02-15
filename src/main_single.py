import os
from hill_climbing import hill_climibing
import sys

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