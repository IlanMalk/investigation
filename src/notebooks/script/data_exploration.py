#!/usr/bin/env python
# coding: utf-8

import csv
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import math
vader='../../vader_full.csv'
pjs='../../pitch_jitter_shimmer_cluster.csv'

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


data


hist = data.hist(bins=20, column=["meanF0", "hnr"])


hist = data.hist(bins=20, column=["localabsoluteJitter"])


hnr_db = [20 * math.log(x, 10) for x in data.hnr]
jitter_abs_db = [20 * math.log(x, 10) for x in data.hnr]


hnr_db_plot = plt.hist(hnr_db, bins=20);
plt.title("HNR (db)");


plt.hist(jitter_abs_db, bins=20);
plt.title("Local Abs Jitter (dB)");


hnr_db_t_test = stats.ttest_1samp(hnr_db, popmean=19)
hnr_db_t_test


print(hnr_db_t_test)

