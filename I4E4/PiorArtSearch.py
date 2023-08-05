#이 파일은 HuggingFace에 JSON형식으로 저장되어있는 특허 데이터를 사용해서 프롬트가 주어졋을때 비슷한 문서를 갖고올수있는지 구현하는 코딩페이지

from langchain.embeddings import HuggingFaceEmbeddings
from datasets import load_dataset

patent_example = load_dataset("HUPD/hupd", "all")
print(patent_example)
