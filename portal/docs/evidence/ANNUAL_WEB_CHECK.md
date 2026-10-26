---
status: Validating
updated: "2026-10-26"
review_summary: "Yıllık Python aday sonuçlarının aynı aylık kaynağa bağlanarak webde gösterilmesi."
change_summary: "222 Windows/43 JS/76 Chrome geçti; yedi dosya/manifest 0.4.0, exact kaynak bağı ve eski paket desteği var. Paylaşım durumu SYNC'te ayrılır."
---
# Yıllık aday web ekranı · Gerçek kontrol

2026-10-26, Windows/analysis kendi venv Python, Node ve kurulu Chrome headless. Başlangıç temiz 1a59620, codex/m1-modules-region-a, dokuz yerel commit. Ekip/durum/fikir/devir/pano okundu; fetch sonrası main a1a83d5, uzak M1/M2 6047c42, yeni katkı yok. Kullanıcı devam ve GitHub'a gönderme istedi; hedef mevcut M1 geliştirme dalı, main/Pages değil. [Kullanım/sözleşme](../guide/ANNUAL_WEB.md).

## Gerçek derleme ve kontroller

Yıllık adaylar yeni bilimsel formül eklenmeden annual_weighting.run ile tekrarlandı. Her yılın sıcaklık kaynak byte hash'leri aylık snapshot'la eşleşti. Aylık katalog korunur; yeni data/annual.json exact katalog SHA-256 bağıyla ayrı sunulur. Yeni web zarfı 0.1.0, mevcut aday rapor 0.1.0; yedi genel dosya, manifest 0.4.0. Önceki manifest sürümleri için ayrı allowlist korunur.

Hedef Python `tests.test_annual_web tests.test_workspace`: **15 test / 69,233 s** geçti; gerçek 48 aday yıl/stored rapor eşleşmesi, kaynak/yıl/kimlik uyumsuzluğu, eski kayıtta açık yokluk, hatalı yıllık derlemede önceki çıktının korunması ve paket bağları sınandı. Yeni test sayısı mevcut suite'e altıdır; burada eski paket testleri de tekrarlandı.

Node karşılaştırma/akış testleri: **43 / 529,5573 ms** geçti. Yeni adaptör testleri kaydedilmiş yıllık sonuçları, katalog/yıllık dosya kaynağını, aday/seçimsiz bayraklarını, artık yıl ağırlıklarını ve null/kapsam ilişkisini denetler. Küçük teknik yüzey alias'ları maskeli bilimsel kanıt değildir; adaptör yıllık sıcaklık ortalamalarını JS'de yeniden hesaplamaz.

`node web/tests/browser.cjs`: **76 Chrome senaryo grubu**, JS hatası 0/dış runtime isteği 0. İki pencerede seçilen yıl kartları ve bütün 24 yılın tablosu gerçek Python raporlarıyla eşleşti. Üst yıl/rapor bağlantısı, tablo yıl düğmesinde Enter/odak ve açık details korunumu, tek/boş pencere ve kara/buz kapsamında kartların kapanması denetlendi. Dosya 503, farklı katalog/hash, farklı kaynak dosyası veya kabul edilmiş yöntem iddiası yıllık bölümü kapatırken aylık ekran kaldı. Web Crypto yokluğunda da aylık grafik kullanılabilir kaldı.

Sentetik 2024 Ocak eksikliğinde iki yıllık aday “Veri yok” kaldı, mevcut API yıllık referansı ayrı gösterildi; bu gerçek kayıttaki eksiklik veya ham NASA doğrulaması değildir. Gerçek kayıtlarda 24'er tam yıl vardır. 1440×1100 ve 390×844 viewport görüntüleri annual-desktop.png / annual-mobile.png incelendi, yatay taşma yok. Gerçek telefon/Mac koşusu değildir; screenshot'lar ignored web/artifacts içindedir.

Son `scripts/workspace.py check`: **222 test / 353,722 s**, OK, 0 atlanan/hata; gerçek eski/yeni A-B kaynak tekrarları, iki aday yıllık rapor tekrarları, **43 JS / 754,0393 ms**, syntax ve son yedi dosyalı builder geçti. Tam komut exit 0, ignored analysis/artifacts/annual-web-final-check.log ve exit kaydında tutulur. NumPy deprecation/kasıtlı duplicate ZIP uyarısı dışında kontrol hatası yok.

Son `scripts/workspace.py package` **6.964.481 byte**, SHA-256 `59f8831c2adb97b8f840ef55fb36718c24389a2198784c7253d67c15aca1b13e` ZIP üretti/doğruladı. Yedi dosya son build ile byte aynı; önceki gerçek altı dosyalı 0.3.0 ZIP de verifier ile geçti. İki ZIP'in data/results.json byte'ları aynı. data/annual.json **192.379 byte**, SHA-256 `c6b366f27a252432130691b47740615cb52d787e60ea7fdc69a7d8f1dc25ab1c`. Paket ignored web/artifacts içindedir; GitHub'a source ile generated ZIP yüklenmez. Ayrı son ZIP iki kez üretilmiş sayılmaz; builder tekrarlanabilirliği mevcut testte kontrol edildi.

Yerel HTTP smoke yedi dosya/annual-monthly hash bağı/.mjs MIME ve özel-kaynak yollarının 404 sonucuyla geçti. Son kapsam metinleri ayrıca hedef Chrome kontrolünde incelendi, 1440/390 px görseller yenilendi; bu ayrı kontrol yeni bir tam 76 senaryo koşusu diye sayılmaz. open_in_codex queued döndü; görünür açılış teyidi değildir. Son paket ve portal sonuçları aşağıda ayrıca kaydedilir.

## Bilimsel ve paylaşım sınırı

Maskesiz yıllık adaylar seçilmiş politika değildir; kaynak yıllık hücreleri aynı NASA/MERRA-2 ürününden gelir ve bağımsız doğruluk ölçümü değildir. Yeni bilimsel formül, maske, kesin dönem, anomali/eğilim/p-değeri veya M2 kabulü yok. Beş düğümlü aylık yüzey motoru değişmedi. Yeni Docker/Mac/Linux/ARM64 koşusu bu yerel kanıt değildir; GitHub CI durumu gözlenirse ayrıca belirtilir. Gönderim sonucu [SYNC](../team/SYNC.md) kaydına bağlanır. QA sunucusu final öncesi kapatılır.
