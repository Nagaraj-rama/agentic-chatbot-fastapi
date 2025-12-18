import streamlit as st
import requests
import time

st.set_page_config(page_title="Agentic Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Agentic Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to call backend API
def get_bot_response(message):
    try:
        response = requests.post(
            "https://agentic-chatbot-fastapi-sk6g.onrender.com/chat",  # your deployed backend
            json={"message": message},
            timeout=30
        )
        if response.ok:
            return response.json().get("response", "No response from bot.")
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Exception: {e}"

# User input
user_input = st.text_input("You:", "", key="input")

if st.button("Send") and user_input:
    # Append user message
    st.session_state.messages.append(("You", user_input))
    
    # Show "Bot is typing..." message
    st.session_state.messages.append(("Bot", "Bot is typing..."))
    
    # Refresh UI to show "Bot is typing..."
    st.experimental_rerun()

# Display chat history
for i, (sender, msg) in enumerate(st.session_state.messages):
    if sender == "You":
        st.markdown(f"**You:** {msg}")
    else:
        # If "Bot is typing...", call backend
        if msg == "Bot is typing...":
            bot_response = get_bot_response(st.session_state.messages[i-1][1])
            st.session_state.messages[i] = ("Bot", bot_response)
            st.experimental_rerun()
        else:
            st.markdown(f"**Bot:** {msg}")
