import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
#from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent

load_dotenv()
@tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers together."""
    print(f"\n[TOOL CALLED] Running multiply() with inputs: a={a}, b={b}")
    return a * b

# # Point ChatOllama to the cloud model name
# llm = ChatOllama(
#     model="gpt-oss:120b-cloud",
#     temperature=0
# )

# Route ChatOpenAI calls directly to Ollama Cloud
llm = ChatOpenAI(
    model="gpt-oss:120b",
    api_key=os.getenv("OLLAMA_API_KEY"),
    base_url="https://ollama.com/v1",
    temperature=0
)

agent = create_agent(llm, tools=[multiply])

response = agent.invoke({
    "messages": [("user", "What is 123 multiply by 456?")]
})

print(response["messages"][-1].content)