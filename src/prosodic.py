from parselmouth.praat import run_file
import pickle
import os
import numpy as np
import pandas as pd
import re

# fuction taken from myprosody library
def run_praat_file(m: str, p: str) -> list[str] | None:
    """
    m : filename
    p : path to dataset folder
    

    returns : objects outputed by the praat script
    """
    sound: str = p+"/"+"dataset"+"/"+"audioFiles"+"/"+m+".wav"
    sourcerun: str = p+"/"+"dataset"+"/"+"essen"+"/"+"myspsolution.praat"
    path: str = p+"/"+"dataset"+"/"+"audioFiles"+"/"

    assert os.path.isfile(sound), "Wrong path to audio file"
    assert os.path.isfile(sourcerun), "Wrong path to praat script"
    assert os.path.isdir(path), "Wrong path to audio files"

    try:
        objects = run_file(sourcerun, -20, 2, 0.3, "yes",
                           sound, path, 80, 400, 0.01, capture_output=True)
        # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        # print(objects[0])
        # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z1 = str(objects[1])
        z2 = z1.strip().split()
        return z2
    except:
        z3 = 0
        print("Try again the sound of the audio was not clear")

def mysptotal(m: str, p: str) -> pd.DataFrame:
    """
    Overview: returns dataframe of all values
    """
    z2 = run_praat_file(m, p)
    z3 = np.array(z2)
    z4 = np.array(z3)[np.newaxis]
    z5 = z4.T
    dataset: pd.DataFrame = pd.DataFrame({"file": m[0 : 20], "number_ of_syllables": z5[0, :], "number_of_pauses": z5[1, :], "rate_of_speech": z5[2, :], "articulation_rate": z5[3, :], "speaking_duration": z5[4, :],
                        "original_duration": z5[5, :], "balance": z5[6, :], "f0_mean": z5[7, :], "f0_std": z5[8, :], "f0_median": z5[9, :], "f0_min": z5[10, :], "f0_max": z5[11, :],
                        "f0_quantile25": z5[12, :], "f0_quan75": z5[13, :]})
    return dataset

def extract_prosodic_from_folder(p: str) -> pd.DataFrame:
    """
    Extracts prosodic feature from all .wav files in dataset
    p: path to dataset folder
    """
    path: str = p+"/"+"dataset"+"/"+"audioFiles"+"/"
    files: list[str] = os.listdir(path)
    print(files)
    wav_files: list[str] = [os.path.splitext(x)[0] for x in files if re.search(r'\.wav$', x) ]
    print(wav_files)
    features: list[pd.DataFrame] = [mysptotal(file, p) for file in wav_files]
    feature_df = pd.concat(features, ignore_index=True)
    return feature_df





def main():
    curr_dirname = os.path.dirname(__file__)
    database_dirname = os.path.join(curr_dirname, '../myprosody/myprosody')

    # m: str = "test" # Audio File title "
    p: str = database_dirname # Path to the Audio_File directory (Python 3.7) 

    feature_df: pd.DataFrame = extract_prosodic_from_folder(p)
    # feature_df: pd.DataFrame = mysptotal(m, p)
    print(feature_df)

if __name__ == "__main__":
    main()
