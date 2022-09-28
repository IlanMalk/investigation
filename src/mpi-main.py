# library imports
from cmath import isnan
from mpi4py import MPI
from os import environ
from typing import Union, List, Tuple, Literal
import pandas as pd
import os
import re

# custom code imports
from prosodic import mysptotal

MPIComm = Union[MPI.Intracomm, MPI.Intercomm]

# Our main routine.  It sanity-checks MPI and calls the correct code.
def main():
    """Executed when called via the CLI.

    Performs some sanity checks, and then calls the appropriate method.
    """

    # Get our MPI communicator, our rank, and the world size.
    mpi_comm = MPI.COMM_WORLD
    mpi_rank = mpi_comm.Get_rank()
    mpi_size = mpi_comm.Get_size()

    # Do we only have one process?  If yes, then exit.
    if mpi_size == 1:
        print('You are running an MPI program with only one slot/task!')
        print('Are you using `mpirun` (or `srun` when in SLURM)?')
        print('If you are, then please use an `-n` of at least 2!')
        print('(Or, when in SLURM, use an `--ntasks` of at least 2.)')
        print('If you did all that, then your MPI setup may be bad.')
        return 1

    # Is our world size over 999?  The output will be a bit weird.
    # NOTE: Only rank zero does anything, so we don't get duplicate output.
    if mpi_size >= 1000 and mpi_rank == 0:
        print('WARNING:  Your world size {} is over 999!'.format(mpi_size))
        print("The output formatting will be a little weird, but that's it.")

    # Sanity checks complete!

    # Call the appropriate function, based on our rank
    curr_dirname = os.path.dirname(os.path.abspath(__file__))
    database_dirname = os.path.join(curr_dirname, os.pardir, 'myprosody', 'myprosody')

    # m: str = "test" # Audio File title "
    p: str = database_dirname # Path to the Audio_File directory (Python 3.7) 

    feature_df: pd.DataFrame = extract_prosodic_from_folder(p, mpi_comm)
    
    if mpi_rank == 0: # root process
        feature_df_combined = gather_and_combine(mpi_comm, feature_df)
        print(feature_df_combined)

    return 0



# This program has two parts: The controller and the worker part.
# The controller is executed by rank 0; the workers by everyone else.
# SOME TERMINOLOGY:
# MPI World: All of the MPI processes, spawned by `mpirun` or SLURM/srun.
# MPI Size: The number of MPI slots (or SLURM tasks).
#     Within a SLURM job, this is the number of tasks (--ntasks) for the job.
#     Outside of a SLURM job, this is the `-n` option given to `mpirun`.
#     (Or, with `mpirun`, by providing a list of hosts on which to run.)
# MPI Rank: An integer number, in the range [0, MPI size).
#     The MPI rank is unique to each worker.

# This program follows the convention that rank 0 is the "controller", and all
# non-zero ranks are "workers".  This is important when using things like
# broadcast, or scatter/gather.  But if you are only doing simple send/receive
# (which we do not), then you don't need to stick to the controller-worker
# paradigm.  But it's still a good idea!
def extract_prosodic_from_folder(p: str, mpi_comm: MPIComm) -> pd.DataFrame:
    """
    Extracts prosodic feature from all .wav files in dataset
    p: path to dataset folder
    """

    mpi_rank: int = mpi_comm.Get_rank()
    mpi_size: int = mpi_comm.Get_size()

    path: str = os.path.join(p, "dataset", "audioFiles", "")
    files: list[str] = os.listdir(path)
    wav_files: list[str] = [os.path.splitext(x)[0] for x in files if re.search(r'\.wav$', x) ]
    features: list[pd.DataFrame] = [mysptotal(file, p) for [idx, file] in enumerate(wav_files) if mpi_rank == (idx % mpi_size)]
    feature_df = pd.concat(features, ignore_index=True)
    if mpi_rank != 0:
            response = feature_df
            mpi_comm.gather(response)
    
    return feature_df


def gather_and_combine(mpi_comm: MPIComm, feature_df):
    """
    Function to be called by root process.
    Combines all responses into one dataframe
    """
    response_array = mpi_comm.gather(None)
    # Sanity check: Did we get back a response from everyone?
    mpi_size = mpi_comm.Get_size()
    if response_array is None:
        print("ERROR! Response array is none")
        return 1

    if len(response_array) != mpi_size:
        print('ERROR!  The MPI world has {} members, but we only gathered {}!'
            .format(mpi_size, len(response_array))
        )
        return 1

    print(type(response_array))
    print(len(response_array))
    response_array.append(feature_df)
    print(len(response_array))
    feature_df_combined = pd.concat(response_array, ignore_index=True)
    return feature_df_combined
    
# Run main()
if __name__ == '__main__':
    import sys
    sys.exit(main())


