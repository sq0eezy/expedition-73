---
status: Validating
updated: "2026-10-21"
review_summary: "İsteğe bağlı Docker ve ortak geliştirme/ZIP paketinin gerçek yerel kontrolleri."
change_summary: "Windows ve Linux AMD64/ARM64 emülasyonunda 171 test + 8 JS testi; Docker önizlemesi 22 Chrome senaryosu ve HTTP smoke ile doğrulandı."
---
# Geliştirme paketi · Gerçek kontrol kaydı

2026-10-21, M1 dalı. M1 büyük bir paketle devam istedi; [Docker/native kullanım, ortak kontrol ve ZIP](../guide/DEV_PACKAGE.md) bu teknik kapsamla hazırlandı. Nihai yığın/hosting veya bilimsel profil seçimi değildir. Başlangıçta temiz dal `6047c42`, fetch sonrası main/M2 hâlâ `a1a83d5`; yeni ekip katkısı yoktu. M2’nin 2026-10-19 notları dikkate alındı, onun adına yeni tercih/inceleme kaydı yazılmadı.

## Uygulananlar

- `scripts/workspace.py`: doctor/setup/check/build/preview/package/verify-package. Kontrol, bağımlılık veya alt komut hatasında durur; eksik NetCDF/Node ile kısmi başarı raporlamaz. A/B akışlarının geçici klasörü temizlenir; kaynak/saklı özel artifacts değiştirilmez.
- Windows CMD ve Mac POSIX başlatıcıları; normal serve varsayılanı localhost, Docker için açık bind parametresi. `.mjs` JavaScript MIME düzeltmesi korundu.
- Resmi çok mimarili index digest'lerine sabit iki aşamalı Docker hedefi: analiz/test ve yalnız statik önizleme. On pip paketinin sürümleri kilitli; `.dockerignore` dar izin listesi. Compose açık boş env dosyası kullanır; özel Earthdata .env verilmez. Son önizleme imajında Node/NetCDF/analiz kodu yok.
- Yalnız beş genel dosya + manifest içeren deterministik demo ZIP'i, SHA-256 bütünlük denetimi; ZIP çıkarma yok. Yedi yeni Python testi: izin listesi/özel alan dışlama, aynı girdide tekrar, bozulma, ek/yinelenen/üst-dizin girdisi, hedef sınırı, hatalı derlemede eski paketi koruma ve hata durdurma.
- Native Windows/Mac/Ubuntu ve Docker AMD64/QEMU ARM64 için CI matrisi; ortak komutlar, yalnız ZIP artifact'i, yedi gün saklama. Workflow hazırlandı, bu oturumda GitHub'a gönderilip uzakta koşturulmadı.

## Gerçek koşular

