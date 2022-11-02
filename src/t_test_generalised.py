import csv
import pandas as pd
from scipy import stats
import numpy as np


def t_test_dataframes(df_debates, df_ted):
    common_columns = np.intersect1d(df_debates.columns, df_ted.columns)
    # print out unused columns
    columns_to_avoid = ["speaker"]
    unused_columns_debates = columns_to_avoid
    for column in df_debates.columns:
        if column not in common_columns:
            unused_columns_debates.append(column)
    print(f"Debates unused columns: {unused_columns_debates}")
    unused_columns_ted = columns_to_avoid
    for column in df_ted.columns:
        if column not in common_columns:
            unused_columns_ted.append(column)
    print(f"Ted unused columns: {unused_columns_ted}")

    for column in common_columns:
        if column in columns_to_avoid:
            continue

        print("------------------------------")
        print(column)
        debates_values = df_debates[column].values
        ted_values = df_ted[column].values
        debates_mean = np.mean(debates_values)
        print(f"Debates mean: {debates_mean}")
        ted_mean = np.mean(ted_values)
        print(f"TED mean: {ted_mean}")
        welch = stats.ttest_ind(ted_values, debates_values, equal_var=False)
        print(welch)
        print("------------------------------")
        


# debate='vader_full.csv'
# ted='vaderTED.csv'

# file = open(debate)
# type(file)
# print('A')
# csvreader = csv.reader(file)

# header = []
# header = next(csvreader)
# #print(header)
# print('B')

# rows = []
# for row in csvreader:
#         rows.append(row)
# #print(rows)

# data_debate=pd.read_csv(debate)

# file = open(ted)
# type(file)
# print('A')
# csvreader = csv.reader(file)

# header = []
# header = next(csvreader)
# #print(header)
# print('B')

# rows = []
# for row in csvreader:
#         rows.append(row)
# #print(rows)

# data_ted=pd.read_csv(ted)
# ted_pos=data_ted.pos.tolist()
# debate_pos=data_debate.pos.tolist()
# result_pos=stats.ttest_ind(ted_pos, debate_pos, equal_var=True)
# print(result_pos)

# ted_compound=data_ted.compound.tolist()
# debate_compound=data_debate.compound.tolist()
# result_compound=stats.ttest_ind(ted_compound, debate_compound, equal_var=False)
# print(result_compound)

# ted_compound=data_ted.compound.tolist()
# debate_compound=data_debate.compound.tolist()
# result_compound=stats.ttest_ind(ted_compound, debate_compound, equal_var=True)
# print(result_compound)

# result_compound_anova=stats.f_oneway(ted_compound,debate_compound)
# print(result_compound_anova)

def main():
    # df_debates = pd.read_csv("../results/vader_full.csv")
    # df_ted = pd.read_csv("../results/vaderTED.csv")
    df_debates = pd.read_csv("../results/pjs-debates-grouped-speaker.csv")
    df_ted = pd.read_csv("../results/pjs-ted-grouped-speaker.csv")
    t_test_dataframes(df_debates, df_ted)

if __name__ == "__main__":
    main()