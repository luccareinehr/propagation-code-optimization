#!/bin/sh
#SBATCH --time=5
echo "================================="
/usr/bin/mpirun -np 8 -map-by ppr:1:socket -rank-by socket -bind-to socket python3 src/main.py
echo "================================="