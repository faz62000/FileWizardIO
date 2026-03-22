# 1. Base Image: Hafif ve Güvenli Python 3.10 Sürümü
FROM python:3.10-slim

# 2. Sistem Bağımlılıkları (Milyon Dolarlık Kısım Burası)
# ffmpeg: Video birleştirme ve format değiştirme için ZORUNLU.
# poppler-utils: PDF'i resme çevirmek için ZORUNLU.
RUN apt-get update && apt-get install -y \
    ffmpeg \
    poppler-utils \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# 3. Çalışma Dizini
WORKDIR /app

# 4. Cache Optimizasyonu: Önce sadece requirements kopyalanır.
# Kodda bir satır değiştirsen bile kütüphaneler tekrar indirilmez (HIZLI BUILD).
COPY requirements.txt .

# 5. Python Kütüphanelerini Kur
RUN pip install --no-cache-dir -r requirements.txt

# 6. Tüm Proje Dosyalarını Kopyala
COPY . .

# 7. İndirme ve Temp Klasörlerini Oluştur (Garanti Olsun)
RUN mkdir -p downloads static/temp_pdf

# 8. Portu Dışarı Aç
EXPOSE 8080

# 9. Uygulamayı Başlat (Prodüksiyon Modu)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]