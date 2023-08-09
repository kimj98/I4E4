#이 파일은 HuggingFace에 JSON형식으로 저장되어있는 특허 데이터를 사용해서 프롬트가 주어졋을때 비슷한 문서를 갖고올수있는지 구현하는 코딩페이지

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import Chroma
from docload import dataset_dict


def retrieve(prompt, db):
    retrieval = db.similarity_search(prompt, k =3)
    return retrieval

def retrieval2text(collections):
    text = ""
    for doc in collections:
        content = doc.page_content
        text += "\n" + content
    return text

#Text문서를 Embedding Vector로 변환시켜줄 모델 
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#미국 특허 예제 문서를 Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
patent_samples = dataset_dict["train"][:100]["claims"]

list_texts = []
for sample in patent_samples:
    split_text = text_splitter.split_text(sample)
    list_texts.extend(split_text)

#Chroma DB에 추출할때 사용할 Embedding Model과 Split된 문서 데이터 업로드
us_patent = Chroma.from_texts(list_texts, embedding_model)





