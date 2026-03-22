// URL Yönlendirme Haritası
const routeMap = {
    "/araclar/arka-plan-silici": "/en/tools/background-remover",
    "/en/tools/background-remover": "/araclar/arka-plan-silici",
    "/araclar/otomatik-filigran": "/en/tools/auto-watermark",
    "/en/tools/auto-watermark": "/araclar/otomatik-filigran",
    "/araclar/toplu-islem": "/en/tools/batch-processing",
    "/en/tools/batch-processing": "/araclar/toplu-islem",
    "/araclar/ai-studyo": "/en/tools/ai-studio",
    "/en/tools/ai-studio": "/araclar/ai-studyo",
    "/araclar/bulut-senkronizasyonu": "/en/tools/cloud-sync",
    "/en/tools/cloud-sync": "/araclar/bulut-senkronizasyonu",
    "/gelistirici-api": "/en/developer-api",
    "/en/developer-api": "/gelistirici-api",
    "/araclar/video-kucultme": "/en/tools/video-compressor",
    "/en/tools/video-compressor": "/araclar/video-kucultme",
    "/": "/en/",
    "/en/": "/"
};

window.CURRENT_LANG = window.location.pathname.startsWith("/en/") ? "en" : "tr";

function toggleLanguage() {
    const currentPath = window.location.pathname;
    if (routeMap[currentPath]) {
        window.location.href = routeMap[currentPath];
    } else {
        window.location.href = window.CURRENT_LANG === "tr" ? "/en/" : "/";
    }
}

