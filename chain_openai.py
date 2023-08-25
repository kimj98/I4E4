from dotenv import find_dotenv, load_dotenv
from langchain.llms import OpenAI
import openai
from dataload import retrieve, retrieval2text,claims_list, solar_description, claims, abtract_rule, text_splitter, claim_rule, backgroundtip
import os
from langchain.chains.summarize import load_summarize_chain

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


def generate_output(input_dict):
    output = GPT_Output()
    patent_title = input_dict.patent_title
    patent_category = input_dict.patent_category
    tech_description = input_dict.tech_description
    claims = claims_list(input_dict.claim)
    designs = input_dict.designs_files
    designs_info = input_dict.designs_info

    #요약
    prompt = "{} \n Here is the A: \n{}. \n Output B".format(claim_rule, claims[0])
    claim1 = response(prompt)
    print(claim1)
    prompt = "{}. 발명 제목: {}. 청구항: {}.".format(abtract_rule,patent_title,claim1)
    abstract= response(prompt)
    output.abstract = abstract
    print(abstract)
    """ 

    #기술분야 (Task 1)
    prompt = ""
    background = response(prompt)
    output.backgroud = background 

    #배경기술 (Task 2) 
    claim_num = len(claims)
    claim_summary = []

    first_half_claims = "\n".join(claims[:claim_num//2])
    last_half_claims = "\n".join(claims[claim_num//2:])

    prompt = "다음은 접이식 솔라셀 모듈 특허 명세서의 청구항들 절반이야. 각 내가 주어주는 청구항들을 읽고 요약해줘. \n {}".format(first_half_claims)
    op = response(prompt)
    claim_summary.append(op)
    prompt = "나머지 반도 요약해줘: \n {}".format(last_half_claims)
    op = response(prompt)
    claim_summary.append(op)
    summary_output = "\n".join(claim_summary)

    prompt = "다음은 방금 너가 요약해준 청구항들이야. \n {} \n {} \n 이제 특허 명세서에 들어갈 배경기술을 작성해줘".format(summary_output, backgroundtip)
    backg = response(prompt)
    # output.background = backg

    print(backg)

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


    #발명 배경내용 만들어주는 프롬트 
    #prompt1 = "Write me a background/context of the invention using this text: {}"
    #prompt_with_text= prompt1.format(text_example)
    #input_token_estimation = len(prompt_with_text)/4
    #background=llm(prompt_with_text)
    #print(background)
    return output


