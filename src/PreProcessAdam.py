#import pandas as pd
import os
import pathlib


def changeFileExtension():
    i=0
    path1="C:/Users/Adam Blumenthal/Documents/Electrical Engineering/Year 4/Lab/investigation/investigation/src/AudioTranscriptsTED_Lium3/"
    path2="C:/Users/Adam Blumenthal/Documents/Electrical Engineering/Year 4/Lab/investigation/investigation/src/TedTranscripts2/"
    #path=os.path.join()
    for filename in os.listdir(path1):
        #my_source =path1 + filename
        f = open(filename, 'r')
        
        with open(os.path.join(path2,filename), "w") as newfile:
            #toFile = raw_input("Write what you want into the field")
            for line in f:
                newfile.write("\t".join(x for index, x in enumerate(line.split()) if index > 6) + "\n")
                newfile.close()
        #g = open(filename, "w")

        
             #g.write("\t".join(x for index, x in enumerate(line.split()) if index in >6) + "\n")

        f.close()
        #g.close()
        #og=os.path.splitext(filename)[0]
        #print(og)
        #print(my_source)
        #os.rename(my_source, og + '.txt')
        #print(i)
        i+=1
        
    print(i)

changeFileExtension()