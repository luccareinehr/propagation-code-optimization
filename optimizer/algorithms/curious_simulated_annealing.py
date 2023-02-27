from solution import Solution
import random
import numpy as np
from random_solution import get_random_solution


def acceptance_func(energy_diff, temp):
    return 1 / (1 + energy_diff / temp)


def curious_simulated_annealing(n_iter, init_state=None, n_particles=6, temperature_schedule=None):
    # Initialize the particles

    PROBLEM_SIZE_X = '256'
    PROBLEM_SIZE_Y = '256'
    PROBLEM_SIZE_Z = '256'

    if init_state is None:
        init_state = get_random_solution(PROBLEM_SIZE_X, PROBLEM_SIZE_Y, PROBLEM_SIZE_Z)
    particles = [init_state for _ in range(n_particles)]
    particle_weights = np.ones(n_particles) / n_particles
    path = [(init_state, init_state.cost())]

    if temperature_schedule is None:
        temperature_schedule = range(200, 0, round(-200/(n_iter/n_particles)))

    # Initialize the current state and current energy
    current_state = init_state
    current_energy = init_state.cost()

    print('Cost= ', current_energy, end=' ')
    current_state.display()

    # Iterate over the temperature schedule
    for temp in temperature_schedule:
        # Resample the particles based on the current weights
        indices = np.random.choice(np.arange(n_particles), size=n_particles, p=particle_weights)
        particles = [particles[i] for i in indices]
        particle_weights = np.ones(n_particles) / n_particles

        # Update each particle
        for i in range(n_particles):
            # Perturb the particle

            perturbed_particle = particles[i].get_random_neighbor()
            print('Cost= ', perturbed_particle.cost(), end=' ')
            perturbed_particle.display()

            # Calculate the energy difference
            energy_diff = perturbed_particle.cost() - particles[i].cost()

            # Update the particle or move to a new state with a certain probability
            if acceptance_func(energy_diff, temp) > np.random.uniform():
                particles[i] = perturbed_particle

        # Update the particle weights based on the new states
        for i in range(n_particles):
            particle_weights[i] = np.exp((particles[i].cost())/temp)

        # Normalize the weights
        particle_weights /= np.sum(particle_weights)

        # Update the current state and current energy
        best_particle = particles[np.argmin([p.cost() for p in particles])]
        best_energy = best_particle.cost()

        if best_energy > current_energy:
            current_state = best_particle
            current_energy = best_energy
            path.append((current_state, current_energy))

    return current_state, path

