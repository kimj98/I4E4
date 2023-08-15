from dotenv import find_dotenv, load_dotenv
from langchain.llms import OpenAI
from dataload import retrieve, retrieval2text, patent_db, text_example
import os


load_dotenv(find_dotenv()) 


llm = OpenAI(temperature = 0.8)

prompt = "please give me a novel invention about a gym workout machine that can help people with leg disability"

#비슷한 청구 내용 갖고오기 (DB퀄리티 따라서 좋은 답변)
patent_example = retrieve(prompt,patent_db,3)
patent_example_text = retrieval2text(patent_example)


#발명 배경내용 만들어주는 프롬트 
prompt1 = "Write me a background/context of the invention using this text: {}"
prompt_with_text= prompt1.format(text_example)
input_token_estimation = len(prompt_with_text)/4
background=llm(prompt_with_text)
print(background)


