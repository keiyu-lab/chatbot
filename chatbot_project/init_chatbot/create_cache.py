""" 
    set up file
    if database for cache already exists, don't need to run this file
"""

import os, re, django, sys
import openai
from datetime import datetime
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from django.utils import timezone
from chatbot_app.models import QACache

# load django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_project.settings')
django.setup()

CHROMA_DB_DIRECTORY="chroma_db/opneAI"
CHROMA_DB_DIRECTORY_FOR_QUERY="chroma_db/for_query"
openai.api_key = os.environ["OPENAI_API_KEY"] # set your api key in your machine

template_question_generator = """
    You are given the following extracted parts of document and question only about making a template question.
    Predict a template questions from user.
    If you make multiplex questions, don't make similar questions which you have already made.
"""

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
    
def generate_template_questions():
    """generate template questions from vectordb to use new template"""
    
    #load the database
    vectordb = Chroma(
        persist_directory=CHROMA_DB_DIRECTORY, 
        embedding_function=OpenAIEmbeddings(),
        collection_name="opneAI"
        )
    retriever = vectordb.as_retriever()  
    # set a prompt
    prompt = PromptTemplate(
            input_variables=["chat_history","input"], 
            template=template_question_generator
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
    question="Create 10 template questions whose head has ・ from the document. "
    res = chain({'question': question, 'chat_history': chat_history})
    print(res["answer"])
    return res["answer"]

def get_template_answre(question):
    """get answer to use same template"""
    
    #load the database
    vectordb = Chroma(
        persist_directory=CHROMA_DB_DIRECTORY, 
        embedding_function=OpenAIEmbeddings(),
        collection_name="opneAI"
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
    
    return res["answer"]

def build_vectorestore_for_query(questions):
    "put template questions embeddings to chromadb"
    
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_texts(
        texts = questions,
        embedding=embeddings,
        collection_name="for_query",
        persist_directory=CHROMA_DB_DIRECTORY_FOR_QUERY,
    )
    vectordb.persist()
    
    return vectordb

template_questions = generate_template_questions()

template_questions_list = re.split("[・]", template_questions)

template_pair = [] # (question, answer)
for index,item in enumerate(template_questions_list):
    template_answer = get_template_answre(item)
    template_pair.append((item, template_answer))

print(template_pair)

bd = build_vectorestore_for_query(template_questions_list)

vectordb_for_query = Chroma(
        persist_directory=CHROMA_DB_DIRECTORY_FOR_QUERY, 
        embedding_function=OpenAIEmbeddings(),
        collection_name="for_query"
    )
collection_for_query = vectordb_for_query._collection
ids_for_query = collection_for_query.get()["ids"]

qa_cache = QACache()

for index, id in enumerate(ids_for_query):
    QACache.objects.create(
        question_id= id,
        question=collection_for_query.get()["documents"][index],
        answer=template_pair[index][1],
        created_time=timezone.now()
    )
