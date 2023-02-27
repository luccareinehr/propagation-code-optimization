#!/bin/sh
#SBATCH --time=15
echo "================================="
/usr/bin/mpirun -np 4 -map-by ppr:1:node:PE=16 -rank-by node python3 src/main.py
echo "================================="