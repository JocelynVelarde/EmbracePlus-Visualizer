import json
import pandas as pd

# List of input file paths
input_file_paths = ["AVROS final/Primera/Meditador 1/1-1-MED1_1714159675.csv", "AVROS final/Primera/Meditador 1/1-1-MED1_1714161478.csv", "AVROS final/Primera/Meditador 1/1-1-MED1_1714163277.csv"]

# Initialize an empty DataFrame for the combined data
combined_eda = pd.DataFrame()

# Loop over the files
for file_path in input_file_paths:
    # Read the file into a DataFrame
    df = pd.read_csv(file_path)

    # Extract the "eda" data from the "rawData" column and convert it from JSON to a DataFrame
    eda = df['rawData'].apply(json.loads).apply(lambda x: x['eda']).apply(pd.Series)

    # Append the "eda" data to the combined DataFrame
    combined_eda = combined_eda.append(eda, ignore_index=True)


combined_eda.to_csv("combined_eda.csv", index=False)