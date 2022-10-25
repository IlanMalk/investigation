#!/bin/env python3

# library imports
from fileinput import filename
import numpy as np
import glob
from mpi4py import MPI
from os import environ
from typing import Union, List, Tuple, Literal
import pandas as pd
import os
import re
import parselmouth
import sys
from pprogress import ProgressBar


# custom code imports
from prosodic import mysptotal
from PitchJittchShimmerHNR import measurePitch

MPIComm = Union[MPI.Intracomm, MPI.Intercomm]

# Our main routine.  It sanity-checks MPI and calls the correct code.
def main():
    """Executed when called via the CLI.

    Performs some sanity checks, and then calls the appropriate method.
    """

    # Get our MPI communicator, our rank, and the world size.
    mpi_comm = MPI.COMM_WORLD
    mpi_rank: int = mpi_comm.Get_rank()
    mpi_size: int = mpi_comm.Get_size()

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

    # the 'dataset' folder should be at ../dataset
    curr_dirname: str = os.path.dirname(os.path.abspath(__file__))
    # parent_dirname: str = os.path.join(curr_dirname, os.pardir)
    audio_dir: str = sys.argv[1]
    # each process extracts features from files partitioned to it and returns a dataframe
    # feature_df: pd.DataFrame = extract_prosodic_from_folder(parent_dirname, mpi_comm)
    feature_df: pd.DataFrame = extract_pitch_jitter_shimmer_from_folder(audio_dir, mpi_comm)
   
    
    # root process combines the dataframes
    if mpi_rank == 0: 
        feature_df_combined = gather_and_combine(mpi_comm, feature_df)
        if isinstance(feature_df_combined, pd.DataFrame):
            feature_df_combined.to_csv(os.path.join(curr_dirname, os.pardir, "pitch_jitter_shimmer.csv"), encoding='utf-8', index=False)
        print(feature_df_combined)

    return 0


# SOME TERMINOLOGY:
# MPI World: All of the MPI processes, spawned by `mpirun` or SLURM/srun.
# MPI Size: The number of MPI slots (or SLURM tasks).
#     Within a SLURM job, this is the number of tasks (--ntasks) for the job.
#     Outside of a SLURM job, this is the `-n` option given to `mpirun`.
#     (Or, with `mpirun`, by providing a list of hosts on which to run.)
# MPI Rank: An integer number, in the range [0, MPI size).
#     The MPI rank is unique to each worker.
def extract_prosodic_from_folder(dataset_folder: str, mpi_comm: MPIComm) -> pd.DataFrame:
    """
    Extracts prosodic features from all .wav files in dataset that are partitioned to the particular process
    dataset_folder: path to dataset folder
    """

    mpi_rank: int = mpi_comm.Get_rank()
    mpi_size: int = mpi_comm.Get_size()

    path: str = os.path.join(dataset_folder, "dataset", "audioFiles", "")
    files: list[str] = os.listdir(path)
    wav_files: list[str] = [os.path.splitext(x)[0] for x in files if re.search(r'\.wav$', x) ]
    features: list[pd.DataFrame] = [mysptotal(file, dataset_folder) for (idx, file) in enumerate(wav_files) if mpi_rank == (idx % mpi_size)]
    feature_df = pd.concat(features, ignore_index=True)
    if mpi_rank != 0:
            response = feature_df
            mpi_comm.gather(response)
    
    return feature_df


def extract_pitch_jitter_shimmer_from_folder(audio_dir: str, mpi_comm: MPIComm) -> pd.DataFrame:
    """
    Extracts various pitch, jitter and shimmer features from each file in audio_dir
    Returns result as DataFrame
    """
    file_list = []
    # list containing the 1-row dataframes returned from measurePitch() function
    feature_df_list: list[pd.DataFrame] = []
    # rank of this MPI process
    mpi_rank: int = mpi_comm.Get_rank()
    # total number of MPI processes
    mpi_size: int = mpi_comm.Get_size()

    # audio_file_string = os.path.join(dataset_folder, "dataset", "audioFiles", "*.wav")
    # check that audio_dir is a directory
    if not os.path.isdir(audio_dir):
        raise NotADirectoryError("ERROR: please enter a directory as a command line argument")   
    
    audio_file_string: str = os.path.join(audio_dir, "*.wav")
    wave_files = glob.glob(audio_file_string)
    # calculate number of files that this process will execute (for progress bar)
    files_for_process = len(wave_files) // mpi_size + int(mpi_rank < len(wave_files) % mpi_size)
    progress_bar = ProgressBar(files_for_process)

    # loop through files and extract features
    for (idx, wave_file) in enumerate(wave_files):
        if mpi_rank == (idx % mpi_size):
            sound = parselmouth.Sound(wave_file)
            feature_df: pd.DataFrame = measurePitch(sound, 75, 500, "Hertz")
            filename = os.path.basename(wave_file)
            # add the filename to the dataframe
            feature_df.insert(loc=0, column="filename", value=[filename])
            feature_df_list.append(feature_df)
            progress_bar.update()

    # concatenate features from this process's files into single DataFrame
    df: pd.DataFrame = pd.concat(feature_df_list, ignore_index=True)
    progress_bar.done()
    # communicate results to master process
    if mpi_rank != 0:
        response = df
        mpi_comm.gather(response)

    return df

def gather_and_combine(mpi_comm: MPIComm, feature_df):
    """
    Function to be called by root process.
    Combines all responses into one dataframe
    
    mpi_comm: the MPI communicator
    feature_df: the dataframe computed by the root process
    """
    response_array = mpi_comm.gather(None)
    # Sanity check: Did we get back a response from everyone?
    mpi_size: int = mpi_comm.Get_size()
    if response_array is None:
        print("ERROR! Response array is none")
        return 1

    if len(response_array) != mpi_size:
        print('ERROR!  The MPI world has {} members, but we only gathered {}!'
            .format(mpi_size, len(response_array))
        )
        return 1

    response_array.append(feature_df)
    feature_df_combined: pd.DataFrame = pd.concat(response_array, ignore_index=True)
    return feature_df_combined




# Run main()
if __name__ == '__main__':
    sys.exit(main())

# REMEMBER: IF ON CLUSTER, USE -hostfile or ssh away from head node
# mpiexec -n 2 python3 mpi_pjs.py audio/
# time mpiexec -hostfile /home/shared/machinefile -np 10 python3 -m mpi4py mpi_pjs.py

