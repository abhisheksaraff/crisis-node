import threading
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.scraping_service import scraper_wrapper
from app.api.alerts import router as alerts_router
from app.api.execute import router as execute_router

app = FastAPI()
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

# GET /alerts (Feed the map)
# GET /plan/{alert_id} (Fetches the AIs generated Response)
# POST /execute/{alert_id} (Triggers the action when user approves)

app.include_router(alerts_router, prefix="/alerts")
app.include_router(execute_router, prefix="/execute")

@app.exception_handler(404)
async def custom_404(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"Route {request.url.path} not found."}
    )