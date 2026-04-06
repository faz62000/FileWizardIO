from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

# Güvenlik Ayarları
# Production ortamında (DigitalOcean'da) bu şifre Environment Variables'dan çekilecek. 
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "forgelogic-super-gizli-anahtar-778899")
ALGORITHM = "HS256"

# MİLYON DOLARLIK GÜVENLİK DOKUNUŞU: 
# Token ömrü 1 hafta yerine 15 dakikaya düşürüldü. 
# Kullanıcı aktifse ön yüzdeki JavaScript bu süreyi sessizce 5 dakikada bir uzatacak.
ACCESS_TOKEN_EXPIRE_MINUTES = 15  

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Kullanıcının girdiği şifre ile veritabanındaki kriptolu şifreyi karşılaştırır."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Yeni kayıt olan kullanıcının şifresini geri döndürülemez şekilde kriptolar."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Giriş yapan kullanıcıya dijital bir pasaport (JWT) üretir."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt