'''import csv
import json
import matplotlib.pyplot as plt
import numpy as np

csv.field_size_limit(2147483647)
input_file_path = "AVROS final/Primera/Meditador 1/MED1.csv"

bvp_data = []
time_data = []

with open(input_file_path, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        raw_data = json.loads(row['rawData'])
        if 'eda' in raw_data:
            values = raw_data['eda']['values']
            sampling_frequency = raw_data['eda']['samplingFrequency']
            # Split the values into chunks of size sampling_frequency (1 second of data)
            chunks = [values[int(i):int(i + sampling_frequency)] for i in np.arange(0, len(values), sampling_frequency)]
            # Calculate the average of each chunk and add it to bvp_data
            bvp_data.extend([sum(chunk) / len(chunk) for chunk in chunks if chunk])
            # Add the corresponding time data
            time_data.extend(np.arange(0, len(bvp_data)/sampling_frequency, 1/sampling_frequency))

# Plot the data
plt.plot(time_data, bvp_data)
plt.xlabel('Time (s)')
plt.ylabel('EDA')
plt.show()'''

import csv
import json
import ast
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

csv.field_size_limit(2147483647)

# Load the combined EDA data
combined_eda = pd.read_csv("combined_eda.csv")

# Initialize lists to hold the time and EDA data
time_data = []
eda_data = []

# Initialize a variable to hold the accumulated time
accumulated_time = 0

# Loop over the rows in the DataFrame
for _, row in combined_eda.iterrows():
    # Convert the 'values' string to a list
    values = ast.literal_eval(row['values'])
    # Calculate the time for each value based on the sampling frequency
    time = np.arange(0, len(values)/row['samplingFrequency'], 1/row['samplingFrequency'])
    # Add the accumulated time to the time data
    time += accumulated_time
    # Update the accumulated time
    accumulated_time = time[-1]
    # Append the time and values data to the lists
    time_data.extend(time)
    eda_data.extend(values)

# Plot the data
plt.plot(time_data, eda_data)
plt.title('Meditador 1 (Sampled at 4Hz)')
plt.legend(['EDA'])
plt.xlabel('Time (s)')
plt.ylabel('EDA')
plt.show()