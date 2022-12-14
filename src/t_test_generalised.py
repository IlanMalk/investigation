import csv
import pandas as pd
from pandas.api.types import is_numeric_dtype
from scipy import stats
import numpy as np



def t_test_dataframes(df_debates: pd.DataFrame, df_ted: pd.DataFrame, columns_to_avoid=["filename","speaker"]):
    common_columns = np.intersect1d(df_debates.columns, df_ted.columns)
    # print out unused columns
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

    welch_results = []
    for column in common_columns:
        if column in columns_to_avoid:
            continue
        
        debates_values = df_debates[column].values
        ted_values = df_ted[column].values
        # check that types are numeric
        if (not is_numeric_dtype(debates_values)) or (not is_numeric_dtype(ted_values)):
            print(f"WARNING: column {column} has a non-numeric type. Skipping over it")
            continue

        # print("------------------------------")
        # print(column)
        debates_mean = np.mean(debates_values)
        debates_std = np.std(debates_values)   
        # print(f"Debates mean: {debates_mean}")
        ted_mean = np.mean(ted_values)
        ted_std = np.std(ted_values)
        # print(f"TED mean: {ted_mean}")
        welch = stats.ttest_ind(ted_values, debates_values, equal_var=False)
        # print(welch)
        # print("------------------------------")
        result = pd.DataFrame({"feature": column, "pvalue": welch.pvalue, "statistic": welch.statistic, "debates_mean": debates_mean, "ted_mean": ted_mean, "debates_std": debates_std, "ted_std": ted_std}, index=[0])
        welch_results.append(result)
    welch_df = pd.concat(welch_results, ignore_index=True)
    return welch_df
        

def main():
    # df_debates = pd.read_csv("../results/vader_full.csv")
    # df_ted = pd.read_csv("../results/vaderTED.csv")
    df_debates = pd.read_csv("../results/pjs-debates-grouped-speaker.csv")
    df_ted = pd.read_csv("../results/pjs-ted-grouped-speaker.csv")
    t_test_dataframes(df_debates, df_ted)

if __name__ == "__main__":
    main()