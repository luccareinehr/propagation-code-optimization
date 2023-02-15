from solution import Solution
import random


def hill_climibing(kmax):
    Sbest = Solution('-O3', 'avx512', '256', '256',
                     '256', '16', '32', '32', '32')
    Ebest = Sbest.cost()
    neighbors = Sbest.get_neighbors()
    k = 0
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
            Sbest.display()
            Ebest = E_new
            Sbest = S_new
            path.append((Sbest, Ebest))
            neighbors = Sbest.get_neighbors()
        k += 1
    return Sbest, path
