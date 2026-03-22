# 1. Base Image: Hafif ve Güvenli Python 3.10 Sürümü
FROM python:3.10-slim

# Python Ayarları (Hız ve Loglama için zorunlu)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Çalışma Dizini
WORKDIR /app

# 2. Sistem Bağımlılıkları (Milyon Dolarlık Kısım Burası)
# ffmpeg: Video birleştirme ve format değiştirme için ZORUNLU.
# poppler-utils: PDF'i resme çevirmek için ZORUNLU.
# libgl1 & libglib2.0-0: OpenCV ve AI Modelleri (Görüntü İşleme) için ZORUNLU.
# --no-install-recommends: Sadece gerekeni kurar, gereksiz paketleri atlar, build süresini dramatik kısaltır.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4. Cache Optimizasyonu: Önce sadece requirements kopyalanır.
# Kodda bir satır değiştirsen bile kütüphaneler tekrar indirilmez (HIZLI BUILD).
COPY requirements.txt .

# 5. Python Kütüphanelerini Kur (Önce pip güncellenir, sonra paketler kurulur)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Tüm Proje Dosyalarını Kopyala
COPY . .

# 7. İndirme ve Temp Klasörlerini Oluştur (Garanti Olsun)
RUN mkdir -p downloads static/temp_pdf

# 8. Portu Dışarı Aç
EXPOSE 8080

# 9. Uygulamayı Başlat (Prodüksiyon Modu - Gunicorn ve Uvicorn Birlikte)
# 300 saniye timeout (5 dakika) ağır video/AI işlemleri için hayat kurtarır.
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080", "--timeout", "300"]