import csv
import glob
import os
import librosa
import subprocess
import numpy as np
import preprocess_data
import sys


def convert_sph( sph, wav ):
    """Convert an sph file into wav format for further processing"""
    command = [
        'sox','-t','sph', sph, '-b','16','-t','wav', wav
    ]
    subprocess.check_call( command ) # Did you install sox (apt-get install sox)


def process_ted(csv_path: str, parent_path: str):

    # parent_path = data_path + 'TEDLIUM_release2/' + category + '/'
    labels = []
    wave_files: list[str] = [] 
    offsets = []
    durs = []

    # create csv writer
    with open(csv_path, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')

        # read STM file list
        stm_list = glob.glob(parent_path + 'stm/*')
        # print(stm_list)
        for stm in stm_list:
            with open(stm, 'rt') as f:
                records = f.readlines()
                for record in records:
                    field = record.split()

                    # wave file name
                    wave_file = parent_path + 'sph/%s.sph.wav' % field[0]
                    wave_files.append(wave_file)

                    # label index
                    labels.append(preprocess_data.str2index(' '.join(field[6:])))

                    # start, end info
                    start, end = float(field[3]), float(field[4])
                    offsets.append(start)
                    durs.append(end - start)

        # save results
        for i, (wave_file, label, offset, dur) in enumerate(zip(wave_files, labels, offsets, durs)):
            fn = "%s-%.2f" % (wave_file.split('/')[-1], offset)
            target_filename = 'mfcc/' + fn + '.npy'
            if os.path.exists( target_filename ):
                continue
            # print info
            print("TEDLIUM corpus preprocessing (%d / %d) - '%s-%.2f]" % (i, len(wave_files), wave_file, offset))
            # load wave file
            if not os.path.exists( wave_file ):
                sph_file = wave_file.rsplit('.',1)[0]
                if os.path.exists( sph_file ):
                    convert_sph( sph_file, wave_file )
                else:
                    raise RuntimeError("Missing sph file from TedLium corpus at %s"%(sph_file))
            wave, sr = librosa.load(wave_file, mono=True, offset=offset, duration=dur)

            # get mfcc feature
            mfcc = librosa.feature.mfcc(y=wave, sr=16000)

            # save result ( exclude small mfcc data to prevent ctc loss )
            if len(label) < mfcc.shape[1]:
                # filename

                # save meta info
                writer.writerow([fn] + label)

                # save mfcc
                np.save(target_filename, mfcc, allow_pickle=False)

def main():
    parent_path = sys.argv[1]
    csv_path = sys.argv[2]
    process_ted(parent_path=parent_path, csv_path=csv_path)


if __name__ == "__main__":
    main()
