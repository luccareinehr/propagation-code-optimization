from solution import Solution


def greedy(kmax):
    Sbest = Solution('-O3', 'avx512', '256', '256',
                     '256', '16', '32', '32', '32')
    Ebest = Sbest.cost()
    neighbors = Sbest.get_neighbors()
    k = 0
    newBetterS = True

    print('Cost= ', Ebest, end=' ')
    path = [(Sbest, Ebest)]
    Sbest.display()

    while k < kmax and len(neighbors) > 0 and newBetterS:
        S1 = neighbors.pop()
        E1 = S1.cost()
        for S2 in neighbors:
            E2 = S2.cost()
            if E2 < E1:
                S1 = S2
                E1 = E2
        if E1 < Ebest:
            Sbest = S1
            Ebest = E1
            neighbors = Sbest.get_neighbors()
            path.append((Sbest, Ebest))

            print('New best:', end=' ')
            Sbest.display()
            print('Actual Cost: ' + str(Ebest))

        else:
            newBetterS = False
            print("\nNo better element. End of the loop")

        k = k+1
    print("End of the loop via number of iterations")
    return Sbest, path


def improved_greedy(kmax):
    Sbest = Solution('-O3', 'avx512', '256', '256',
                     '256', '16', '32', '32', '32')
    Ebest = Sbest.cost()
    neighbors = Sbest.get_neighbors()
    k = 0
    newBetterS = True

    visited = set()
    neighbors = subset(neighbors)

    print('Cost= ', Ebest, end=' ')
    path = [(Sbest, Ebest)]
    Sbest.display()

    while k < kmax and len(neighbors) > 0 and newBetterS:
        S1 = neighbors.pop()
        E1 = S1.cost()
        for S2 in neighbors:
            E2 = S2.cost()
            visited.update([S2])

            if E2 < E1:
                S1 = S2
                E1 = E2
        if E1 < Ebest:
            Sbest = S1
            Ebest = E1
            neighbors = subset(Sbest.get_neighbors(), visited)

            path.append((Sbest, Ebest))

            print('New best:', end=' ')
            Sbest.display()
            print('Actual Cost: ' + str(Ebest))

        else:
            newBetterS = False
            print("\nNo better element. End of the loop")

        k = k+1
    print("End of the loop via number of iterations")
    return Sbest, path


def subset(neighborhood, visited=set()):
    new_set = []

    # Elimination of visited sets and use of prior knowledge conditions
    for i in neighborhood:
        if (i not in visited) and (1):  # Implement the prior knowledge conditions
            new_set.append(i)

    return new_set
