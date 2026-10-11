from fastapi import FastAPI
from app.routers import system, processes

app = FastAPI(title="Linux Monitoring API", version="2.0.0")


app.include_router(system.router, prefix="/api", tags=["Sistem"])
app.include_router(processes.router, prefix="/api", tags=["Surecler"])

@app.get("/health", status_code=200, tags=["Health"])
def health_check():
    return {"status": "ok"}