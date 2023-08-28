from dotenv import load_dotenv, find_dotenv
import os
import openai
load_dotenv(find_dotenv()) 
from openai_parallel_toolkit import ParallelToolkit



openai.organization = "org-MrDsrQoFKXtTofmqyBqdRdOA"
openai.api_key = os.getenv("OPENAI_API_KEY")

def response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0].message.content


    

