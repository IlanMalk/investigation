# investigation
This repository contains the code for Ilan Malkin and Adam Blumenthal's BScEng Investigation Project entitled A Vocal Analysis of Expert Debating speeches.

# Important folders and files
The `src` folder contains the source code.

The most important files are as follows:
- `PitchJittchShimmerHNR.py` contains the code used for extraction of voice quality features
- `prosodic.py` does likewise for prosodic features
- `sentiment-analysis.py` performs VADER sentiment analysis
- `gender_join.py` and `group_by_speaker.py` are for postprocessing the data
- `t_test_generalised.py` is used for t-testing
- The `Jupyter Notebook` named `t_tests_specific.ipynb` is used as a front end to call the functions that perform postprocessing and t-testing

The following files contain code that can be used to perform acoustic feature extraction using a compute cluster via the Message Passing Interface (MPI):
- `mpi_pjs.py` for voice quality features
- `mpi_prosodic.py` for prosodic features
