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
proj_scope = """
This web-based application is a capstone deliverable for the AI Champions Bootcamp(July 2024 - Oct 2024) conducted by Government Technology Agency of Singapore.
The capstone aims to assess bootcampers' ability to synthesize trainings on advanced Prompt Engineering, advanced Retrieval Augmented Generation, AI Agents and
web-app development and deployment via Streamlit. The scope of work includes:
1) Domain area - research and choose specific public service domain area to work on;
2) Data sources - select relevant data from various official and trustworthy sources that are publicly accessible;
3) Use cases - for the chosen domain area, conceptualise use cases to address specific user needs;
4) Backend development - strategise optimal means to extract data from sources, clean and process the data according to use case requirements and efficiently
                         store the data for downstream processes;
5) Frontend development - conceptualise user interface design and implementation;
6) System integration - synthesize frontend and backend development, including relevant security measures to minimise the chances of the app being exploited.
"""
st.write(proj_scope)
st.divider()
st.subheader("Objectives")
objectives = """
This application focuses on the *purchase of HDB flat in the resale market*.\n
**The Problem**\n
Individuals purchasing a resale HDB flat, especially first-timers, can easily feel overwhelmed by the sheer amount of information involved. From understanding
resale trends by location and flat types, to navigating HDB’s terms and conditions, and preparing for the associated costs of homeownership, the process can be
daunting. Choosing the right real estate agent also requires research, and while agents can assist with information gathering, not all provide thorough insights
that benefit the buyer. Additionally, some buyers may prefer not to engage an agent at all. In such cases, buyers must conduct their own research, which can be 
time-consuming and challenging, particularly for busy working adults.\n
**Proposed Solution**\n
Imagine having an interactive, one-stop platform that aggregates accurate, up-to-date information from official and trusted sources—one that is also tailored to
guide buyers through every step of their resale HDB flat journey, from the moment they decide to start their search. This application aims to fulfil these objectives
via three use cases.
1) 
"""
st.write(objectives)
st.divider()
st.subheader("Data Sources")
st.divider()
st.subheader("App Features")