from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate  
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(
    model="llama-3.3-70b-versatile",
)

class Book(BaseModel):
    Book_Title: str
    Authors : str
    Publicate_Date : Optional[int]
    ISBN : Optional[int]
    Language: str
    Number_of_Pages : str
    Edition : Optional[int]

parser = PydanticOutputParser(pydantic_object=Book)


prompt = ChatPromptTemplate.from_messages([
    ('system',"""
Extract Book information from the paragraph
    {format_instructions}
"""),
("human","{paragraph}")
]
)


input_paragraph = input('Give your Paragraph: ')

final_paragraph  = prompt.invoke(
    {
        "paragraph" : input_paragraph,
        "format_instructions" : parser.get_format_instructions(),
        
    }
)

response = model.invoke(final_paragraph)
book_data = parser.parse(response.content)
print(book_data)