import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings # Updated Import
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

# 1. Load the PDF
# Using double backslashes or a raw string for Windows paths to avoid escape errors
file_path = r'Document_loader\Adnan_CV.pdf'
data = PyMuPDFLoader(file_path) 
docs = data.load()

# 2. Split into chunks
# Increased chunk_size slightly for better Gemini performance
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500, 
    chunk_overlap = 50,
)
chunks = splitter.split_documents(docs)

# 3. Clean chunks (Important to avoid metadata or empty string errors)
cleaned_chunks = [chunk for chunk in chunks if chunk.page_content.strip()]

# 4. Initialize Gemini Embeddings
# Ensure your .env has GOOGLE_API_KEY
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

# 5. Create Vector Store
try:
    vectorstore = Chroma.from_documents(
        documents = cleaned_chunks,
        embedding = embedding_model,
        persist_directory = "chroma-db"
    )
    print(" Success! Gemini embeddings generated and Chroma DB created.")
except Exception as e:
    print(f" An error occurred: {e}")