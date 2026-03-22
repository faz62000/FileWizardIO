from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from functools import partial
import asyncio
from typing import List
from services.batch_service import process_batch_logic
from shared import update_progress

router = APIRouter()

@router.post("/process-multiple")
async def process_batch(
    files: List[UploadFile] = File(...),
    task_id: str = Form(...),
    target_format: str = Form("jpeg"),
    resize_width: int = Form(0)
):
    try:
        total_files = len(files)
        if total_files > 50:
            return JSONResponse(status_code=400, content={"error": "Tek seferde maksimum 50 dosya yükleyebilirsiniz."})

        await update_progress(task_id, 10, f"{total_files} dosya stüdyoya alınıyor...")
        
        # FastAPI UploadFile nesnelerini senkron çalışan Pillow'a iletmek için baytlara çevir
        files_data = []
        for f in files:
            content = await f.read()
            files_data.append((f.filename, content))
            
        await update_progress(task_id, 40, "Yapay zeka tüm dosyaları aynı anda işliyor...")
        
        # CPU'yu yormadan arka planda işlemi başlat
        loop = asyncio.get_running_loop()
        zip_io, zip_filename = await loop.run_in_executor(
            None,
            partial(process_batch_logic, files_data, target_format, resize_width)
        )
        
        await update_progress(task_id, 100, "İşlem bitti, ZIP dosyası hazırlanıyor!")
        
        # Sonucu direkt indirme akışı (Stream) olarak gönder
        return StreamingResponse(
            zip_io, 
            media_type="application/zip", 
            headers={"Content-Disposition": f"attachment; filename={zip_filename}"}
        )
        
    except Exception as e:
        await update_progress(task_id, 100, f"Hata: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})