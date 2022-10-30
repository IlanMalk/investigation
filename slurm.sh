#!/bin/bash

#SBATCH -J mpi_pjs_full
#SBATCH -o mpi_pjs_full%j.txt
#SBATCH -e mpi_pjs_full%j.err
#SBATCH --time=00:10:00
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=1

# exec srun --mpi=pmi2 time python3 -m mpi4py src/mpi_pjs.py /data1/22p98/full/wav/
exec srun --mpi=pmi2 time python3 -m mpi4py src/mpi_pjs.py dataset/audioFiles/