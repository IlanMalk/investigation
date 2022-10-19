#!/bin/bash

#SBATCH -J mpi_feature_extract
#SBATCH -o mpi_feature_extract_%j.txt
#SBATCH -e mpi_feature_extract_%j.err
#SBATCH --time=02:00:00
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=4

exec srun --mpi=pmi2 time python3 -m mpi4py src/mpi-main.py