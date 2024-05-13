import pandas as pd
import fastavro
import json
import csv
import json
import ast
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




def convert_files(uploaded_files):
    dataframes = []
    combined_eda = pd.DataFrame()

    for file in uploaded_files:
        reader = fastavro.reader(file)
        records = [r for r in reader]
        df = pd.DataFrame.from_records(records)
        dataframes.append(df)
        if df['rawData'].apply(lambda x: isinstance(x, dict)).all():
            # If all elements in 'rawData' are dictionaries, no need to use json.loads
            eda = df['rawData'].apply(lambda x: x['eda']).apply(pd.Series)
        else:
            # If not all elements in 'rawData' are dictionaries, use json.loads
            eda = df['rawData'].apply(json.loads).apply(lambda x: x['eda']).apply(pd.Series)
        combined_eda = combined_eda.append(eda, ignore_index=True)

      
    combined_eda = combined_eda.sort_values('timestampStart')
    combined_eda = combined_eda.explode('values')
    time_data = []
    eda_data = []
    accumulated_time = 0 

    for _, row in combined_eda.iterrows():
        values = row['values']
        time = np.arange(0, 1/row['samplingFrequency'], 1/row['samplingFrequency'])
        time += accumulated_time
        accumulated_time = time[-1]
        #time_data = [t / row['samplingFrequency'] for t in time_data]
        time_data.extend(time)
        eda_data.append(values)

    data = pd.DataFrame({
        'Time': time_data,
        'EDA': eda_data
    })

    st.line_chart(data)
    st.write(combined_eda)
    

    return dataframes


import streamlit as st

st.write("Upload your AVRO files here and we will graph them for you!")

uploaded_files = st.file_uploader("Upload Files", type="avro", accept_multiple_files=True)
dataframes = convert_files(uploaded_files)


