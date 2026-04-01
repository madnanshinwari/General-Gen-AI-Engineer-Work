import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate  
from pydantic import BaseModel
from typing import Optional
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# 🎯 Model Setup
# -------------------------------
model = ChatGroq(
    model="llama-3.3-70b-versatile",
)

# -------------------------------
# 📘 Pydantic Model
# -------------------------------
class Book(BaseModel):
    Book_Title: str
    Authors: str
    Publicate_Date: Optional[int]
    ISBN: Optional[int]
    Language: str
    Number_of_Pages: str
    Edition: Optional[int]

parser = PydanticOutputParser(pydantic_object=Book)

# -------------------------------
# 🧠 Prompt Template
# -------------------------------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Extract Book information from the paragraph.

Follow this format:
{format_instructions}
"""
    ),
    ("human", "{paragraph}")
])


# -------------------------------
# 🎨 Streamlit UI
# -------------------------------
st.set_page_config(page_title="📚 Book Info Extractor", layout="centered")

st.markdown(
    """
    <h1 style='text-align:center; color:#4A90E2;'>📚 Book Information Extractor</h1>
    <p style='text-align:center; font-size:18px;'>
        Paste any paragraph and extract structured book details using LLaMA + Pydantic.
    </p>
    """,
    unsafe_allow_html=True
)

st.write("")  # spacing

paragraph = st.text_area(
    "📝 Enter the paragraph here:",
    placeholder="Paste the book description or paragraph...",
    height=200
)

extract_btn = st.button("🔍 Extract Information", use_container_width=True)

if extract_btn:
    if not paragraph.strip():
        st.warning("⚠ Please enter a paragraph before clicking extract.")
    else:
        with st.spinner("🔎 Extracting book details..."):
            # Prepare final prompt
            final_prompt = prompt.invoke(
                {
                    "paragraph": paragraph,
                    "format_instructions": parser.get_format_instructions(),
                }
            )

            # Model response
            response = model.invoke(final_prompt)

            # Parse model output
            try:
                parsed_result = parser.parse(response.content)
                st.success("✅ Extraction Successful!")
                
                st.markdown("### 📄 Extracted Book Information")

                st.code(parsed_result.json(indent=2), language="json")

            except Exception as e:
                st.error("❌ Failed to parse model output.")
                st.write("Raw Output:")
                st.code(response.content)


# Footer
st.markdown(
    "<hr><p style='text-align:center; color:gray;'>✨ Developed by Muhammad Adnan Khan</p>",
    unsafe_allow_html=True
)