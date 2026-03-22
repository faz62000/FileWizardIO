from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from functools import partial
import asyncio
from services.watermark_service import process_watermark_logic
from shared import update_progress

router = APIRouter()

@router.post("/process")
async def process_watermark(
    base_image: UploadFile = File(...),
    logo_image: UploadFile = File(...),
    task_id: str = Form(...),
    opacity: int = Form(100),
    position: str = Form("bottom_right"),
    target_format: str = Form("png")
):
    try:
        await update_progress(task_id, 10, "Görseller stüdyoya alınıyor...")
        
        loop = asyncio.get_running_loop()
        await update_progress(task_id, 40, "Yapay zeka katmanları analiz ediyor...")
        
        output_io, filename = await loop.run_in_executor(
            None, 
            partial(
                process_watermark_logic, 
                base_image.file, 
                logo_image.file, 
                opacity, 
                position, 
                target_format
            )
        )
        
        await update_progress(task_id, 100, "Markalama Tamamlandı!")
        
        media_type = "image/jpeg" if target_format in ["jpg", "jpeg"] else f"image/{target_format}"
        return StreamingResponse(output_io, media_type=media_type, headers={"Content-Disposition": f"attachment; filename={filename}"})
        
    except Exception as e:
        await update_progress(task_id, 100, f"Hata: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})