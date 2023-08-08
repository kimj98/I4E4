#이 파일은 HuggingFace에 JSON형식으로 저장되어있는 특허 데이터를 사용해서 프롬트가 주어졋을때 비슷한 문서를 갖고올수있는지 구현하는 코딩페이지

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import Chroma
from docload import dataset_dict




embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
patent_samples = dataset_dict["train"][:100]["claims"]

list_texts = []
for sample in patent_samples:
    split_text = text_splitter.split_text(sample)
    list_texts.extend(split_text)


db = Chroma.from_texts(list_texts, embedding_model)

def retrieve(prompt):
    retrieval = db.similarity_search(prompt, k =3)
    return retrieval




