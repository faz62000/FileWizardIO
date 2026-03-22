from fastapi import APIRouter, Header, HTTPException, Form
from fastapi.responses import JSONResponse
from services.api_auth_service import generate_new_api_key, validate_and_consume_quota, get_api_key_stats
import asyncio

# Mevcut güçlü video servisimizi dışa açmak için içe aktarıyoruz
from services.video_service import get_media_info_logic

router = APIRouter()

# --- 1. PORTAL İŞLEMLERİ (Ön yüz için) ---

@router.post("/generate-key")
async def create_api_key(email: str = Form(...), plan: str = Form("free")):
    """Geliştirici portalından gelen yeni anahtar taleplerini işler."""
    try:
        if not email or "@" not in email:
            return JSONResponse(status_code=400, content={"error": "Lütfen geçerli bir e-posta adresi giriniz."})
            
        api_key, quota = generate_new_api_key(email, plan)
        return JSONResponse({
            "success": True, 
            "message": "API Anahtarınız başarıyla oluşturuldu.",
            "api_key": api_key,
            "monthly_quota": quota
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/stats")
async def get_stats(api_key: str = Form(...)):
    """Geliştiricilerin arayüz üzerinden kotalarını sorgulamasını sağlar."""
    stats = get_api_key_stats(api_key)
    if not stats:
        return JSONResponse(status_code=404, content={"error": "API Anahtarı sistemde bulunamadı."})
        
    return JSONResponse({
        "success": True,
        "email": stats["email"],
        "plan": stats["plan"],
        "usage": stats["usage"],
        "quota_limit": stats["quota_limit"],
        "remaining": stats["quota_limit"] - stats["usage"],
        "status": stats["status"]
    })

# --- 2. DIŞA AÇILAN HİZMETLER (Diğer geliştiriciler için) ---

@router.post("/v1/video-info")
async def external_video_info(url: str = Form(...), x_api_key: str = Header(None)):
    """
    Bu uç nokta, diğer geliştiricilerin kendi projelerinde bizim motorumuzu 
    kullanarak video bilgisi çekmelerini sağlar. (Kota harcar)
    """
    # Güvenlik ve Kota Kontrolü
    if not x_api_key:
        return JSONResponse(status_code=401, content={"error": "Yetkilendirme reddedildi. 'X-API-Key' başlığı (header) zorunludur."})
        
    is_valid, message = validate_and_consume_quota(x_api_key)
    if not is_valid:
        return JSONResponse(status_code=403, content={"error": message})
        
    # Arka plandaki mevcut mantığı kullanarak işlemi gerçekleştir
    try:
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(None, get_media_info_logic, url)
        return JSONResponse({
            "success": True,
            "data": data,
            "developer_message": "İşlem başarılı. Aylık kotanızdan 1 kredi düşüldü."
        })
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})