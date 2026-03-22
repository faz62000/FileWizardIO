from fastapi import APIRouter, UploadFile, File, Request, Form
from fastapi.responses import JSONResponse, FileResponse
from functools import partial
import asyncio
import time
from typing import List
from services.pdf_service import pdf_to_images_logic, reconstruct_pdf_logic, compress_pdf_logic, merge_pdfs_logic
from shared import pdf_sessions, update_progress

router = APIRouter()

@router.post("/upload")
async def pdf_upload(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        loop = asyncio.get_running_loop()
        task_id, preview_data = await loop.run_in_executor(None, pdf_to_images_logic, file_bytes)
        
        # RAM Oturumu
        pdf_sessions[task_id] = {"data": file_bytes, "timestamp": time.time()}
        
        return JSONResponse({"task_id": task_id, "pages": preview_data})
    except Exception as e: return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/save")
async def pdf_save(request: Request):
    try:
        data = await request.json()
        task_id = data.get("task_id")
        if task_id not in pdf_sessions: return JSONResponse(status_code=404, content={"error": "Zaman aşımı"})
        
        loop = asyncio.get_running_loop()
        output_path, filename = await loop.run_in_executor(None, partial(reconstruct_pdf_logic, pdf_sessions[task_id]["data"], data.get("operations")))
        return JSONResponse({"download_url": f"/downloads/{filename}"})
    except Exception as e: return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/compress")
async def pdf_compress(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        loop = asyncio.get_running_loop()
        output_path, filename = await loop.run_in_executor(None, compress_pdf_logic, file_bytes)
        return FileResponse(output_path, filename=filename, media_type="application/pdf")
    except Exception as e: return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/merge")
async def pdf_merge(files: List[UploadFile] = File(...)):
    try:
        file_list_bytes = []
        for f in files: file_list_bytes.append(await f.read())
        
        loop = asyncio.get_running_loop()
        output_path, filename = await loop.run_in_executor(None, merge_pdfs_logic, file_list_bytes)
        return FileResponse(output_path, filename=filename, media_type="application/pdf")
    except Exception as e: return JSONResponse(status_code=500, content={"error": str(e)})