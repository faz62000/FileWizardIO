from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.background import BackgroundTasks
import os
import uuid
import asyncio
import shutil
from services.video_compress_service import compress_video_logic
from shared import progress_store

router = APIRouter()

TEMP_DIR = "downloads"
os.makedirs(TEMP_DIR, exist_ok=True)

@router.post("/process")
async def compress_video_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    task_id: str = Form(...),
    compression_level: str = Form("medium")
):
    input_ext = os.path.splitext(file.filename)[1]
    if not input_ext: 
        input_ext = ".mp4"
        
    unique_name = str(uuid.uuid4())
    input_path = os.path.join(TEMP_DIR, f"in_{unique_name}{input_ext}")
    output_path = os.path.join(TEMP_DIR, f"out_{unique_name}.mp4")

    # MİLYON DOLARLIK RAM OPTİMİZASYONU
    # Videoyu RAM'e yükleyen "await file.read()" yerine, 
    # shutil ile RAM'e hiç dokunmadan videoyu doğrudan SSD'ye akıtıyoruz (Streaming).
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        return JSONResponse({"error": f"Dosya yazma hatası: {str(e)}"}, status_code=400)

    # Orijinal dosyanın boyutunu ölç (Akıllı kontrol için)
    original_size = os.path.getsize(input_path)

    # CRF Değerlerini Güncelledik (Modern videolar zaten çok sıkıştırılmıştır)
    # Değerleri artırdık ki gerçekten "sıkıştırma" yapsın.
    crf_map = {
        "light": "28",    # Hafif
        "medium": "32",   # Standart 
        "extreme": "38"   # Maksimum
    }
    crf_value = crf_map.get(compression_level, "32")

    # Sıkıştırma işlemini asenkron (Thread içinde) başlat
    success = await asyncio.to_thread(compress_video_logic, input_path, output_path, task_id, crf_value)

    if success and os.path.exists(output_path):
        compressed_size = os.path.getsize(output_path)
        
        # AKILLI BOYUT KONTROLÜ: Eğer sıkışan dosya orijinalden büyükse, orijinali ver!
        if compressed_size >= original_size:
            os.replace(input_path, output_path) # Orijinali output'un üzerine yaz
        else:
            # Sıkıştırma başarılı ve boyut küçüldüyse orijinali silebiliriz
            if os.path.exists(input_path):
                os.remove(input_path)

        # Kullanıcı dosyayı indirdikten sonra sunucudan silinmesi için arkaplan görevi
        background_tasks.add_task(os.remove, output_path)
        
        return FileResponse(
            path=output_path,
            filename=f"FileWizard_Compressed_{unique_name}.mp4",
            media_type="video/mp4"
        )
    else:
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        return JSONResponse({"error": "Video sıkıştırma işlemi başarısız oldu."}, status_code=500)