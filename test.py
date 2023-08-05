from dotenv import find_dotenv, load_dotenv
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os 
load_dotenv(find_dotenv()) 

print(os.getenv("HUGGINGFACEHUB_API_TOKEN"))


def imagetotext(url):
    model = pipeline("image-to-text",model="Salesforce/blip-image-captioning-base")
    text = model(url)
    print(text)
    return text

def text2text(text):
    model = pipeline("text2text-generation", model="google/flan-t5-base")
    response = model(text)
    print(response)
    return response

def document(url):
    model = pipeline("document-question-answering", model="magorshunov/layoutlm-invoices")
    response = model()
