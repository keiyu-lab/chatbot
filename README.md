## Description
This FAQ Chatbot knowledge is based on scraped web pages or additional documents that you provide.  
It can accurately answer user queries and has a caching system to shorten response time, which contributes to limit the number of connections to the OpenAI API. 
Additionally, it possesses dynamic response functionality to keep users engaged while waiting for a response.

## Motivation


## Usage
1. In create_embeddings.py, update the URLs you want to scrape and embed the information into the Chroma database. By default, the URL is set to the OpenPIM Wikipedia page.  
2. Run $ python create_embeddings.py.  
3. Run $ python create_cache.py.  
Later on above, You can finally integrate this chatbot into your web app or site to enhance visitor service and have fun to try it.  
(You must use your own OpenAI API key)

## Environment
Server: Python3.8 (Django)  
  python version needs to be 3.7~3.11 (dependancies require)
Frontend: Plain JavaScript
Database: SQLite, Chroma database  
used api: OpenAI  
