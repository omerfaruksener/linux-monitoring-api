from fastapi import APIRouter, Query, HTTPException
from typing import List
from app.schemas.metrics import ProcessInfo
from app.services.system_monitor import get_top_processes_data

router = APIRouter()

@router.get("/top-processes", response_model=List[ProcessInfo])
def get_top_processes(
    limit: int = Query(default=10, ge=1, le=50, description="Listelenecek surec sayisi")
):
    try:
        return get_top_processes_data(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {str(e)}")