import yt_dlp
import os
import uuid
from shared import DOWNLOADS_DIR

def get_media_info_logic(url: str):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get('title', 'Bilinmeyen Video'),
            "thumbnail": info.get('thumbnail', ''),
            "duration": info.get('duration_string', '00:00'),
            "uploader": info.get('uploader', 'Gizli Hesap'),
            "platform": info.get('extractor_key', 'Video')
        }

def download_media_logic(url: str, format_type: str):
    unique_name = f"vid_{uuid.uuid4().hex[:8]}"
    
    ydl_opts = {
        'outtmpl': f'{DOWNLOADS_DIR}/{unique_name}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'format': 'bestaudio/best' if format_type == 'mp3' else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    }

    if format_type == 'mp3':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        ext = 'mp3' if format_type == 'mp3' else info.get('ext', 'mp4')
        filename = f"{unique_name}.{ext}"
        return os.path.join(DOWNLOADS_DIR, filename), filename