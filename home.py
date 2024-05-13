import streamlit as st

st.title("Get Started with our platform! 💡")

st.divider()

st.header(":blue[Tell us your location and destination to get the safest route]")
st.write("1. Type your desired route in the search bar.")
st.write("2. Speak your desired route using the microphone button.")
st.write("3. Click on the 'Search Route' button to get the safest route to your destination.")
st.write("4. View your route on an interactive map")
st.write("5. Also get understandable instructions to reach your destination.")

st.header("Example of a user's request")

container = st.container(border=True)

st.caption("You can just go ahead and type or speak any way you like and we will understand you.")
container.write("I want to go from Churubusco to Coapa but I do not know how, could you help me?")


st.divider()

st.page_link("pages/visualize.py", label="Click this button to Search Route", icon="🔍")

st.divider()

st.write("Thank you for choosing SafeNav!")