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
    filelist = [
        "1_HDBResalePriceIndex2009_2024.csv",
        "2_HDBMedianResalePrices2020_2024.csv",
        "3_HDBResalePricesDetailsOct23_Oct24.csv",
        "4_CEAAgentTransactionsSep23-Sep24.csv",
    ]
    datalist = []
    for file in filelist:
        df = pd.read_csv(f"{directory}/" + file)
        datalist.append(df)
    return datalist[0], datalist[1], datalist[2], datalist[3]


# Load all relevant datasets for visualisation
df1, df2, df3, df4 = load_data()
df3["lease_commence_date"] = df3["lease_commence_date"].astype(str)

# Initialise memory for RenoChat in session_state
if "chatbot_memory" not in st.session_state:
    st.session_state["chatbot_memory"] = [{"role": "system", "content": system_msg}]

st.markdown(
    "### Need help with buying HDB resale flats? You may find the following 3 tools useful 😃"
)

st.markdown(
    "#### 1. ResaleStats - Your Insightful Data Illustrator"
)

col_topleft, col_topright = st.columns(2, gap='medium')

with col_topleft:
    # line chart
    st.write("**1a. HDB Resale Price Index from 2004Q1 (index=100 in 2009Q1)**")
    st.line_chart(df1, x="quarter", y="index", x_label="quarter", y_label="Price Index")

with col_topright:
    # bar chart
    st.write(
        "**1b. HDB Median Resale Prices($), by flat types, across locations and over time from 2020Q1**"
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

st.divider()

st.write("*The following location filter applies to both tables in 1c and 1d*")
townoptions = st.multiselect(
        "Select the location(s)",
        options=df3.town.unique().tolist(),
        default=df3.town.unique().tolist(),
        key="town_selector",
    )

col_midleft, col_midright = st.columns(2, gap='medium')

with col_midleft:
    st.write("**1c. HDB Resale Transaction Details (Oct 2023-Oct 2024)**")
    # st.sidebar.write("Filters for HDB Resale Transaction Details")
    fieldoptions = st.multiselect(
        "Select the fields to be displayed",
        options=df3.columns.tolist(),
        default=df3.columns.tolist(),
        key="field_selector",
    )
    monthoptions = st.multiselect(
        "Select the time period(s)",
        options=df3.month.unique().tolist(),
        default=df3.month.unique().tolist(),
        key="month_selector",
    )
    flatoptions = st.multiselect(
        "Select the flat type(s)",
        options=df3.flat_type.unique().tolist(),
        default=df3.flat_type.unique().tolist(),
        key="flat_selector",
    )
    # Subset HDB Resale Transaction Details dataset based on applied filters
    df3_filter = df3[
        (df3["month"].isin(monthoptions))
        & (df3["town"].isin(townoptions))
        & df3["flat_type"].isin(flatoptions)
    ]
    # display HDB Resale Transaction Details data as table visualisation
    st.dataframe(df3_filter, column_order=fieldoptions, key="pricedetails_df")
    # Widget for chatting with HDB Resale Transaction Details data
    form = st.form(key="ResaleTxnDetails")
    form.write("Chat with your data!")

    user_query_HDB = form.text_area(
        """Try querying the above HDB resale transaction details data in words""",
        height=30, key="ResaleTxnDetails_text"
    )

    if form.form_submit_button("Submit"):
        st.toast(f"Query Submitted - {user_query_HDB}")
        response_HDB = llm.LLM_query_df(user_query_HDB, df3_filter, llm.system_msg_HDB)
        st.write(response_HDB)

with col_midright:
    st.write("**1d. CEA Agent Transaction Details (Sep 2023-Oct 2024)**")
    # Subset CEA Agent Transaction Details dataset based on applied town filter
    df4_filter = df4[df4["town"].isin(townoptions)]
    # display CEA Agent Transaction Details data as table visualisation
    st.dataframe(df4_filter, column_order=['resale_transaction_date', 'town', 'sales_agent_name', 'real_estate_company_name'], key="CEAdetails_df")
    # Widget for chatting with CEA Agent Transaction Details data
    form = st.form(key="CEAAgentTxnDetails")
    form.write("Chat with your data!")

    user_query_CEA = form.text_area(
        """Try querying the above CEA agent transaction details data in words""",
        height=30, key="CEAAgentTxnDetails_text"
    )

    if form.form_submit_button("Submit"):
        st.toast(f"Query Submitted - {user_query_CEA}")
        response_CEA = llm.LLM_query_df(user_query_CEA, df4_filter, llm.system_msg_CEA)
        st.write(response_CEA)

st.divider()

col_bottomleft, col_bottomright = st.columns(2, gap='medium')

with col_bottomright:
    # st.write(st.session_state.chatbot_memory)
    form = st.form(key="renochatform")
    form.markdown("#### 3. RenoChat-Your Friendly Renovation Assistant")

    user_prompt = form.text_area(
        """Pose your renovation related queries here and the assistant\
        will provide you with curated answers sourced from internet.
        (NB: the AI bot has been told not to entertain any\
        non-renovation related queries) :""",
        height=200, key="renochatform_text"
    )

    if form.form_submit_button("Submit"):
        st.toast(f"Query Submitted - {user_prompt}")
        st.divider()
        response, memory = chatbot_response(
            user_prompt, st.session_state["chatbot_memory"]
        )
        st.session_state["chatbot_memory"] = memory
        st.write(response)