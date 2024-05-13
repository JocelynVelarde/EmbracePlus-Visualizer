import streamlit as st

st.set_page_config(
        page_title="EmbracePlus Visualizer",
        page_icon="📈",
)
st.title("Get Started with EmbracePlus Visualizer 📈")

st.divider()

st.header(":blue[Upload your .avro files and we will graph them for you!]")
st.write("1. Click on the 'Browse files' button to upload your AVRO files. You can select all of the files related to a session at once.")
st.write("2. Once you have uploaded the files, click on the 'Visualize' button to see the graphs.")
st.write("3. You can also download the data in CSV format by clicking on the 'Download CSV' button.")
st.write("4. If you want to clear the uploaded files, click on the 'Clear Files' button.")
st.write("5. If you want to save the graphs as an image, click on the 'Save as Image' button.")


st.header("Example of a processed graph:")

container = st.container(border=True)

st.caption("Note: This is an example of a graph that will be generated after uploading the files. The actual graph will be based on the data in your files.")
container.image("assets/example.png", use_column_width=True)


st.divider()

st.page_link("pages/visualize.py", label="Click this button to start uploading", icon="📁")

st.divider()

st.write("Code by: [JocelynVelarde](https://github.com/JocelynVelarde)")