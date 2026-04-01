# Model Class Method use from langchain
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os 
load_dotenv()

api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not api_key:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN not found! check your .env file.")

# Initialize HuggingFace model
model = HuggingFaceEndpoint(
    repo_id= "deepseek-ai/DeepSeek-R1",
    huggingfacehub_api_token=api_key,
)

model = ChatHuggingFace(llm = model)

response = model.invoke("who are you?")
print(response.content)