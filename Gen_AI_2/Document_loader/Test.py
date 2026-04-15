from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter


data = TextLoader('Document_loader/notes.txt')

docs = data.load()

splitter = CharacterTextSplitter(
    separator= "",  #Cut at the nearest space before you hit 10.
    chunk_size = 10,
    chunk_overlap = 1
)

chunks = splitter.split_documents(docs)

#print(docs[0].page_content)
#print(len(chunks))
#print(chunks)

for i in chunks:
    print(i.page_content)
    print()
    print()