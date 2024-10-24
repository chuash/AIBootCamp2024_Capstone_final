import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(layout="wide", page_title="My Streamlit App")
# endregion <--------- Streamlit App Configuration --------->

st.title("Methodology")
st.write("""In **About Us**, an overview of the features for the three tools supporting the three use cases is presented. Here, the implementation details
         and data flows for each tool will be explained, accompanied by flow charts illustrating the process flow behind each tool.""")

st.subheader("ResaleStats")
st.image(
    "./pages/images/ResaleStats.drawio.png",
    caption="Flow chart showing overall process flow for ResaleStats",
    width=1024,
)
st.write("""The 5 downloaded csv files were preprocesed before visualisation. The following details the data preprocessing steps. After preprocessing, visualisations
         , including filters, are created using standard streamlit functions.""")
data_transformation = """
**Data preprocessing and transformation**
1) *HDB Resale Price Index (1Q2009 = 100), Quarterly*
    - Read csv into pandas dataframe and filter for time period ('quarter') to start from 2004-Q1.
    - Keep the 'quarter' and 'index' fields, and store the dataframe as csv in the data folder.
2) *Median Resale Prices for Registered Applications by Town and Flat Type*
    - Read csv into pandas dataframe and filter for time period ('quarter') to start from 2020-Q1 (past 5 years).
    - Replace 'na' and '-' values in the price field with None.
    - Select the fields 'quarter', 'town', 'flat_type' and 'price', and store the dataframe as csv in the data folder.
3) *Resale flat prices based on registration date from Jan-2017 onwards*
    - Read csv into pandas dataframe and filter for time period ('month') to start from 2023-10 (past 12 months).
    - Remove redundant field - 'remaining_lease', and store the dataframe as csv in the data folder.
4) *CEA Salespersons’ Property Transaction Records (residential)*, *CEA Salesperson Information*
    - Read both csvs into pandas dataframes.
    - For the dataframe from the first csv:
        - Convert the 'transaction_date' field to python datetime format and filter to start from 2023-09-01
        - Remove records that are not associated with any salesperson.
        - Given the focus on HDB flat resale activity, remove other transaction activities by filtering for 'property_type' is HDB and 
          'transaction_type' is resale.
    - Left-join this processed dataframe with the dataframe from the second csv by the common key -> salesperson registration number, so
      as to get the real estate company that the salesperson is employed under
    - Select the relevant fields and store the joint dataframe as csv in the data folder.\n   
(For specific codes, refer to https://github.com/chuash/AIBootCamp2024_Capstone_final/blob/main/data_prep.py)
"""
st.write(data_transformation)
st.write("""In addition to interactive data analysis, users are also able to query data using words or natural language. The following details the implementation
         steps for the chat with data agent""")
st.image(
    "./pages/images/ResaleStatsChatAgent.drawio.png",
    caption="Flow chart showing process flow for chat with data agent",
    width=512,
)
agent = """
**Chat with data agent**
- Under the hood, the 'create_pandas_dataframe_agent' from *langchain_experimental.agents.agent_toolkits* is used, which in turn utilises OpenAI's 'gpt-4o-mini' model.
- When user inputs query, an OpenAI API call is made to ask gpt-4o-mini, suitably prompted with system message and few shot learning examples, to assess for
  potential prompt injection and malicious instructions. 
- If assessment is negative, then another OpenAI API call will be made to ask gpt-4o-mini, again suitably prompted with system message and few shot learning examples,to
  assess if the query is related to the underlying dataset. To help the LLM better assess, the dataset metadata is included in the system message to let the LLM understand
  the data it has access to. As added precaution against prompt injection, XML-like tags are used in both system and user messages.
- If assessment is positive, i.e. query is related to underlying dataset, then the 'create_pandas_dataframe_agent' is initialised, which will then access python repl tool
  to execute script on the underlying dataset. Queried results from the dataset are then passed to LLM to generate user response.
  
(For specific codes, refer to https://github.com/chuash/AIBootCamp2024_Capstone_final/blob/main/logics/agent.py)
"""
st.write(agent)

st.subheader("ResaleSearch")
st.image(
    "./pages/images/RAG.png",
    caption="Flow chart showing overall process flow for ResaleSearch",
    width=1024,
)