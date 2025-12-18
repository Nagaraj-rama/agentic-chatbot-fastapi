import streamlit as st
import requests

st.set_page_config(page_title="Agentic Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Agentic Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to call backend API
def get_bot_response(message):
    try:
        response = requests.post(
            "https://agentic-chatbot-fastapi-sk6g.onrender.com/chat",  # your backend
            json={"message": message},
            timeout=30
        )
        if response.ok:
            return response.json().get("response", "No response from bot.")
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Exception: {e}"

# Display chat history
for sender, msg in st.session_state.messages:
    if sender == "You":
        st.write(f"**You:** {msg}")
    else:
        st.write(f"**Bot:** {msg}")

# User input
user_input = st.text_input("Type your message:")

# Send button
if st.button("Send") and user_input:
    # Append user message
    st.session_state.messages.append(("You", user_input))
    
    # Get bot response
    bot_response = get_bot_response(user_input)
    
    # Append bot message
    st.session_state.messages.append(("Bot", bot_response))
