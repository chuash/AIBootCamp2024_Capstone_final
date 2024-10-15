import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(layout="wide", page_title="My Streamlit App")
# endregion <--------- Streamlit App Configuration --------->

st.title("Methodology")
st.write("- A comprehensive explanation of the data flows and implementation details.")
st.write("- A flowchart illustrating the process flow for each of the use cases in the application.")
st.image("./images/Flow_chart1.jpg, caption= flow chart showing process flow for use case 1")
st.image("./images/Flow_chart2.jpg, caption= flow chart showing process flow for use case 2")
