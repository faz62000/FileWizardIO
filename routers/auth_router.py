from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import get_db
import models
from security import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
import os
import secrets
from dotenv import load_dotenv

from fastapi_sso.sso.google import GoogleSSO
from fastapi_sso.sso.facebook import FacebookSSO
from fastapi_sso.sso.twitter import TwitterSSO
from dependencies import get_current_user

router = APIRouter()

load_dotenv()

HOST_URL = os.environ.get("HOST_URL", "https://filewizardio.com")

google_sso = GoogleSSO(
    client_id=os.environ.get("GOOGLE_CLIENT_ID", "your-google-id"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", "your-google-secret"),
    redirect_uri=f"{HOST_URL}/api/auth/google/callback",
    allow_insecure_http=True 
)

facebook_sso = FacebookSSO(
    client_id=os.environ.get("FACEBOOK_CLIENT_ID", "your-facebook-id"),
    client_secret=os.environ.get("FACEBOOK_CLIENT_SECRET", "your-facebook-secret"),
    redirect_uri=f"{HOST_URL}/api/auth/facebook/callback",
    allow_insecure_http=True
)

twitter_sso = TwitterSSO(
    client_id=os.environ.get("TWITTER_CLIENT_ID", "your-twitter-id"),
    client_secret=os.environ.get("TWITTER_CLIENT_SECRET", "your-twitter-secret"),
    redirect_uri=f"{HOST_URL}/api/auth/x/callback",
    allow_insecure_http=True
)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Bu e-posta adresi sistemde zaten kayıtlı.")
    
    hashed_password = get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="E-posta veya şifre hatalı.")
    
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="E-posta veya şifre hatalı.")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# MİLYON DOLARLIK SESSİZ YENİLEME (SILENT REFRESH) UÇ NOKTASI
@router.post("/refresh", response_model=Token)
def refresh_token(current_user: models.User = Depends(get_current_user)):
    """Aktif kullanıcının token ömrünü, işlemi bozmadan 15 dakika daha uzatır."""
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": new_access_token, "token_type": "bearer"}

async def process_sso_login(email: str, db: Session):
    if not email:
        raise HTTPException(status_code=400, detail="E-posta bilgisi alınamadı.")

    db_user = db.query(models.User).filter(models.User.email == email).first()

    if not db_user:
        random_password = secrets.token_urlsafe(32)
        hashed_password = get_password_hash(random_password)
        db_user = models.User(email=email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return access_token

def generate_sso_html_response(token: str):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Giriş Başarılı</title></head>
    <body>
        <script>
            localStorage.setItem('fw_token', '{token}');
            window.location.href = '/';
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.get("/google/login")
async def google_login():
    return await google_sso.get_login_redirect()

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    sso_user = await google_sso.verify_and_process(request)
    token = await process_sso_login(sso_user.email, db)
    return generate_sso_html_response(token)

@router.get("/facebook/login")
async def facebook_login():
    return await facebook_sso.get_login_redirect()

@router.get("/facebook/callback")
async def facebook_callback(request: Request, db: Session = Depends(get_db)):
    sso_user = await facebook_sso.verify_and_process(request)
    token = await process_sso_login(sso_user.email, db)
    return generate_sso_html_response(token)

@router.get("/x/login")
async def twitter_login():
    return await twitter_sso.get_login_redirect()

@router.get("/x/callback")
async def twitter_callback(request: Request, db: Session = Depends(get_db)):
    sso_user = await twitter_sso.verify_and_process(request)
    token = await process_sso_login(sso_user.email, db)
    return generate_sso_html_response(token)