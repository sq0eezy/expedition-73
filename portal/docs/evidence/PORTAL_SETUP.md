# Portal kurulumu ve doğrulama

**Tarih:** 2026-10-15 · **Ortam:** Windows, PowerShell, Python 3.12.14.

## Kaynak ve kapsam

Project Context Portal'ın `eae414b8e5a920cffb6409255318491969edaa3a` commit'i alındı. Proje belgeleri, Türkçe gezinme ve sabit proje kimliği uyarlandı. Python/JavaScript motoru değiştirilmedi. Bağımlılıklar yalnızca `portal/.venv` içine kuruldu.

## Gerçek kontroller

Komutlar `portal/` klasöründen çalıştırıldı:

| Yöntem / komut | Sonuç |
|---|---|
| Python 3.12.14 ile `scripts/portal.py setup` | Yerel `.venv` kurulumu tamamlandı |
| `.venv/Scripts/python.exe scripts/portal.py check` | Yerel bağlantı, durum, gezinme ve token kontrolleri geçti |
| `.venv/Scripts/python.exe scripts/portal.py build` | Strict MkDocs derlemesi başarılı |
| `.venv/Scripts/python.exe -m unittest discover -s tests -v` | 29 kaynak araç testi geçti |
| `node tests/test_reader_core.cjs` | 12 okuma mantığı testi geçti |
| `.venv/Scripts/python.exe scripts/portal.py serve` | `127.0.0.1:8000` üzerinde foreground sunucu başladı |
| PowerShell `Invoke-WebRequest` ile aşağıdaki yollar | 12 isteğin tümü HTTP 200 |
| `Invoke-RestMethod` ile okuma kataloğu | Proje kimliği doğru; 33 belge sayfası |
| Depo kökünde `git diff --check` | İzlenen dosyalarda boşluk hatası yok |
| `git check-ignore` ile `.venv`, `site`, `.portal` örnekleri | Yerel çıktılar Git dışında |

HTTP yolları: `/`, `/control-center/`, `/product/`, `/architecture/`, `/architecture/SYSTEM_MAP/`, `/planning/`, `/planning/WORK_BOARD/`, `/decisions/`, `/evidence/`, `/discovery/IDEA_COMPARISON/`, `/review/`, `/assets/reader/catalog.json`.

## Tarayıcı gözlemi

Codex uygulama içi tarayıcıda başlangıç sayfası açıldı: Türkçe içerik, doğru keşif aşaması ve Türkçe okuma kontrolleri görüldü. Sistem haritasının Mermaid diyagramı çizildi; konsol sorgusunda hata/uyarı görülmedi. İnceleme merkezinde katalog, Türkçe seçenekler ve başlangıç kaydı olmayan ilk kullanım durumu görüldü. Kişisel okuma işaretleri veya başlangıç karşılaştırması değiştirilmedi. Başlangıç görünümü yerel, Git dışında kalan `.portal/preview.png` dosyasına kaydedildi.

Sunucu terminal açıkken çalışır; Ctrl+C ile durdurulur. Yeniden açmak için aynı `serve` komutu kullanılır. Kalıcı hizmet kurulmadı.

## Sınırlama

Bu kayıt yalnızca portal içindir. Ayrı mobil cihaz, tüm tarayıcı depolama hata durumları veya tüm dış bağlantılar bu oturumda uçtan uca sınanmadı. NASA sayısal verisi indirilmedi ve uygulama davranışı doğrulanmadı. Kaynak sayfası incelemesi [araştırmada](../research/DATA_SOURCES.md) kayıtlıdır.
