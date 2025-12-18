# step1: setup pydantic model(schema vlaidation) for request and response

from pydantic import BaseModel

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: list[str]
    allow_search: bool


# step2: setup AI agent from front end request

from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

ALLOWED_MODELS_NAMES=["gpt-4o-mini","llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile"]

app= FastAPI(title="langGraph AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    API Endpoint to interact with the chatbot using langgraph and
    search tools. It dynamically selects the model 
    specifirs in the request.
    """

    if request.model_name not in ALLOWED_MODELS_NAMES:
        return {"error": "Model not supported."}
    
    llm_id= request.model_name
    query= request.messages[0]
    allow_search= request.allow_search
    system_prompt= request.system_prompt
    provider= request.model_provider
    
    # Create AI agent and get response from it
    response= get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider) 
    return {"response":response}



# step3: Run app and explore swagger UI Docs

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8005)

