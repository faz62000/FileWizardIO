// URL Yönlendirme Haritası (Kısa ve Clean URL)
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
    
    // YASAL SAYFA ROTALARI (Statik HTML Yapısı)
    "/legal/terms.html": "/legal/terms.html",
    "/legal/privacy.html": "/legal/privacy.html",
    "/legal/refund.html": "/legal/refund.html",
    "/legal/cookies.html": "/legal/cookies.html",
    
    "/": "/en/",
    "/en/": "/"
};

window.CURRENT_LANG = window.location.pathname.startsWith("/en/") ? "en" : "tr";

if (window.location.pathname.includes('/legal/')) {
    if (document.documentElement.lang === "en") window.CURRENT_LANG = "en";
    else window.CURRENT_LANG = "tr";
}

function toggleLanguage() {
    const currentPath = window.location.pathname;
    
    if(currentPath.includes('/legal/')) {
        const trContent = document.getElementById('content-tr');
        const enContent = document.getElementById('content-en');
        const langBtnText = document.getElementById("lang-btn-text");

        if (window.CURRENT_LANG === "tr") {
            trContent.classList.remove('active');
            enContent.classList.add('active');
            document.documentElement.lang = "en";
            window.CURRENT_LANG = "en";
            if(langBtnText) langBtnText.innerText = "TR";
        } else {
            enContent.classList.remove('active');
            trContent.classList.add('active');
            document.documentElement.lang = "tr";
            window.CURRENT_LANG = "tr";
            if(langBtnText) langBtnText.innerText = "EN";
        }
        
        const elements = document.querySelectorAll("[data-i18n]");
        elements.forEach(el => {
            const key = el.getAttribute("data-i18n");
            if (translations[window.CURRENT_LANG] && translations[window.CURRENT_LANG][key]) {
                el.innerHTML = translations[window.CURRENT_LANG][key];
            }
        });
        return;
    }

    if (routeMap[currentPath]) {
        window.location.href = routeMap[currentPath];
    } else {
        window.location.href = window.CURRENT_LANG === "tr" ? "/en/" : "/";
    }
}

