from hill_climbing import HillClimbing
from greedy import Greedy, TabuGreedy

ALGORITHMS = {
    'hill_climbing': HillClimbing,
    'greedy': Greedy,
    'tabu_greedy': TabuGreedy,
}

def get_algorithm(algorithm_name):
    if ALGORITHMS.get(algorithm_name) is None:
        raise NotImplementedError
    return ALGORITHMS[algorithm_name]