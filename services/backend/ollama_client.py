import os
import httpx
import logfire

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma:2b")

class OllamaClient:
    """Client class to query local Ollama model engines within the Docker compose cluster."""
    
    def __init__(self):
        self.base_url = OLLAMA_HOST
        self.model = OLLAMA_MODEL

    async def generate_workflow_schema(self, user_prompt: str) -> dict:
        """
        Submits plain English automation tasks to the Gemma 2B model.
        Forces structured JSON outputs containing Odoo Automated Actions bindings.
        """
        system_instruction = (
            "You are an expert ERP integration agent. Translate the user's natural language "
            "automation workflow into a valid JSON schema representing Odoo Automated Actions. "
            "Respond ONLY with raw valid JSON. Do not include any explanation or markdown formatting."
        )

        logfire.info("Querying Ollama model {model} at {host}...", model=self.model, host=self.base_url)

        payload = {
            "model": self.model,
            "prompt": f"System: {system_instruction}\nUser: {user_prompt}",
            "stream": False,
            "format": "json"
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(f"{self.base_url}/api/generate", json=payload)
                response.raise_for_status()
                result = response.json()
                
                # Parse generated response text containing JSON back to python dict
                raw_response = result.get("response", "{}")
                logfire.info("Ollama successfully generated workflow: {raw_response}", raw_response=raw_response)
                return httpx.Response(status_code=200, json=raw_response).json()
                
        except Exception as e:
            logfire.error("Failed connecting to Ollama LLM container: {error}", error=str(e))
            # Fallback mock schema if LLM is offline or model is compiling
            return {
                "nodes": [
                    {"id": "1", "type": "input", "data": {"label": f"Trigger: {user_prompt}"}, "position": {"x": 250, "y": 25}}
                ],
                "edges": []
            }
