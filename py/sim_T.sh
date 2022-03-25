#!/bin/bash

#SBATCH -J final_vel_w_teperature   # job name
#SBATCH -o final_vel_w_teperature.%j.out   # standard output and error log
#SBATCH -t 70:00:00               # Run time (hh:mm:ss)

python3 main.py T