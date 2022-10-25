import os
from sphfile import SPHFile
import sys
import glob

if len(sys.argv) != 3:
    print("ERROR: Enter sph and wav directory locations")
    sys.exit(1)

# directory path must be RELATIVE TO PYTHON FILE
sph_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[1])
wave_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[2])

#path = 'C:\Users\Adam Blumenthal\Documents\Electrical Engineering\Year 4\Lab\investigation\investigation\src\audio'  # Path of folder containing .sph files
print(sph_dir)
print(wave_dir)
for sph_file in glob.glob(sph_dir + "*.sph"):

# sph_dir = os.path.join(os.path.dirname(__file__), os.pardir, "tedlium", "sph")
# basename =  "AalaElKhani_2016X"

    sph =SPHFile(
        sph_file
        # '..sph/tedlium/AalaElKhani_2016X.sph'
    )
    print( sph.format )
    basename = os.path.basename(sph_file)
    basename = os.path.splitext(basename)[0]
    sph.write_wav(wave_dir + basename + ".wav")