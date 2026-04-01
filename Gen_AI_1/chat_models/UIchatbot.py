import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Select Gemini model
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

# App Title
st.title("💬 Simple Gemini Chatbot")

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a professional English teacher."}
    ]

# User Input
user_input = st.text_input("👤 You:", "")

if st.button("🚀 Send"):
    if user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Convert messages for Gemini
        gemini_msgs = [
            {"role": m["role"], "parts": [m["content"]]}
            for m in st.session_state.messages
        ]

        # Generate reply
        response = model.generate_content(gemini_msgs)
        bot_reply = response.text

        st.session_state.messages.append(
            {"role": "assistant", "content": bot_reply}
        )

# Chat History Display
st.write("---")
st.subheader("📜 Chat History")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.write(f"🧑 **You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.write(f"🤖 **Bot:** {msg['content']}")