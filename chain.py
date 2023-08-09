from dotenv import find_dotenv, load_dotenv
import os 
from langchain.llms import OpenAI
from PiorArtSearch import retrieve, retrieval2text,us_patent

load_dotenv(find_dotenv()) 

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data
llm = OpenAI(temperature = 0.8)

prompt1 = "please give me a novel invention about a gym workout machine that can help people with leg disability"

#비슷한 청구 내용 갖고오기 (DB퀄리티 따라서 좋은 답변)
patent_example = retrieve(prompt1,us_patent)
patent_example_text = retrieval2text(patent_example)

#ChatGPT가 만들어준 발명내용 "please give me a novel invention about a gym workout machine that can help people with leg disability" 을 넣고 받은 답변을 example.txt에 저장함 
text_example = read_text_file("/Users/alexkim/PatentAI/I4E4/example.txt")

#발명 배경내용 만들어주는 프롬트 
prompt1 = "Write me a background/context of the invention using this text: {}"
prompt_with_text= prompt1.format(text_example)
input_token_estimation = len(prompt_with_text)/4
response=llm(prompt_with_text)
print(response)


