from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.alerts import router as alerts_router
from app.api.execute import router as execute_router

app = FastAPI()

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