import os
from hill_climbing import hill_climibing
import subprocess

from solution import Solution
from multiprocessing import get_number_of_nodes

if __name__ == "__main__":
    cmd = "sbatch -p cpu_prod --exclusive -N 4 -n 128 --qos=16nodespu src/launch_batch.sh" 
    print("Executed command: " + cmd)
    print("---->")
    res = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE)

    