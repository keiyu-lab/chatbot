import threading
import openai
import os, django

# Djangoプロジェクトの設定をロード
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_project.settings')
django.setup()

from chatbot_app.models import QACache
from datetime import datetime
from typing import Any, Dict, List
from queue import Queue
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.utils import timezone


from langchain.llms.openai import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult

CHROMA_DB_DIRECTORY="chroma_db/opneAI"
CHROMA_DB_DIRECTORY_FOR_QUERY="chroma_db/for_query"
openai.api_key = os.environ["OPENAI_API_KEY"]


template = """ 
    You are given the following extracted parts of documents and question.
    You are an AI assitant for answering questions about the document. Provide a conversational answer and also add the source.
    If you don't know the answer, just say "I am not sure". Don't try to make an answer.
    If the question is not about the document, politely inform questioner that you are tuned up to only answer questions about the document.
    If you say like "Please contact us" in end of your answer or the question was relevant to inquiry, add this source "https://www.profield.jp/contact/?_gl=1*1uegfc6*_ga*Mzg0MDIxNjM2LjE3MDA2MzU1ODM.*_ga_LS9QH7Q4YY*MTcwMTEzMjA0MC44LjEuMTcwMTEzMjQ3Ny41OS4wLjA.".
    
    
    {chat_history}
    Question:{question}
    Information:{context}
    Answer in Markdown:
    Source:
    """
    
def get_template_answre(question):
    """get answer to use same template"""
    #load the database
    vectordb = Chroma(
        persist_directory=CHROMA_DB_DIRECTORY, 
        embedding_function=OpenAIEmbeddings(),
        collection_name="ask_OpenPIM"
        )
    retriever = vectordb.as_retriever()  
    # set a prompt
    prompt = PromptTemplate(
            input_variables=["chat_history","input"], 
            template=template
            )
    
    chat_history = []
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo-16k",
        temperature=0,
        )
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        condense_question_prompt=prompt,
        return_source_documents=True,
        )
    res = chain({'question': question, 'chat_history': chat_history})
    #print(res["answer"])
    return res["answer"]
before = timezone.now()
#load the database
vectordb = Chroma(
    persist_directory=CHROMA_DB_DIRECTORY_FOR_QUERY, 
    embedding_function=OpenAIEmbeddings(),
    collection_name="for_query"
    )
collection = vectordb._collection
print(collection.count())
print(vectordb.get())
query="what is openai"
docs_with_scores = []
docs_with_scores=vectordb.similarity_search_with_relevance_scores(query)
print(docs_with_scores)

