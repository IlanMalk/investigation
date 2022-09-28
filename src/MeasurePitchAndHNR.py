import glob
import numpy as np
import pandas as pd
import parselmouth
from parselmouth.praat import call # type: ignore

def measurePitch(voiceID, f0min, f0max, unit):
    sound = parselmouth.Sound(voiceID) # read the sound
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max) #create a praat pitch object
    meanF0 = call(pitch, "Get mean", 0, 0, unit) # get mean pitch
    stdevF0 = call(pitch, "Get standard deviation", 0 ,0, unit) # get standard deviation
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    return meanF0, stdevF0, hnr

file_list = []
mean_F0_list = []
sd_F0_list = []
hnr_list = []

for wave_file in glob.glob("audio/*.wav"):
    sound = parselmouth.Sound(wave_file)
    (meanF0, stdevF0, hnr) = measurePitch(sound, 75, 500, "Hertz")
    file_list.append(wave_file) # make an ID list
    mean_F0_list.append(meanF0) # make a mean F0 list
    sd_F0_list.append(stdevF0) # make a sd F0 list
    hnr_list.append(hnr)

df = pd.DataFrame(np.column_stack([file_list, mean_F0_list, sd_F0_list, hnr_list]), 
                               columns=['voiceID', 'meanF0Hz', 'stdevF0Hz', 'HNR'])  #add these lists to pandas in the right order



# Write out the updated dataframe
df.to_csv("processed_results3.csv", index=False) 