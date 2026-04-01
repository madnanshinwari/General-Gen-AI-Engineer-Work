from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Select Gemini model
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

messages = [
    {"role": "system", "content": "You are a professional English teacher."}
]

print("------------- Simple Gemini Chatbot ----------------")
print("------------- Enter 0 to exit -----------------------")

while True:
    prompt = input("You: ")

    if prompt == "0":
        print("Exiting chatbot...")
        break

    messages.append({"role": "user", "content": prompt})

    # Generate response
    response = model.generate_content(
        [{"role": m["role"], "parts": [m["content"]]} for m in messages]
    )

    reply = response.text
    print("Bot:", reply)

    messages.append({"role": "assistant", "content": reply})