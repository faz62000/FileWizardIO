import io
import zipfile
from PIL import Image
import uuid

def process_batch_logic(files_data, target_format="jpeg", resize_width=None):
    """
    Onlarca dosyayı aynı anda işleyip ZIP formatında paketleyen yüksek performanslı motor.
    files_data: [(dosya_adi, dosya_byte_verisi), ...] şeklinde liste alır.
    """
    zip_buffer = io.BytesIO()
    
    # ZIP dosyasını RAM üzerinde (ZIP_DEFLATED ile sıkıştırarak) oluştur
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_name, file_bytes in files_data:
            try:
                # Görseli baytlardan oku
                img = Image.open(io.BytesIO(file_bytes))
                
                # Format Dönüşümü İçin Şeffaflık Kontrolü (Örn: PNG'den JPG'ye)
                if img.mode != 'RGB' and target_format.lower() in ['jpeg', 'jpg']:
                    if img.mode in ('RGBA', 'LA'):
                        bg = Image.new('RGB', img.size, (255, 255, 255))
                        bg.paste(img, mask=img.split()[-1])
                        img = bg
                    else:
                        img = img.convert('RGB')
                
                # Akıllı Yeniden Boyutlandırma (Oranı koruyarak)
                if resize_width and resize_width > 0:
                    w_percent = (resize_width / float(img.size[0]))
                    h_size = int((float(img.size[1]) * float(w_percent)))
                    img = img.resize((resize_width, h_size), Image.Resampling.LANCZOS)
                
                # İşlenmiş görseli geçici bir belleğe kaydet
                img_buffer = io.BytesIO()
                fmt = target_format.upper().replace("JPG", "JPEG")
                img.save(img_buffer, format=fmt, quality=90, optimize=True)
                
                # Yeni dosya adını oluştur ve ZIP içerisine yaz
                base_name = file_name.rsplit('.', 1)[0]
                new_name = f"{base_name}_fw.{target_format.lower()}"
                
                zip_file.writestr(new_name, img_buffer.getvalue())
                
            except Exception as e:
                # Bozuk dosya gelirse sistemi çökertme, pas geç
                print(f"Toplu işlem sırasında '{file_name}' atlandı: {e}")
                continue
    
    # ZIP dosyasını başa sar ve indirmeye hazır hale getir
    zip_buffer.seek(0)
    final_filename = f"FileWizard_Batch_{uuid.uuid4().hex[:6]}.zip"
    
    return zip_buffer, final_filename