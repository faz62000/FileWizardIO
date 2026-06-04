from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
import os
import json
import asyncio
from shared import progress_store
from routers import (
    video_router, image_router, pdf_router, watermark_router,
    developer_router, batch_router, ai_router, cloud_router,
    bg_remove_router, video_compress_router, auth_router
)
from routers import stripe_router
from database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FileWizardIO Pro API",
    description="Ultimate Media Processing Engine",
    version="8.1.0",
    docs_url=None,
    redoc_url=None
)

# GZIP
app.add_middleware(GZipMiddleware, minimum_size=1000)

# CORS — sadece kendi domain
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "https://filewizardio.com").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# ROUTER'LAR
app.include_router(video_router.router, prefix="/api", tags=["Video"])
app.include_router(image_router.router, prefix="/api", tags=["Image"])
app.include_router(pdf_router.router, prefix="/api/pdf", tags=["PDF"])
app.include_router(watermark_router.router, prefix="/api/watermark", tags=["Watermark"])
app.include_router(developer_router.router, prefix="/api/developer", tags=["Developer"])
app.include_router(batch_router.router, prefix="/api/batch", tags=["Batch"])
app.include_router(ai_router.router, prefix="/api/ai", tags=["AI"])
app.include_router(cloud_router.router, prefix="/api/cloud", tags=["Cloud"])
app.include_router(bg_remove_router.router, prefix="/api/bg-remove", tags=["Background Remove"])
app.include_router(video_compress_router.router, prefix="/api/compress", tags=["Video Compress"])
app.include_router(auth_router.router, prefix="/api/auth", tags=["Auth"])
app.include_router(stripe_router.router, prefix="/api/billing", tags=["Billing"])

# SSE PROGRESS STREAM
@app.get("/api/progress/{task_id}")
async def progress_stream(request: Request, task_id: str):
    async def event_generator():
        retry = 0
        max_retries = 3000
        while True:
            if await request.is_disconnected():
                break
            data = progress_store.get(task_id)
            if not data:
                retry += 1
                if retry > max_retries:
                    yield f"data: {json.dumps({'percent': 100, 'message': 'Hata: Zaman aşımı'})}\n\n"
                    break
                await asyncio.sleep(0.2)
                continue
            retry = 0
            yield f"data: {json.dumps(data)}\n\n"
            if data["percent"] >= 100 or str(data["message"]).startswith("Hata"):
                await asyncio.sleep(0.5)
                if task_id in progress_store:
                    del progress_store[task_id]
                break
            await asyncio.sleep(0.2)
    return StreamingResponse(event_generator(), media_type="text/event-stream")

# TR SAYFALAR
@app.get("/araclar/otomatik-filigran", include_in_schema=False)
async def watermark_tr(): return FileResponse("static/watermark.html") if os.path.exists("static/watermark.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/gelistirici-api", include_in_schema=False)
async def developer_tr(): return FileResponse("static/developer.html") if os.path.exists("static/developer.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/araclar/toplu-islem", include_in_schema=False)
async def batch_tr(): return FileResponse("static/batch.html") if os.path.exists("static/batch.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/araclar/ai-studyo", include_in_schema=False)
async def ai_studio_tr(): return FileResponse("static/ai_studio.html") if os.path.exists("static/ai_studio.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/araclar/bulut-senkronizasyonu", include_in_schema=False)
async def cloud_tr(): return FileResponse("static/cloud_sync.html") if os.path.exists("static/cloud_sync.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/araclar/arka-plan-silici", include_in_schema=False)
async def bg_tr(): return FileResponse("static/bg_remove.html") if os.path.exists("static/bg_remove.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/araclar/video-kucultme", include_in_schema=False)
async def compress_tr(): return FileResponse("static/video_compress.html") if os.path.exists("static/video_compress.html") else JSONResponse({"detail":"not found"}, 404)

# YASAL SAYFALAR TR
@app.get("/kosullar", include_in_schema=False)
async def terms_tr(): return FileResponse("static/legal/terms.html") if os.path.exists("static/legal/terms.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/gizlilik-politikasi", include_in_schema=False)
async def privacy_tr(): return FileResponse("static/legal/privacy.html") if os.path.exists("static/legal/privacy.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/iade-politikasi", include_in_schema=False)
async def refund_tr(): return FileResponse("static/legal/refund.html") if os.path.exists("static/legal/refund.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/cerez-politikasi", include_in_schema=False)
async def cookies_tr(): return FileResponse("static/legal/cookies.html") if os.path.exists("static/legal/cookies.html") else JSONResponse({"detail":"not found"}, 404)

# EN SAYFALAR
@app.get("/en/", include_in_schema=False)
@app.get("/en", include_in_schema=False)
async def home_en(): return FileResponse("static/index.html") if os.path.exists("static/index.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/tools/auto-watermark", include_in_schema=False)
async def watermark_en(): return FileResponse("static/watermark.html") if os.path.exists("static/watermark.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/developer-api", include_in_schema=False)
async def developer_en(): return FileResponse("static/developer.html") if os.path.exists("static/developer.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/tools/batch-processing", include_in_schema=False)
async def batch_en(): return FileResponse("static/batch.html") if os.path.exists("static/batch.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/tools/ai-studio", include_in_schema=False)
async def ai_en(): return FileResponse("static/ai_studio.html") if os.path.exists("static/ai_studio.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/tools/cloud-sync", include_in_schema=False)
async def cloud_en(): return FileResponse("static/cloud_sync.html") if os.path.exists("static/cloud_sync.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/tools/background-remover", include_in_schema=False)
async def bg_en(): return FileResponse("static/bg_remove.html") if os.path.exists("static/bg_remove.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/tools/video-compressor", include_in_schema=False)
async def compress_en(): return FileResponse("static/video_compress.html") if os.path.exists("static/video_compress.html") else JSONResponse({"detail":"not found"}, 404)

# YASAL SAYFALAR EN
@app.get("/en/terms", include_in_schema=False)
async def terms_en(): return FileResponse("static/legal/terms.html") if os.path.exists("static/legal/terms.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/privacy-policy", include_in_schema=False)
async def privacy_en(): return FileResponse("static/legal/privacy.html") if os.path.exists("static/legal/privacy.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/refund-policy", include_in_schema=False)
async def refund_en(): return FileResponse("static/legal/refund.html") if os.path.exists("static/legal/refund.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/cookie-policy", include_in_schema=False)
async def cookies_en(): return FileResponse("static/legal/cookies.html") if os.path.exists("static/legal/cookies.html") else JSONResponse({"detail":"not found"}, 404)

# SEO
@app.get("/robots.txt", include_in_schema=False)
async def robots(): return FileResponse("static/robots.txt") if os.path.exists("static/robots.txt") else JSONResponse({"detail":"not found"}, 404)

@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap(): return FileResponse("static/sitemap.xml", media_type="application/xml") if os.path.exists("static/sitemap.xml") else JSONResponse({"detail":"not found"}, 404)

# STATİK DOSYALAR
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")
app.mount("/temp_pdf", StaticFiles(directory="static/temp_pdf"), name="temp_pdf")
app.mount("/", StaticFiles(directory="static", html=True), name="static")
