import streamlit as st
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
    combined_temperature = pd.DataFrame()

    eda_frames = []
    bvp_frames = []
    temperature_frames = []

    for file in uploaded_files:
        reader = fastavro.reader(file)
        records = [r for r in reader]
        df = pd.DataFrame.from_records(records)
        dataframes.append(df)
        if df['rawData'].apply(lambda x: isinstance(x, dict)).all():
            eda = df['rawData'].apply(lambda x: x['eda']).apply(pd.Series)
            bvp = df['rawData'].apply(lambda x: x['bvp']).apply(pd.Series)
            temp = df['rawData'].apply(
                lambda x: x['temperature']).apply(pd.Series)
        else:
            eda = df['rawData'].apply(json.loads).apply(
                lambda x: x['eda']).apply(pd.Series)
            bvp = df['rawData'].apply(json.loads).apply(
                lambda x: x['bvp']).apply(pd.Series)
            temp = df['rawData'].apply(json.loads).apply(
                lambda x: x['temperature']).apply(pd.Series)
        eda_frames.append(eda)
        bvp_frames.append(bvp)
        temperature_frames.append(temp)

    combined_eda = pd.concat(eda_frames, ignore_index=True)
    combined_bvp = pd.concat(bvp_frames, ignore_index=True)
    combined_temperature = pd.concat(temperature_frames, ignore_index=True)
    st.write(uploaded_files)

    combined_eda = combined_eda.sort_values('timestampStart')
    combined_eda = combined_eda.explode('values')
    combined_bvp = combined_bvp.sort_values('timestampStart')
    combined_bvp = combined_bvp.explode('values')
    combined_temperature = combined_temperature.sort_values('timestampStart')
    combined_temperature = combined_temperature.explode('values')

    time_data_eda = []
    time_data_bvp = []
    time_data_temperature = []
    eda_data = []
    bvp_data = []
    temperature_data = []
    accumulated_time_eda = 0
    accumulated_time_bvp = 0
    accumulated_time_temperature = 0

    for _, row in combined_eda.iterrows():
        values = row['values']
        time = np.arange(0, 1/row['samplingFrequency'],
                         1/row['samplingFrequency'])
        time += accumulated_time_eda
        accumulated_time_eda = time[-1]
        time_data_eda.extend(time)
        eda_data.append(values)

    for _, row in combined_bvp.iterrows():
        values = row['values']
        time = np.arange(0, 1/row['samplingFrequency'],
                         1/row['samplingFrequency'])
        time += accumulated_time_bvp
        accumulated_time_bvp = time[-1]
        time_data_bvp.extend(time)
        bvp_data.append(values)

    for _, row in combined_temperature.iterrows():
        values = row['values']
        time = np.arange(0, 1/row['samplingFrequency'],
                         1/row['samplingFrequency'])
        time += accumulated_time_temperature
        accumulated_time_temperature = time[-1]
        time_data_temperature.extend(time)
        temperature_data.append(values)

    data_eda = pd.DataFrame({
        'Time': time_data_eda,
        'EDA': eda_data
    })

    data_bvp = pd.DataFrame({
        'Time': time_data_bvp,
        'BVP': bvp_data
    })

    data_temperature = pd.DataFrame({
        'Time': time_data_temperature,
        'Temperature': temperature_data
    })

    st.title("EDA Data")
    st.divider()
    st.line_chart(data_eda)
    st.caption(
        "To obtain the data in minutes, divide the x-axis by 4 and then by 60.")
    st.caption("For example: 14,000 / 4 = 3,500 and 3,500 / 60 = 58.33 minutes")

    st.title("BVP Data")
    st.divider()
    st.line_chart(data_bvp)
    st.caption(
        "To obtain the data in minutes, divide the x-axis by 64 and then by 60.")
    st.caption("For example 240,000 / 64 = 3,750 and 3,750 / 60 = 62.5 minutes")

    st.title("Temperature Data")
    st.divider()
    st.line_chart(data_temperature)
    st.caption(
        "To obtain the data in minutes, divide the x-axis by 0.999 and then by 60.")
    st.caption("For example 260 / 0.999 = 260.26 and 260.26 / 60 = 4.3 minutes")

    st.title("Dataframe download")
    st.subheader(
        "Make sure to hover at the top of the table to download as .csv")
    st.write("EDA Data")
    st.write(combined_eda)
    st.divider()
    st.write("BVP Data")
    st.write(combined_bvp)
    st.divider()
    st.write("Temperature Data")
    st.write(combined_temperature)

    st.divider()
    st.subheader("Splitting the dataframes into two halves if data is to large to download")

    # Calculate the midpoint of the DataFrame
    midpoint = len(combined_bvp) // 2

    # Split the DataFrame into two halves
    combined_bvp_first_half = combined_bvp.iloc[:midpoint]
    combined_bvp_second_half = combined_bvp.iloc[midpoint:]

    # Write the first half
    st.write("BVP Data - First Half")
    st.write(combined_bvp_first_half)

    # Write the second half
    st.write("BVP Data - Second Half")
    st.write(combined_bvp_second_half)

    return dataframes


st.set_page_config(
    page_title="EmbracePlus Visualizer",
    page_icon="📈",
)

st.title("Upload your .avro files here to visualize them 🔍")


uploaded_files = st.file_uploader(
    "Upload Files", type="avro", accept_multiple_files=True)
visualize_files = st.button("Upload Files")

st.title("Timestamp Converter for EDA")
timeCalculate = st.number_input(
    "Enter the timestamp you want to convert in minutes")
timeCalculate = timeCalculate / 4
timeCalculate = timeCalculate / 60
st.write("The time in minutes is: ", timeCalculate)

st.title("Timestamp Converter for BVP")
timeCalculateBVP = st.number_input(
    "Enter the timestamp you want to convert in minutes", key="bvp")
timeCalculateBVP = timeCalculateBVP / 64
timeCalculateBVP = timeCalculateBVP / 60
st.write("The timestamp in minutes is: ", timeCalculateBVP)

st.title("Timestamp Converter for Temperature")
timeCalculateTemperature = st.number_input(
    "Enter the timestamp you want to convert in minutes", key="temperature")
timeCalculateTemperature = timeCalculateTemperature / 0.999
timeCalculateTemperature = timeCalculateTemperature / 60
st.write("The timestamp in minutes is: ", timeCalculateTemperature)

if visualize_files and uploaded_files:
    st.success("Files uploaded successfully, visualizing...")
    dataframes = convert_files(uploaded_files)

else:
    st.warning("Please upload files to visualize")


st.divider()

st.write("Code by: [JocelynVelarde](https://github.com/JocelynVelarde)")
