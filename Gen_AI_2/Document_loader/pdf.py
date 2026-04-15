from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter


data = PyPDFLoader('Document_loader\Impact of Generative AI on Critical Thinking.pdf')

docs = data.load()


splitter = TokenTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 10,
)


chunks = splitter.split_documents(docs)
#print(docs[0].page_content)

#print(len(docs))

#print(len(chunks))

print(chunks[0].page_content)


