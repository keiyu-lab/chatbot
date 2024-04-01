import threading
import openai
import os

from chatbot_app.chatbot.conversational_chatbot import ConversationalChatBot
from chatbot_app.chatbot.cache_for_chatbot import cache
from datetime import datetime
from typing import Any, Dict, List
from queue import Queue

from django.shortcuts import render
from django.http import StreamingHttpResponse

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult

SIMILARITY_SCORE_BOARDER = 0.95
openai.api_key = os.environ["OPENAI_API_KEY"]

class CustomStreamingCallbackHandler(BaseCallbackHandler):
    """Callback Handler that Stream LLM response."""

    def __init__(self, queue):
        self.queue = queue
 
        
    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        self.queue.put(token)
      
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> Any:
        """Run when LLM starts running."""
        self.start_time = datetime.now()
        
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        self.end_time = datetime.now()
        time_take_by_llm_to_generate_text = self.end_time - self.start_time
        print(time_take_by_llm_to_generate_text)


def chatbot(request):
    """view"""
    
    #load the vectore datebase
    vectordb = ConversationalChatBot.get_vectordb()
    retriever = vectordb.as_retriever()
    # set a prompt
    prompt = ConversationalChatBot.get_propmt()
    
    if request.method == 'POST':
       
        query = request.POST.get('message')
        
        # similar query search and return (query, answer) from cache
        vectordb_for_query = cache.init_cache()
        print(vectordb_for_query.get())
        max_score, most_similar_question_id = cache.search_most_similarity(query, vectordb_for_query)
        if max_score > SIMILARITY_SCORE_BOARDER:
            print("answer is in cache")
            answer = cache.get_answer_from_cache(most_similar_question_id)
            print(answer)
            if answer!= None:
                return  StreamingHttpResponse(generate_response_for_cache(answer), content_type="text/event-stream")
            else:
                return EOFError
            
            
        # There was no similarity in cache, so make an answer and put it to that cache
        
        queue = Queue()  
        chat_history = []
        job_done = object()
        
        # use a thread for streaming function
        task = threading.Thread(
            target=openai_response_generator,
            args=(queue, retriever, prompt, query, chat_history, job_done, vectordb_for_query)
        )
        task.start()
        
        response = StreamingHttpResponse(generate_stream(queue, job_done), content_type="text/event-stream")
        
        return response
    
    return render(request, "chatbot.html")
    


def openai_response_generator(queue ,retriever, prompt, query, chat_history, job_done, vectordb_for_query):
    
    llm = ChatOpenAI(
            model_name="gpt-3.5-turbo-16k",
            streaming=True,
            temperature=0,
            callbacks=([CustomStreamingCallbackHandler(queue)]),
    )

    chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            condense_question_prompt=prompt,
            return_source_documents=True,
            )
    
 
    res = chain({'question': query, 'chat_history': chat_history})
    
    # put entire answer to cache( pushing and deleting actions are executed after responded)
    print(res["answer"])
    
    # check if it is ok then we can push
    # if completly same, don't push
    is_same = False
    questions = vectordb_for_query.get()["documents"]  
    for question in questions:
        if question == query:
            print("there is same question in vectordb_for_query")
            is_same = True
    if is_same == False:
        print("push this question to cache")
        q_id = cache.push_query_embedding(query, vectordb_for_query)
        cache.push_qa(q_id, query, res["answer"])
    
    # delete expired data
    expired_q_ids = cache.delete_qa()
    if(len(expired_q_ids) > 0):
        cache.delete_query_embedding(expired_q_ids, vectordb_for_query)
    
    queue.put(job_done)
 
        

def generate_stream(q: Queue, job_done):
    while (...):
        try:
            stream = q.get(True, timeout=1)
            
            if stream is job_done:
                return "done"
               
            for index, item in enumerate(stream):
                yield item
        except:
            continue
        
def generate_response_for_cache(answer):
    yield answer


