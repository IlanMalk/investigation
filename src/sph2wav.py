import os
from sphfile import SPHFile


#path = 'C:\Users\Adam Blumenthal\Documents\Electrical Engineering\Year 4\Lab\investigation\investigation\src\audio'  # Path of folder containing .sph files

sph =SPHFile(
    'sph\AalaElKhani_2016X.sph'
)
print( sph.format )
sph.write_wav( 'test.wav', 0.00, 120.00 )