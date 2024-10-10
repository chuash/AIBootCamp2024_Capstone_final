import os
import streamlit as st
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI


# if load_dotenv('.env'):
# for local environment
#    OPENAI_KEY = os.getenv('OPENAI_API_KEY')
# else:
#    OPENAI_KEY = st.secrets['OPENAI_API_KEY']

# Pass the API Key to the OpenAI Client
# client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# client = OpenAI(api_key=OPENAI_KEY)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


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
    value = " ".join([x.get("content") for x in messages])
    return len(encoding.encode(value))
