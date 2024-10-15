import os
import pandas as pd
import streamlit as st
from helper_functions.utility import check_password

from helper_functions import llm
from logics.renochat import chatbot_response, system_msg


# region <--------- Streamlit App Configuration --------->
st.set_page_config(layout="wide", page_title="HDB Resale Tips App")
# endregion <--------- Streamlit App Configuration --------->

st.title("HDB Resale Tips App")

with st.expander("*Disclaimer*"):
    st.write(
        """

    **IMPORTANT NOTICE**:

    This web application is a prototype developed for **educational purposes only**. The information provided here is **NOT intended for real-world usage** and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

    Always consult with qualified professionals for accurate and personalized advice.

    """
    )

# st.cache_data.clear()

# Do not continue if check_password is not True.
if not check_password():
    st.stop()


# Declaring functions relevant for visuals
@st.cache_data
def load_data(directory="./data"):
    """This function loads all relevant datasets for visualisation

    Args:
        directory (str, optional): Directory where data files are stored. Defaults to "./data".

    Returns:
        _type_: relevant datasets in pandas dataframe
    """
    datalist = []
    for file in os.listdir(directory):
        df = pd.read_csv(f"{directory}/" + file)
        datalist.append(df)
    return datalist[0], datalist[1], datalist[2], datalist[3]


def filterdf(df, colname, value):
    return df[df[colname] == value]


# Load all relevant datasets for visualisation
df1, df2, df3, df4 = load_data()
df3["lease_commence_date"] = df3["lease_commence_date"].astype(str)

# Initialise memory for RenoChat in session_state
if "chatbot_memory" not in st.session_state:
    st.session_state["chatbot_memory"] = [{"role": "system", "content": system_msg}]

st.markdown(
    "#### Need help with buying HDB resale flats? You may find the following tools useful 😃"
)

col_left, col_right = st.columns([0.6, 0.4])

with col_right:
    # st.write(st.session_state.chatbot_memory)
    form = st.form(key="renochatform")
    form.subheader("RenoChat-Your Friendly Renovation Assistant")

    user_prompt = form.text_area(
        """Pose your renovation related queries here and the assistant\
        will provide you with curated answers sourced from internet.
        (NB: the AI bot has been told not to entertain any\
        non-renovation related queries) :""",
        height=200,
    )

    if form.form_submit_button("Submit"):
        st.toast(f"Query Submitted - {user_prompt}")
        st.divider()
        response, memory = chatbot_response(
            user_prompt, st.session_state["chatbot_memory"]
        )
        st.session_state["chatbot_memory"] = memory
        st.write(response)
        st.divider()

with col_left:
    st.write("**1. HDB Resale Price Index from 2004Q1 (index=100 in 2009Q1)**")
    st.line_chart(df1, x="quarter", y="index", x_label="quarter", y_label="Price Index")
    
    st.write(
        "**2. HDB Median Resale Prices($), by flat types, across locations and over time from 2020Q1**"
    )
    # radio buttons to select either by location or period
    period_location = st.radio(
        "2) Filter HDB median resale prices by: ",
        ["Location", "Period"],
        key="period_loc_selector",
        horizontal=True,
        captions=[
            "Prices over periods for a selected location",
            "Prices over locations for a selection time period",
        ],
    )
    # if location is selected
    if period_location == "Location":
        loc_value = st.selectbox(
            "Select a location", df2.town.unique().tolist(), key="loc_selector"
        )
        st.bar_chart(
            df2[df2["town"] == loc_value],
            x="quarter",
            y="price",
            y_label="price($)",
            color="flat_type",
            stack=False,
        )
    else:
        period_value = st.selectbox(
            "Select a time period", df2.quarter.unique().tolist(), key="period_selector"
        )
        st.bar_chart(
            df2[df2["quarter"] == period_value],
            x="town",
            y="price",
            y_label="price($)",
            color="flat_type",
            stack=False,
        )
    
    st.write("**3. HDB Resale Transaction Details (Oct 2023-Oct 2024)**")
    st.sidebar.write("Filters for HDB Resale Transaction Details")
    # Creating filters at the sidebar
    fieldoptions = st.sidebar.multiselect(
        "Select the fields to be displayed",
        options=df3.columns.tolist(),
        default=df3.columns.tolist(),
        key="field_selector",
    )
    townoptions = st.sidebar.multiselect(
        "Select the locations",
        options=df3.town.unique().tolist(),
        default=df3.town.unique().tolist(),
        key="town_selector",
    )
    monthoptions = st.sidebar.multiselect(
        "Select the periods",
        options=df3.month.unique().tolist(),
        default=df3.month.unique().tolist(),
        key="month_selector",
    )
    flatoptions = st.sidebar.multiselect(
        "Select the flat types",
        options=df3.flat_type.unique().tolist(),
        default=df3.flat_type.unique().tolist(),
        key="flat_selector",
    )
    # Subset HDB Resale Transaction details dataset based on applied filters
    df3_filter = df3[
        (df3["month"].isin(monthoptions))
        & (df3["town"].isin(townoptions))
        & df3["flat_type"].isin(flatoptions)
    ]
    st.dataframe(df3_filter, column_order=fieldoptions, key="pricedetails_df")
    form = st.form(key="ResaleTxnDetails")
    form.write("Chat with your data!")

    user_query_HDB = form.text_area(
        """Try querying the above HDB resale transaction details data in words""",
        height=50,
    )

    if form.form_submit_button("Submit"):
        st.toast(f"Query Submitted - {user_query_HDB}")
        response_HDB = llm.LLM_query_df(
            user_query_HDB, df3_filter)
        st.write(response_HDB)
