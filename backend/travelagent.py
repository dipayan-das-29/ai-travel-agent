import os
import re
from urllib import response
from dotenv import load_dotenv
from ddgs import DDGS
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()

# -------------------------------------------------------------
# 1. DYNAMIC TOOLS
# -------------------------------------------------------------

@tool
def live_travel_search(query: str) -> str:
    """Searches the live web for hotel rates, attraction tickets, or flight estimates.
    Example queries: 'average flight price Kolkata to Tokyo 2026', 'budget hotel price per night in Kyoto'
    """
    print(f"\n[AGENT DECISION] Searching web live for: '{query}'")
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=4):
            results.append(f"Title: {r['title']}\nSnippet: {r['body']}\n")
    
    return "\n---\n".join(results) if results else "No live pricing results found."

@tool
def calculate_trip_budget(flights_cost: float, hotel_nightly_rate: float, daily_allowance: float, days: int) -> str:
    """Calculates total trip cost using prices dynamically discovered by the agent."""
    print(f"\n[AGENT DECISION] Running exact budget calculations...")
    total_hotel = hotel_nightly_rate * days
    total_allowance = daily_allowance * days
    grand_total = flights_cost + total_hotel + total_allowance
    
    return (
        f"Calculated Financial Summary:\n"
        f"- Discovered Flight Cost: ${flights_cost:.2f}\n"
        f"- Lodging ({days} nights @ ${hotel_nightly_rate:.2f}/night): ${total_hotel:.2f}\n"
        f"- Daily Expenses ({days} days @ ${daily_allowance:.2f}/day): ${total_allowance:.2f}\n"
        f"- GRAND TOTAL ESTIMATE: ${grand_total:.2f}"
    )

tools = [live_travel_search, calculate_trip_budget]

# -------------------------------------------------------------
# 2. MODEL SETUP
# -------------------------------------------------------------

llm = ChatOpenAI(
    model="gpt-oss:120b",
    api_key=os.getenv("OLLAMA_API_KEY"),
    base_url="https://ollama.com/v1",
    temperature=0.1
)

# System prompt forcing the agent to fetch prices dynamically
system_prompt = (
    "You are an autonomous Smart Travel Planner. "
    "DO NOT make up or guess flight or hotel costs. "
    "1. Use `live_travel_search` to find real current hotel prices and flight estimates for the destination. "
    "2. Extract real pricing numbers from the search results. "
    "3. Pass those real numbers into `calculate_trip_budget` to verify if the total fits the user's budget. "
    "4. Output a detailed itinerary only after pricing is calculated."
)

agent = create_react_agent(llm, tools=tools)

# -------------------------------------------------------------
# 3. EXPORTABLE EXECUTION FUNCTION
# -------------------------------------------------------------

#user_query = "Plan a 3-day budget-friendly trip to Kyoto for 1 person. Find real hotel rates and flight options, then calculate the full cost."

def run_travel_agent(user_prompt: str) -> str:
    """Invokes the agent with a user prompt and returns the final string response."""
    response = agent.invoke({
        "messages": [
            ("system", system_prompt),
            ("user", user_prompt)
        ]
    })
    print("\n" + "="*50)
    print("FINAL AUTONOMOUS AGENT OUTPUT:\n")
    print(response["messages"][-1].content)
    return response["messages"][-1].content

