from sqlalchemy import Boolean, Column, Integer, String, DateTime
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    # VIP / PREMIUM DURUMU
    is_premium = Column(Boolean, default=False)
    
    # LEMONSQUEEZY ENTEGRASYON VERİLERİ
    customer_id = Column(String, nullable=True, index=True)        # LemonSqueezy Müşteri ID
    subscription_id = Column(String, nullable=True, index=True)    # Abonelik ID
    subscription_status = Column(String, nullable=True)            # 'active', 'past_due', 'canceled' vb.
    premium_valid_until = Column(DateTime, nullable=True)          # Abonelik bitiş tarihi
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)