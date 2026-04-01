from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

# load credentials from .env (GOOGLE_API_KEY)
load_dotenv()

# create a LangChain-compatible embeddings object
# NOTE: the underlying `google.generativeai` package is deprecated;
# you will see a warning at runtime and should migrate to
# `google.genai` in the future.
emb = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    api_key=os.getenv("GOOGLE_API_KEY"),
    output_dimensionality=64  # optional override
)

# embed a single query
vector = emb.embed_query("What is AI?")
print(vector)
# print(len(vector))

