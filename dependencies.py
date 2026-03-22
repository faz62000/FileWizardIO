from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database import get_db
import models
from security import SECRET_KEY, ALGORITHM

# FastAPI'nin standart token okuma mekanizması (Ön yüzdeki giriş formunu işaret eder)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Kullanıcının gönderdiği JWT Token'ı çözer ve kim olduğunu bulur."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Kimlik doğrulama başarısız oldu. Lütfen tekrar giriş yapın.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Şifreli pasaportu (Token) açıyoruz
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # E-posta bulundu, veritabanından kullanıcıyı getir
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def get_premium_user(current_user: models.User = Depends(get_current_user)):
    """Kullanıcının PRO (Premium) yetkisi olup olmadığını kontrol eder."""
    if not current_user.is_premium:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu premium aracı kullanmak için PRO üyeliğe sahip olmalısınız. Lütfen aboneliğinizi yükseltin."
        )
    return current_user