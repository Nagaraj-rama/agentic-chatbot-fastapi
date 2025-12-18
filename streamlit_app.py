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

# Function to display chat
def display_chat():
    chat_html = ""
    for sender, msg in st.session_state.messages:
        if sender == "You":
            chat_html += f"""
            <div style="text-align: right; background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin:5px 0;">
                <b>You:</b> {msg}
            </div>
            """
        else:
            chat_html += f"""
            <div style="text-align: left; background-color: #F1F0F0; padding: 10px; border-radius: 10px; margin:5px 0;">
                <b>Bot:</b> {msg}
            </div>
            """
    st.markdown(chat_html, unsafe_allow_html=True)

# Display existing chat
display_chat()

# User input
user_input = st.text_input("Type your message:", key="input")

# Send button
if st.button("Send") and user_input:
    # Add user message
    st.session_state.messages.append(("You", user_input))
    # Add temporary bot message
    st.session_state.messages.append(("Bot", "Bot is typing..."))
    
    # Refresh display with typing message
    display_chat()
    st.experimental_rerun() if hasattr(st, "experimental_rerun") else None

    # Get bot response
    bot_response = get_bot_response(user_input)
    # Replace "Bot is typing..." with actual response
    st.session_state.messages[-1] = ("Bot", bot_response)

# Display chat again to ensure latest message shows
display_chat()

# Scrollable chat container
st.markdown("""
<style>
div.block-container {
    max-height: 70vh;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)
