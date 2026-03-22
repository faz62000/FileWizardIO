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

# --- SAAS DÖNÜŞÜMÜ İÇİN EKLENEN SSO KÜTÜPHANELERİ ---
from fastapi_sso.sso.google import GoogleSSO
from fastapi_sso.sso.facebook import FacebookSSO
from fastapi_sso.sso.twitter import TwitterSSO
# ----------------------------------------------------

router = APIRouter()

# --- SSO (SOSYAL GİRİŞ) YAPILANDIRMASI ---
# DigitalOcean'da çalışırken HOST_URL kendi alan adınız olmalıdır (örn: https://filewizardio.com)
HOST_URL = os.environ.get("HOST_URL", "http://localhost:8000")

google_sso = GoogleSSO(
    client_id=os.environ.get("GOOGLE_CLIENT_ID", "your-google-id"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", "your-google-secret"),
    redirect_uri=f"{HOST_URL}/api/auth/google/callback",
    allow_insecure_http=True # Geliştirme (Localhost) aşamasında HTTP için izin veriyoruz
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
# -------------------------

# --- Pydantic Şemaları (Ön yüzden gelen veriyi doğrulamak için) ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
# -----------------------------------------------------------------

@router.post("/register", response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Yeni kullanıcı kaydı oluşturur."""
    # E-posta daha önce kayıtlı mı diye veritabanını kontrol et
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Bu e-posta adresi sistemde zaten kayıtlı.")
    
    # Yeni kullanıcıyı oluştur ve şifresini kriptolayarak veritabanına kaydet
    hashed_password = get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Kullanıcı kayıt olur olmaz giriş yapmış saysın diye anında token üretip ver
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """Mevcut kullanıcının sisteme giriş yapmasını sağlar."""
    # Kullanıcıyı veritabanında e-postasıyla bul
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="E-posta veya şifre hatalı.")
    
    # Bulunan kullanıcının şifresini doğrula
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="E-posta veya şifre hatalı.")
    
    # Her şey doğruysa giriş başarılı, yepyeni bir token üret
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- SOSYAL GİRİŞ (SSO) YARDIMCI FONKSİYONLARI ---
async def process_sso_login(email: str, db: Session):
    """Sosyal ağdan gelen e-posta ile kullanıcıyı bulur veya otomatik kayıt eder."""
    if not email:
        raise HTTPException(status_code=400, detail="E-posta bilgisi alınamadı.")

    db_user = db.query(models.User).filter(models.User.email == email).first()

    # Eğer kullanıcı sistemde yoksa, arka planda otomatik olarak kayıt et
    if not db_user:
        # Rastgele, kırılamaz bir şifre oluştur (Kullanıcı zaten Google/X ile girecek, şifreyi bilmesine gerek yok)
        random_password = secrets.token_urlsafe(32)
        hashed_password = get_password_hash(random_password)
        db_user = models.User(email=email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    # Giriş yapması için token (pasaport) üret
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return access_token

def generate_sso_html_response(token: str):
    """Token'ı tarayıcının hafızasına (localStorage) yazıp anasayfaya yönlendiren sihirli HTML."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Giriş Başarılı</title></head>
    <body>
        <script>
            // Token'ı tarayıcıya kaydet
            localStorage.setItem('fw_token', '{token}');
            // Kullanıcıyı anasayfaya geri gönder
            window.location.href = '/';
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# --- GOOGLE ROTALARI ---
@router.get("/google/login")
async def google_login():
    """Kullanıcıyı Google'ın giriş sayfasına yönlendirir."""
    return await google_sso.get_login_redirect()

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Google'dan dönen veriyi alır ve sisteme giriş yaptırır."""
    sso_user = await google_sso.verify_and_process(request)
    token = await process_sso_login(sso_user.email, db)
    return generate_sso_html_response(token)


# --- FACEBOOK ROTALARI ---
@router.get("/facebook/login")
async def facebook_login():
    """Kullanıcıyı Facebook'un giriş sayfasına yönlendirir."""
    return await facebook_sso.get_login_redirect()

@router.get("/facebook/callback")
async def facebook_callback(request: Request, db: Session = Depends(get_db)):
    """Facebook'tan dönen veriyi alır ve sisteme giriş yaptırır."""
    sso_user = await facebook_sso.verify_and_process(request)
    token = await process_sso_login(sso_user.email, db)
    return generate_sso_html_response(token)


# --- X (TWITTER) ROTALARI ---
@router.get("/x/login")
async def twitter_login():
    """Kullanıcıyı X (Twitter) giriş sayfasına yönlendirir."""
    return await twitter_sso.get_login_redirect()

@router.get("/x/callback")
async def twitter_callback(request: Request, db: Session = Depends(get_db)):
    """X'ten dönen veriyi alır ve sisteme giriş yaptırır."""
    sso_user = await twitter_sso.verify_and_process(request)
    token = await process_sso_login(sso_user.email, db)
    return generate_sso_html_response(token)