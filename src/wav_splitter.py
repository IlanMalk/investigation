import wave
import os
import pandas as pd

def split_wav(input_wave: str, starts, durs):
    # check lengths the same
    if (len(starts) != len(durs)):
        print("ERROR: starts and durs must have equal lengths")
        assert(False)

    # file to extract the snippet from
    with wave.open(input_wave, "rb") as infile:
        # get file data
        nchannels = infile.getnchannels()
        sampwidth = infile.getsampwidth()
        framerate = infile.getframerate()

        
        # create parent folder for split wavs
        output_wave_parent_dir = os.path.join(os.path.dirname(input_wave), os.pardir, "wavSplit", "")
        if not os.path.isdir(output_wave_parent_dir):
            os.mkdir(output_wave_parent_dir)
        
        # create particular folder for soundbytes from the particular wav
        basename = os.path.basename(input_wave)
        index_of_dot = basename.index('.')
        basename = basename[:index_of_dot]
        output_wave_dir = os.path.join(output_wave_parent_dir, basename, "")
        if not os.path.isdir(output_wave_dir):
            os.mkdir(output_wave_dir)
        
        for start, dur in zip(starts, durs):
            # times between which to extract the wave from
            end = start + dur # seconds 

        
            # set position in wave to start of segment
            infile.setpos(int(start * framerate))
            # extract data
            data = infile.readframes(int((end - start) * framerate))

            # write the extracted data to a new file

            
            
            output_wave = os.path.join(output_wave_dir, f"{start:2f}.wav")
            with wave.open(output_wave, 'w') as outfile:
                outfile.setnchannels(nchannels)
                outfile.setsampwidth(sampwidth)
                outfile.setframerate(framerate)
                outfile.setnframes(int(len(data) / sampwidth))
                outfile.writeframes(data)


def main():
    basename = "911Mothers_2010W"
    input_wave = f"../tedliumtemp/wav/{basename}.wav"
    feature_df = pd.read_csv(f"../results/pjs-ted/{basename}.csv")
    feature_df.dropna(inplace=True)
    feature_df.reset_index(drop=True, inplace=True)
    starts = feature_df["start"].values
    durs = feature_df["duration"].values
    split_wav(input_wave, starts, durs)

if __name__ == "__main__":
    main()