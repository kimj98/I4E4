from dotenv import find_dotenv, load_dotenv
import os 
from langchain.llms import OpenAI
from PiorArtSearch import retrieve

load_dotenv(find_dotenv()) 

llm = OpenAI(temperature = 0.9)

prompt1 = "give me claims about a computer system"

def retrieval2text(collections):
    text = ""
    for doc in collections:
        content = doc.page_content
        text += "\n" + content
    return text

claims = retrieve(prompt1)

content = retrieval2text(claims)

prompt2 = "write a background summary about this claim: {}"
prompt2_content = prompt2.format(content)

response = llm(prompt2_content)

print(llm("translate this in korean {}".format(response)))
