import pandas as pd
import os
import pathlib

#filename=pathlib.Path('C:/Users/Adam Blumenthal/Documents/Electrical Engineering/Year 4/Lab/investigation/investigation/src/911Mothers_2010W.stm')
 

#print(filename)
def changeFileExtension():
    i=0
    path="C:/Users/Adam Blumenthal/Documents/Electrical Engineering/Year 4/Lab/investigation/investigation/src/stm/"
    #path=os.path.join()
    for filename in os.listdir(path):
        my_source =path + filename
        og=os.path.splitext(filename)[0]
        print(og)
        print(my_source)
        os.rename(my_source, og + '.txt')
        #print(i)
        i+=1
        
    print(i)

changeFileExtension()
#data = pd.read_csv(r, sep=" ", header=None)
#data.columns = ["a", "b", "c", "d", "e", "f", "g"]

#print(data)