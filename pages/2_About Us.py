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
This prototype web-based application is a capstone deliverable for the AI Champions Bootcamp(July 2024 - Oct 2024) conducted by Government Technology Agency of Singapore.
The capstone aims to assess bootcampers' ability to synthesize trainings on advanced Prompt Engineering, advanced Retrieval Augmented Generation, AI Agents and
web-app development and deployment via Streamlit. The scope of work includes:
1) Domain area - research and choose specific public service domain area to work on;
2) Data sources - select relevant data from various official and trustworthy sources that are publicly accessible;
3) Use cases - for the chosen domain area, conceptualise use cases to address specific user needs;
4) Backend development - strategise optimal means to extract data from sources, clean and process the data according to use case requirements and efficiently
                         store the data for downstream processes;
5) Frontend development - conceptualise user interface design and implementation;
6) API integration - Set up API calls to allow application to communicate with commercial large language models
6) System integration - integrate frontend and backend development, including relevant security measures to minimise the chances of the app being exploited.
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
guide buyers through every step of their resale HDB flat journey, from the moment they decide to start their search. This proof-of-concept application aims to
fulfil this outcome via three tools, catering to three different use cases.
1) *ResaleStats*
	- A **dashboard** that caters to prospective buyers who might have the need to compare HDB resale prices across locations, by flat types and over time to help
    them make more informed purchasing decisions. Also provides actual transaction details by real estate agents registered with the Council for Estate Agencies (CEA)
    to provide insights on top agents.
2) *ResaleSearch*
	- A **semantic Q&A engine** that caters to prospective buyers who might not have the time to browse through the specifics of HDB resale terms and conditions
    and other relevant policies.
3) *RenoChat*
	- A **chatbot assistant** that caters to buyers who are about to renovate their resale flats and who are new to home renovation. The assistant will provide
    ideas, suggestions and answers (curated from the internet) in response to renovation related queries.
"""
st.write(objectives)
st.divider()
st.subheader("Data Sources")
data = """
Data used to develop the application include:
1) https://data.gov.sg
	- *HDB Resale Price Index (1Q2009 = 100), Quarterly* \n
	(url = "https://data.gov.sg/api/action/datastore_search?resource_id="  + "d_14f63e595975691e7c24a27ae4c07c79")
	- *Median Resale Prices for Registered Applications by Town and Flat Type* \n
	(url = "https://data.gov.sg/api/action/datastore_search?resource_id="  + "d_b51323a474ba789fb4cc3db58a3116d4")
	- *Resale flat prices based on registration date from Jan-2017 onwards* \n
	(url = "https://data.gov.sg/api/action/datastore_search?resource_id="  + "d_8b84c4ee58e3cfc0ece0d773c8ca6abc")
	- *CEA Salespersons’ Property Transaction Records (residential)* \n
	(url = "https://data.gov.sg/api/action/datastore_search?resource_id="  + "d_ee7e46d3c57f7865790704632b0aef71")
	- *CEA Salesperson Information* \n
	(url = "https://data.gov.sg/api/action/datastore_search?resource_id="  + "d_07c63be0f37e6e59c07a4ddc2fd87fcb")

2) https://www.hdb.gov.sg/cs/infoweb/e-resale/resale-purchase-of-an-hdb-resale-flat
3) https://www.hdb.gov.sg/residential/buying-a-flat/understanding-your-eligibility-and-housing-loan-options/flat-and-grant-eligibility/couples-and-families/cpf-housing-grants-for-resale-flats-families
4) https://www.cpf.gov.sg/member/infohub/educational-resources/hdb-option-fee-and-housing-expenses-you-should-know
"""
st.write(data)
st.divider()
st.subheader("App Features")
features = """
1) ResaleStats
	- A static line chart showing the trend of HDB resale price index starting from 2004Q1
	- A bar chart showing the HDB median resale prices by flat types. User is able to select, from the radio buttons "Location" or "Period" to d

"""
st.write(features)