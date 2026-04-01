from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(
    model = 'text-embedding-3-small',
    dimensions= 64 # it means each text is converted into a List in 64 numbers (64 items / numbers in a list form).
)

vector = embeddings.embed_query('what is AI')
print(vector)