from solution import Solution
import random
import math


def local_conditionnal_acceptance(kmax, T0, f):
    S_best = Solution('-O3', 'avx512', '256', '256',
                      '256', '16', '32', '32', '32')
    E_best = S_best.cost()
    S = S_best
    E = E_best
    neighbors = S_best.get_neighbors()
    T = T0
    k = 0
    while k < kmax and len(neighbors) > 0:
        selected_index = random.randint(0, len(neighbors)-1)
        S_new = neighbors[selected_index]
        E_new = S_new.cost()
        print('Cost= ', E_new, end=' ')
        S_new.display()
        if E_new > E_best or random.rand() < math.exp((E_best-E_new)/T):
            S = S_new
            E = E_new
            neighbors = S.get_neighbors()
            if E_new > E_best:
                S_best = S
                E_best = E
        T = f(T)
        k += 1
    return S_best, E_best
