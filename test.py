import aiohttp
import asyncio
import os
from dotenv import find_dotenv, load_dotenv
from langchain.llms import OpenAI
import openai
from aiohttp import ClientSession
from dataload import retrieve, retrieval2text,claims_list, solar_description, claims, abtract_rule, ptbs_format, claim_rule

load_dotenv(find_dotenv()) 
openai.organization = "org-MrDsrQoFKXtTofmqyBqdRdOA"
openai.api_key = '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' 


async def response(prompt):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0].message.content


title = "접이식 솔라 모듈"
tech_description = solar_description
claims = claims

async def main():

    #과제 해결수단 (청구항의 문장 형태를 바꾸면됨)
    claim_num = len(claims)
    changed_claims = []
    coroutines = [response("{} \n Here is the A: \n{}. \n Output B:".format(claim_rule, claims[i])) for i in range(int(claim_num))]
    changed_claims = await asyncio.gather(*coroutines)
    problem_solve = "\n".join(changed_claims)
    print(problem_solve)

    prompt1 = "{} \n Here is the A: \n{}. \n Output B".format(claim_rule, claims[0])
    claim1 = await response(prompt1)
    prompt2 = "{}. 발명 제목: {}. 청구항: {}.".format(abtract_rule,title,claim1)
    abstract= response(prompt2)
    #기술분야 
    prompt3 = "Write what {} is about in one sentence using Korean".format(title)
    domain = response(prompt3)
    #배경기술 
    prompt4 = "What is background information about {}. In korean".format(title)
    background = response(prompt4)
    #해결하려는 과제 
    prompt5 = "As a patent attorney, you will write down the part of problem to be solved in the patent specification for {}. The following is the description of writing the problem to be solved part for the patent specification:\n{}\nThen, using the above information, write about the problem to be solved in the patent specification in Korean. Use this rule: {}".format(title, tech_description, ptbs_format)    
    problem = response(prompt5)
    #발명의 효과 
    prompt6 = "what would be the effect of inventing this {} using {} in korean".format(title,tech_description)
    effect = response(prompt6)

    print('before running coroutines')

    #Run Independent Prompts concurrently to speed up 
    coroutines = [abstract, domain, background, problem, effect]
    abstract_result, domain_result, background_result, problem_result, effect_result = await asyncio.gather(*coroutines)
    #print(abstract_result)
    #print(domain_result)
    #print(background_result)
    print(problem_result)
    #print(effect_result)
    #print(problem_solve)



if __name__ == "__main__":
    asyncio.run(main())

