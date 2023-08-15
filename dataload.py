#이 파일은 HuggingFace에 JSON형식으로 저장되어있는 특허 데이터를 사용해서 프롬트가 주어졋을때 비슷한 문서를 갖고올수있는지 구현하는 코딩페이지

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from datasets import load_dataset
from langchain.document_loaders import PyPDFDirectoryLoader, DirectoryLoader
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

dataset_dict = load_dataset('HUPD/hupd',
    name='sample',
    data_files="https://huggingface.co/datasets/HUPD/hupd/blob/main/hupd_metadata_2022-02-22.feather", 
    icpr_label=None,
    train_filing_start_date='2016-01-01',
    train_filing_end_date='2016-01-21',
    val_filing_start_date='2016-01-22',
    val_filing_end_date='2016-01-31',
)

#Load PDF Example
pdf_loader = PyPDFDirectoryLoader('/Users/alexkim/PatentAI/I4E4/data', glob = './*.pdf')
pdf_documents = pdf_loader.load()

#From Patent Dataset
patent_samples = dataset_dict["train"][:100]["claims"]

#Text문서를 Embedding Vector로 변환시켜줄 모델 
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#미국 특허 예제 문서를 Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap = 200)
pdf_samples = text_splitter.split_documents(pdf_documents)

list_texts = []
for sample in patent_samples:
    #Returns Document with pagecontent/ metadata 
    split_text = text_splitter.split_text(sample)
    list_texts.extend(split_text)

#Chroma DB에 추출할때 사용할 Embedding Model과 Split된 문서 데이터 업로드
patent_db = Chroma.from_texts(list_texts, embedding_model)
pdf_db = Chroma.from_documents(pdf_samples, embedding_model)





