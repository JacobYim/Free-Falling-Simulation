#!/bin/bash

#SBATCH -J final_vel_w_mass_rate   # job name
#SBATCH -o final_vel_w_mass_rate.%j.out   # standard output and error log
#SBATCH -t 70:00:00               # Run time (hh:mm:ss)
#SBATCH --nodes=4              
#SBATCH --ntasks-per-node=32
#SBATCH --mail-user=jyim@buffalo.edu    
#SBATCH --mem=250000

python3 main.py MR