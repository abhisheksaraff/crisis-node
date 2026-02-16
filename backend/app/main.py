import os
import asyncio
import threading
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from apscheduler.schedulers.background import BackgroundScheduler
from app.db.db import run_db_init
from app.db.news_db import delete_all_news
from app.services.scraping_service import scraper_wrapper
from app.services.verification_service import verification_wrapper
from app.services.orchestration_service import trigger_orchestration_workflow
from app.routers.user_router import router as user_router
from app.routers.agent_router import router as agent_router

app = FastAPI(title="Crisis Node")
scheduler = BackgroundScheduler()

import os

def run_crisis_pipeline():
    run_delete = os.getenv("ENABLE_DELETE", "True").lower() == "true"
    run_scraper = os.getenv("ENABLE_SCRAPER", "True").lower() == "true"
    run_verify = os.getenv("ENABLE_VERIFICATION", "True").lower() == "true"
    run_orchestration = os.getenv("ENABLE_ORCHESTRATION", "True").lower() == "true"

    print(f"--- Pipeline Config: Delete={run_delete}, Scrape={run_scraper}, Verify={run_verify} ---")
    
    try:
        run_db_init()
        
        if run_delete:
            print("Step 1: Clearing database...")
            delete_all_news()
        
        if run_scraper:
            print("Step 2: Running scraper...")
            scraper_wrapper()
        
        if run_verify:
            print("Step 3: Running News Verification...")
            verification_wrapper(limit=50)
            
        if run_orchestration:
            print("Step 4: Running Orchestration Workflow...")
            asyncio.run(trigger_orchestration_workflow())
            
        print("--- Pipeline Cycle Complete ---")
    except Exception as e:
        print(f"--- Pipeline Failed: {e} ---")

scheduler.add_job(run_crisis_pipeline, 'interval', hours=24)

@app.on_event("startup")
async def startup_event():
    scheduler.start() 
    threading.Thread(target=run_crisis_pipeline, daemon=True).start() 
    print("FastAPI started and Crisis Pipeline is running.")

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
    print("Scheduler shut down.")

# Human User Interface Routes
app.include_router(user_router, tags=["User Dashboard"])

# AI Agent Skill Routes
app.include_router(agent_router, tags=["AI Orchestrator"])

@app.exception_handler(404)
async def custom_404(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"Route {request.url.path} not found."}
    )