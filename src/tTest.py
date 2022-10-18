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

l=stats.ttest_1samp(f0, popmean=200)
print(l)

hnr=data.hnr.tolist()

h=stats.ttest_1samp(hnr, popmean=5)
print(h)
