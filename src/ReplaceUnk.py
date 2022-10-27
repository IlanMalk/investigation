import os
import pathlib






def changeFileExtension():
    i=0
    #path1="C:/Users/Adam Blumenthal/Documents/Electrical Engineering/Year 4/Lab/investigation/investigation/src/AudioTranscriptsTED_Lium3/"
    path1="C:/Users/Adam Blumenthal/Documents/Electrical Engineering/Year 4/Lab/investigation/investigation/src/TedTranscipts/"
    #path=os.path.join()
    os.chdir(path1)
 
    print("Directory changed")
    for filename in os.listdir(path1):
        # Read in the file
        with open(filename, 'r') as file :
          filedata = file.read()
#print(filedata)
# Replace the target string
        filedata = filedata.replace('<unk>', '')

# Write the file out again
        with open(filename, 'w') as file:
          file.write(filedata)
        print(i)
        i+=1 
    print(i)

changeFileExtension()