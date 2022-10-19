from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav
import os
import glob

# extracts MFCCs of all .wav files in directory
def extract_mfccs(directory):
    file_list = []
    mfcc_list = []
    for wav_file in glob.glob(os.path.join(directory, "*.wav")):
        (rate,sig) = wav.read(wav_file)
        mfcc_feat = mfcc(sig,rate, nfft=1024)
        mfcc_list.append(mfcc_feat)
        file_list.append(os.path.basename(wav_file))
    return (file_list, mfcc_list)

def main():
    directory = os.path.join(os.path.dirname(__file__), os.pardir, "dataset", "audioFiles")
    file_list, mfcc_list = extract_mfccs(directory)
    print(mfcc_list)

if __name__ == "__main__":
    main()