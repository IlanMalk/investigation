import os
import pathlib


def changeFileExtension():
    i=0
    path1="C:/Users/Adam Blumenthal/Documents/Electrical Engineering/Year 4/Lab/investigation/investigation/src/AudioTranscriptsTED_Lium3/"
    path2="C:/Users/Adam Blumenthal/Documents/Electrical Engineering/Year 4/Lab/investigation/investigation/src/TedTranscipts/"
    #path=os.path.join()
    os.chdir(path1)
 
    print("Directory changed")
    for filename in os.listdir(path1):
        path_to_file = os.path.join(os.path.dirname(path1), filename)
        f = open(filename,"r")
        os.chdir(path2)
        #with open(os.path.join(path2,filename), "w") as newfile:
            #toFile = raw_input("Write what you want into the field")
        newfile = open(filename, "w")
        print(i)
        for line in f:
            print(i)
            newfile.write("\t".join(x for index, x in enumerate(line.split()) if index > 5) + "\n")
        newfile.close()   
        os.chdir(path1)
        f.close()
        i+=1 
    print(i)

changeFileExtension()