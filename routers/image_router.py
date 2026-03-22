from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from functools import partial
import asyncio
from services.image_service import process_image_logic
from shared import update_progress

router = APIRouter()

@router.post("/process-image-advanced")
async def process_image_advanced(
    file: UploadFile = File(...), task_id: str = Form(...),
    crop_x: float = Form(None), crop_y: float = Form(None),
    crop_width: float = Form(None), crop_height: float = Form(None),
    rotate: int = Form(0), flip_horizontal: bool = Form(False),
    brightness: float = Form(1.0), contrast: float = Form(1.0),
    saturation: float = Form(1.0), sharpness: float = Form(1.0),
    preset: str = Form("none"),
    resize_mode: str = Form("none"), target_width: float = Form(None),
    target_height: float = Form(None), resize_percentage: int = Form(None),
    target_format: str = Form("png")
):
    try:
        await update_progress(task_id, 10, "Görsel stüdyoda işleniyor...")
        
        # Verileri paketle
        crop_data = {'x': crop_x, 'y': crop_y, 'width': crop_width, 'height': crop_height, 'rotate': rotate, 'flip': flip_horizontal}
        filter_data = {'brightness': brightness, 'contrast': contrast, 'saturation': saturation, 'sharpness': sharpness, 'preset': preset}
        resize_data = {'mode': resize_mode, 'width': target_width, 'height': target_height, 'percentage': resize_percentage}
        
        loop = asyncio.get_running_loop()
        output_io, filename = await loop.run_in_executor(
            None, 
            partial(process_image_logic, file.file, crop_data, filter_data, resize_data, {}, target_format)
        )
        
        await update_progress(task_id, 100, "İşlem Tamamlandı!")
        
        media_type = "image/jpeg" if target_format in ["jpg", "jpeg"] else f"image/{target_format}"
        return StreamingResponse(output_io, media_type=media_type, headers={"Content-Disposition": f"attachment; filename={filename}"})
        
    except Exception as e:
        await update_progress(task_id, 100, f"Hata: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})