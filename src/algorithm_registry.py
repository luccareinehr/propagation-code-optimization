from hill_climbing import HillClimbing
from greedy import Greedy

ALGORITHMS = {
    'hill_climbing': HillClimbing,
    'greedy': Greedy,
}

def get_algorithm(algorithm_name):
    if ALGORITHMS.get(algorithm_name) is None:
        raise NotImplementedError
    return ALGORITHMS[algorithm_name]