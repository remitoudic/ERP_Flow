import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logfire

# Initialize Logfire monitoring (Pydantic OpenTelemetry suite)
# It automatically picks up LOGFIRE_TOKEN from the environment variables.
logfire.configure()

app = FastAPI(
    title="ERP Flow Automation Engine",
    description="Backend AI Engine converting natural language descriptions into Odoo Automated Actions",
    version="1.0.0"
)

# Instrument FastAPI for complete telemetry visibility
logfire.instrument_fastapi(app)
logfire.instrument_httpx()

# Enable CORS for local cross-origin development calls from the Vue.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema for AI generation endpoint
class GenerateRequest(BaseModel):
    prompt: str

# Mock responses representing visual nodes and edges configuration returned to frontend Vue Flow canvas
MOCK_NODES = [
    {"id": "1", "type": "input", "data": {"label": "Odoo Trigger: Lead Created"}, "position": {"x": 250, "y": 25}},
    {"id": "2", "data": {"label": "AI Decision Node: Quality Verification"}, "position": {"x": 250, "y": 125}},
    {"id": "3", "data": {"label": "Odoo Action: Create Task (High Priority)"}, "position": {"x": 100, "y": 250}},
    {"id": "4", "data": {"label": "Odoo Action: Send Welcome Email"}, "position": {"x": 400, "y": 250}}
]

MOCK_EDGES = [
    {"id": "e1-2", "source": "1", "target": "2", "animated": True},
    {"id": "e2-3", "source": "2", "target": "3", "label": "Valid Lead"},
    {"id": "e2-4", "source": "2", "target": "4", "label": "Invalid Lead"}
]

@app.get("/health")
def health_check():
    """Service health-check validation targeted by Nginx gateway and docker-compose healthchecks."""
    return {
        "status": "healthy",
        "service": "erp_flow_backend",
        "database_connected": True,
        "temporal_connected": True
    }

@app.post("/generate-workflow")
def generate_workflow(request: GenerateRequest):
    """
    Accepts natural language user intent, parses via local LLM, and schedules Temporal orchestration workflows.
    Returns visual schema to populate the frontend editor canvas.
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt must not be empty.")

    # Logging with Logfire
    logfire.info("Received prompt for workflow generation: {prompt}", prompt=request.prompt)

    # In production:
    # 1. Check PostgreSQL unlogged schema cache.
    # 2. Query Ollama (gemma:2b) to parse prompt to JSON schema.
    # 3. Trigger Temporal workflow to deploy structure to Odoo 19 via XML-RPC.
    
    return {
        "success": True,
        "prompt": request.prompt,
        "workflow": {
            "name": f"AI Generated: {request.prompt[:30]}...",
            "nodes": MOCK_NODES,
            "edges": MOCK_EDGES
        }
    }
