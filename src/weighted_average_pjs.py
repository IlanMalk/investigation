# %%
import pandas as pd
import numbers
import glob
import traceback

# %%
def weighted_average(speech_df_og: pd.DataFrame):
    speech_df = speech_df_og.dropna()
    speech_df.reset_index(drop=True, inplace=True)
    
    # check we've successfully removed null values
    if speech_df.isna().sum().sum() > 0:
        print("OOPS")
        assert(False)
    # check no empty records or records with wrong number of columns
    if speech_df.shape[0] < 1 or speech_df.shape[1] != 17:
        print("--------------------------------------")
        print("PROBLEM WITH SHAPE!")
        print(speech_df["filename"])
        print(f"{speech_df.shape}")
        print("--------------------------------------")

    durations = list(speech_df.duration.values)        

    average_dict = {}
    average_dict["filename"] = speech_df["filename"][0]
    total_duration: float = sum(speech_df["duration"])
    average_dict["duration"] = total_duration
    
    for (columnName, columnData) in speech_df.items():
        if (columnName == "filename" or columnName == "start" or columnName == "duration"):
            continue
        
        weighted_sum = 0.0
        for i, value in enumerate(columnData.values):
            if not isinstance(value, numbers.Number):
                print(f"Column '{columnName}' contains non-numeric value {value}")
                break

            weighted_sum +=  value * durations[i]

        weighted_average = weighted_sum/total_duration
        average_dict[columnName] = weighted_average

    average_df_columns = speech_df.columns.drop(["start"])
    average_df = pd.DataFrame(data=average_dict, columns=average_df_columns, index=[0])
    return average_df




# %%
average_dfs = []
for csv_file in sorted(glob.glob("../results/pjs-ted/*.csv")):
    speech_df = pd.read_csv(csv_file)
    try:
        average_df = weighted_average(speech_df)
        average_dfs.append(average_df)
    except:
        print(csv_file)
        traceback.print_exc()
    
    
    
combined_df = pd.concat(average_dfs, ignore_index=True)

# check no null values
if combined_df.isna().sum().sum() > 0:
    print("NULL VALUES IN COMBINED DF")
    

combined_df.to_csv("../pjs-combined.csv")
combined_df.head()