import os, openai
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult


CHROMA_DB_DIRECTORY="chroma_db/opneAI"
openai.api_key = os.environ["OPENAI_API_KEY"]

class ConversationalChatBot:
    
    template = """ 
    You are given the following extracted parts of documents and question.
    You are an AI assitant for answering questions about the document. Provide a conversational answer and also add the source.
    If you don't know the answer, just say "I am not sure". Don't try to make an answer.
    If the question is not about the document, politely inform questioner that you are tuned up to only answer questions about the document.
    
    
    {chat_history}
    Question:{question}
    Information:{context}
    Answer in Markdown:
    Source:
    """
    
    #load the vectore datebase
    vectordb = Chroma(
        persist_directory=CHROMA_DB_DIRECTORY, 
        embedding_function=OpenAIEmbeddings(api_key = openai.api_key),
        collection_name="opneAI"
        )
    
    # set a prompt
    prompt = PromptTemplate(
            input_variables=["chat_history","input"], 
            template=template
            )
    
    @classmethod
    def get_vectordb(self):
        return self.vectordb
    @classmethod
    def get_propmt(self):
        return self.prompt
