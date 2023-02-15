from solution import Solution
import random

from random_solution import get_random_solution

PROBLEM_SIZE_X='256'
PROBLEM_SIZE_Y='256'
PROBLEM_SIZE_Z='256'

def hill_climibing(kmax):
    # Sbest = get_random_solution(PROBLEM_SIZE_X, PROBLEM_SIZE_Y, PROBLEM_SIZE_Z)
    Sbest = Solution('-O3', 'avx512', '256', '256', '256', '16', '32', '32', '32')

    Ebest = Sbest.cost()
    neighbors = Sbest.get_neighbors()
    k = 0
    print('Initial:', end=' ')
    Sbest.display()
    print('Cost= ', Ebest, end=' ')
    path = [(Sbest, Ebest)]
    Sbest.display()
    while k < kmax and len(neighbors) > 0:
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