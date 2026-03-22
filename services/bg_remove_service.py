import io
from PIL import Image
from rembg import remove
import uuid

def remove_background_logic(file_bytes):
    """
    Yapay zeka (U2-Net) kullanarak fotoğrafların arka planını saç teline kadar 
    kusursuzca silen milyon dolarlık motor.
    """
    # Görseli byte akışından oku
    input_img = Image.open(io.BytesIO(file_bytes))
    
    # rembg kütüphanesi ile yapay zeka modelini çalıştırıp arka planı sil
    # Çıktı her zaman şeffaf bir PNG dosyasıdır
    output_img = remove(input_img)
    
    # İşlenmiş görseli belleğe (RAM'e) kaydet
    output_io = io.BytesIO()
    output_img.save(output_io, format="PNG", optimize=True)
    output_io.seek(0)
    
    filename = f"FileWizard_MagicBG_{uuid.uuid4().hex[:6]}.png"
    return output_io, filename