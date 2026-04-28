from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

# Set Gemini Key before importing agent
from dotenv import load_dotenv
load_dotenv()

from agent import triage_agent, AgentState

app = FastAPI(title="Mumzworld Triage AI Backend")

# Allow React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TriageRequest(BaseModel):
    email_text: str
    image_attached: bool = False
    image_description: Optional[str] = None
    image_base64: Optional[str] = None
    
@app.get("/api/health")
async def health_check():
    """Simple probe endpoint to verify that the FastAPI Uvicorn engine is actively online."""
    return {"status": "online", "message": "Mumzworld AI Triage Core is live and awaiting execution."}
    
@app.post("/api/triage")
async def process_ticket(req: TriageRequest):
    try:
        initial_state: AgentState = {
            "customer_email": req.email_text,
            "image_attached": req.image_attached,
            "image_description": req.image_description,
            "image_base64": req.image_base64,
            "detected_order_id": None,
            "order_data": None,
            "customer_data": None,
            "policy_context": None,
            "final_response": None
        }
        
        # Invoke LangGraph
        final_state = triage_agent.invoke(initial_state)
        
        if not final_state.get("final_response"):
            raise HTTPException(status_code=500, detail="AI failed to generate a structured response.")
            
        resp = final_state["final_response"].dict()
        resp["context_order"] = final_state.get("order_data")
        resp["context_customer"] = final_state.get("customer_data")
        return resp
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
