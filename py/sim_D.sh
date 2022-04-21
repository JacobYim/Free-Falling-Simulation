#!/bin/bash
#SBATCH --job-name=D_multiprocessing
#SBATCH --output=D_multiprocessing.out
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

python main.py D 0 &
python main.py D 1 &
python main.py D 2 &
python main.py D 3 &
python main.py D 4 &
python main.py D 5 &
python main.py D 6 &
python main.py D 7 &
python main.py D 8 &
python main.py D 9 &
