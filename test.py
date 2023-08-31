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



if __name__ == "__main__":
    asyncio.run(main())

