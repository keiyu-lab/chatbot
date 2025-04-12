# FAQ Chatbot
## 📚Description
This FAQ chatbot is built on knowledge scraped from web pages or loaded from additional documents you provide.
It accurately answers user queries and includes a caching system to reduce response time, helping limit the number of OpenAI API calls.
Additionally, it features dynamic responses to keep users engaged while they wait for a reply.

## 🎯Motivation
The goal of this project is to create a practical and extensible chatbot that enhances visitor support while minimizing API usage and optimizing cost efficiency.

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
