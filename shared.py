import asyncio
import os

# Geçici RAM Bellekleri (Redis yerine hızlı çözüm)
progress_store = {}
pdf_sessions = {}

# Klasör Ayarları
DOWNLOADS_DIR = "downloads"
TEMP_PDF_DIR = "static/temp_pdf"

# Klasörleri Garantiye Al
os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(TEMP_PDF_DIR, exist_ok=True)

async def update_progress(task_id: str, percent: int, message: str):
    """
    Tüm servislerin ilerleme çubuğunu güncellediği güvenli fonksiyon.
    """
    try:
        progress_store[task_id] = {"percent": percent, "message": message}
        # Çakışmayı önlemek için milisaniyelik nefes alma
        await asyncio.sleep(0.01)
    except Exception as e:
        print(f"Progress Error: {e}")