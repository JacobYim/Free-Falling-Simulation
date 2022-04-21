#!/bin/bash
#SBATCH --job-name=RR_multiprocessing
#SBATCH --output=RR_multiprocessing.out
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

python main.py RR 0 &
python main.py RR 1 &
python main.py RR 2 &
python main.py RR 3 &
python main.py RR 4 &
python main.py RR 5 &
python main.py RR 6 &
python main.py RR 7 &
python main.py RR 8 &
python main.py RR 9 &
