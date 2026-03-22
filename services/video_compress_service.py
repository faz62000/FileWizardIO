import os
import subprocess
import re
from shared import progress_store

def get_video_duration(input_path: str):
    """Videonun toplam uzunluğunu saniye cinsinden alır."""
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(result.stdout.strip())
    except Exception:
        return 0.0

def compress_video_logic(input_path: str, output_path: str, task_id: str, crf: str = "28"):
    """
    Video sıkıştırma işlemini FFmpeg kullanarak yapar ve ilerlemeyi kaydeder.
    CRF (Constant Rate Factor): Daha düşük değer = Yüksek kalite, Daha yüksek değer = Yüksek sıkıştırma
    """
    progress_store[task_id] = {"percent": 5, "message": "Video analiz ediliyor..."}
    
    duration = get_video_duration(input_path)
    
    progress_store[task_id] = {"percent": 10, "message": "Sıkıştırma motoru başlatılıyor..."}
    
    # FFmpeg komutu (H.264 codec ve CRF kalite/boyut kontrolü)
    cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-vcodec', 'libx264', '-crf', crf,
        '-preset', 'fast', # Hız ve kalite dengesi
        '-threads', '1',   # MİLYON DOLARLIK DOKUNUŞ: FFmpeg'in tüm işlemciyi sömürmesini engeller, sunucu çökmez!
        '-acodec', 'aac',  # Ses formatını koruma
        output_path
    ]
    
    # İşlemi başlat ve çıktıları oku
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, universal_newlines=True)
    
    # FFmpeg ilerleme süresini yakalamak için Regex kalıbı
    time_pattern = re.compile(r"time=(\d+):(\d+):(\d+\.\d+)")
    
    for line in process.stderr:
        match = time_pattern.search(line)
        if match and duration > 0:
            hours = float(match.group(1))
            minutes = float(match.group(2))
            seconds = float(match.group(3))
            current_time = (hours * 3600) + (minutes * 60) + seconds
            
            # Yüzdeyi 10 ile 95 arasında tut
            percent = int((current_time / duration) * 85) + 10 
            progress_store[task_id] = {"percent": min(percent, 95), "message": "Kareler sıkıştırılıyor (Kalite korunuyor)..."}
    
    process.wait()
    
    if process.returncode == 0 and os.path.exists(output_path):
        progress_store[task_id] = {"percent": 100, "message": "Sıkıştırma başarıyla tamamlandı!"}
        return True
    else:
        progress_store[task_id] = {"percent": 100, "message": "Hata: Sıkıştırma motorunda kritik bir hata oluştu."}
        return False