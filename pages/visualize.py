import pandas as pd
import fastavro
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def convert_files(uploaded_files):
    dataframes = []
    combined_eda = pd.DataFrame()
    combined_bvp = pd.DataFrame()

    for file in uploaded_files:
        reader = fastavro.reader(file)
        records = [r for r in reader]
        df = pd.DataFrame.from_records(records)
        dataframes.append(df)
        if df['rawData'].apply(lambda x: isinstance(x, dict)).all():
            eda = df['rawData'].apply(lambda x: x['eda']).apply(pd.Series)
            bvp = df['rawData'].apply(lambda x: x['bvp']).apply(pd.Series)
        else:
            eda = df['rawData'].apply(json.loads).apply(lambda x: x['eda']).apply(pd.Series)
            bvp = df['rawData'].apply(json.loads).apply(lambda x: x['bvp']).apply(pd.Series)
        combined_eda = combined_eda.append(eda, ignore_index=True)
        combined_bvp = combined_bvp.append(bvp, ignore_index=True)

      
    combined_eda = combined_eda.sort_values('timestampStart')
    combined_eda = combined_eda.explode('values')
    combined_bvp = combined_bvp.sort_values('timestampStart')
    combined_bvp = combined_bvp.explode('values')
    
    time_data_eda = []
    time_data_bvp = []
    eda_data = []
    bvp_data = []
    accumulated_time_eda = 0 
    accumulated_time_bvp = 0

    for _, row in combined_eda.iterrows():
        values = row['values']
        time = np.arange(0, 1/row['samplingFrequency'], 1/row['samplingFrequency'])
        time += accumulated_time_eda
        accumulated_time_eda = time[-1]
        time_data_eda.extend(time)
        eda_data.append(values)

    for _, row in combined_bvp.iterrows():
        values = row['values']
        time = np.arange(0, 1/row['samplingFrequency'], 1/row['samplingFrequency'])
        time += accumulated_time_bvp
        accumulated_time_bvp = time[-1]
        time_data_bvp.extend(time)
        bvp_data.append(values)

    data_eda = pd.DataFrame({
        'Time': time_data_eda,
        'EDA': eda_data
    })

    data_bvp = pd.DataFrame({
        'Time': time_data_bvp,
        'BVP': bvp_data
    })

    st.title("EDA Data")
    st.divider()
    st.line_chart(data_eda)

    st.title("BVP Data")
    st.divider()
    st.line_chart(data_bvp)

    st.title("Dataframe download")
    st.write("EDA Data")
    st.write(combined_eda)
    st.divider()
    st.write("BVP Data")
    st.write(combined_bvp)
    
    return dataframes


import streamlit as st

st.set_page_config(
        page_title="EmbracePlus Visualizer",
        page_icon="📈",
)

st.title("Upload your .avro files here to visualize them 🔍")

uploaded_files = st.file_uploader("Upload Files", type="avro", accept_multiple_files=True)
visualize_files = st.button("Upload Files")

if visualize_files and uploaded_files:
    st.success("Files uploaded successfully, visualizing...")
    dataframes = convert_files(uploaded_files)

else:
    st.warning("Please upload files to visualize")


st.divider()

st.write("Code by: [JocelynVelarde](https://github.com/JocelynVelarde)")
