from urllib.parse import urlparse
from langchain_chroma import Chroma
# from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings


def generate_name_html(url: str):
    parsed_url = urlparse(url)
    substring = parsed_url.netloc + parsed_url.path
    return substring


def return_vector_store(database: str = "New"):
    vector_store = Chroma(persist_directory=f"./database", collection_name=database,
                          embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"))
    return vector_store


def return_splitter():
    splitter = RecursiveCharacterTextSplitter(chunk_size=1024,
                                              chunk_overlap=20,
                                              length_function=len,
                                              is_separator_regex=False,
                                              )
    return splitter
