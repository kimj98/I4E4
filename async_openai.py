import aiohttp
import asyncio
import os
from dotenv import find_dotenv, load_dotenv
from langchain.llms import OpenAI
import openai
from dataload import retrieve, retrieval2text,claims_list, claims, abtract_rule, ptbs_format, claim_rule, background_format,effect_format
import time

class User_Input:
    def __init__(self, patent_title, patent_category, tech_description,claim, designs_info, design_files):
        self.patent_title = patent_title
        self.patent_category = patent_category
        self.tech_description = tech_description
        self.claim = claim
        self.designs_info = designs_info
        self.designs_files = design_files

async def response(prompt):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0].message.content

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
        self.stepstosolve = ""
        #발명의 효과
        self.effect = ""


async def generate_output_async(input_dict):
    start_time = time.time()
    output = GPT_Output()
    patent_title = input_dict.patent_title
    patent_category = input_dict.patent_category
    tech_description = input_dict.tech_description
    claims = claims_list(input_dict.claim)
    all_claims = input_dict.claim
    designs = input_dict.designs_files
    designs_info = input_dict.designs_info

    #요약
    prompt1 = "{}. 설명한대로 규칙 지키면서 바꿔줘. 바꿀내용: {}. ".format(claim_rule, claims[0])
    claim1 = await response(prompt1)
    print(claim1)

    prompt2 = "{}. 발명 제목: {}. 청구항: {}.".format(abtract_rule,patent_title,claim1)
    abstract= response(prompt2)
    
    #기술분야 
    prompt3 = "한 문장으로 {} 소개. ~한다".format(patent_title)
    domain = response(prompt3)
    
    #배경기술 
    prompt4 = "{} 의 전반적인 배경. ~있다 말투로 끝내줘 {}".format(patent_title,background_format)
    background = response(prompt4)
    
    #해결하려는 과제 
    prompt5 = "{}. 발명 내용:{}".format(ptbs_format, tech_description)    
    problem = response(prompt5)

    #발명의 효과 
    prompt6 = "{}. 발명:{} 내용: {}.".format(effect_format,patent_title,tech_description)
    effect = response(prompt6)

    #Run Independent Prompts concurrently to speed up 
    print('before running coroutines')
    coroutines = [abstract, domain, background, problem, effect]
    output.abstract, output.domain, output.background, output.problem, output.effect = await asyncio.gather(*coroutines)
    print('before running coroutines2')
    
    #과제 해결수단 (청구항의 문장 형태를 바꾸면됨)
    claim_num = len(claims)
    changed_claims = []
    coroutines = []
    
    coroutines = [response("{} \n 이 문단을 바꿔줘: {}. ".format(claim_rule, claims[i])) for i in range(int(claim_num))]
    changed_claims = await asyncio.gather(*coroutines)
    output.stepstosolve = "\n".join(changed_claims)


    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
    return output
    

