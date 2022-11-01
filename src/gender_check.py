from fileinput import filename
import pandas as pd

def is_probably_woman(meanF0) -> bool: 
    if meanF0 > 160:
        return True
    elif meanF0 <= 160:
        return False
    else:
        raise Exception("Invalid meanF0")


def main():
    # read meanF0 and genders from files
    pjs_df = pd.read_csv("../results/pjs-combined.csv")
    pjs_df.sort_values(by=["filename"], inplace=True)
    pjs_df.reset_index(inplace=True)
    meanF0s = pjs_df["meanF0"].values
    gender_df = pd.read_csv("../results/GenderedTed.csv")
    gender_df.sort_values(by=["filename"], inplace=True)
    gender_df.reset_index(inplace=True)
    genders = gender_df["gender"].values
    filenames = pjs_df["filename"].tolist()
    gender_df_filenames = [filename.split('.')[0] for filename in gender_df["filename"].values]
    if (filenames != gender_df_filenames):
        print("Some filenames do not match between pjs_df and gender_df")
        for filename, gender_df_filename in zip(filenames, gender_df_filenames):
            if filename != gender_df_filename:
                print(filename, gender_df_filename)
        return 1
    
    matches = 0
    for meanF0, gender, filename in zip(meanF0s, genders, filenames):
        if (is_probably_woman(meanF0) and gender.upper() == "M") or (not is_probably_woman(meanF0) and gender.upper() == "F"):
            print(f"{filename} is {gender.upper()} in csv but has meanF0 of {meanF0}")
        else:
            matches += 1
    print(matches)

if __name__ == "__main__":
    main()
