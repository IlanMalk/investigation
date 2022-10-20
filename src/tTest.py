import csv
import pandas as pd
from scipy import stats
vader='vader_full.csv'
pjs='pitch_jitter_shimmer_cluster.csv'

file = open(pjs)
type(file)
print('A')
csvreader = csv.reader(file)

header = []
header = next(csvreader)
#print(header)
print('B')

rows = []
for row in csvreader:
        rows.append(row)
#print(rows)

data=pd.read_csv(pjs)

f0=data.meanF0.tolist()
#print(f0)

l=stats.ttest_1samp(f0, popmean=130)
print(l)

hnr=data.hnr.tolist()

h=stats.ttest_1samp(hnr, popmean=5)
print(h)


localJit=data.localJitter.tolist()

localJitter=stats.ttest_1samp(localJit, popmean=0.027)
print(localJitter)

#Comparison to Dbates
f0=data.meanF0.tolist()
#print(f0)

l=stats.ttest_1samp(f0, popmean=220)
print(l)

f0St=data.stdevF0.tolist()
#print(f0)

f0STDEV=stats.ttest_1samp(f0St, popmean=88.2)
print(f0STDEV)


hnr=data.hnr.tolist()

h=stats.ttest_1samp(hnr, popmean=4.43)
print(h)


localJit=data.localJitter.tolist()

localJitter=stats.ttest_1samp(localJit, popmean=0.027)
print(localJitter)

rapJitter=data.rapJitter.tolist()

rapJitter1=stats.ttest_1samp(rapJitter, popmean=0.017)
print(rapJitter1)

ppq5Jitter=data.ppq5Jitter.tolist()

ppq5Jitter1=stats.ttest_1samp(ppq5Jitter, popmean=0.0190)
print(ppq5Jitter1)

