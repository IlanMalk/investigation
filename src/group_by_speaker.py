import pandas as pd
import os
import glob

def group_by_speaker(feature_df):
    if "speaker" not in feature_df.columns:
        speakers = [filename.split("_")[0] for filename in feature_df["filename"].tolist()]
        feature_df["speaker"] = speakers
    grouped = feature_df.groupby(["speaker"]).mean()
    return grouped

def main():
    # csv_str = os.path.join(os.pardir, "results", "pjs-debates", "*.csv")
    # csvs = glob.glob(csv_str)
    # speech_dfs = [pd.read_csv(csv) for csv in csvs]
    # # feature_df = pd.read_csv("../pitch_jitter_shimmer.csv")
    # feature_df = pd.concat(speech_dfs, ignore_index=True)
    # grouped = group_by_speaker(feature_df)
    # print(grouped)
    # grouped.to_csv("../pjs-debates-grouped-speaker.csv")
    feature_df = pd.read_csv("../results/vaderTED.csv")
    grouped = group_by_speaker(feature_df)
    print(grouped)
    grouped.to_csv("../vader-ted-grouped-speaker.csv")



if __name__ == "__main__":
    main()