import os
from hill_climbing import hill_climibing

if __name__ == "__main__":
    os.chdir('iso3dfd-st7')
    best_solution, path = hill_climibing(50)
    print('\n\nPath taken:')
    for sol in path:
        print(sol[1], end=' ')
        sol[0].display()

    print('\n\nBest soltuion found:', end=' ')
    best_solution.display()
    print(best_solution.cost(verbose=True))
