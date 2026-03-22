from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from functools import partial
import asyncio
from services.cloud_service import upload_to_dropbox_logic
from shared import update_progress

router = APIRouter()

@router.post("/sync-dropbox")
async def sync_to_dropbox(
    file: UploadFile = File(...),
    task_id: str = Form(...),
    access_token: str = Form(...)
):
    try:
        await update_progress(task_id, 15, "Dosya FileWizard sunucularına alınıyor...")
        file_bytes = await file.read()
        filename = file.filename
        
        await update_progress(task_id, 50, "Bulut sunucularıyla güvenli bağlantı kuruluyor ve aktarım başlıyor...")
        
        # CPU'yu ve ana akışı kilitlemeden arka planda yüklemeyi gerçekleştir
        loop = asyncio.get_running_loop()
        uploaded_name, uploaded_size = await loop.run_in_executor(
            None,
            partial(upload_to_dropbox_logic, file_bytes, filename, access_token)
        )
        
        await update_progress(task_id, 100, "Bulut senkronizasyonu başarıyla tamamlandı!")
        
        return JSONResponse({
            "success": True,
            "message": "Dosya başarıyla Dropbox hesabınıza kaydedildi.",
            "file_name": uploaded_name,
            "size_bytes": uploaded_size
        })
        
    except Exception as e:
        await update_progress(task_id, 100, f"Hata: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})