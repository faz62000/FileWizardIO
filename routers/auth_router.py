from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import get_db
import models
from security import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter()

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