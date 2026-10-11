import os
import time
import platform
import socket
import psutil


def get_system_info_data():
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time

    return {
        "os": platform.system(),
        "hostname": socket.gethostname(),
        "release": platform.release(),
        "architecture": platform.machine(),
        "cpu_count": os.cpu_count(),
        "uptime_seconds": round(uptime_seconds, 2)
    }

def get_system_metrics_data():
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


def get_top_processes_data(limit: int):

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
