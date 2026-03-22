from fastapi import APIRouter, UploadFile, File, Form, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from functools import partial
import asyncio
from services.bg_remove_service import remove_background_logic
from shared import update_progress

# --- SAAS DÖNÜŞÜMÜ İÇİN YENİ EKLENEN KİLİTLER ---
from dependencies import get_premium_user
import models
# ------------------------------------------

router = APIRouter()

@router.post("/process")
async def process_bg_remove(
    file: UploadFile = File(...),
    task_id: str = Form(...),
    # MİLYON DOLARLIK KİLİT: Bu satır, kullanıcının PRO olup olmadığını denetler.
    # PRO değilse arka plan silme motorunu (AI) asla çalıştırmaz, hata fırlatır!
    current_user: models.User = Depends(get_premium_user)
):
    try:
        await update_progress(task_id, 15, "Görsel yapay zeka analizine alınıyor...")
        file_bytes = await file.read()
        
        await update_progress(task_id, 45, "Yapay zeka nesneyi tespit edip arka planı siliyor (Bu işlem birkaç saniye sürebilir)...")
        
        # Yapay zeka işlemi CPU/GPU yoğun olduğu için sunucuyu kilitlememesi adına arka planda (thread) çalıştırıyoruz
        loop = asyncio.get_running_loop()
        output_io, filename = await loop.run_in_executor(
            None, 
            remove_background_logic, 
            file_bytes
        )
        
        await update_progress(task_id, 100, "Arka plan kusursuzca silindi!")
        
        # Sonucu direkt olarak şeffaf PNG formatında indir
        return StreamingResponse(
            output_io, 
            media_type="image/png", 
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        await update_progress(task_id, 100, f"Hata: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})