from dotenv import find_dotenv, load_dotenv
from langchain.llms import OpenAI
from dataload import retrieve, retrieval2text, solar
import os

load_dotenv(find_dotenv()) 
llm = OpenAI(temperature = 0.8)

class GPT_Output:
    def __init__(self):
        self.abstract = ""
        self.background = ""
        self.tech_description = ""
        self.claims = ""

def generate_output(input_dict):
    output = GPT_Output()
    title = input_dict.patent_title
    description = input_dict.tech_description 

    prompt = "Write an abstract for a patent application of a invention titled {}. Use this description: {}.".format(title,description)
    abstract = llm(prompt)
    output.abstract = abstract

    promt = "Write how this invention will solve existing problem and the background context of invention"
    
    return output 
    

    #비슷한 청구 내용 갖고오기 (DB퀄리티 따라서 좋은 답변)
    #patent_example = retrieve(prompt,patent_db,3)
    #patent_example_text = retrieval2text(patent_example)


    #발명 배경내용 만들어주는 프롬트 
    #prompt1 = "Write me a background/context of the invention using this text: {}"
    #prompt_with_text= prompt1.format(text_example)
    #input_token_estimation = len(prompt_with_text)/4
    #background=llm(prompt_with_text)
    #print(background)


