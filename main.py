from dotenv import load_dotenv

# --- 401 HATASI ÇÖZÜMÜ: .env dosyasını router'lardan önce zorla okut ---
load_dotenv()
# -----------------------------------------------------------------------

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
import os
import json
import asyncio
from shared import progress_store
from routers import video_router, image_router, pdf_router, watermark_router, developer_router, batch_router, ai_router, cloud_router, bg_remove_router, video_compress_router

# --- SAAS DÖNÜŞÜMÜ İÇİN YENİ EKLENENLER ---
# Lemon Squeezy yerine ForgeLogic LLC için Paddle altyapısı eklendi
from routers import auth_router, paddle_router 
from database import engine, Base

# Uygulama başlarken veritabanı tablolarını otomatik olarak oluştur (Sadece ilk çalışmada tabloları çizer)
Base.metadata.create_all(bind=engine)
# ------------------------------------------

app = FastAPI(
    title="FileWizardIO Pro API",
    description="Ultimate Media Processing Engine",
    version="8.0.0",
    docs_url=None, # Production'da gizle
    redoc_url=None
)

# 1. HIZ İÇİN GZIP SIKIŞTIRMA (ÖNEMLİ SEO PUANI)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 2. GÜVENLİK (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Production'da kendi domainini yaz: ["https://filewizardio.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. ROUTERLARI BAĞLA
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

# YENİ: SaaS rotaları (Kayıt, Giriş ve Ödeme Dinleyici - Paddle)
app.include_router(auth_router.router, prefix="/api/auth", tags=["Auth"])
app.include_router(paddle_router.router, prefix="/api/billing", tags=["Billing"])

# 4. SSE (PROGRESS BAR) STREAM
@app.get("/api/progress/{task_id}")
async def progress_stream(request: Request, task_id: str):
    async def event_generator():
        retry = 0
        max_retries = 3000 # 10 dakika bekleme
        while True:
            if await request.is_disconnected(): break
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
                if task_id in progress_store: del progress_store[task_id]
                break
            await asyncio.sleep(0.2)
    return StreamingResponse(event_generator(), media_type="text/event-stream")

# 5. MICRO-TOOLS VE YASAL SAYFA YÖNLENDİRMELERİ - TÜRKÇE (TR - YEREL SEO)
@app.get("/araclar/otomatik-filigran", include_in_schema=False)
async def get_watermark_page_tr():
    return FileResponse("static/watermark.html") if os.path.exists("static/watermark.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/gelistirici-api", include_in_schema=False)
async def get_developer_page_tr():
    return FileResponse("static/developer.html") if os.path.exists("static/developer.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/araclar/toplu-islem", include_in_schema=False)
async def get_batch_page_tr():
    return FileResponse("static/batch.html") if os.path.exists("static/batch.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/araclar/ai-studyo", include_in_schema=False)
async def get_ai_studio_page_tr():
    return FileResponse("static/ai_studio.html") if os.path.exists("static/ai_studio.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/araclar/bulut-senkronizasyonu", include_in_schema=False)
async def get_cloud_sync_page_tr():
    return FileResponse("static/cloud_sync.html") if os.path.exists("static/cloud_sync.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/araclar/arka-plan-silici", include_in_schema=False)
async def get_bg_remove_page_tr():
    return FileResponse("static/bg_remove.html") if os.path.exists("static/bg_remove.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/araclar/video-kucultme", include_in_schema=False)
async def get_video_compress_page_tr():
    return FileResponse("static/video_compress.html") if os.path.exists("static/video_compress.html") else JSONResponse({"detail":"not found"}, 404)

# --- TR YASAL SAYFALAR (static/legal klasörüne güncellendi) ---
@app.get("/kosullar", include_in_schema=False)
async def get_terms_page_tr():
    return FileResponse("static/legal/terms.html") if os.path.exists("static/legal/terms.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/gizlilik-politikasi", include_in_schema=False)
async def get_privacy_page_tr():
    return FileResponse("static/legal/privacy.html") if os.path.exists("static/legal/privacy.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/iade-politikasi", include_in_schema=False)
async def get_refund_page_tr():
    return FileResponse("static/legal/refund.html") if os.path.exists("static/legal/refund.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/cerez-politikasi", include_in_schema=False)
async def get_cookies_page_tr():
    return FileResponse("static/legal/cookies.html") if os.path.exists("static/legal/cookies.html") else JSONResponse({"detail":"not found"}, 404)


# 5.1 MICRO-TOOLS VE YASAL SAYFA YÖNLENDİRMELERİ - İNGİLİZCE (EN - GLOBAL SEO)

@app.get("/en/", include_in_schema=False)
@app.get("/en", include_in_schema=False)
async def get_home_page_en():
    return FileResponse("static/index.html") if os.path.exists("static/index.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/tools/auto-watermark", include_in_schema=False)
async def get_watermark_page_en():
    return FileResponse("static/watermark.html") if os.path.exists("static/watermark.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/developer-api", include_in_schema=False)
async def get_developer_page_en():
    return FileResponse("static/developer.html") if os.path.exists("static/developer.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/tools/batch-processing", include_in_schema=False)
async def get_batch_page_en():
    return FileResponse("static/batch.html") if os.path.exists("static/batch.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/tools/ai-studio", include_in_schema=False)
async def get_ai_studio_page_en():
    return FileResponse("static/ai_studio.html") if os.path.exists("static/ai_studio.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/tools/cloud-sync", include_in_schema=False)
async def get_cloud_sync_page_en():
    return FileResponse("static/cloud_sync.html") if os.path.exists("static/cloud_sync.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/tools/background-remover", include_in_schema=False)
async def get_bg_remove_page_en():
    return FileResponse("static/bg_remove.html") if os.path.exists("static/bg_remove.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/tools/video-compressor", include_in_schema=False)
async def get_video_compress_page_en():
    return FileResponse("static/video_compress.html") if os.path.exists("static/video_compress.html") else JSONResponse({"detail":"not found"}, 404)

# --- EN YASAL SAYFALAR (static/legal klasörüne güncellendi) ---
@app.get("/en/terms", include_in_schema=False)
async def get_terms_page_en():
    return FileResponse("static/legal/terms.html") if os.path.exists("static/legal/terms.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/privacy-policy", include_in_schema=False)
async def get_privacy_page_en():
    return FileResponse("static/legal/privacy.html") if os.path.exists("static/legal/privacy.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/refund-policy", include_in_schema=False)
async def get_refund_page_en():
    return FileResponse("static/legal/refund.html") if os.path.exists("static/legal/refund.html") else JSONResponse({"detail":"not found"}, 404)

@app.get("/en/cookie-policy", include_in_schema=False)
async def get_cookies_page_en():
    return FileResponse("static/legal/cookies.html") if os.path.exists("static/legal/cookies.html") else JSONResponse({"detail":"not found"}, 404)


# 6. SEO DOSYALARI
@app.get("/robots.txt", include_in_schema=False)
async def get_robots():
    return FileResponse("static/robots.txt") if os.path.exists("static/robots.txt") else JSONResponse({"detail":"not found"}, 404)

@app.get("/sitemap.xml", include_in_schema=False)
async def get_sitemap():
    return FileResponse("static/sitemap.xml", media_type="application/xml") if os.path.exists("static/sitemap.xml") else JSONResponse({"detail":"not found"}, 404)

# 7. STATİK DOSYALAR (EN SON)
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")
app.mount("/temp_pdf", StaticFiles(directory="static/temp_pdf"), name="temp_pdf")
app.mount("/", StaticFiles(directory="static", html=True), name="static")