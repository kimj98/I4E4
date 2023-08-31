from dataload import retrieve, patent_db, retrieval2text
from langchain.chains import RetrievalQAWithSourcesChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv()) 
model = ChatOpenAI(model_name='gpt-3.5-turbo')

prompt = ""
patent_example = retrieve(prompt,patent_db,3)
patent_example_text = retrieval2text(patent_example)


query  = "솔라 모듈의 배경이뭐야?"

print(retrieve(query, patent_db, 10))

#유사 특허의 배경기술만 extract 
