import os, django
from django.utils import timezone
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from chatbot_app.models import QACache

CHROMA_DB_DIRECTORY_FOR_QUERY="chroma_db/for_query"
EXPIRED_DATA_DEADLINE = 7   # days

class cache:
    @classmethod
    def init_cache(self):
        #load
        vectordb_for_query = Chroma(
            persist_directory=CHROMA_DB_DIRECTORY_FOR_QUERY, 
            embedding_function=OpenAIEmbeddings(),
            collection_name="for_query"
        )
        return vectordb_for_query
    
    @classmethod
    def search_most_similarity(self, query, vectordb):
        docs_with_scores=vectordb.similarity_search_with_relevance_scores(query)
        print(docs_with_scores)
        most_similar_question = (docs_with_scores[0][0]).page_content
        index = (vectordb.get()["documents"]).index(most_similar_question)
        most_similar_question_id = vectordb.get()["ids"][index]
        max_score = docs_with_scores[0][1]    
        
        return max_score, most_similar_question_id
    
    @classmethod
    def get_answer_from_cache(self, question_id):
        answer = QACache.objects.filter(question_id=question_id).first()    # answer : string
        
        return answer
    
    @classmethod
    def push_qa(self, q_id, query, answer):
        # check if it is ok that we can push
        # if completly same don't push to avoid error happend in djangoapp
        is_same = True
        QACache.objects
        QACache.objects.create(
            question_id= q_id,
            question=query,
            answer=answer,
            created_time=timezone.now()
        )
    
    @classmethod
    def push_query_embedding(self, query, vectordb):
        vectordb.add_texts([query])    
        index = (vectordb.get()["documents"]).index(query)
        q_id = vectordb.get()["ids"][index]
        # print(q_id)
        return q_id

    @classmethod
    def delete_qa(self):
        now = timezone.now()
        time_delta = timezone.timedelta(days=EXPIRED_DATA_DEADLINE)
        over_expired_date = now - time_delta
        # print(over_expired_date)
        qa_caches=QACache.objects.all()
        expired_q_ids = []
        for qa_cache in qa_caches:
            # print(qa_cache.question_id, qa_cache.question, qa_cache.answer,  qa_cache.created_time)
            if qa_cache.created_time < over_expired_date:
                print("this data is over expired date : " + str(qa_cache.question_id))
                expired_q_ids.append(qa_cache.question_id)
                qa_cache.delete()

        return expired_q_ids

    @classmethod
    def delete_query_embedding(self, q_ids, vectordb):
        vectordb.delete(q_ids)