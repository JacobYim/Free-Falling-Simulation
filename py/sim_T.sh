#!/bin/bash
#SBATCH --job-name=T_multiprocessing
#SBATCH --output=T_multiprocessing.out
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

python main.py T 0 &
python main.py T 1 &
python main.py T 2 &
python main.py T 3 &
python main.py T 4 &
python main.py T 5 &
python main.py T 6 &
python main.py T 7 &
python main.py T 8 &
python main.py T 9 &