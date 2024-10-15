import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="My Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About Us")
st.write("This page provides details on the project scope, objectives of the project, data sources used, and features of the app.")
st.subheader("Project Scope")
st.divider()
st.subheader("Objectives")
st.divider()
st.subheader("Data Sources")
st.divider()
st.subheader("App Features")