const translations = {
    "tr": {
        // --- ORTAK ---
        "nav_return": "Ana Siteye Dön",
        "footer_copy": "© 2026 FileWizardIO Enterprise API by ForgeLogic LLC.",
        "footer_privacy": "Gizlilik",
        "footer_terms": "Koşullar",
        "footer_cookies": "Çerezler",
        "footer_contact": "İletişim",
        
        // --- ANA SAYFA VİTRİNİ ---
        "home_nav_media": "Video İndirici",
        "home_nav_image": "Görsel Stüdyo",
        "home_nav_pdf": "PDF Araçları",
        "home_nav_premium": "PREMİUM ARAÇLAR",
        "home_nav_batch": "Toplu İşlem",
        "home_nav_bg": "Arka Plan Silici",
        "home_nav_ai": "AI Stüdyo",
        "home_nav_cloud": "Bulut Senk.",
        "home_nav_wm": "Filigran",
        "home_nav_vc": "Video Küçültme",
        "home_nav_api": "Geliştirici API",
        "home_support_title": "Sorun mu yaşıyorsun?",
        "home_support_btn": "Destek Ekibi",
        
        "home_hero_title": "Sınırsız.",
        "home_hero_desc": "YouTube, TikTok, Instagram, X. <span class='text-white font-bold'>Filigransız İndir.</span>",
        "home_input_placeholder": "Video bağlantısını yapıştır...",
        "home_btn_paste": "YAPIŞTIR",
        "home_btn_fetch": "<i class='fa-solid fa-bolt text-indigo-600'></i> Videoyu Getir",
        
        "home_pdf_edit_title": "Canlı Düzenle",
        "home_pdf_edit_desc": "Sayfaları döndür, sil veya yerini değiştir. Görsel editör.",
        "home_pdf_merge_title": "PDF Birleştir",
        "home_pdf_merge_desc": "Birden fazla PDF dosyasını tek bir dosyada topla.",
        "home_pdf_compress_title": "PDF Sıkıştır",
        "home_pdf_compress_desc": "Kaliteyi koruyarak dosya boyutunu %80'e kadar küçült.",
        "home_pdf_drop": "Dosyaları buraya bırakın",
        "home_pdf_btn_select": "Dosya Seç",

        // --- ARKA PLAN SİLİCİ ---
        "bg_title": "Kusursuz <span class='text-transparent bg-clip-text bg-gradient-to-r from-fuchsia-400 to-purple-500'>Dekupe.</span>",
        "bg_desc": "Yapay zeka (U²-Net) motorumuzla fotoğraflarınızın arka planını saç teline kadar ayırın ve saniyeler içinde şeffaf PNG'ye dönüştürün.",
        "bg_drop_title": "Sihri Başlatmak İçin Sürükleyin",
        "bg_drop_desc": "veya bilgisayarınızdan seçmek için tıklayın (JPEG, PNG, WEBP)",
        "bg_btn_change": "Değiştir",
        "bg_info_title": "Sihirli Motor Hazır",
        "bg_info_1_title": "Yüksek Hassasiyet",
        "bg_info_1_desc": "Saç telleri, kürk veya karmaşık kenarlar yapay zeka tarafından milimetrik hesaplanır.",
        "bg_info_2_title": "E-Ticaret Uyumlu",
        "bg_info_2_desc": "Ürün fotoğraflarınızı saniyeler içinde pazar yeri standartlarına uygun hale getirin.",
        "bg_info_3_title": "Kayıpsız Şeffaflık",
        "bg_info_3_desc": "Çıktılar her zaman profesyonel tasarım programlarıyla uyumlu şeffaf PNG formatındadır.",
        "bg_btn_process": "<i class='fa-solid fa-eraser'></i> ARKA PLANI SİL VE İNDİR",
        "bg_modal_title": "İşleniyor",
        "bg_modal_desc": "Yapay zeka nesneyi analiz ediyor...",
        
        // --- TOPLU İŞLEM ---
        "batch_title": "Toplu <span class='text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-500'>Dönüştürücü.</span>",
        "batch_desc": "Tek seferde 50 dosyaya kadar yükleyin. Görselleri topluca yeniden boyutlandırın, formatını değiştirin ve zamandan tasarruf edin.",
        "batch_drop_title": "Görselleri Buraya Sürükleyin",
        "batch_drop_desc": "veya seçmek için tıklayın (Maks: 50 Dosya, JPEG/PNG/WEBP)",
        "batch_btn_select": "Dosyaları Seç",
        "batch_file_selected": "Dosya Seçildi",
        "batch_btn_clear": "Temizle",
        "batch_settings_title": "Toplu İşlem Ayarları",
        "batch_format_label": "Çıktı Formatı",
        "batch_format_jpeg": "JPEG (Varsayılan, Düşük Boyut)",
        "batch_format_png": "PNG (Kayıpsız Kalite)",
        "batch_format_webp": "WEBP (Web İçin Optimize)",
        "batch_resize_label": "Genişliğe Göre Boyutlandır (Opsiyonel)",
        "batch_resize_placeholder": "Örn: 1080",
        "batch_pixel": "Piksel",
        "batch_resize_info": "Boş bırakırsanız orijinal boyut korunur. Yükseklik otomatik ayarlanır.",
        "batch_btn_process": "<i class='fa-solid fa-bolt'></i> TÜMÜNÜ İŞLE VE İNDİR (.ZIP)",
        "batch_modal_title": "İşleniyor",
        "batch_modal_desc": "Dosyalar hazırlanıyor...",

        // --- AI STUDIO ---
        "ai_title": "Kusursuz <span class='text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500'>Detaylar.</span>",
        "ai_desc": "Yapay zeka motorumuzla düşük çözünürlüklü fotoğrafları canlandırın, pürüzleri giderin ve pikselleri yeniden inşa edin.",
        "ai_drop_title": "Sihri Başlatmak İçin Dokun",
        "ai_drop_desc": "İyileştirilecek görseli seçin veya sürükleyin",
        "ai_btn_change": "Değiştir",
        "ai_model_title": "İşlem Modelini Seçin",
        "ai_model_1_title": "4K Upscale (Çözünürlük Katlama)",
        "ai_model_1_desc": "Pikselleri kayıpsız bir şekilde yeniden inşa ederek görselinizin çözünürlüğünü 2 katına çıkarır ve keskinleştirir.",
        "ai_model_2_title": "Renk ve Kontrast Canlandırma",
        "ai_model_2_desc": "Eski, soluk veya karanlık fotoğrafların renklerini analiz eder, kontrastı derinleştirir ve detayları ortaya çıkarır.",
        "ai_model_3_title": "AI Denoise (Pürüz Giderme)",
        "ai_model_3_desc": "Düşük ışıkta çekilmiş karlı (noise) fotoğraflardaki pürüzleri filtreler ve yüzeyleri pürüzsüzleştirir.",
        "ai_btn_process": "<i class='fa-solid fa-bolt'></i> YAPAY ZEKA İLE İYİLEŞTİR VE İNDİR",
        "ai_modal_title": "İşleniyor",
        "ai_modal_desc": "Yapay zeka pikselleri analiz ediyor...",

        // --- CLOUD SYNC ---
        "cloud_title": "Sınırları <span class='text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-blue-500'>Aşın.</span>",
        "cloud_desc": "Cihazınızda yer açın. İşlenmiş veya büyük boyutlu dosyalarınızı doğrudan Dropbox bulut hesabınıza fırlatın.",
        "cloud_drop_title": "Buluta Gönderilecek Dosya",
        "cloud_drop_desc": "Görsel, PDF veya Video sürükleyip bırakın",
        "cloud_btn_change": "Başka Dosya Seç",
        "cloud_settings_title": "Bulut Bağlantısı",
        "cloud_token_label": "Dropbox Access Token (Erişim Anahtarı)",
        "cloud_token_placeholder": "sl.B... (Gizli Tokeniniz)",
        "cloud_token_info": "Dropbox Geliştirici panelinden aldığınız tokeni girin. Bu bilgi sunucularımızda <span class='text-sky-400 font-bold'>asla kaydedilmez.</span>",
        "cloud_btn_process": "<i class='fa-solid fa-cloud-arrow-up'></i> DOĞRUDAN BULUTA FIRLAT",
        "cloud_modal_title": "Senkronize Ediliyor",
        "cloud_modal_desc": "Bulut bağlantısı kuruluyor...",

        // --- DEVELOPER API ---
        "dev_title": "Geliştirici <span class='text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-500'>API.</span>",
        "dev_desc": "FileWizard motorunu kendi uygulamalarınıza bağlayın. Otomasyon süreçlerinizi saniyeler içinde ayağa kaldırın.",
        "dev_get_key_title": "API Anahtarı Al",
        "dev_email_label": "E-Posta Adresi",
        "dev_email_placeholder": "sirket@domain.com",
        "dev_btn_generate": "<i class='fa-solid fa-key'></i> ANAHTAR OLUŞTUR",
        "dev_quota_title": "Kota Durumu",
        "dev_key_label": "API Anahtarınız",
        "dev_key_placeholder": "fw_live_...",
        "dev_btn_check": "<i class='fa-solid fa-magnifying-glass'></i> Sorgula",
        "dev_doc_title": "Hızlı Başlangıç (cURL)",
        "dev_used_quota": "Kullanılan",
        "dev_rem_quota": "Kalan Kota",
        "dev_api_desc": "Verilen bir YouTube, TikTok veya Instagram bağlantısındaki medyanın meta verilerini, başlığını ve format bilgilerini yüksek hızda çözer.",
        "dev_curl_example": "cURL Örneği",
        "dev_example_res": "Örnek Yanıt (JSON)",
        
        // --- AUTO WATERMARK ---
        "wm_main_title": "Görsellerinizi <span class='text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-500'>Markalayın.</span>",
        "wm_main_desc": "İçeriklerinizi koruyun. Logonuzu saniyeler içinde, profesyonel kalitede görsellerinize entegre edin.",
        "wm_box1_title": "1. Ana Görsel",
        "wm_box1_desc": "Filigran eklenecek fotoğrafı seçin",
        "wm_box2_title": "2. Logonuz",
        "wm_box2_desc": "Şeffaf arka planlı logonuzu seçin (PNG)",
        "wm_uploaded": "Yüklendi",
        "wm_settings_title": "Filigran Ayarları",
        "wm_opacity": "Şeffaflık (Opacity)",
        "wm_position": "Logo Konumu",
        "wm_format_label": "Çıktı Formatı",
        "wm_fmt_png": "PNG (Kayıpsız, Yüksek Kalite)",
        "wm_fmt_jpg": "JPG (Daha Düşük Dosya Boyutu)",
        "wm_fmt_webp": "WEBP (Web Optimizasyonu)",
        "wm_btn_process": "<i class='fa-solid fa-wand-magic-sparkles'></i> LOGOYU UYGULA VE İNDİR",
        "wm_modal_title": "İşleniyor",
        "wm_modal_desc": "Sunucu ile iletişim kuruluyor...",

        // --- VIDEO COMPRESSOR ---
        "vc_title": "Boyutu Küçült. <span class='text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-orange-500'>Kaliteyi Koru.</span>",
        "vc_desc": "Gelişmiş FFmpeg motorumuzla videolarınızın kalitesini bozmadan dosya boyutunu %80'e kadar küçültün. WhatsApp ve e-posta sınırlarına takılmayın.",
        "vc_drop_title": "Videoyu Buraya Sürükleyin",
        "vc_drop_desc": "veya seçmek için tıklayın (MP4, MOV, AVI, WEBP)",
        "vc_btn_change": "Başka Video Seç",
        "vc_settings_title": "Sıkıştırma Ayarları",
        "vc_level_label": "Sıkıştırma Seviyesi",
        "vc_level_light_title": "Hafif (Mükemmel Kalite)",
        "vc_level_light_desc": "Orijinale en yakın kalite. Dosya boyutu yaklaşık %20-30 küçülür.",
        "vc_level_medium_title": "Standart (Tavsiye Edilen)",
        "vc_level_medium_desc": "Gözle görülür kalite kaybı olmadan dosya boyutunu %50 civarında küçültür.",
        "vc_level_extreme_title": "Maksimum (WhatsApp Uyumlu)",
        "vc_level_extreme_desc": "Dosya boyutunu radikal şekilde (%80'e kadar) düşürür. Sosyal medya gönderimleri için idealdir.",
        "vc_btn_process": "<i class='fa-solid fa-compress'></i> SIKIŞTIR VE İNDİR",
        "vc_modal_title": "İşleniyor",
        "vc_modal_desc": "Video analiz ediliyor...",

        // --- JS ALERTS (SWEETALERT) ---
        "swal_error_title": "İşlem Başarısız",
        "swal_missing_file_title": "Görsel Eksik",
        "swal_missing_file_text": "Lütfen fotoğraf yükleyin.",
        "swal_success_title": "Mükemmel!",
        "swal_success_wm_text": "Markalama başarıyla tamamlandı.",
        "swal_limit_title": "Limit Aşıldı",
        "swal_limit_text": "Tek seferde en fazla 50 dosya yükleyebilirsiniz.",
        "swal_invalid_file_title": "Sadece görsel dosyaları kabul edilir.",
        "swal_missing_batch_title": "Dosya Yok",
        "swal_missing_batch_text": "Lütfen işlenecek görselleri yükleyin.",
        "swal_success_batch_title": "İşlem Başarılı!",
        "swal_success_batch_text": "Tüm görselleriniz ZIP olarak indirildi.",
        "swal_missing_ai_title": "Görsel Eksik",
        "swal_missing_ai_text": "Lütfen iyileştirilecek fotoğrafı yükleyin.",
        "swal_success_ai_title": "Mükemmel!",
        "swal_success_ai_text": "Görseliniz yapay zeka ile başarıyla iyileştirildi.",
        "swal_missing_cloud_file_title": "Dosya Eksik",
        "swal_missing_cloud_file_text": "Lütfen buluta aktarılacak dosyayı seçin.",
        "swal_missing_token_title": "Token Eksik",
        "swal_missing_token_text": "Lütfen Dropbox Access Token bilginizi girin.",
        "swal_success_cloud_title": "Senkronizasyon Başarılı!",
        "swal_success_cloud_text": "Dosya başarıyla Dropbox hesabınıza aktarıldı.",
        "swal_missing_email_title": "E-Posta Eksik",
        "swal_missing_email_text": "Lütfen geçerli bir e-posta adresi girin.",
        "swal_missing_key_title": "Anahtar Eksik",
        "swal_missing_key_text": "Lütfen sorgulanacak API anahtarını girin.",
        "swal_success_key_title": "Anahtar Oluşturuldu",
        "swal_success_key_text": "API anahtarınız oluşturuldu. Lütfen güvenli bir yere kaydedin.",
        "swal_missing_vc_title": "Video Eksik",
        "swal_missing_vc_text": "Lütfen sıkıştırılacak videoyu yükleyin.",
        "swal_success_vc_text": "Videonuz başarıyla sıkıştırıldı ve indirildi."
    },
    "en": {
        // --- COMMON ---
        "nav_return": "Back to Home",
        "footer_copy": "© 2026 FileWizardIO Enterprise API by ForgeLogic LLC.",
        "footer_privacy": "Privacy Policy",
        "footer_terms": "Terms of Service",
        "footer_cookies": "Cookies",
        "footer_contact": "Contact",
        
        // --- HOME SHOWCASE ---
        "home_nav_media": "Video Downloader",
        "home_nav_image": "Image Studio",
        "home_nav_pdf": "PDF Tools",
        "home_nav_premium": "PREMIUM TOOLS",
        "home_nav_batch": "Batch Processing",
        "home_nav_bg": "BG Remover",
        "home_nav_ai": "AI Studio",
        "home_nav_cloud": "Cloud Sync",
        "home_nav_wm": "Watermark",
        "home_nav_vc": "Video Compressor",
        "home_nav_api": "Developer API",
        "home_support_title": "Need help?",
        "home_support_btn": "Support Team",
        
        "home_hero_title": "Limitless.",
        "home_hero_desc": "YouTube, TikTok, Instagram, X. <span class='text-white font-bold'>Download without Watermark.</span>",
        "home_input_placeholder": "Paste video link...",
        "home_btn_paste": "PASTE",
        "home_btn_fetch": "<i class='fa-solid fa-bolt text-indigo-600'></i> Fetch Video",
        
        "home_pdf_edit_title": "Live Edit",
        "home_pdf_edit_desc": "Rotate, delete, or reorder pages. Visual editor.",
        "home_pdf_merge_title": "Merge PDF",
        "home_pdf_merge_desc": "Combine multiple PDF files into one.",
        "home_pdf_compress_title": "Compress PDF",
        "home_pdf_compress_desc": "Reduce file size up to 80% while keeping quality.",
        "home_pdf_drop": "Drop files here",
        "home_pdf_btn_select": "Select File",

        // --- BG REMOVER ---
        "bg_title": "Flawless <span class='text-transparent bg-clip-text bg-gradient-to-r from-fuchsia-400 to-purple-500'>Cutout.</span>",
        "bg_desc": "Separate the background of your photos down to a single strand of hair with our AI (U²-Net) engine and convert to transparent PNG in seconds.",
        "bg_drop_title": "Drag & Drop to Start Magic",
        "bg_drop_desc": "or click to select from your computer (JPEG, PNG, WEBP)",
        "bg_btn_change": "Change File",
        "bg_info_title": "Magic Engine Ready",
        "bg_info_1_title": "High Precision",
        "bg_info_1_desc": "Hair, fur, or complex edges are calculated down to the millimeter by AI.",
        "bg_info_2_title": "E-Commerce Ready",
        "bg_info_2_desc": "Make your product photos marketplace-compliant in seconds.",
        "bg_info_3_title": "Lossless Transparency",
        "bg_info_3_desc": "Outputs are always in transparent PNG format compatible with professional design software.",
        "bg_btn_process": "<i class='fa-solid fa-eraser'></i> REMOVE BG & DOWNLOAD",
        "bg_modal_title": "Processing",
        "bg_modal_desc": "AI is analyzing the object...",

        // --- BATCH PROCESSING ---
        "batch_title": "Bulk <span class='text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-500'>Converter.</span>",
        "batch_desc": "Upload up to 50 files at once. Bulk resize images, change formats, and save time.",
        "batch_drop_title": "Drag & Drop Images Here",
        "batch_drop_desc": "or click to select (Max: 50 Files, JPEG/PNG/WEBP)",
        "batch_btn_select": "Select Files",
        "batch_file_selected": "Files Selected",
        "batch_btn_clear": "Clear",
        "batch_settings_title": "Batch Settings",
        "batch_format_label": "Output Format",
        "batch_format_jpeg": "JPEG (Default, Low Size)",
        "batch_format_png": "PNG (Lossless Quality)",
        "batch_format_webp": "WEBP (Optimized for Web)",
        "batch_resize_label": "Resize by Width (Optional)",
        "batch_resize_placeholder": "E.g. 1080",
        "batch_pixel": "Pixels",
        "batch_resize_info": "Leave blank to keep original size. Height adjusts automatically.",
        "batch_btn_process": "<i class='fa-solid fa-bolt'></i> PROCESS ALL & DOWNLOAD (.ZIP)",
        "batch_modal_title": "Processing",
        "batch_modal_desc": "Preparing files...",

        // --- AI STUDIO ---
        "ai_title": "Flawless <span class='text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500'>Details.</span>",
        "ai_desc": "Revive low-resolution photos, remove noise, and reconstruct pixels with our AI engine.",
        "ai_drop_title": "Tap to Start Magic",
        "ai_drop_desc": "Select or drag an image to enhance",
        "ai_btn_change": "Change",
        "ai_model_title": "Select Processing Model",
        "ai_model_1_title": "4K Upscale",
        "ai_model_1_desc": "Losslessly reconstructs pixels to double the resolution and sharpen your image.",
        "ai_model_2_title": "Color & Contrast Restore",
        "ai_model_2_desc": "Analyzes colors of old, faded, or dark photos, deepens contrast, and reveals details.",
        "ai_model_3_title": "AI Denoise",
        "ai_model_3_desc": "Filters out noise in low-light photos and smoothes surfaces.",
        "ai_btn_process": "<i class='fa-solid fa-bolt'></i> ENHANCE WITH AI & DOWNLOAD",
        "ai_modal_title": "Processing",
        "ai_modal_desc": "AI is analyzing pixels...",

        // --- CLOUD SYNC ---
        "cloud_title": "Break the <span class='text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-blue-500'>Limits.</span>",
        "cloud_desc": "Free up space on your device. Send your processed or large files directly to your Dropbox cloud account.",
        "cloud_drop_title": "File to Send to Cloud",
        "cloud_drop_desc": "Drag & Drop Image, PDF or Video",
        "cloud_btn_change": "Select Another File",
        "cloud_settings_title": "Cloud Connection",
        "cloud_token_label": "Dropbox Access Token",
        "cloud_token_placeholder": "sl.B... (Your Secret Token)",
        "cloud_token_info": "Enter the token from your Dropbox Developer panel. This info is <span class='text-sky-400 font-bold'>never saved</span> on our servers.",
        "cloud_btn_process": "<i class='fa-solid fa-cloud-arrow-up'></i> UPLOAD DIRECTLY TO CLOUD",
        "cloud_modal_title": "Synchronizing",
        "cloud_modal_desc": "Establishing cloud connection...",

        // --- DEVELOPER API ---
        "dev_title": "Developer <span class='text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-500'>API.</span>",
        "dev_desc": "Connect the FileWizard engine to your own applications. Set up your automation processes in seconds.",
        "dev_get_key_title": "Get API Key",
        "dev_email_label": "Email Address",
        "dev_email_placeholder": "company@domain.com",
        "dev_btn_generate": "<i class='fa-solid fa-key'></i> GENERATE KEY",
        "dev_quota_title": "Quota Status",
        "dev_key_label": "Your API Key",
        "dev_key_placeholder": "fw_live_...",
        "dev_btn_check": "<i class='fa-solid fa-magnifying-glass'></i> Check Quota",
        "dev_doc_title": "Quick Start (cURL)",
        "dev_used_quota": "Used",
        "dev_rem_quota": "Remaining",
        "dev_api_desc": "Resolves metadata, title, and format information of media from a given YouTube, TikTok, or Instagram link at high speed.",
        "dev_curl_example": "cURL Example",
        "dev_example_res": "Example Response (JSON)",
        
        // --- AUTO WATERMARK ---
        "wm_main_title": "Brand Your <span class='text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-500'>Images.</span>",
        "wm_main_desc": "Protect your content. Integrate your logo into your images in seconds with professional quality.",
        "wm_box1_title": "1. Base Image",
        "wm_box1_desc": "Select the photo to watermark",
        "wm_box2_title": "2. Your Logo",
        "wm_box2_desc": "Select your transparent background logo (PNG)",
        "wm_uploaded": "Uploaded",
        "wm_settings_title": "Watermark Settings",
        "wm_opacity": "Opacity",
        "wm_position": "Logo Position",
        "wm_format_label": "Output Format",
        "wm_fmt_png": "PNG (Lossless, High Quality)",
        "wm_fmt_jpg": "JPG (Lower File Size)",
        "wm_fmt_webp": "WEBP (Web Optimization)",
        "wm_btn_process": "<i class='fa-solid fa-wand-magic-sparkles'></i> APPLY LOGO & DOWNLOAD",
        "wm_modal_title": "Processing",
        "wm_modal_desc": "Communicating with server...",

        // --- VIDEO COMPRESSOR ---
        "vc_title": "Shrink Size. <span class='text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-orange-500'>Keep Quality.</span>",
        "vc_desc": "Reduce video file size by up to 80% without losing quality using our advanced FFmpeg engine. Bypass WhatsApp and email limits.",
        "vc_drop_title": "Drag Video Here",
        "vc_drop_desc": "or click to select (MP4, MOV, AVI, WEBP)",
        "vc_btn_change": "Select Another Video",
        "vc_settings_title": "Compression Settings",
        "vc_level_label": "Compression Level",
        "vc_level_light_title": "Light (Excellent Quality)",
        "vc_level_light_desc": "Closest to original quality. File size reduces by approx. 20-30%.",
        "vc_level_medium_title": "Standard (Recommended)",
        "vc_level_medium_desc": "Reduces file size by around 50% with no visible quality loss.",
        "vc_level_extreme_title": "Extreme (WhatsApp Ready)",
        "vc_level_extreme_desc": "Radically reduces file size (up to 80%). Ideal for social media sharing.",
        "vc_btn_process": "<i class='fa-solid fa-compress'></i> COMPRESS & DOWNLOAD",
        "vc_modal_title": "Processing",
        "vc_modal_desc": "Analyzing video...",

        // --- JS ALERTS (SWEETALERT) ---
        "swal_error_title": "Operation Failed",
        "swal_missing_file_title": "Missing Image",
        "swal_missing_file_text": "Please upload a photo.",
        "swal_success_title": "Excellent!",
        "swal_success_wm_text": "Watermark successfully added.",
        "swal_limit_title": "Limit Exceeded",
        "swal_limit_text": "You can upload a maximum of 50 files at a time.",
        "swal_invalid_file_title": "Only image files are accepted.",
        "swal_missing_batch_title": "No Files",
        "swal_missing_batch_text": "Please upload images to process.",
        "swal_success_batch_title": "Process Successful!",
        "swal_success_batch_text": "All your images have been downloaded as a ZIP.",
        "swal_missing_ai_title": "Missing Image",
        "swal_missing_ai_text": "Please upload a photo to enhance.",
        "swal_success_ai_title": "Excellent!",
        "swal_success_ai_text": "Your image has been successfully enhanced with AI.",
        "swal_missing_cloud_file_title": "Missing File",
        "swal_missing_cloud_file_text": "Please select a file to upload to the cloud.",
        "swal_missing_token_title": "Missing Token",
        "swal_missing_token_text": "Please enter your Dropbox Access Token.",
        "swal_success_cloud_title": "Sync Successful!",
        "swal_success_cloud_text": "File successfully transferred to your Dropbox account.",
        "swal_missing_email_title": "Missing Email",
        "swal_missing_email_text": "Please enter a valid email address.",
        "swal_missing_key_title": "Missing Key",
        "swal_missing_key_text": "Please enter the API key to check.",
        "swal_success_key_title": "Key Generated",
        "swal_success_key_text": "Your API key has been generated. Please save it securely.",
        "swal_missing_vc_title": "Missing Video",
        "swal_missing_vc_text": "Please upload a video to compress.",
        "swal_success_vc_text": "Your video has been successfully compressed and downloaded."
    }
};

window.t = function(key) {
    return translations[window.CURRENT_LANG][key] || key;
};

document.addEventListener("DOMContentLoaded", () => {
    const langBtnText = document.getElementById("lang-btn-text");
    if(langBtnText) {
        langBtnText.innerText = window.CURRENT_LANG === "tr" ? "EN" : "TR";
    }

    const elements = document.querySelectorAll("[data-i18n]");
    elements.forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (translations[window.CURRENT_LANG] && translations[window.CURRENT_LANG][key]) {
            el.innerHTML = translations[window.CURRENT_LANG][key];
        }
    });
    
    // Placeholder çevirileri
    const placeholders = document.querySelectorAll("[data-i18n-placeholder]");
    placeholders.forEach(el => {
        const key = el.getAttribute("data-i18n-placeholder");
        if (translations[window.CURRENT_LANG] && translations[window.CURRENT_LANG][key]) {
            el.setAttribute("placeholder", translations[window.CURRENT_LANG][key]);
        }
    });
});