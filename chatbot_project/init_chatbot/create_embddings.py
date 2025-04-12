""" 
    set up file
    if database for cache already exists, don't need to run this file
    when you want to change the source given to chatbot, change the url
"""

import os
import openai

from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import WebBaseLoader, TextLoader

openai.api_key = os.environ["OPENAI_API_KEY"]
CHROMA_DB_DIRECTORY="chroma_db/opneAI"

def build_database(urls, collection_name):
    loader = WebBaseLoader(urls)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    splitted_documents = text_splitter.split_documents(documents)
    
    # add doucuments explaing some diagrams and pictures
    # run diectory is "/chatbot_OpenPIM/chatbot_project"
    additional_loader = TextLoader("additional_document.txt", encoding="utf-8")
    additional_document = additional_loader.load()
    splitted_additinal_documents = text_splitter.split_documents(additional_document)

    # add Document to list(Document)
    # splitted_additional_documents is list(Document)
    splitted_documents.append(splitted_additinal_documents[0])

    embeddings = OpenAIEmbeddings()
       
    # .from_documents is more suitable for searching information than from_texts 
    # save to disk
    vectordb = Chroma.from_documents(
        documents=splitted_documents,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=CHROMA_DB_DIRECTORY,
    )
    
    vectordb.persist()
    
    return vectordb
        
# default url 
url = [
       "https://en.wikipedia.org/wiki/OpenAI"
]
vectordb=build_database(url, "opneAI")
 
