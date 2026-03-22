from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.background import BackgroundTasks
import os
import uuid
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

    # Dosyayı sunucuya kaydet
    try:
        with open(input_path, "wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        return JSONResponse({"error": f"Dosya yazma hatası: {str(e)}"}, status_code=400)

    # Sıkıştırma seviyesine göre CRF değerini belirle
    # Düşük CRF = Daha yüksek dosya boyutu, Yüksek CRF = Daha yüksek sıkıştırma
    crf_map = {
        "light": "24",    # Hafif sıkıştırma (Mükemmel kalite)
        "medium": "28",   # Standart (Tavsiye edilen)
        "extreme": "35"   # Maksimum sıkıştırma (WhatsApp/Mail uyumlu)
    }
    crf_value = crf_map.get(compression_level, "28")

    # Sıkıştırma işlemini senkron (bekleyerek) başlat
    success = compress_video_logic(input_path, output_path, task_id, crf_value)

    # Orijinal girdiyi temizle
    if os.path.exists(input_path):
        os.remove(input_path)

    if success and os.path.exists(output_path):
        # Kullanıcı dosyayı indirdikten sonra sunucudan silinmesi için arkaplan görevi
        background_tasks.add_task(os.remove, output_path)
        
        return FileResponse(
            path=output_path,
            filename=f"FileWizard_Compressed_{unique_name}.mp4",
            media_type="video/mp4"
        )
    else:
        if os.path.exists(output_path):
            os.remove(output_path)
        return JSONResponse({"error": "Video sıkıştırma işlemi başarısız oldu."}, status_code=500)