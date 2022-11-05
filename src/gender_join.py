import pandas as pd
import os

# join gender csv with feature csv
def gender_join(feature_df: pd.DataFrame, gender_df: pd.DataFrame, on="speaker"):
    # if gender column is already present in feature_df, return it
    if "gender" in feature_df.columns:
        print("Feature df already has gender column")
        return feature_df

    if on == "speaker":
        # add speaker column to feature_df and gender_df if not already there
        if "speaker" not in feature_df.columns:
            speakers = [filename.split("_")[0] for filename in feature_df["filename"].tolist()]
            feature_df["speaker"] = speakers
        if "speaker" not in gender_df.columns:
            speakers = [filename.split("_")[0] for filename in gender_df["filename"].tolist()]
            gender_df["speaker"] = speakers
        
        print(feature_df)
        print(gender_df)
    
    # left join since we may have multiple records in feature_df for a single speaker
    combined_df: pd.DataFrame = feature_df.merge(gender_df, on=on, how="left")
    print(combined_df)
        
    # check no n/a values in gender col
    gender_is_na = combined_df["gender"].isna()
    if gender_is_na.sum() > 0:
        print("WARNING: There are null values in gender column")
        print("Printing records with null genders")
        for record, na in zip(combined_df, gender_is_na):
            if na:
                print(record)
        raise Exception("Null genders")

    return combined_df



def main():
    feature_df = pd.read_csv("../results/pjs-ted-combined.csv")
    gender_df = pd.read_csv("../results/ted-gender.csv")
    combined_df = gender_join(feature_df, gender_df, on="filename")
    if combined_df == 1:
        print("ERROR: gender_join failed")
        return 1
    combined_df.to_csv("../results/pjs-ted-gender.csv", index=False)
    return 0

if __name__ == "__main__":
    main()
