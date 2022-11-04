import pandas as pd
import os
import glob

def combine_csvs(csv_dir):
    csv_str = os.path.join(csv_dir, "*.csv")
    csvs = glob.glob(csv_str)
    speech_dfs = [pd.read_csv(csv) for csv in csvs]
    combined_df = pd.concat(speech_dfs, ignore_index=True)
    return combined_df

def main():
    csv_dir = os.path.join(os.pardir, "results", "pjs-debates", "")
    combined_df = combine_csvs(csv_dir)
    print(combined_df)
    combined_df.to_csv("../results/pjs-debates-combined.csv", index=False)

if __name__ == "__main__":
    main()