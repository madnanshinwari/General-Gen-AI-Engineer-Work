"""
In this code i have created chatbot using googel APIs and small
memory (JSON) to store previous chat history and load then if i 
use again.. the responses is store in chat_history.json file.

"""

from dotenv import load_dotenv
import google.generativeai as genai
import json
import os

load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Select the Gemini model
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

HISTORY_FILE = 'chat_history.json'


def load_chat_history():
    """Load chat history from JSON file."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            print("Warning: Could not load chat history. Starting fresh.")
    return []


def save_chat_history(messages):
    """Save chat history to JSON file."""
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(messages, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save chat history: {e}")


# Load previous chat
messages = load_chat_history()

print("------------- Welcome to Gemini Bot ----------------")
print("------------- If you want to exit enter 0 -----------")
print(f"Loaded {len(messages)} previous messages from history.")


while True:
    prompt = input("You: ")

    if prompt == "0":
        break
    elif prompt.lower() == "clear":
        messages = []
        print("Chat history cleared.")
        continue

    # Add user message
    messages.append({"role": "user", "content": prompt})

    # Convert chat into Gemini message format
    gemini_messages = []
    for msg in messages:
        gemini_messages.append(msg["role"] + ": " + msg["content"])

    # Send to Gemini
    response = model.generate_content("\n".join(gemini_messages))

    bot_reply = response.text

    # Add bot message
    messages.append({"role": "assistant", "content": bot_reply})

    print("Bot:", bot_reply)


# Save chat history on exit
save_chat_history(messages)
print("---- Chat history saved. Exit -----")