const translations = {
    "tr": {
        "nav_return": "Ana Siteye Dön",
        "nav_home_tooltip": "Ana Sayfa",
        "footer_copy": "© 2026 FileWizardIO Enterprise API by ForgeLogic LLC.",
        "footer_privacy": "Gizlilik",
        "footer_terms": "Koşullar",
        "footer_cookies": "Çerezler",
        "footer_refund": "İade",
        "footer_contact": "İletişim",
        "prog_title": "İşleniyor",
        "prog_desc": "Sunucu ile iletişim kuruluyor...",
        
        "session_warning_title": "Oturum Kapanıyor",
        "session_warning_desc": "Hareketsizlik nedeniyle oturumunuz <b>60</b> saniye içinde kapatılacak.",
        "session_ask_continue": "İşlemlere devam etmek istiyor musunuz?",
        "session_btn_continue": "Devam Et",
        "session_btn_logout": "Çıkış Yap",
        "session_expired_title": "Oturum Sonlandı",
        "session_expired_desc": "Güvenliğiniz için oturumunuz otomatik olarak kapatıldı.",
        
        "swal_missing_title": "Eksik Görsel",
        "swal_missing_text": "Lütfen işlenecek görseli seçin.",
        "swal_success_title": "Başarılı",
        "swal_success_text": "İşlem kusursuzca tamamlandı.",
        "swal_error_title": "İşlem Başarısız",
        "swal_limit_title": "Limit Aşıldı",
        "swal_limit_text": "Maksimum 50 dosya yükleyebilirsiniz.",
        "swal_invalid_file_title": "Sadece görsel dosyaları desteklenir.",
        "swal_missing_batch_title": "Dosya Yok",
        "swal_missing_batch_text": "Lütfen en az bir görsel yükleyin.",
        "swal_success_batch_title": "Toplu İşlem Tamam",
        "swal_success_batch_text": "Dosyalarınız sıkıştırılarak ZIP formatında indirildi.",
        "swal_missing_ai_title": "Eksik Görsel",
        "swal_missing_ai_text": "Lütfen iyileştirilecek görseli seçin.",
        "swal_success_ai_title": "Mükemmel",
        "swal_success_ai_text": "Yapay zeka işlemi başarıyla tamamlandı.",
        "swal_missing_cloud_file_title": "Dosya Eksik",
        "swal_missing_cloud_file_text": "Lütfen buluta aktarılacak dosyayı seçin.",
        "swal_missing_token_title": "Token Eksik",
        "swal_missing_token_text": "Dropbox erişim anahtarınızı (Token) girmelisiniz.",
        "swal_success_cloud_title": "Buluta Aktarıldı",
        "swal_success_cloud_text": "Dosyanız başarıyla Dropbox hesabınıza gönderildi.",
        "swal_missing_email_text": "Lütfen geçerli bir e-posta adresi girin.",
        "swal_success_key_title": "API Anahtarınız Hazır",
        "swal_success_key_text": "Lütfen anahtarınızı güvenli bir yere kopyalayın.",
        "swal_missing_key_title": "Eksik Bilgi",
        "swal_missing_key_text": "Lütfen sorgulamak için API anahtarınızı girin.",
        "swal_missing_file_title": "Eksik Dosya",
        "swal_missing_file_text": "Lütfen hem ana görseli hem de logonuzu yükleyin.",
        "swal_success_wm_text": "Markalama başarıyla tamamlandı.",
        "swal_missing_vc_title": "Video Eksik",
        "swal_missing_vc_text": "Lütfen sıkıştırılacak videoyu yükleyin.",
        "swal_success_vc_text": "Videonuz başarıyla sıkıştırıldı ve indirildi.",

        // YENİ EKLENEN PAYWALL ÇEVİRİLERİ
        "swal_auth_required_title": "Premium Kilitli",
        "swal_auth_required_text": "Bu araca erişmek için hesap oluşturmalı ve PRO plana (9.99$/Ay) geçmelisiniz.",

        "header_login": "Giriş Yap",
        "header_register": "Üye Ol",
        "header_upgrade": "Yükselt",
        "auth_login_title": "Hoş Geldiniz",
        "auth_login_desc": "FileWizardIO hesabınıza giriş yapın.",
        "auth_email_label": "E-Posta",
        "auth_email_placeholder": "ornek@mail.com",
        "auth_pass_label": "Şifre",
        "auth_pass_placeholder": "••••••••",
        "auth_pass_reg_placeholder": "En az 6 karakter",
        "auth_login_btn": "Giriş Yap",
        "auth_or_with": "Veya Şununla",
        "auth_no_account": "Hesabınız yok mu?",
        "auth_register_link": "Üye Olun",
        "auth_reg_title": "Kayıt Ol",
        "auth_reg_desc": "Sınırsız araçlar için aramıza katıl.",
        "auth_reg_btn": "Ücretsiz Kayıt Ol",
        "auth_quick_reg": "Hızlı Kayıt",
        "auth_has_account": "Zaten üye misiniz?",
        "auth_login_link": "Giriş Yapın",
        
        "upg_title": "PRO'ya Yükselt",
        "upg_desc": "Yapay zeka araçları ve sınırsız sıkıştırma için Premium'a geç.",
        "upg_f1": "Limitsiz Video Küçültme (Asla çökmez)",
        "upg_f2": "AI Arka Plan Silici",
        "upg_f3": "Yapay Zeka Stüdyosu",
        "upg_f4": "Öncelikli Sunucu İşlemcisi",
        "upg_btn": "Hemen PRO Ol ($9.99/Ay)",

        "home_nav_media": "Medya Yedekleme",
        "home_nav_image": "Görsel Stüdyo",
        "home_nav_pdf": "PDF Araçları",
        "home_nav_premium": "PREMİUM ARAÇLAR",
        "home_nav_batch": "Toplu İşlem",
        "home_nav_bg": "Arka Plan Silici",
        "home_nav_ai": "AI Stüdyo",
        "home_nav_cloud": "Bulut Senk.",
        "home_nav_wm": "Filigran",
        "home_nav_vc": "Video Küçültme",
        "home_nav_pricing": "Fiyatlandırma",
        "home_nav_api": "Geliştirici API",
        "home_support_title": "Sorun mu yaşıyorsun?",
        "home_support_btn": "Destek Ekibi",
        
        "home_hero_title": "Profesyonel.",
        "home_hero_desc": "İçeriklerinizi güvenle yedekleyin ve <span class='text-white font-bold'>kişisel arşivinizi oluşturun.</span>",
        "home_input_placeholder": "Medya bağlantısını buraya yapıştırın...",
        "home_btn_paste": "YAPIŞTIR",
        "home_btn_fetch": "<i class='fa-solid fa-cloud-arrow-down text-indigo-600'></i> Medyayı Hazırla",
        "home_btn_mp4": "Arşivi Kaydet (MP4)",
        "home_btn_mp3": "Sesi Yedekle (MP3)",
        
        "home_pdf_edit_title": "Canlı Düzenle",
        "home_pdf_edit_desc": "Sayfaları döndür, sil veya yerini değiştir. Görsel editör.",
        "home_pdf_merge_title": "PDF Birleştir",
        "home_pdf_merge_desc": "Birden fazla PDF dosyasını tek bir dosyada topla.",
        "home_pdf_compress_title": "PDF Sıkıştır",
        "home_pdf_compress_desc": "Kaliteyi koruyarak dosya boyutunu %80'e kadar küçült.",
        "home_pdf_drop": "Dosyaları buraya bırakın",
        "home_pdf_btn_select": "Dosya Seç",
        "pdf_btn_back": "<i class='fa-solid fa-arrow-left'></i> Geri Dön",

        "img_btn_upload": "Görsel Yükle",
        "img_placeholder": "Düzenlemek için bir görsel seçin",
        "img_tab_crop": "KIRP",
        "img_tab_filter": "FİLTRE",
        "img_tab_adjust": "AYAR",
        "img_tab_export": "ÇIKTI",
        "img_crop_free": "Serbest",
        "img_crop_square": "1:1 Kare",
        "img_crop_yt": "16:9 YT",
        "img_crop_story": "9:16 Story",
        "img_crop_insta": "4:5 Insta",
        "img_filter_normal": "Normal",
        "img_filter_bw": "B&W",
        "img_filter_sepia": "Sepia",
        "img_filter_vintage": "Vintage",
        "img_adj_bright": "Parlaklık",
        "img_adj_contrast": "Kontrast",
        "img_adj_sat": "Doygunluk",
        "img_exp_ai": "AI Silgi",
        "img_exp_ai_desc": "Arka planı otomatik sil.",
        "img_fmt_png": "PNG (Yüksek Kalite)",
        "img_fmt_jpg": "JPG (Düşük Boyut)",
        "img_fmt_webp": "WEBP (Web İçin)",
        "img_btn_process": "İŞLE & İNDİR",

        "bg_title": "Kusursuz <span class='text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-500'>Dekupe.</span>",
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
        
        "batch_title": "Toplu <span class='text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400'>Dönüştürücü.</span>",
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

        "dev_title": "Gücü <span class='text-emerald-400 neon-glow'>Entegre Edin.</span>",
        "dev_desc": "FileWizardIO medya motorunu REST API üzerinden kendi projelerinizde kullanın. Hemen ücretsiz bir anahtar oluşturun.",
        "dev_get_key_title": "API Anahtarı Al",
        "dev_email_label": "Şirket / Geliştirici E-postası",
        "dev_email_placeholder": "dev@sirketiniz.com",
        "dev_btn_generate": "ANAHTAR OLUŞTUR",
        "dev_quota_title": "Kota Durumu",
        "dev_key_label": "API Anahtarınız",
        "dev_key_placeholder": "API Anahtarınızı girin...",
        "dev_btn_check": "Sorgula",
        "dev_doc_title": "Dokümantasyon",
        "dev_used_quota": "Kullanılan",
        "dev_rem_quota": "Kalan Kota",
        "dev_api_desc": "Verilen bir YouTube, TikTok veya Instagram bağlantısındaki medyanın meta verilerini, başlığını ve format bilgilerini yüksek hızda çözer.",
        "dev_curl_example": "cURL Örneği",
        "dev_example_res": "Örnek Yanıt (JSON)",
        
        "wm_main_title": "Görsellerinizi <span class='text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-sky-500'>Markalayın.</span>",
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

        "footer_copy_wm": "© 2026 FileWizardIO by ForgeLogic LLC. Tüm hakları saklıdır.",
        "footer_privacy_wm": "Gizlilik Politikası",
        "footer_terms_wm": "Kullanım Koşulları",
        "wm_modal_title": "İşleniyor",
        "wm_modal_desc": "Sunucu ile iletişim kuruluyor...",
        "ai_modal_title": "İşleniyor",
        "ai_modal_desc": "Yapay zeka pikselleri analiz ediyor...",
        "batch_modal_title": "İşleniyor",
        "batch_modal_desc": "Dosyalar hazırlanıyor...",
        "cloud_modal_title": "Senkronize Ediliyor",
        "cloud_modal_desc": "Bulut bağlantısı kuruluyor...",
        "vc_modal_title": "İşleniyor",
        "vc_modal_desc": "Video analiz ediliyor..."
    },
    "en": {
        "nav_return": "Back to Home",
        "nav_home_tooltip": "Home",
        "footer_copy": "© 2026 FileWizardIO Enterprise API by ForgeLogic LLC.",
        "footer_privacy": "Privacy Policy",
        "footer_terms": "Terms of Service",
        "footer_cookies": "Cookies",
        "footer_refund": "Refund Policy",
        "footer_contact": "Contact",
        "prog_title": "Processing",
        "prog_desc": "Communicating with server...",
        
        "session_warning_title": "Session Expiring",
        "session_warning_desc": "Due to inactivity, your session will expire in <b>60</b> seconds.",
        "session_ask_continue": "Do you want to continue?",
        "session_btn_continue": "Continue",
        "session_btn_logout": "Log Out",
        "session_expired_title": "Session Expired",
        "session_expired_desc": "For your security, your session has been closed automatically.",

        "swal_missing_title": "Missing Image",
        "swal_missing_text": "Please select an image to process.",
        "swal_success_title": "Success",
        "swal_success_text": "The process was completed flawlessly.",
        "swal_error_title": "Process Failed",
        "swal_limit_title": "Limit Exceeded",
        "swal_limit_text": "You can upload a maximum of 50 files.",
        "swal_invalid_file_title": "Only image files are supported.",
        "swal_missing_batch_title": "No Files",
        "swal_missing_batch_text": "Please upload at least one image.",
        "swal_success_batch_title": "Batch Process Complete",
        "swal_success_batch_text": "Your files have been compressed and downloaded in ZIP format.",
        "swal_missing_ai_title": "Missing Image",
        "swal_missing_ai_text": "Please select an image to enhance.",
        "swal_success_ai_title": "Perfect",
        "swal_success_ai_text": "AI processing completed successfully.",
        "swal_missing_cloud_file_title": "File Missing",
        "swal_missing_cloud_file_text": "Please select the file to upload to the cloud.",
        "swal_missing_token_title": "Token Missing",
        "swal_missing_token_text": "You must enter your Dropbox access token.",
        "swal_success_cloud_title": "Uploaded to Cloud",
        "swal_success_cloud_text": "Your file was successfully sent to your Dropbox account.",
        "swal_missing_email_text": "Please enter a valid email address.",
        "swal_success_key_title": "Your API Key is Ready",
        "swal_success_key_text": "Please copy your key to a safe place.",
        "swal_missing_key_title": "Missing Information",
        "swal_missing_key_text": "Please enter your API key to check.",
        "swal_missing_file_title": "Missing File",
        "swal_missing_file_text": "Please upload both the base image and your logo.",
        "swal_success_wm_text": "Watermarking completed successfully.",
        "swal_missing_vc_title": "Video Missing",
        "swal_missing_vc_text": "Please upload a video to compress.",
        "swal_success_vc_text": "Your video has been successfully compressed and downloaded.",

        // NEW PAYWALL TRANSLATIONS
        "swal_auth_required_title": "Premium Locked",
        "swal_auth_required_text": "You must create an account and upgrade to PRO ($9.99/Mo) to access this tool.",

        "header_login": "Login",
        "header_register": "Sign Up",
        "header_upgrade": "Upgrade",
        "auth_login_title": "Welcome Back",
        "auth_login_desc": "Login to your FileWizardIO account.",
        "auth_email_label": "Email Address",
        "auth_email_placeholder": "example@mail.com",
        "auth_pass_label": "Password",
        "auth_pass_placeholder": "••••••••",
        "auth_pass_reg_placeholder": "At least 6 characters",
        "auth_login_btn": "Sign In",
        "auth_or_with": "Or Continue With",
        "auth_no_account": "Don't have an account?",
        "auth_register_link": "Sign Up Now",
        "auth_reg_title": "Create Account",
        "auth_reg_desc": "Join us for unlimited tools.",
        "auth_reg_btn": "Sign Up for Free",
        "auth_quick_reg": "Quick Register",
        "auth_has_account": "Already have an account?",
        "auth_login_link": "Log In",
        
        "upg_title": "Upgrade to PRO",
        "upg_desc": "Go Premium for AI tools and unlimited compression.",
        "upg_f1": "Unlimited Video Compression (Never crashes)",
        "upg_f2": "AI Background Remover",
        "upg_f3": "Artificial Intelligence Studio",
        "upg_f4": "Priority Server Processing",
        "upg_btn": "Get PRO Now ($9.99/Mo)",
        
        "home_nav_media": "Media Backup",
        "home_nav_image": "Image Studio",
        "home_nav_pdf": "PDF Tools",
        "home_nav_premium": "PREMIUM TOOLS",
        "home_nav_batch": "Batch Processing",
        "home_nav_bg": "BG Remover",
        "home_nav_ai": "AI Studio",
        "home_nav_cloud": "Cloud Sync",
        "home_nav_wm": "Watermark",
        "home_nav_vc": "Video Compressor",
        "home_nav_pricing": "Pricing",
        "home_nav_api": "Developer API",
        "home_support_title": "Need help?",
        "home_support_btn": "Support Team",
        
        "home_hero_title": "Professional.",
        "home_hero_desc": "Securely back up your content and <span class='text-white font-bold'>build your personal archive.</span>",
        "home_input_placeholder": "Paste media link here...",
        "home_btn_paste": "PASTE",
        "home_btn_fetch": "<i class='fa-solid fa-cloud-arrow-down text-indigo-600'></i> Prepare Media",
        "home_btn_mp4": "Save Archive (MP4)",
        "home_btn_mp3": "Backup Audio (MP3)",
        
        "home_pdf_edit_title": "Live Edit",
        "home_pdf_edit_desc": "Rotate, delete, or reorder pages. Visual editor.",
        "home_pdf_merge_title": "Merge PDF",
        "home_pdf_merge_desc": "Combine multiple PDF files into one.",
        "home_pdf_compress_title": "Compress PDF",
        "home_pdf_compress_desc": "Reduce file size up to 80% while keeping quality.",
        "home_pdf_drop": "Drop files here",
        "home_pdf_btn_select": "Select File",
        "pdf_btn_back": "<i class='fa-solid fa-arrow-left'></i> Go Back",

        "img_btn_upload": "Upload Image",
        "img_placeholder": "Select an image to edit",
        "img_tab_crop": "CROP",
        "img_tab_filter": "FILTER",
        "img_tab_adjust": "ADJUST",
        "img_tab_export": "EXPORT",
        "img_crop_free": "Free",
        "img_crop_square": "1:1 Square",
        "img_crop_yt": "16:9 YT",
        "img_crop_story": "9:16 Story",
        "img_crop_insta": "4:5 Insta",
        "img_filter_normal": "Normal",
        "img_filter_bw": "B&W",
        "img_filter_sepia": "Sepia",
        "img_filter_vintage": "Vintage",
        "img_adj_bright": "Brightness",
        "img_adj_contrast": "Contrast",
        "img_adj_sat": "Saturation",
        "img_exp_ai": "AI Eraser",
        "img_exp_ai_desc": "Automatically remove background.",
        "img_fmt_png": "PNG (High Quality)",
        "img_fmt_jpg": "JPG (Lower Size)",
        "img_fmt_webp": "WEBP (For Web)",
        "img_btn_process": "PROCESS & DOWNLOAD",

        "bg_title": "Flawless <span class='text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-500'>Cutout.</span>",
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

        "batch_title": "Bulk <span class='text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400'>Converter.</span>",
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

        "dev_title": "<span class='text-emerald-400 neon-glow'>Integrate</span> the Power.",
        "dev_desc": "Connect the FileWizard engine to your own applications. Set up your automation processes in seconds.",
        "dev_get_key_title": "Get API Key",
        "dev_email_label": "Company / Developer Email",
        "dev_email_placeholder": "company@domain.com",
        "dev_btn_generate": "GENERATE KEY",
        "dev_quota_title": "Quota Status",
        "dev_key_label": "Your API Key",
        "dev_key_placeholder": "Enter your API Key...",
        "dev_btn_check": "Check Quota",
        "dev_doc_title": "Documentation",
        "dev_used_quota": "Used",
        "dev_rem_quota": "Remaining",
        "dev_api_desc": "Resolves metadata, title, and format information of media from a given YouTube, TikTok, or Instagram link at high speed.",
        "dev_curl_example": "cURL Example",
        "dev_example_res": "Example Response (JSON)",
        
        "wm_main_title": "Brand Your <span class='text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-sky-500'>Images.</span>",
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

        "footer_copy_wm": "© 2026 FileWizardIO by ForgeLogic LLC. All rights reserved.",
        "footer_privacy_wm": "Privacy Policy",
        "footer_terms_wm": "Terms of Use",
        "wm_modal_title": "Processing",
        "wm_modal_desc": "Communicating with server...",
        "ai_modal_title": "Processing",
        "ai_modal_desc": "AI is analyzing pixels...",
        "batch_modal_title": "Processing",
        "batch_modal_desc": "Preparing files...",
        "cloud_modal_title": "Syncing",
        "cloud_modal_desc": "Establishing cloud connection...",
        "vc_modal_title": "Processing",
        "vc_modal_desc": "Analyzing video..."
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
    
    const placeholders = document.querySelectorAll("[data-i18n-placeholder]");
    placeholders.forEach(el => {
        const key = el.getAttribute("data-i18n-placeholder");
        if (translations[window.CURRENT_LANG] && translations[window.CURRENT_LANG][key]) {
            el.setAttribute("placeholder", translations[window.CURRENT_LANG][key]);
        }
    });

    const titles = document.querySelectorAll("[data-i18n-title]");
    titles.forEach(el => {
        const key = el.getAttribute("data-i18n-title");
        if (translations[window.CURRENT_LANG] && translations[window.CURRENT_LANG][key]) {
            el.setAttribute("title", translations[window.CURRENT_LANG][key]);
        }
    });
});