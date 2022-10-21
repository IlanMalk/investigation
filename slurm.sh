#!/bin/bash

#SBATCH -J mpi_pjs_full
#SBATCH -o mpi_pjs_full%j.txt
#SBATCH -e mpi_pjs_full%j.err
#SBATCH --time=02:00:00
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=4

exec srun --mpi=pmi2 time python3 -m mpi4py src/mpi_pjs.py /data1/22p98/full/wav/