| Ortam / komut | Sonuç |
|---|---|
| Windows / Python 3.12.14 · `analysis/.venv` Python ile `scripts/workspace.py check` | **171 test / 73,631 s / OK**, 0 skipped; ardından gerçek nokta/alan/fraksiyon ve A/B beş düğümlü akışlar, 8 JS testi ve builder başarılı |
| Linux AMD64 / Python 3.12.15 · Compose `run --rm --build checks` | **171 test / 36,180 s / OK**, gerçek replay/akışlar, **8 JS testi / 127,693 ms**, JS syntax ve builder başarılı; runtime network none, read_only, UID 10001 |
| Linux ARM64 / Python 3.12.15 · AMD64 Windows üzerinde QEMU emülasyonu | **171 test / 611,289 s / OK**, 0 skipped; gerçek nokta/alan/fraksiyon/A/B akışları, **8 JS testi / 3319,944 ms**, syntax ve builder başarılı; ağsız/read_only/UID 10001 |
| Windows `workspace.py setup` | Kilitli on paketin tümü zaten kurulu; sürüm/global Python veya .env değiştirilmedi |
| Windows `scripts/start-preview.cmd --port 8874` | Kayıtlı build ve HTTP sunucu açıldı; beş genel dosya/MIME/null kaynak yolları smoke kontrolü geçti; kapatıldı |
| Mac başlatıcısı | Git Bash `-n` sözdizimi geçti; gerçek macOS başlatıcı çalıştırması yapılmadı |
| Docker statik önizleme · port 8873 | Compose healthy; HTTP 200, JS MIME, kayıtlı veri sözleşmesi, `.env` ve analiz/sunucu kaynak yolları 404 |
| Docker HTTP üzerinde Playwright / yüklü Chrome headless | **22 senaryo grubu**, JS hatası 0, dış origin runtime isteği 0; masaüstü 1440×1100/mobil 390×844, taşma yok |
| Ayrı demo dosyalarıyla yerel HTTP | ZIP içindeki beş dosya doğrulanmış izin listesiyle sahip olunan geçici klasöre kopyalandı; MIME ayarlı stdlib HTTP smoke geçti, sunucu/klasör kapatıldı |
| Demo paketi üretme + `verify-package` | 297.997 byte; beş dosya + manifest, doğrulandı. SHA-256: `879341571720ed282917f1fc11e2870c1916e4701f73a620fbfdadf558fb8ab2` |
| Workflow YAML / Compose config | YAML ayrıştırıldı; Compose config --quiet başarılı |

Python testlerindeki eski NumPy deprecation uyarısı hata üretmedi. Yinelenen ZIP girdisi testinde beklenen UserWarning oluştu; bozuk arşiv doğrulaması reddedildi. Bu test başarısı bilimsel maske/alan ölçüsü kabulü değildir.

## İmaj ve kaynak sınırı

Python index digest: `sha256:5d9e6adc9abd558bc0ce05f9ab16cef71328916fc9728f6b81e337af86a737e2`; Node index: `sha256:91acba91b842bec0bf7ea6f5e09c644c7ccad72c4996ed9616d861d1c7cd60d4`. Resmi registry manifestlerinde AMD64/ARM64 bildirimi görüldü; bu bildirim tek başına çalışma kanıtı sayılmadı. Docker Desktop 4.47.0 / Linux Engine 28.4.0 başlangıçta kapalıydı; CLI ile başlatıldı. İlk sandbox probe'undaki config erişim reddi sonrası izinli Docker CLI ile kontrol edildi; config/token içeriği gösterilmedi.

Docker runtime kontrolleri UID 10001, token env anahtarının/.env dosyasının yokluğu ve preview'de analiz kaynaklarının bulunmadığını doğruladı. NASA API isteği veya Earthdata token okuma yapılmadı. Build aşaması yalnız resmi imaj/pip paketleri için internet kullandı. Kayıtlı `analysis/examples` dosyaları değiştirilmedi.

Docker QA önizleme projesi `down --remove-orphans` ile kapatıldı; Windows başlatıcı oturumu da durduruldu. 8873 ve 8874 portlarının artık yanıt vermediği doğrulandı. Diğer Docker projeleri silinmedi. Codex açma isteği queued döndü; gerçek tarayıcı QA bağımsız Chrome ile tamamlandı. İncelenen ekran görüntüleri ve ZIP Git dışında `web/artifacts` altındadır.

ARM64 hedefi yalnız test/build imajı olarak emülasyonla koşturuldu; ayrı ARM64 önizleme hizmeti/gerçek Apple Silicon Mac test edilmedi. CI bu önizleme adımını da içerir, fakat henüz uzakta koşmadı.

Yeni kod henüz GitHub/main/Pages'e gönderilmedi; uzak CI, gerçek Mac veya M2 kabulü iddia edilmez. ZIP hash kontrolü kaynak kimliği/dijital imza değildir. Docker kullanımı bilimin uygunluğunu veya nihai web barındırmasını belirlemez; maske/sınır/uzun dönem kararları açık.
