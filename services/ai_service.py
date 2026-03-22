import io
from PIL import Image, ImageEnhance, ImageFilter

def process_ai_enhance_logic(file_bytes, enhancement_type, scale_factor=2.0):
    """
    Görsellerin kalitesini, çözünürlüğünü ve renklerini iyileştiren motor.
    """
    img = Image.open(io.BytesIO(file_bytes))

    # Şeffaflık (Alpha) kanalı olan görselleri güvenli bir şekilde RGB'ye çevir
    if img.mode != 'RGB':
        if img.mode in ('RGBA', 'LA'):
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        else:
            img = img.convert('RGB')

    if enhancement_type == 'upscale':
        # Yüksek kaliteli Lanczos algoritması ile çözünürlüğü kayıpsız katla
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Upscale sonrası detayları ortaya çıkarmak için akıllı keskinleştirme
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    elif enhancement_type == 'restore':
        # Eski/Soluk fotoğrafları canlandırma (Renk ve Kontrast optimizasyonu)
        color_enhancer = ImageEnhance.Color(img)
        img = color_enhancer.enhance(1.4) # %40 daha canlı renkler

        contrast_enhancer = ImageEnhance.Contrast(img)
        img = contrast_enhancer.enhance(1.2) # %20 daha derin kontrast

        sharpness_enhancer = ImageEnhance.Sharpness(img)
        img = sharpness_enhancer.enhance(1.5) # Hatları belirginleştir

    elif enhancement_type == 'denoise':
        # Kumlanmayı (noise) azaltmak için pürüzsüzleştirme ve detay kurtarma
        img = img.filter(ImageFilter.MedianFilter(size=3))
        # Hafif bir keskinlik ekleyerek blur etkisini kır
        img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=100, threshold=5))

    # İşlenmiş görseli belleğe kaydet
    output = io.BytesIO()
    img.save(output, format="JPEG", quality=95, optimize=True)
    output.seek(0)

    filename = f"FileWizard_Pro_{enhancement_type.capitalize()}.jpg"
    return output, filename