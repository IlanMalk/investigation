from parselmouth.praat import run_file # type: ignore
import pickle
import os
import numpy as np
import pandas as pd
import re

# fuction taken from myprosody library
def run_praat_file(m: str, p: str):
    """
    m : filename
    p : path to dataset folder
    

    returns : objects outputed by the praat script
    """
    sound: str = os.path.join(p, "dataset", "audioFiles", f"{m}.wav")
    sourcerun: str = os.path.join(p, "dataset", "essen", "myspsolution.praat")
    path: str = os.path.join(p, "dataset", "audioFiles", "")

    assert os.path.isfile(sound), f"Wrong path to audio file \n {sound}"
    assert os.path.isfile(sourcerun), "Wrong path to praat script"
    assert os.path.isdir(path), "Wrong path to audio files"

    # try:
    print(sourcerun)
    objects = run_file(sourcerun, -20, 2, 0.3, "yes",
                        sound, path, 80, 400, 0.01, capture_output=True)
    # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
    # print(objects[0])
    # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
    # print(type(objects[1]))
    z1: str = str(objects[1])
    z2: list[float] = list(map(float, z1.strip().split()))
    return z2
    # except:
    #     print("The PRAAT script failed")
    #     return []

def mysptotal(m: str, p: str) -> pd.DataFrame:
    """
    Overview: returns dataframe of all values
    """
    z2 = run_praat_file(m, p)
    # z3 = np.array(z2)
    # z4 = np.array(z3)[np.newaxis]
    # z5 = z4.T
    dataset: pd.DataFrame = pd.DataFrame({"file": m[0 : 20], "number_ of_syllables": z2[0], "number_of_pauses": z2[1], "rate_of_speech": z2[2], "articulation_rate": z2[3], "speaking_duration": z2[4],
                        "original_duration": z2[5], "balance": z2[6], "f0_mean": z2[7], "f0_std": z2[8], "f0_median": z2[9], "f0_min": z2[10], "f0_max": z2[11],
                        "f0_quantile25": z2[12], "f0_quan75": z2[13]}, index = [0])
    return dataset

def extract_prosodic_from_folder(p: str) -> pd.DataFrame:
    """
    Extracts prosodic feature from all .wav files in dataset
    p: path to dataset folder
    """
    path: str = os.path.join(p, "dataset", "audioFiles", "")
    files = os.listdir(path)
    wav_files = [os.path.splitext(x)[0] for x in files if re.search(r'\.wav$', x) ]
    features = [mysptotal(file, p) for file in wav_files]
    feature_df = pd.concat(features, ignore_index=True)
    return feature_df

def main():
    curr_dirname = os.path.dirname(os.path.abspath(__file__))
    print(curr_dirname) 
    database_dirname = os.path.join(curr_dirname, os.path.pardir, 'myprosody', 'myprosody')

    # m: str = "test" # Audio File title "
    p: str = database_dirname # Path to the Audio_File directory (Python 3.7)


    feature_df: pd.DataFrame = extract_prosodic_from_folder(p)
    # feature_df: pd.DataFrame = mysptotal(m, p)
    print(feature_df)

if __name__ == "__main__":
    main()
