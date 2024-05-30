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

    eda_frames = []
    bvp_frames = []

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
        eda_frames.append(eda)
        bvp_frames.append(bvp)

    combined_eda = pd.concat(eda_frames, ignore_index=True)
    combined_bvp = pd.concat(bvp_frames, ignore_index=True)
    st.write(uploaded_files)    
      
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
  
    st.title("EDA Data Filtered 2160-9361")
    data_index = data_eda.iloc[2160:9361]
    st.line_chart(data_index)
    st.caption("EDA Data filtered from 2160 to 9361")

    st.title("EDA Data Filtered 2400-9600")
    data_index_two = data_eda.iloc[2400:9600]
    st.line_chart(data_index_two)
    st.caption("EDA Data filtered from 2400 to 9600")

    st.title("EDA Data")
    st.divider()
    st.line_chart(data_eda)
    st.caption("To obtain the data in minutes, divide the x-axis by 4 and then by 60.")
    st.caption("For example: 14,000 / 4 = 3,500 and 3,500 / 60 = 58.33 minutes")

    st.title("BVP Data")
    st.divider()
    st.line_chart(data_bvp)
    st.caption("To obtain the data in minutes, divide the x-axis by 64 and then by 60.")
    st.caption("For example 240,000 / 64 = 3,750 and 3,750 / 60 = 62.5 minutes")

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

st.title("Time Converter for EDA")
timeCalculate = st.number_input("Enter the time you want to convert in minutes")
timeCalculate = timeCalculate / 4
timeCalculate = timeCalculate / 60
st.write("The time in minutes is: ", timeCalculate)

st.title("Time Converter for BVP")
timeCalculateBVP = st.number_input("Enter the time you want to convert in minutes", key="bvp")
timeCalculateBVP = timeCalculateBVP / 64
timeCalculateBVP = timeCalculateBVP / 60
st.write("The time in minutes is: ", timeCalculateBVP)

if visualize_files and uploaded_files:
    st.success("Files uploaded successfully, visualizing...")
    dataframes = convert_files(uploaded_files)

else:
    st.warning("Please upload files to visualize")



st.divider()

st.write("Code by: [JocelynVelarde](https://github.com/JocelynVelarde)")