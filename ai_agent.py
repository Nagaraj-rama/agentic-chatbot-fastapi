# Step1: Setup API keys for Groq and travily



import os

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")



# Step2: Setup LLM and Tools

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
# from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch

openai_llm = ChatOpenAI(model="gpt-4o-mini")
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")
# search_tool = TavilySearchResults(max_results=2)
search_tool = TavilySearch(max_results=2)



# step3: Setup AI Agent with search tool functionality

from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

system_prompt = "Act as an AI chatbot who is smart and friendly"

def get_response_from_ai_agent(llm_id,query, allow_search,system_prompt,provider):
    # if provider == "Groq":
    #     llm=ChatGroq(model=llm_id)
    # elif provider == "OpenAI":
    #     llm=ChatOpenAI(model=llm_id)

    # tools = [TavilySearch(max_results=2)] if allow_search else []
    if provider == "Groq":
        llm = ChatGroq(model=llm_id, api_key=GROQ_API_KEY)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=llm_id, api_key=OPENAI_API_KEY)

    tools = [TavilySearch(max_results=2, api_key=TAVILY_API_KEY)] if allow_search else []


    agent = create_react_agent(
        model=llm,
        tools=tools,
        # state_modifier = system_prompt
        # system_prompt = system_prompt 
    )   
    # state = {"messages" : query}
    state = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    }
    response = agent.invoke(state)
    messages = response.get("messages")
    ai_messages= [message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]

