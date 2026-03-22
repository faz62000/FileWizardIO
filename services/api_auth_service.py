import os
import json
import secrets
import time

API_KEYS_FILE = "api_keys.json"

def _load_keys():
    """Kayıtlı API anahtarlarını JSON dosyasından okur."""
    if not os.path.exists(API_KEYS_FILE):
        return {}
    try:
        with open(API_KEYS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_keys(keys_data):
    """API anahtarlarını ve kota durumlarını JSON dosyasına kaydeder."""
    with open(API_KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(keys_data, f, indent=4)

def generate_new_api_key(developer_email: str, plan: str = "free"):
    """Yeni bir geliştirici hesabı ve API anahtarı oluşturur."""
    keys_data = _load_keys()
    
    # Benzersiz ve güvenli API anahtarı oluştur (Örn: fw_live_8f72a...)
    new_key = f"fw_live_{secrets.token_hex(16)}"
    
    # Planlara göre aylık sorgu kotası belirle
    quota = 5000 if plan == "pro" else 100
    
    keys_data[new_key] = {
        "email": developer_email,
        "plan": plan,
        "quota_limit": quota,
        "usage": 0,
        "created_at": time.time(),
        "status": "active"
    }
    
    _save_keys(keys_data)
    return new_key, quota

def validate_and_consume_quota(api_key: str):
    """Gelen isteğin API anahtarını doğrular ve kotadan düşer."""
    keys_data = _load_keys()
    
    if api_key not in keys_data:
        return False, "Geçersiz API Anahtarı. Lütfen Geliştirici Portalı'ndan yeni bir anahtar alın."
        
    key_info = keys_data[api_key]
    
    if key_info.get("status") != "active":
        return False, "Bu API Anahtarı güvenlik nedeniyle askıya alınmıştır."
        
    if key_info.get("usage", 0) >= key_info.get("quota_limit", 0):
        return False, "Aylık kota sınırınıza ulaştınız. Lütfen Pro plana geçiş yapın."
        
    # Kotayı 1 artır ve yeni durumu diske kaydet
    key_info["usage"] = key_info.get("usage", 0) + 1
    keys_data[api_key] = key_info
    _save_keys(keys_data)
    
    return True, "Başarılı"

def get_api_key_stats(api_key: str):
    """Geliştiricinin kalan kotasını ve istatistiklerini döndürür."""
    keys_data = _load_keys()
    if api_key in keys_data:
        return keys_data[api_key]
    return None