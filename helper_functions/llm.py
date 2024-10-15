import os
import streamlit as st
import tiktoken
from dotenv import load_dotenv
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from openai import OpenAI

if load_dotenv(".env"):
    # for local environment
    OPENAI_KEY = os.environ["OPENAI_API_KEY"]
else:
    # for streamlit community cloud environment
    OPENAI_KEY = st.secrets["OPENAI_API_KEY"]

# Pass the API Key to the OpenAI Client
client = OpenAI(api_key=OPENAI_KEY)
# client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_embedding(input, model="text-embedding-3-small"):
    """This is the function for generating embedding for input string

    Args:
        input (str): input text
        model (str, optional): embedding model. Defaults to 'text-embedding-3-small'.

    Returns:
        list: a list of vector values
    """
    response = client.embeddings.create(input=input, model=model)
    return [x.embedding for x in response.data]


def get_completion(
    prompt,
    model="gpt-4o-mini",
    temperature=0,
    top_p=1.0,
    max_tokens=1024,
    n=1,
    json_output=False,
):
    """This is the helper function for calling OpenAI LLM, with a single prompt

    Args:
        prompt (str): input query
        model (str, optional): ID of the OpenAI LLM model to use. Defaults to "gpt-4o-mini".
        temperature (int, optional): parameter that controls the randomness of LLM model’s predictions. Defaults to 0.
        top_p (float, optional): nucleus sampling. Defaults to 1.0.
        max_tokens (int, optional): An upper bound for the number of tokens that can be generated . Defaults to 256.
        n (int, optional): number of chat completion choices to generate. Defaults to 1.
        json_output (bool, optional): whether output format is in JSON. Defaults to False.

    Returns:
        str: LLM's textual response
    """
    if json_output == True:
        output_json_structure = {"type": "json_object"}
    else:
        output_json_structure = None

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_completion_tokens=max_tokens,
        n=1,
        response_format=output_json_structure,
    )
    return response.choices[0].message.content


# Note that this function directly take in "messages" as the parameter.
def get_completion_by_messages(
    messages, model="gpt-4o-mini", temperature=0, top_p=1.0, max_tokens=1024, n=1
):
    """This is the helper function for calling OpenAI LLM, with a series of messages

    Args:
        messages (list): a list of messages between bot and user
        model (str, optional): ID of the OpenAI LLM model to use. Defaults to "gpt-4o-mini".
        temperature (int, optional): parameter that controls the randomness of LLM model’s predictions. Defaults to 0.
        top_p (float, optional): nucleus sampling. Defaults to 1.0.
        max_tokens (int, optional): An upper bound for the number of tokens that can be generated . Defaults to 256.
        n (int, optional): number of chat completion choices to generate. Defaults to 1.

    Returns:
        str: LLM's textual response
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_completion_tokens=max_tokens,
        n=1,
    )
    return response.choices[0].message.content


def count_tokens(text):
    """This function is for calculating the tokens given the "message"
    This is simplified implementation that is good enough for a rough
    estimation

    Args:
        text (str): input text

    Returns:
        int: number of tokens
    """
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    return len(encoding.encode(text))


def count_tokens_from_message(messages):
    """This function is for calculating the tokens given a list of
    "messages". This is simplified implementation that is good enough
    for a rough estimation

    Args:
        messages (list): list of input text

    Returns:
        int: number of tokens
    """
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    # Extract the contents from each message and concatenate them
    value = " ".join([x.get("content") for x in messages])
    return len(encoding.encode(value))


def LLM_query_df(query, df, model="gpt-4o-mini", temperature=0):
    """This function takes in user query and the dataframe in which
    the query is to be applied on. It then passes them to the LLM to
    provide a response.

    Args:
        query (str): input user query
        df (pd.DataFrame): pandas dataframe to query from
        model (str, optional): _description_. Defaults to "gpt-4o-mini".
        temperature (int, optional): _description_. Defaults to 0.

    Returns:
        str: response from LLM
    """
    # initialise the LLM
    llm = ChatOpenAI(model=model, temperature=temperature)
    # initialise the agent
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code=True,
    )
    response = agent.invoke(query)
    # If there is no output in the returned response, inform the user accordingly
    if response.get("output", "") == "":
        return "The LLM is unable to provide an answer to your query. Please consider refining your query."
    else:
        return response.get("output", "")
