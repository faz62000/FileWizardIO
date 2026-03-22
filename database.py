from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Şimdilik SQLite kullanıyoruz. Sunucuya ekstra maliyet bindirmez.
SQLALCHEMY_DATABASE_URL = "sqlite:///./filewizard.db"

# connect_args SQLite'ın çoklu thread (iş parçacığı) ile çalışmasına izin verir
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()