#이 파일은 HuggingFace에 JSON형식으로 저장되어있는 특허 데이터를 사용해서 프롬트가 주어졋을때 비슷한 문서를 갖고올수있는지 구현하는 코딩페이지

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import Chroma
from datasets import load_dataset
from langchain.document_loaders import PyPDFDirectoryLoader, DirectoryLoader, PyPDFLoader
import os 


def retrieve(prompt, db, num):
    retrieval = db.similarity_search(prompt, k = num)
    return retrieval

def retrieval2text(collections):
    text = ""
    for doc in collections:
        content = doc.page_content
        text += "\n" + content
    return text

def read_txt(directory_path):
    """Read all .txt files from a given directory."""
    data = {}
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):
            with open(os.path.join(directory_path, file_name), 'r') as file:
                data[file_name] = file.read()
    return data

def claims_list(claims):
    text = ""
    chunks = claims.split('청구항 ')[1:]
    claims_list = ["청구항 " + chunk for chunk in chunks]
    return claims_list

solar_description = read_txt('data')["Description.txt"]
claims = claims_list(read_txt('data')["Claims.txt"])
claim_rule = read_txt('data')["ClaimRule.txt"]
abtract_rule = read_txt('data')['AbstractRule.txt']
ptbs_format = read_txt("data")["PTBS.txt"]
effect_format = read_txt("data")["Effect.txt"]
background_format = read_txt("data")["Background.txt"]

#Load PDF Example
pdf_folder = '/Users/alexkim/PatentAI/I4E4/pdf/'
#print([i for i in os.listdir(pdf_folder) if i.endswith('.pdf')])
pdf_loader = [PyPDFLoader(pdf_folder + fn).load() for fn in os.listdir(pdf_folder) if fn.endswith('.pdf')] 
doc_list = [item for sublist in pdf_loader for item in sublist]

#Text문서를 Embedding Vector로 변환시켜줄 모델 
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#미국 특허 예제 문서를 Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap = 100)

#Input list of documents with pdf document by pages. (PDFs with 30 pages = 30 documents)

#pdf_samples = text_splitter.split_documents(doc_list)
#list_texts = []
#for sample in patent_samples: """
    #Returns Document with pagecontent/ metadata 
#    split_text = text_splitter.split_text(sample)
#    list_texts.extend(split_text)

#Chroma DB에 추출할때 사용할 Embedding Model과 Split된 문서 데이터 업로드

#patent_db = Chroma.from_texts(list_texts, embedding_model)


patent_db = Chroma.from_documents(doc_list, embedding_model)

#print(pdf_samples) 







