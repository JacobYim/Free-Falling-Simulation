#!/bin/bash
#SBATCH --job-name=D1_multiprocessing
#SBATCH --output=D1_multiprocessing.out
#SBATCH --time 70:00:00               # Run time (hh:mm:ss)
#SBATCH --mail-user=jyim@buffalo.edu
#SBATCH --mail-type=ALL

#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --exclusive
#SBATCH --partition=general-compute

#SBATCH --mem=48000
#SBATCH --ntasks-per-node=12            

module load python/anaconda
ulimit -s unlimited

python main.py D 1