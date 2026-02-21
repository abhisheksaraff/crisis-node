import os
import httpx

async def trigger_orchestration_workflow():
    """Triggers the n8n orchestration workflow asynchronously."""
    ORCHESTRATION_URL_DOCKER =  os.getenv("ORCHESTRATION_URL_FASTAPI")
    
    async with httpx.AsyncClient() as client:
        try:
            print("DEBUG: Triggering n8n orchestration workflow...", flush=True)
            response = await client.post(ORCHESTRATION_URL_DOCKER, timeout=10.0)
            print(f"DEBUG: n8n response: {response.status_code}", flush=True)
            return True
        except Exception as e:
            print(f"DEBUG: Failed to trigger n8n: {e}", flush=True)
            
        return False