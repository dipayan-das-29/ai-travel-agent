from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import the core execution function from agent.py
from travelagent import run_travel_agent

app = FastAPI(
    title="Smart Travel Agent API",
    description="API layer serving Agentic workflows powered by Ollama Cloud."
)

# Enable CORS for Angular frontend running on port 4200
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TravelQueryRequest(BaseModel):
    prompt: str

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Travel Agent API is running"}

@app.post("/api/plan")
async def generate_plan(request: TravelQueryRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    try:
        # Call the imported agent function
        result_markdown = run_travel_agent(request.prompt)
        return {"result": result_markdown}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)