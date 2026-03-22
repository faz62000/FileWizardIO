from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from io import BytesIO

def apply_preset(img, preset_name):
    """Instagram tarzı hızlı filtreler"""
    if preset_name == 'grayscale':
        return ImageOps.grayscale(img).convert("RGB")
    elif preset_name == 'sepia':
        # Sepia Matrix
        sepia = img.convert("L")
        return ImageOps.colorize(sepia, "#704214", "#C0C0C0")
    elif preset_name == 'vintage':
        img = ImageEnhance.Color(img).enhance(0.5)
        img = ImageEnhance.Contrast(img).enhance(1.2)
        return img
    elif preset_name == 'blur':
        return img.filter(ImageFilter.GaussianBlur(2))
    return img

def process_image_logic(file_stream, crop_data, filter_data, resize_data, bg_data, target_format):
    img = Image.open(file_stream)
    img = ImageOps.exif_transpose(img) # Mobil foto düzeltme

    # 1. HIZ İÇİN ÖNCE KIRP (GÜVENLİ HALE GETİRİLDİ)
    try:
        if all(k in crop_data and crop_data[k] is not None for k in ['x', 'y', 'width', 'height']):
            # Koordinatları yuvarlayarak tam sayıya çevir
            x = int(round(float(crop_data['x'])))
            y = int(round(float(crop_data['y'])))
            w = int(round(float(crop_data['width'])))
            h = int(round(float(crop_data['height'])))
            
            img_w, img_h = img.size
            
            # Sınır Güvenliği: Koordinatların resim sınırları içinde kalmasını sağla
            x = max(0, min(x, img_w - 1))
            y = max(0, min(y, img_h - 1))
            w = max(1, min(w, img_w - x))
            h = max(1, min(h, img_h - y))
            
            if w > 0 and h > 0:
                img = img.crop((x, y, x + w, y + h))
    except Exception as e:
        print(f"Kırpma Hatası Pas Geçildi: {e}")

    # 2. BOYUTLANDIR
    if resize_data.get('mode') == 'pixels':
        img = img.resize((int(resize_data['width']), int(resize_data['height'])), Image.Resampling.LANCZOS)
    elif resize_data.get('mode') == 'percentage':
        pct = int(resize_data['percentage']) / 100.0
        img = img.resize((int(img.width * pct), int(img.height * pct)), Image.Resampling.LANCZOS)

    # 3. DÖNDÜR & AYNA
    if crop_data.get('rotate'):
        img = img.rotate(-int(crop_data['rotate']), expand=True)
    if crop_data.get('flip') == 'true' or crop_data.get('flip') is True:
        img = ImageOps.mirror(img)

    # 4. RENK AYARLARI
    if filter_data.get('brightness') != 1.0: img = ImageEnhance.Brightness(img).enhance(float(filter_data['brightness']))
    if filter_data.get('contrast') != 1.0: img = ImageEnhance.Contrast(img).enhance(float(filter_data['contrast']))
    if filter_data.get('saturation') != 1.0: img = ImageEnhance.Color(img).enhance(float(filter_data['saturation']))
    if filter_data.get('sharpness') != 1.0: img = ImageEnhance.Sharpness(img).enhance(float(filter_data['sharpness']))

    # 5. EFEKT FİLTRELERİ
    if filter_data.get('preset') and filter_data.get('preset') != 'none':
        img = apply_preset(img, filter_data['preset'])

    # 6. KAYDET
    output = BytesIO()
    fmt = target_format.upper().replace('JPG', 'JPEG')
    
    # JPEG/JPG için şeffaflık düzeltmesi
    if fmt == 'JPEG' and img.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    elif fmt == 'JPEG' and img.mode != 'RGB':
        img = img.convert('RGB')
        
    img.save(output, format=fmt, quality=90, optimize=True)
    output.seek(0)
    
    return output, f"edited_image.{target_format.lower()}"