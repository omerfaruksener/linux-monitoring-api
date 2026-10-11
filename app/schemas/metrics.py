from pydantic import BaseModel

# --- 1. DTO / MODEL TANIMLARI (Pydantic) ---

class SystemInfo(BaseModel):
    os: str
    hostname: str
    release: str
    architecture: str
    cpu_count: int
    uptime_seconds: float

class ProcessInfo(BaseModel):
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float

class CpuInfo(BaseModel):
    usage_percent: float

class MemoryInfo(BaseModel):
    total_gb: float
    used_gb: float
    usage_percent: float

class DiskInfo(BaseModel):
    total_gb: float
    free_gb: float
    usage_percent: float

# Ana yanıt modelimiz 
class SystemMetricsResponse(BaseModel):
    status: str
    cpu: CpuInfo
    memory: MemoryInfo
    disk: DiskInfo

class AboutInfo(BaseModel):
    app_name: str
    version: str
    developer: str