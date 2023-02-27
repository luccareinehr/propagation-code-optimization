from solution import Solution
import random
import math


def local_conditionnal_acceptance(kmax, T0, f):
    S_best = Solution('-O3', 'avx512', '256', '256',
                      '256', '16', '48', '32', '32')
    E_best = S_best.cost()
    S = S_best
    E = E_best
    neighbors = S_best.get_neighbors()
    T = T0
    k = 0
    while k < kmax > 0:
        selected_index = random.randint(0, len(neighbors)-1)
        S_new = neighbors[selected_index]
        E_new = S_new.cost()
        print('Cost= ', E_new, end=' ')
        S_new.display()
        path = [(S_best, E_best)]
        if E_new > E or random.uniform(0, 1) < math.exp((E_new-E)/T):
            if E_new <= E:
                print('Risky choice !', end=' ')
                S.display()
            S = S_new
            E = E_new
            neighbors = S.get_neighbors()
            if E > E_best:
                S_best = S
                E_best = E
                print('New best:', end=' ')
                S_new.display()
                path.append((S_best, E_best))
        T = f(T)
        k += 1
    return S_best, path
