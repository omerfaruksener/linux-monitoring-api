FastAPI ve `psutil` kullanilarak gelistirilmis, Linux sistem metriklerini (CPU, RAM, Disk) ve en cok kaynak tuketen surecleri izleyen REST API.
* Python 3
* FastAPI
* Uvicorn
* psutil (Donanim metrikleri icin)
* Pydantic (Veri dogrulama ve DTO icin)
1. Repoyu klonlayin.
2. Sanal ortami kurun: `python -m venv venv`
3. Aktif edin: `source venv/bin/activate`
4. Paketleri yukleyin: `pip install -r requirements.txt`
5. Calistirin: `uvicorn main:app --reload`
