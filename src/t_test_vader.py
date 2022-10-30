import csv
import pandas as pd
from scipy import stats
debate='vader_full.csv'
ted='vaderTED.csv'

file = open(debate)
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

data_debate=pd.read_csv(debate)

file = open(ted)
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

data_ted=pd.read_csv(ted)
ted_pos=data_ted.pos.tolist()
debate_pos=data_debate.pos.tolist()
result_pos=stats.ttest_ind(ted_pos, debate_pos, equal_var=True)
print(result_pos)

ted_compound=data_ted.compound.tolist()
debate_compound=data_debate.compound.tolist()
result_compound=stats.ttest_ind(ted_compound, debate_compound, equal_var=False)
print(result_compound)

ted_compound=data_ted.compound.tolist()
debate_compound=data_debate.compound.tolist()
result_compound=stats.ttest_ind(ted_compound, debate_compound, equal_var=True)
print(result_compound)

result_compound_anova=stats.f_oneway(ted_compound,debate_compound)
print(result_compound_anova)