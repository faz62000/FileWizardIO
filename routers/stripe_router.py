"""
FileWizardIO — Stripe Ödeme Entegrasyonu
ForgeLogic LLC adına ödeme toplama ve webhook işleme
"""

import os
import stripe
from fastapi import APIRouter, HTTPException, Request, Depends, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
import models

router = APIRouter()

# Stripe key'leri environment variable'dan al
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")
PRICE_ID_PRO = os.environ.get("STRIPE_PRICE_ID_PRO")  # Stripe Dashboard'dan alınacak


# ── ÖDEME AŞAMASI 1: Checkout Session Oluştur ────────────────────────────────
@router.post("/create-checkout-session")
async def create_checkout_session(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Kullanıcıyı Stripe ödeme sayfasına yönlendir.
    Ödeme tamamlandığında Stripe webhook'u tetikler.
    """
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe yapılandırılmamış")

    try:
        # Mevcut Stripe customer varsa onu kullan, yoksa yeni oluştur
        customer_id = getattr(current_user, "stripe_customer_id", None)
        if not customer_id:
            customer = stripe.Customer.create(
                email=current_user.email,
                name=current_user.email,
                metadata={"user_id": str(current_user.id)}
            )
            customer_id = customer.id
            current_user.stripe_customer_id = customer_id
            db.commit()

        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[{"price": PRICE_ID_PRO, "quantity": 1}],
            mode="subscription",
            success_url="https://filewizardio.com/?payment=success",
            cancel_url="https://filewizardio.com/?payment=cancelled",
            metadata={"user_id": str(current_user.id)}
        )
        return {"checkout_url": session.url}

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e.user_message))


# ── ÖDEME AŞAMASI 2: Webhook — Stripe'tan gelen olayları işle ────────────────
@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Stripe'ın sunucumuzdan doğrudan çağırdığı endpoint.
    Ödeme onayı, iptal, yenileme gibi olayları buradan alırız.
    İmza doğrulaması ile sahte istekler reddedilir.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Webhook secret yapılandırılmamış")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Geçersiz webhook imzası")

    event_type = event["type"]
    data = event["data"]["object"]

    # Ödeme tamamlandı → kullanıcıyı PRO yap
    if event_type == "checkout.session.completed":
        user_id = data.get("metadata", {}).get("user_id")
        if user_id:
            user = db.query(models.User).filter(models.User.id == int(user_id)).first()
            if user:
                user.is_premium = True
                user.stripe_customer_id = data.get("customer")
                user.stripe_subscription_id = data.get("subscription")
                db.commit()

    # Abonelik yenilendi → PRO durumunu koru
    elif event_type == "invoice.payment_succeeded":
        subscription_id = data.get("subscription")
        if subscription_id:
            user = db.query(models.User).filter(
                models.User.stripe_subscription_id == subscription_id
            ).first()
            if user:
                user.is_premium = True
                db.commit()

    # Ödeme başarısız / abonelik iptal edildi → PRO kaldır
    elif event_type in ("invoice.payment_failed", "customer.subscription.deleted"):
        subscription_id = data.get("id") if event_type == "customer.subscription.deleted" else data.get("subscription")
        if subscription_id:
            user = db.query(models.User).filter(
                models.User.stripe_subscription_id == subscription_id
            ).first()
            if user:
                user.is_premium = False
                db.commit()

    return JSONResponse({"status": "ok"})


# ── İPTAL: Kullanıcı kendi aboneliğini iptal etsin ───────────────────────────
@router.post("/cancel-subscription")
async def cancel_subscription(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.stripe_subscription_id:
        raise HTTPException(status_code=400, detail="Aktif abonelik bulunamadı")

    try:
        # Dönem sonunda iptal et (anında kesmez)
        stripe.Subscription.modify(
            current_user.stripe_subscription_id,
            cancel_at_period_end=True
        )
        return {"message": "Aboneliğiniz dönem sonunda iptal edilecek"}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e.user_message))


# ── DURUM: Abonelik bilgisini getir ──────────────────────────────────────────
@router.get("/subscription-status")
async def subscription_status(current_user: models.User = Depends(get_current_user)):
    return {
        "is_premium": current_user.is_premium,
        "subscription_id": getattr(current_user, "stripe_subscription_id", None)
    }
