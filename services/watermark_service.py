from PIL import Image
from io import BytesIO

def process_watermark_logic(base_file_stream, logo_file_stream, opacity, position, target_format):
    # Ana resmi güvenle aç
    base_img = Image.open(base_file_stream).convert("RGBA")
    base_w, base_h = base_img.size

    # Logoyu aç (Transparanlığı koruyarak)
    logo_img = Image.open(logo_file_stream).convert("RGBA")
    
    # Profesyonel görünüm için logoyu ana resmin genişliğinin %15'i kadar ölçeklendir
    logo_w, logo_h = logo_img.size
    target_logo_w = max(1, int(base_w * 0.15))
    scale_ratio = target_logo_w / float(logo_w)
    target_logo_h = max(1, int(float(logo_h) * scale_ratio))
    
    logo_img = logo_img.resize((target_logo_w, target_logo_h), Image.Resampling.LANCZOS)

    # Şeffaflık (Opacity) Ayarı
    if opacity < 100:
        alpha = logo_img.split()[3]
        alpha = alpha.point(lambda p: p * (opacity / 100.0))
        logo_img.putalpha(alpha)

    # Kenar Boşlukları (Margin)
    margin = int(base_w * 0.03) # %3'lük estetik boşluk
    
    # Pozisyon Hesaplama
    if position == 'bottom_right':
        pos = (base_w - target_logo_w - margin, base_h - target_logo_h - margin)
    elif position == 'bottom_left':
        pos = (margin, base_h - target_logo_h - margin)
    elif position == 'top_right':
        pos = (base_w - target_logo_w - margin, margin)
    elif position == 'top_left':
        pos = (margin, margin)
    else: # center
        pos = ((base_w - target_logo_w) // 2, (base_h - target_logo_h) // 2)

    # Logoyu şeffaf bir katman üzerine yapıştır ve ana resimle birleştir
    transparent = Image.new('RGBA', base_img.size, (0,0,0,0))
    transparent.paste(logo_img, pos, mask=logo_img)
    result_img = Image.alpha_composite(base_img, transparent)

    # İstenilen formata göre çıktı üret
    fmt = target_format.upper().replace('JPG', 'JPEG')
    if fmt == 'JPEG':
        # Arka plan transparan ise JPG'de beyaza çevir
        bg = Image.new('RGB', result_img.size, (255, 255, 255))
        bg.paste(result_img, mask=result_img.split()[3])
        result_img = bg
    else:
        # PNG/WEBP ise sadece RGB veya RGBA kalmasını garantile
        if result_img.mode != 'RGBA':
            result_img = result_img.convert('RGBA')
            
    output = BytesIO()
    # Optimize ve kalite ayarlarıyla kaydet
    result_img.save(output, format=fmt, quality=92, optimize=True)
    output.seek(0)
    
    return output, f"filewizard_watermarked.{target_format.lower()}"