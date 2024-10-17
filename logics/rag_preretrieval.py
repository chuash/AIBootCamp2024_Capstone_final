#__import__("pysqlite3")
#import sys

#sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import os
import requests
from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    PyPDFLoader,
    WebBaseLoader,
    BSHTMLLoader,
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# embedding model to be used
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

# Step 1: Loading data from external source
os.environ["USER_AGENT"] = "myagent"
loader = PyPDFLoader(
    "https://www.developer.tech.gov.sg/products/collections/data-science-and-artificial-intelligence/playbooks/prompt-engineering-playbook-beta-v3.pdf"
)
pages = loader.load()

# Step 2: split the loaded documents into appropriate chunk length
text_splitter = RecursiveCharacterTextSplitter(
    # separators=["\n\n", "\n","(?<=\. )", " ", ""],
    chunk_size=1000,
    chunk_overlap=200,  # set at 20% of chunk size
    add_start_index=True,
    # length_function=count_tokens,
    # is_separator_regex=True, # if this is true, it can recognise "\. " as period separator, if False, will see this as \. separator
)

splitted_documents = text_splitter.split_documents(pages)

# Step 3: Embedding and storage of chunked documents
idlist = [
    str(doc.metadata["page"]) + "-" + str(doc.metadata["start_index"])
    for doc in splitted_documents
]
vector_store = Chroma.from_documents(
    collection_name="HDBResale",
    documents=splitted_documents,
    embedding=embeddings_model,
    ids=idlist,
    collection_metadata={"hnsw:space": "cosine"},
    persist_directory="../data/chroma_langchain_db",  # Where to save data locally
)

print(f"Number of docs in chromadb: {vector_store._collection.count()}")
print(f"First doc: {vector_store._collection.peek(limit=1)}")
