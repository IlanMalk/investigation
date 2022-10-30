from email.mime import audio
import glob
import numpy as np
import pandas as pd
import parselmouth
import os
import sys

from parselmouth.praat import call # type: ignore
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def measurePitch(voiceID, f0min, f0max, unit):
    sound = parselmouth.Sound(voiceID) # read the sound
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max) #create a praat pitch object
    meanF0 = call(pitch, "Get mean", 0, 0, unit) # get mean pitch
    stdevF0 = call(pitch, "Get standard deviation", 0 ,0, unit) # get standard deviation
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer =  call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    

    return pd.DataFrame({'meanF0': meanF0, 'stdevF0': stdevF0, 'hnr': hnr, 'localJitter': localJitter, 'localabsoluteJitter': localabsoluteJitter, 'rapJitter': rapJitter, 'ppq5Jitter': ppq5Jitter, 'ddpJitter': ddpJitter, 'localShimmer': localShimmer, 'localdbShimmer': localdbShimmer, 'apq3Shimmer': apq3Shimmer, 'apq5Shimmer': apq5Shimmer, 'apq11Shimmer': apq11Shimmer, 'ddaShimmer': ddaShimmer}, index = [0])
def runPCA(df):
    #Z-score the Jitter and Shimmer measurements
    features = ['localJitter', 'localabsoluteJitter', 'rapJitter', 'ppq5Jitter', 'ddpJitter',
                'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer', 'apq11Shimmer', 'ddaShimmer']
    # Separating out the features
    x = df.loc[:, features].values
    # Separating out the target
    #y = df.loc[:,['target']].values
    # Standardizing the features
    x = StandardScaler().fit_transform(x)
    #PCA
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data = principalComponents, columns = ['JitterPCA', 'ShimmerPCA'])
    principalDf
    return principalDf

def main():

    file_list: list[str] = []
    feature_df_list: list[pd.DataFrame] = []
    audio_dir: str = sys.argv[1]
    if not os.path.isdir(audio_dir):
        raise NotADirectoryError("ERROR: please enter a directory as a command line argument")   
    
    audio_file_string: str = os.path.join(audio_dir, "*.wav")
    wave_files = glob.glob(audio_file_string)
    # audio_files = os.path.join(os.path.dirname(__file__), os.path.pardir, "dataset", "audioFiles", "*.wav")
    for wave_file in wave_files:
        file_list.append(os.path.basename(wave_file))
        sound = parselmouth.Sound(wave_file)
        temp_df: pd.DataFrame = measurePitch(sound, 75, 500, "Hertz")
        feature_df_list.append(temp_df)
    df: pd.DataFrame = pd.concat(feature_df_list, ignore_index=True)
    df.insert(loc=0, column="filename", value=file_list)
    print(df)
    pcaData: pd.DataFrame = runPCA(df)

    df = pd.concat([df, pcaData], axis=1)

    # Write out the updated dataframe
    df.to_csv("processed_results5.csv", index=False)

if __name__ == "__main__":
    main()
