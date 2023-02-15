import os
from hill_climbing import hill_climibing
from local_conditionnal_acceptance import local_conditionnal_acceptance

if __name__ == "__main__":
    def f(x): return 0.95*x
    os.chdir('iso3dfd-st7')
    best_solution, path = local_conditionnal_acceptance(50, 100, f)
    print('\n\nPath taken:')
    for sol in path:
        print(sol[1], end=' ')
        sol[0].display()

    print('\n\nBest soltuion found:', end=' ')
    best_solution.display()
    print(best_solution.cost(verbose=True))
