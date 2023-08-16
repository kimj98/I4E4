from dotenv import find_dotenv, load_dotenv
from langchain.llms import OpenAI
from dataload import retrieve, retrieval2text, solar,text_splitter
import os
class GPT_Output:
    def __init__(self):
        self.abstract = ""
        self.background = ""
        self.tech_description = ""
        self.claims = ""

load_dotenv(find_dotenv()) 

split_description = text_splitter.split_text(solar)

llm = OpenAI(temperature = 0.9)
title = "Foldable Solar Panel"
description = solar
output = GPT_Output()
prompt = "Write an abstract starting with: The present invention is... for a patent application of a invention titled {}. Use this description: {}.".format(title,description)
abstract = llm(prompt)

responses = []
for i in split_description:
    prompt = " Here's the text:{}. Write a patent claim like this format:1. , comprising:; ".format(i)
    response = llm(prompt)
    responses.append(response)
joined =''.join(responses)
prompt = "Write a organized listed patent claims in a structured format. Each claim needs to have number.  Make sure claims do not have the same information"


print(responses)
#비슷한 청구 내용 갖고오기 (DB퀄리티 따라서 좋은 답변)
#patent_example = retrieve(prompt,patent_db,3)
#patent_example_text = retrieval2text(patent_example)


#발명 배경내용 만들어주는 프롬트 
#prompt1 = "Write me a background/context of the invention using this text: {}"
#prompt_with_text= prompt1.format(text_example)
#input_token_estimation = len(prompt_with_text)/4
#background=llm(prompt_with_text)
#print(background)


