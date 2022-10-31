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

from sph2wav import convert_sph

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

def measurePitchTed(stm, f0min, f0max, unit):
    # 

    offsets = []
    durs = []

    # create csv writer
    # with open(csv_path, 'w') as csv_file:
        # writer = csv.writer(csv_file, delimiter=',')

        # read STM file list
        # stm_list = glob.glob(parent_path + 'stm/*')
        # print(stm_list)
        # for stm in stm_list:
    parent_path = os.path.join(os.path.dirname(os.path.abspath(stm)), os.pardir)
    
    # extract info from transcript
    with open(stm, 'rt') as f:
        records = f.readlines()
        filename: str = records[0].split()[0]

        for record in records:
            field = record.split()

            if (field[0] != filename):
                print(f"WARNING: filename of first record is {filename} but filename of a different record is {field[0]}")
            
            # # label index
            # labels.append(preprocess_data.str2index(' '.join(field[6:])))

            # start, end info
            start, end = float(field[3]), float(field[4])
            offsets.append(start)
            durs.append(end - start)

    # load wave file
    wave_file = os.path.join(parent_path, f"wav/{filename}.wav")
    print(f"Wave file: {wave_file}")
    if not os.path.exists( wave_file ):
        sph_file = os.path.join(parent_path, f"sph/{filename}.sph")
        print(f"SPH file: {sph_file}")

        if os.path.exists( sph_file ):
            convert_sph( sph_file, wave_file )
        else:
            raise RuntimeError("Missing sph file from TedLium corpus at %s"%(sph_file))
    sound = parselmouth.Sound(wave_file)
    target_filename = 'pjs/' + filename + '.csv'
    
    # check if file has already been extracted as csv
    if os.path.exists( target_filename ):
        df = pd.read_csv(target_filename)
        if (len(df.index) == len(offsets)):
            return df
        else:
            # csv does not have expected number of records.
            print(f"{target_filename} exists but has a length of {len(df.index)} instead of the expected length of {len(offsets)}")
            print("Attempting to extract features and overwrite file")

    # extract features and save results
    feature_dfs = []
    for i, (offset, dur) in enumerate(zip(offsets, durs)):
        
        # print(f"TEDLIUM corpus preprocessing ({i} / {len(offsets)}) - '{filename}-%{offset:.1f}]")
        
        sound_bite = sound.extract_part(from_time=offset, to_time=offset+dur)
        feature_df = measurePitch(sound_bite, f0min, f0max, unit)
        feature_df.insert(loc=0, column="filename", value=[filename])
        feature_df.insert(loc=1, column="start", value=[offset])
        feature_df.insert(loc=2, column="duration", value=[dur])
        # print(feature_df)
        feature_dfs.append(feature_df)

    feature_df_combined: pd.DataFrame = pd.concat(feature_dfs, ignore_index=True)
    feature_df_combined.to_csv(target_filename, index=False)
    return feature_df_combined

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

    # file_list: list[str] = []
    # feature_df_list: list[pd.DataFrame] = []
    
    # audio_files = os.path.join(os.path.dirname(__file__), os.path.pardir, "dataset", "audioFiles", "*.wav")
    # for wave_file in glob.glob(audio_files):
    #     file_list.append(os.path.basename(wave_file))
    #     sound = parselmouth.Sound(wave_file)
    #     temp_df: pd.DataFrame = measurePitch(sound, 75, 500, "Hertz")
    #     feature_df_list.append(temp_df)
    # df: pd.DataFrame = pd.concat(feature_df_list, ignore_index=True)
    # df.insert(loc=0, column="filename", value=file_list)
    # print(df)
    # pcaData: pd.DataFrame = runPCA(df)

    # df = pd.concat([df, pcaData], axis=1)

    # # Write out the updated dataframe
    # df.to_csv("processed_results5.csv", index=False)

    stm_dir = sys.argv[1] # take stm directory from command line argument
    num_files = 200 # number of files to process
    stm_files = glob.glob(stm_dir + "*.stm")
    # take first num_files files, after sorting alphabetically
    stm_files.sort()
    stm_files = stm_files[ : num_files]
    for i, stm_file in enumerate(stm_files):
        df = measurePitchTed(stm_file, 75, 500, "Hertz")
        print(f"Completed {i} / {num_files}")
    return 0

    # stm_file = "../tedlium/stm/911Mothers_2010W.stm"


if __name__ == "__main__":
    sys.exit(main())


# /data1/22p98/TEDLIUM_release-3/data/stm/