from langchain_community.document_loaders import TextLoader

# load the text file provide the path
data = TextLoader('Document_loader\SRS.txt') 

docs = data.load()

print(docs[0].page_content)