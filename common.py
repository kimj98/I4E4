from dotenv import load_dotenv, find_dotenv
import os
import openai
load_dotenv(find_dotenv()) 
from openai_parallel_toolkit import Gpt35Turbo,request_openai_api


openai.organization = "org-MrDsrQoFKXtTofmqyBqdRdOA"
openai.api_key = os.getenv("OPENAI_API_KEY")

def response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0].message.content

model = Gpt35Turbo(content="hello world", prompt="", temperature=0.7)
result = request_openai_api(openai_model=model, config_path="config.json")
print(result)

    

