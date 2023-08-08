from langchain import document_loaders
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from datasets import load_dataset


text_splitter = CharacterTextSplitter(        
    separator = "\n\n",
    chunk_size = 50,
    chunk_overlap  = 10,
)

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
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
