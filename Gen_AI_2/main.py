"""
from dotenv  import load_dotenv # Load environment variables
from langchain_mistralai import ChatMistralAI
#from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Execute load_dotenv
load_dotenv()

# Create TextLoader for SRS.txt
#data = TextLoader('Document_loader\SRS.txt') 
data = PyPDFLoader('Document_loader\Impact of Generative AI on Critical Thinking.pdf') 

# Load documents
docs = data.load()


splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100, 
    chunk_overlap = 10,
)


chunks = splitter.split_documents(docs)


# Create prompt template
template = ChatPromptTemplate.from_messages(
    # System message for summarizer
    [('system','you are AI Assistant summerize text'),
    # Human message with data placeholder
    ('human','{data}')]
) 

# Initialize Mistral model
model = ChatMistralAI(model = 'mistral-small-2506')
# Format prompt with document content
prompt = template.format_messages(data = docs[0].page_content)

# Invoke model with prompt
response = model.invoke(prompt)
# Print response content
print(response.content)

"""
###############################################################################################

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

vectorstore = Chroma(
    persist_directory= "chroma-db",
    embedding_function=embedding_model
)


retriever = vectorstore.as_retriever(
    search_type = 'mmr',
    search_kwargs = {
        "k" : 4,
        "fetch_k" : 10,
        "lambda_mult" : 0.5
    }
)

llm = ChatMistralAI(model = "mistral-small-2506")

#prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful AI assistant.

Use ONLY the provided context to answer the question.

If the answer is not present in the context,
say: "I could not find the answer in the document."
"""
        ),
        (
            "human",
            """Context:
{context}

Question:
{question}
"""
        )
    ]
    )

print('RAG system created')

print('press 0 to exit')

while True:
    query = input('You : ')
    if query == "0":
        break

    docs = retriever.invoke(query)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    final_prompt = prompt.invoke({
        "context": context,
        "question": query
    })

    response = llm.invoke(final_prompt)
    
    print(f"\n AI: {response.content}")