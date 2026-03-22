from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from functools import partial
import asyncio
from services.ai_service import process_ai_enhance_logic
from shared import update_progress

router = APIRouter()

@router.post("/enhance")
async def ai_enhance(
    file: UploadFile = File(...),
    task_id: str = Form(...),
    enhancement_type: str = Form("upscale"), # upscale, restore, denoise
    scale_factor: float = Form(2.0)
):
    try:
        await update_progress(task_id, 15, "Görsel, yapay zeka stüdyosuna alınıyor...")
        file_bytes = await file.read()

        await update_progress(task_id, 45, "Akıllı motor pikselleri analiz edip yeniden inşa ediyor (Bu işlem biraz sürebilir)...")

        # İşlemi sunucuyu (CPU) kilitlemeden arka planda çalıştır
        loop = asyncio.get_running_loop()
        output_io, filename = await loop.run_in_executor(
            None,
            partial(process_ai_enhance_logic, file_bytes, enhancement_type, scale_factor)
        )

        await update_progress(task_id, 100, "İyileştirme mükemmel bir şekilde tamamlandı!")

        return StreamingResponse(
            output_io,
            media_type="image/jpeg",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        await update_progress(task_id, 100, f"Hata: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})