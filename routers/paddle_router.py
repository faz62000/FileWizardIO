from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db

# HATANIN ÇÖZÜMÜ: User modeli database'den değil models dosyasından çağırıldı
from models import User 
import os
import json
import hmac
import hashlib

router = APIRouter()

# Paddle Billing Webhook Secret Key
PADDLE_WEBHOOK_SECRET = os.getenv("PADDLE_WEBHOOK_SECRET", "forgelogic_paddle_secret_key_here")

@router.post("/webhook")
async def paddle_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    signature_header = request.headers.get("Paddle-Signature")

    if not signature_header:
        raise HTTPException(status_code=400, detail="Eksik imza (Missing Paddle-Signature)")

    # Paddle Signature doğrulama işlemi (ts=...,h1=...)
    try:
        parts = signature_header.split(";")
        ts = parts[0].split("=")[1]
        h1 = parts[1].split("=")[1]
        
        signed_payload = f"{ts}:{payload.decode('utf-8')}"
        computed_signature = hmac.new(
            PADDLE_WEBHOOK_SECRET.encode('utf-8'),
            signed_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        if hmac.compare_digest(computed_signature, h1) is False:
             raise HTTPException(status_code=403, detail="Geçersiz imza (Invalid signature)")
             
    except Exception as e:
        raise HTTPException(status_code=403, detail="İmza doğrulama hatası (Signature validation error)")

    try:
        event_data = json.loads(payload)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Geçersiz JSON (Invalid JSON)")

    event_type = event_data.get("event_type")
    data = event_data.get("data", {})

    # ForgeLogic LLC SaaS Abonelik Yönetimi İşlemleri
    if event_type in ["subscription.created", "subscription.updated"]:
        custom_data = data.get("custom_data", {})
        user_id = custom_data.get("user_id")
        status = data.get("status")

        if user_id:
            # UYUM DÜZELTMESİ: models.py içindeki id (Integer) olduğu için int(user_id) yapıldı
            user = db.query(User).filter(User.id == int(user_id)).first()
            if user:
                if status in ["active", "trialing"]:
                    # UYUM DÜZELTMESİ: models.py içindeki is_premium değeri kullanıldı
                    user.is_premium = True
                    user.subscription_id = data.get("id")
                    user.subscription_status = status
                else:
                    user.is_premium = False
                    user.subscription_status = status
                db.commit()

    elif event_type == "subscription.canceled":
        custom_data = data.get("custom_data", {})
        user_id = custom_data.get("user_id")
        
        if user_id:
            user = db.query(User).filter(User.id == int(user_id)).first()
            if user:
                user.is_premium = False
                user.subscription_status = "canceled"
                db.commit()

    return {"status": "success", "message": "Webhook başarıyla işlendi (Webhook processed successfully)"}

@router.get("/checkout-info")
async def get_checkout_info():
    return {
        "company_name": "ForgeLogic LLC",
        "vendor_id": os.getenv("PADDLE_VENDOR_ID", "your_paddle_vendor_id"),
        "client_token": os.getenv("PADDLE_CLIENT_TOKEN", "your_paddle_client_token"),
        "environment": os.getenv("PADDLE_ENVIRONMENT", "sandbox") # production veya sandbox
    }