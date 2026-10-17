#1.build(taban imaj)
FROM python:3.12-slim

#2.çalışma dizini
WORKDIR /app

#3.build(bağımlılıkları kopyalama)
COPY requirements.txt .

#4.build(paket kurulumu)
RUN pip install --no-cache-dir -r requirements.txt

#5.build(proje kodlarını kopyalma)
COPY . .

#6.port belgeleme
EXPOSE 8000

#7.başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]