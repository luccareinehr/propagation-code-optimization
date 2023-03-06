from hill_climbing import HillClimbing
from greedy import Greedy, TabuGreedy
from local_conditionnal_acceptance import LocalConditionnalAcceptance
from cmaes import CMAESAlgorithm

ALGORITHMS = {
    'hill_climbing': HillClimbing,
    'greedy': Greedy,
    'tabu_greedy': TabuGreedy,
    'simulated_annealing': LocalConditionnalAcceptance,
    'cmaes': CMAESAlgorithm
}

def get_algorithm(algorithm_name):
    if ALGORITHMS.get(algorithm_name) is None:
        raise NotImplementedError
    return ALGORITHMS[algorithm_name]