from optimizer.algorithms.hill_climbing import HillClimbing
from optimizer.algorithms.greedy import Greedy, TabuGreedy
from optimizer.algorithms.local_conditionnal_acceptance import LocalConditionnalAcceptance

ALGORITHMS = {
    'hill_climbing': HillClimbing,
    'greedy': Greedy,
    'tabu_greedy': TabuGreedy,
    'simulated_annealing': LocalConditionnalAcceptance,
}

def get_algorithm(algorithm_name):
    if ALGORITHMS.get(algorithm_name) is None:
        raise NotImplementedError
    return ALGORITHMS[algorithm_name]