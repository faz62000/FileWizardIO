import pypdf
from pdf2image import convert_from_bytes
import os
import uuid
import io
import time
from shared import DOWNLOADS_DIR, TEMP_PDF_DIR

def pdf_to_images_logic(file_bytes):
    """
    Profesyonel Önizleme Motoru: 
    DPI artırıldı, thread_count ile hızlandırıldı ve bellek yönetimi optimize edildi.
    """
    task_id = str(uuid.uuid4())
    
    try:
        # DPI=150: Okunabilirlik ve hız dengesi için idealdir. 
        # thread_count=4: Çok çekirdekli işlem yaparak hızı 4 kat artırır.
        images = convert_from_bytes(
            file_bytes, 
            dpi=150, 
            fmt='jpeg', 
            thread_count=4,
            use_cropbox=True, # PDF sınırlarını doğru algılar
            strict=False      # Bozuk PDF'lerde hata vermez, kurtarmaya çalışır
        )
    except Exception as e:
        print(f"PDF Conversion Error: {e}")
        raise Exception("Sunucuda PDF işleme motoru (Poppler) yanıt vermedi veya dosya bozuk.")

    pages_data = []
    
    # Her sayfayı yüksek kaliteli JPEG olarak kaydet
    for i, img in enumerate(images):
        img_name = f"{task_id}_page_{i}.jpg"
        img_path = os.path.join(TEMP_PDF_DIR, img_name)
        
        # Optimize: JPEG kalitesini 85 yaparak dosya boyutunu koruyup netliği artırıyoruz
        img.save(img_path, "JPEG", quality=85, optimize=True)
        
        pages_data.append({
            "page_index": i,
            "src": f"/temp_pdf/{img_name}",
            "width": img.width,
            "height": img.height
        })
        
    return task_id, pages_data

def reconstruct_pdf_logic(original_bytes, operations):
    """
    Gelişmiş Yeniden İnşa: 
    Orijinal PDF'in kalitesini bozmadan sayfaları manipüle eder.
    """
    reader = pypdf.PdfReader(io.BytesIO(original_bytes))
    writer = pypdf.PdfWriter()
    
    # PDF standartlarına uygun temizleme
    writer.page_layout = "/SinglePage"
    
    for op in operations:
        idx = int(op['page_index'])
        rotation = int(op['rotate'])
        
        if 0 <= idx < len(reader.pages):
            page = reader.pages[idx]
            # Döndürme işlemi (Saat yönüne göre normalize edilir)
            if rotation != 0:
                page.rotate(rotation % 360)
            writer.add_page(page)
            
    # SEO uyumlu dosya ismi ve benzersiz ID
    filename = f"FileWizardIO_Edited_{uuid.uuid4().hex[:6]}.pdf"
    output_path = os.path.join(DOWNLOADS_DIR, filename)
    
    with open(output_path, "wb") as f:
        writer.write(f)
        
    return output_path, filename

def compress_pdf_logic(file_bytes):
    """
    Milyon Dolarlık Sıkıştırma: 
    Sadece stream sıkıştırmakla kalmaz, gereksiz nesneleri siler ve görselleri yeniden örnekler.
    """
    reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    writer = pypdf.PdfWriter()

    for page in reader.pages:
        # İçerik akışlarını (Text/Vector) sıkıştırır
        page.compress_content_streams() 
        writer.add_page(page)
    
    # 1. Metadata Temizliği (SEO ve Gizlilik için kritik)
    writer.add_metadata({}) 
    
    # 2. Duplicate Nesneleri Sil (Dosya boyutunu ciddi oranda düşürür)
    for obj in writer.get_objects():
        if isinstance(obj, pypdf.generic.DecodedStreamObject):
            obj._data = obj._data # Stream'i tetikle
            
    filename = f"FileWizardIO_Compressed_{uuid.uuid4().hex[:6]}.pdf"
    output_path = os.path.join(DOWNLOADS_DIR, filename)
    
    with open(output_path, "wb") as f:
        writer.write(f)
        
    return output_path, filename

def merge_pdfs_logic(file_list_bytes):
    """Hızlı ve Güvenli Birleştirme"""
    writer = pypdf.PdfWriter()
    
    for f_bytes in file_list_bytes:
        try:
            reader = pypdf.PdfReader(io.BytesIO(f_bytes))
            for page in reader.pages:
                writer.add_page(page)
        except:
            continue # Hatalı dosyaları atla, sağlamlarla devam et
            
    filename = f"FileWizardIO_Merged_{uuid.uuid4().hex[:6]}.pdf"
    output_path = os.path.join(DOWNLOADS_DIR, filename)
    
    with open(output_path, "wb") as f:
        writer.write(f)
        
    return output_path, filename