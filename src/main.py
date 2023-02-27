import os
from solution import Solution
from kangaroo import kangaroo
from hill_climbing import hill_climbing

if __name__ == "__main__":
    os.chdir('../../iso3dfd-st7')
    #Sinit = Solution('-O3', 'avx512', '256', '256', '256', '16', '32', '32', '32')
    #best_solution, path = hill_climibing(50, Sinit)
    best_solution, cost, path = kangaroo(n=3, func=hill_climbing, kmax=20)
    print('\n\nPath taken:')
    for sol in path:
        print(sol[1], end=' ')
        sol[0].display()

    print('\n\nBest solution found:', end=' ')
    best_solution.display()
    print(best_solution.cost(verbose=True))
