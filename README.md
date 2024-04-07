## Description
This FAQ Chatbot knowledge is based on scraped web pages or additional documents that you provide.  
It can accurately answer user queries and has a caching system to shorten response time and limit the number of connections to the OpenAI API. 
Additionally, it possesses dynamic response functionality to keep users engaged while waiting for a response.

## Usage
1. In create_embeddings.py, update the URLs you want to scrape and embed the information into the Chroma database. By default, the URL is set to the OpenPIM Wikipedia page.  
2. Run $ python create_embeddings.py.  
3. Run $ python create_cache.py.  
You can then integrate this chatbot into your web app or site to enhance visitor service.  
(You must use your own OpenAI API key)

## Environment
Server: Python (Django)  
Frontend: Plain JavaScript  
Database: SQLite, Chroma database  
API (used): OpenAI  
