# step1: setup UI with streamlit (model provider,model,system prompt,query)
import streamlit as st

st.set_page_config(page_title="LangGraph AI Agent", page_icon="🤖", layout="centered")
st.title("CodeGPT")
st.write("Interact with AI agent")

system_prompt = st.text_area("Define your AI Agent", height=100, placeholder="Type here...")

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

provider= st.radio("Select Model Provider", ("Groq", "OpenAI"))

if provider == "Groq":
    selected_model = st.selectbox("Select Groq Model", MODEL_NAMES_GROQ) 
elif provider == "OpenAI":
    selected_model = st.selectbox("Select OpenAI Model", MODEL_NAMES_OPENAI)


allow_web_search = st.checkbox("Allow Web Search")

user_query = st.text_area("Enter your Query", height=150, placeholder="Ask anything...")

# API_URL="http://127.0.0.1:8005/chat"
API_URL="https://YOUR-BACKEND-URL.onrender.com/chat"



if st.button("Ask Agent"):
    if user_query.strip():
        # step2: connect with backend via URL
        import requests

        payload={
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data['error'])
            else:
                st.subheader("Agent Response:")
                # st.markdown(f"**Final Response:** {response}")
                st.markdown(f"**Final Response:** {response_data['response']}")



    

# step2: connect with backend via URL