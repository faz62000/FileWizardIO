import requests
import os

def upload_to_dropbox_logic(file_bytes, filename, access_token):
    """
    Dosyaları doğrudan kullanıcının Dropbox hesabına yükleyen yüksek hızlı bulut motoru.
    (Sistemde yüklü olan 'requests' kütüphanesi kullanılarak harici bağımlılık yaratılmamıştır.)
    """
    # Dropbox API v2 yükleme uç noktası
    url = "https://content.dropboxapi.com/2/files/upload"
    
    # Dropbox'ın beklediği özel başlıklar (Headers)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Dropbox-API-Arg": f'{{"autoname":true,"mode":"add","path":"/{filename}","strict_conflict":false}}',
        "Content-Type": "application/octet-stream",
    }
    
    # Dosyayı byte akışı olarak doğrudan buluta gönder (RAM dostu)
    response = requests.post(url, headers=headers, data=file_bytes)
    
    if response.status_code == 200:
        # Başarılı yükleme yanıtı
        result = response.json()
        return result.get("name", filename), result.get("size", 0)
    else:
        # API'den gelen detaylı hata mesajını yakala
        error_msg = response.text
        try:
            error_json = response.json()
            error_msg = error_json.get("error_summary", response.text)
        except Exception:
            pass
        raise Exception(f"Bulut Aktarım Hatası: {error_msg}")