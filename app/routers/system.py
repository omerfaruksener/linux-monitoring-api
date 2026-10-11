from fastapi import APIRouter
from app.schemas.metrics import SystemInfo, SystemMetricsResponse,AboutInfo
from app.services.system_monitor import get_system_info_data, get_system_metrics_data,get_about_data


router = APIRouter()

@router.get("/system", response_model=SystemInfo)
def get_system_info():
    return get_system_info_data()

@router.get("/metrics", response_model=SystemMetricsResponse)
def get_system_metrics():
    return get_system_metrics_data()

@router.get("/about", response_model=AboutInfo)
def get_about():
    return get_about_data()
