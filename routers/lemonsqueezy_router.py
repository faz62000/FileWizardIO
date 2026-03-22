from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import hmac
import hashlib
import os
import json
from datetime import datetime

router = APIRouter()

# LemonSqueezy'den gelecek Webhook İmza Şifresi 
# (Bunu LemonSqueezy panelinden oluşturup ileride DigitalOcean Environment Variables kısmına ekleyeceğiz)
LEMONSQUEEZY_WEBHOOK_SECRET = os.environ.get("LEMONSQUEEZY_WEBHOOK_SECRET", "forgelogic-test-webhook-sifresi")

@router.post("/webhook")
async def lemonsqueezy_webhook(request: Request, db: Session = Depends(get_db)):
    """LemonSqueezy'den gelen ödeme başarılı/başarısız bildirimlerini dinler."""
    
    # 1. Gelen isteğin içeriğini ve şifreli imzasını al
    payload = await request.body()
    signature = request.headers.get("X-Signature")

    if not signature:
        raise HTTPException(status_code=400, detail="Güvenlik imzası bulunamadı.")

    # 2. Güvenlik Kontrolü: Bu istek gerçekten LemonSqueezy'den mi geldi? (Hacker koruması)
    mac = hmac.new(LEMONSQUEEZY_WEBHOOK_SECRET.encode('utf-8'), payload, hashlib.sha256)
    expected_signature = mac.hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=400, detail="Geçersiz imza. Kaynak doğrulanamadı.")

    # 3. Gelen JSON verisini oku
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Geçersiz JSON formatı.")

    # 4. Hangi olayın (event) gerçekleştiğini bul
    event_name = data.get("meta", {}).get("event_name")
    custom_data = data.get("meta", {}).get("custom_data", {})
    
    # Ödemeyi yapan müşterinin e-postası
    user_email = custom_data.get("email") or data.get("data", {}).get("attributes", {}).get("user_email")

    if not user_email:
        # E-posta yoksa bile işlemi başarılı sayıp geçiyoruz ki LemonSqueezy hata algılayıp sürekli tekrar denemesin
        return {"status": "success", "message": "Kullanıcı e-postası bulunamadı, webhook atlandı."}

    # 5. Veritabanından o e-postaya sahip kullanıcıyı bul
    user = db.query(models.User).filter(models.User.email == user_email).first()
    
    if not user:
        return {"status": "success", "message": "Ödeme yapan kullanıcı sistemde bulunamadı."}

    # 6. Senaryolar: Ödeme başarılı mı, iptal mi edildi?
    if event_name in ["subscription_created", "subscription_updated"]:
        attributes = data.get("data", {}).get("attributes", {})
        user.subscription_id = str(data.get("data", {}).get("id"))
        user.customer_id = str(attributes.get("customer_id"))
        user.subscription_status = attributes.get("status")
        
        # Eğer ödeme durumu "active" (aktif) ise kullanıcıya hemen PRO yetkisi ver
        if attributes.get("status") == "active":
            user.is_premium = True
            
            # Yenilenme (Bitiş) tarihini veritabanına yaz
            renews_at = attributes.get("renews_at")
            if renews_at:
                # ISO 8601 tarih formatını Python formatına çevir
                user.premium_valid_until = datetime.fromisoformat(renews_at.replace("Z", "+00:00"))
                
    elif event_name in ["subscription_cancelled", "subscription_expired"]:
        # Kullanıcı aboneliği iptal ettiyse veya karttan para çekilemediyse PRO yetkisini geri al
        user.is_premium = False
        user.subscription_status = "canceled"

    # 7. Tüm değişiklikleri veritabanına kaydet
    db.commit()

    return {"status": "success", "message": "Ödeme durumu başarıyla güncellendi."}