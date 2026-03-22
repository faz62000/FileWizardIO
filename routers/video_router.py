from fastapi import APIRouter, Form
from fastapi.responses import FileResponse, JSONResponse
from functools import partial
import asyncio
from services.video_service import get_media_info_logic, download_media_logic
from shared import update_progress

router = APIRouter()

@router.post("/get-media-info")
async def get_media_info(url: str = Form(...)):
    try:
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(None, get_media_info_logic, url)
        return JSONResponse(data)
    except Exception as e: return JSONResponse(status_code=400, content={"error": str(e)})

@router.post("/download-media")
async def download_media(url: str = Form(...), format_type: str = Form(...), task_id: str = Form(...)):
    try:
        await update_progress(task_id, 10, "Bağlantı kuruluyor...")
        loop = asyncio.get_running_loop()
        await update_progress(task_id, 40, "İndirme ve dönüştürme başladı...")
        
        output_path, filename = await loop.run_in_executor(None, partial(download_media_logic, url, format_type))
        
        await update_progress(task_id, 100, "Tamamlandı!")
        media_type = "audio/mpeg" if format_type == "mp3" else "video/mp4"
        return FileResponse(output_path, filename=filename, media_type=media_type)
    except Exception as e:
        await update_progress(task_id, 100, f"Hata: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})