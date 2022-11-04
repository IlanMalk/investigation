import librosa
#import samplerate
import os
import resampy
import soundfile as sf

#audio_file = "testDebate1.wav" #48KHz

#SAME PLAYBACK SPEED
##librosa.output.write_wav("Test1.wav", x, sr=22050, norm=False)
def upSample():
    path1="C:\\Users\\Adam Blumenthal\\Documents\\Electrical Engineering\\Year 4\\Lab\\investigation\\investigation\\src\\dataset\\audioFiles\\Daniel"
    os.chdir(path1)
    for filename in os.listdir(path1):
         
#SAME PLAYBACK SPEED
        y, sr = librosa.load(filename)              
        y_48k = librosa.resample(y, orig_sr=sr, target_sr=48000)
        y.shape, y_48k.shape
        sf.write('48'+filename, y_48k, 48000, subtype='PCM_24')


upSample()
#SLOW PLAYBACK SPEED
#x, sr = librosa.load(audio_file, sr=48000)
#librosa.output.write_wav("Test2.wav", x, sr=44100, norm=False)