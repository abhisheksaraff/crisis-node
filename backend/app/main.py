import threading
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from apscheduler.schedulers.background import BackgroundScheduler
from backend.app.services.scraping_service import scraper_wrapper
from backend.app.api.web_router import router as web_router
from backend.app.api.agent_router import router as agent_router

app = FastAPI(title="Crisis Node AI")
scheduler = BackgroundScheduler()

def run_scheduled_scraper():
    scraper_wrapper()

scheduler.add_job(scraper_wrapper, 'interval', minutes=5)

@app.on_event("startup")
async def startup_event():
    scheduler.start() # Start the scheduler
    threading.Thread(target=run_scheduled_scraper, daemon=True).start() 
    print("FastAPI started and Scheduler is running..")

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
    print("Scheduler shut down.")

# Human User Interface Routes
app.include_router(web_router, prefix="/api", tags=["Web Dashboard"])

# AI Agent Skill Routes
app.include_router(agent_router, prefix="/agent", tags=["AI Orchestrator"])

@app.exception_handler(404)
async def custom_404(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"Route {request.url.path} not found."}
    )