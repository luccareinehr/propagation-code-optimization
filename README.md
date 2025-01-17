# propagation-code-optimization

# Initialize environment

Create a `.env` file with

```
export USER= 
export GROUP=
```

and initialize it with `source .env`.

## Uploading

`make upload`

## Deployment Examples

```
python3 -m optimizer.main --algorithm hill_climbing --steps 4
python3 -m optimizer.main --algorithm greedy --steps 4
python3 -m optimizer.main --algorithm tabu_greedy --steps 4 --hparams '{"n_tabu":5}'
python3 -m optimizer.main --algorithm simulated_annealing --steps 10 --hparams '{"t0":20}'
python3 -m optimizer.main --algorithm cmaes --steps 10
```

Flag `-kangaroo`: runs 4 instances in parallel with different initializations. 
Flag `-parallel`: runs 4 instances to calculate the cost function in parallel. It is only not available for Hill Climbing.

We recommend using parallel for all methods in which it is available.

## FAQ

Installation of CMA: Check if the pip used to install is the same as the Python being used to run. Sometimes we need to use `/usr/bin/pip` (TODO: avoid this).
