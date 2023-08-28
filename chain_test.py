from dotenv import find_dotenv, load_dotenv
from langchain.llms import OpenAI
import openai
from dataload import retrieve, retrieval2text, solar_description, claims, abtract_rule, text_splitter, claim_rule
import os
from langchain.chains.summarize import load_summarize_chain
import asyncio, aiohttp


class GPT_Output:
    def __init__(self):
        #요약
        self.abstract = ""
        #청구범위
        self.claims = ""
        #기술분야
        self.domain = ""
        #배경기술 
        self.background = ""
        #해결하려는 과제
        self.problem = ""
        #과제 해결수단
        self.stepstosovle = ""
        #발명의 효과
        self.effect = ""

load_dotenv(find_dotenv()) 
openai.organization = "org-MrDsrQoFKXtTofmqyBqdRdOA"
openai.api_key = os.getenv("OPENAI_API_KEY")

def response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0].message.content
    


title = "접이식 솔라 모듈"
description = solar_description
claims = claims
output = GPT_Output()

#요약
prompt = "{} \n Here is the A: \n{}. \n Output B".format(claim_rule, claims[0])
claim1 = response(prompt)
print(claim1)
prompt = "발명 제목: {}. 청구항: {}.".format(title,claim1)
abstract= response(prompt)
output.abstract = abstract
print(abstract)
""" 

#기술분야 (Task 1)
prompt = ""
background = response(prompt)
output.backgroud = background 

#배경기술 (Task 2) 
prompt = ""
background = response(prompt)
output.backgroud = background 

#해결하려는 과제 (Improvement to be made)

prompt = "This section is about What problem does this invention trying to solve? what benefit can this invention create? use this description{}. First write about the general usecase of the past/traditional models. Then say Don't explain how it does it, just in general term in korean" .format(description)
problem = response(prompt)
output.problem = problem


#과제 해결수단 (청구항의 문장 형태를 바꾸면됨)
claim_num = len(claims)
changed_claims = []

for i in range(int(claim_num)):
    claim_i = claims[i]
    prompt = "{} \n Here is the A: \n{}. \n Output B:".format(claim_rule, claims[i])
    changed = response(prompt)
    changed_claims.append(changed)

problem_solve = "\n".join(changed_claims)
output.stepstosovle = problem_solve

#발명의 효과 (Task 3)
prompt = ""
effect = response(prompt)
output.effect = effect 
 """

 
#비슷한 청구 내용 갖고오기 (DB퀄리티 따라서 좋은 답변)
#patent_example = retrieve(prompt,patent_db,3)
#patent_example_text = retrieval2text(patent_example)




