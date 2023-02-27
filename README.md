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

## Running batch computation

To test in one node:

```/usr/bin/mpirun -np 2 -map-by ppr:1:socket:PE=8 python src/main.py```

To deploy in batch

```sbatch -p cpu_prod --exclusive -N 4 -n 128 --qos=16nodespu src/launch_batch.sh```


