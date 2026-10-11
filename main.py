from http.client import HTTPException

from fastapi import FastAPI, Query, HTTPException
from typing import List
from pydantic import BaseModel
import platform
import time
import os
import psutil
import socket

app = FastAPI(title="Linux Monitoring API", version="1.0.0")

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

# --- 2. ENDPOINT TANIMI ---
@app.get("/health", status_code=200)
def health_check():
    return {"status": "ok"}

# Madde 1: Geliştirilmiş Sistem Bilgileri (Hostname ve Uptime eklendi)
@app.get("/api/system", response_model=SystemInfo)
def get_system_info():
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time

    return SystemInfo(
        os=platform.system(),
        hostname=socket.gethostname(),
        release=platform.release(),
        architecture=platform.machine(),
        cpu_count=os.cpu_count(),
        uptime_seconds=round(uptime_seconds,2)
    )


@app.get("/api/metrics", response_model=SystemMetricsResponse)
def get_system_metrics():
    bellek = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    cpu_oranı = psutil.cpu_percent(interval=1)

    kritik_durum = cpu_oranı > 85 or bellek.percent > 85 or disk.percent > 85

    # Verileri doğrudan Pydantic modellerine paketleyip dönüyoruz
    return SystemMetricsResponse(
        status="warning" if kritik_durum else "healthy",
        cpu=CpuInfo(usage_percent=cpu_oranı),
        memory=MemoryInfo(
            total_gb=round(bellek.total / (1024 ** 3), 2),
            used_gb=round(bellek.used / (1024 ** 3), 2),
            usage_percent=bellek.percent
        ),
        disk=DiskInfo(
            total_gb=round(disk.total / (1024 ** 3), 2),
            free_gb=round(disk.free / (1024 ** 3), 2),
            usage_percent=disk.percent
        )
    )

#4. En çok Kaynak Tüketen Süreçleri Getiren Rota
@app.get("/api/processes", response_model=List[ProcessInfo])
def get_top_processes(
    limit: int = Query(default=5, ge=1, le=50, description="Listelenecek maksimum süreç sayısı (1-50 arası)")
):

    #süreçlieri alıyoruz
    surecler = []

    #psutil.process_iter Linuxtaki /proc/[PID] dizinini tarar ve her süreç için bir psutil.Process nesnesi döndürür.
    aktif_surecler = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc.cpu_percent(None)  # İlk çağrı: Sayaç sıfırlanır/başlatılır
            aktif_surecler.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # İki ölçüm arasında Linux çekirdeğinin fark hesaplayabilmesi için kısa bir bekleme

    time.sleep(0.1)

    # 2. Aşama: Gerçek kullanım oranlarını topla
    for proc in aktif_surecler:
        try:
            cpu = proc.cpu_percent(None)
            mem = proc.memory_percent()
            surecler.append({
                "pid": proc.pid,
                "name": proc.name(),
                "cpu_percent": round(cpu, 2),
                "memory_percent": round(mem, 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    sirali_surecler = sorted(
        surecler,
        key=lambda p: p['cpu_percent'] ,
        reverse=True
    )[:limit]

    return sirali_surecler

