# FAQ Chatbot
## 📚Description
This FAQ chatbot is built on knowledge scraped from web pages or loaded from additional documents you provide.
It accurately answers user queries and includes a caching system to reduce response time, helping limit the number of OpenAI API calls.
Additionally, it features dynamic responses to keep users engaged while they wait for a reply.
This chatbot also supports queries in almost any language, just like ChatGPT.

## 🎯Motivation
When ChatGPT started gaining attention, I was inspired to build a system that could automatically respond to users and support them on familiar websites and apps using GPT technology.
During my research, I came across LangChain, which provided an API-based framework well-suited for this kind of application.
This project was born from the idea of integrating intelligent, automated assistance into everyday digital experiences using modern language models.

## 🚀Usage
1. Open create_embeddings.py and update the URLs you want to scrape. By default, the URL points to the OpenPIM Wikipedia page. 
2. Run $ python create_embeddings.py.  
3. Run $ python create_cache.py.  
4. You can now integrate this chatbot into your web app or website to improve customer support and make it more interactive. 
⚠️ You must use your own OpenAI API key.

## 🛠Environment
Server: Python3.8 (Django)  
Supported Python versions: 3.7–3.11 (due to dependency requirements)
Frontend: Plain JavaScript
Database: SQLite, Chroma database  
used api: OpenAI  
