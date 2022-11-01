import pandas as pd

def group_by_speaker(feature_df):
    speakers = [filename.split("_")[0] for filename in feature_df["filename"].tolist()]
    feature_df["speaker"] = speakers
    grouped = feature_df.groupby(["speaker"]).mean()
    return grouped

def main():
    feature_df = pd.read_csv("../pitch_jitter_shimmer.csv")
    grouped = group_by_speaker(feature_df)
    print(grouped)

if __name__ == "__main__":
    main()