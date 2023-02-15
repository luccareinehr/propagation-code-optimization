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

From the home dir in the cluster, run

```sbatch -p cpu_prod --exclusive -N 4 -n 128 --qos=16nodespu src/launch_batch.sh```

Then, parse the results with 



