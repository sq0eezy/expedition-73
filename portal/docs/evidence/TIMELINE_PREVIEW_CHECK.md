---
status: Validating
updated: "2026-10-26"
review_summary: "Mevcut 24 yıllık kaydın aylık grafik/tablo ve tek yıl ayrıntılarıyla eşleşmesi."
change_summary: "201 Windows analiz/37 JS/65 Chrome ve son paket kontrolü geçti; kaynak byte'ları ve bilimsel hesap aynı."
---
# Uzun dönem görünümü · Gerçek kontrol

Tarih 2026-10-26, Windows, analysis kendi .venv Python, Node ve kurulu Chrome headless. Başlangıç temiz c9e7d9c, codex/m1-modules-region-a; ekip/durum/fikir/devir/pano okundu. Fetch sonrası main a1a83d5, uzak M1/M2 6047c42; yeni katkı yok. [Kullanım ve yorum sınırı](../guide/T2M_TIMELINE.md).

## Uygulanan

Mevcut comparison.mjs içinde recordedMonthlyHistory yıllık kaynakların aylarını aynen birleştirir; kaynak/sınır/grid/alan/ağırlık/zaman/işlem sözleşmesi eşleşmesini pencere bazında denetler. Kara seçeneklerinde kullanılan fraksiyon kayıtları da eşleşmelidir. Tam kaynak/uygunluk sağlanmadan kısmi uzun dönem çizgisi verilmez. Ayrı grafik, 288 satırlık tablo, ortak pencere/yüzey, odak koruyan ay kaydırıcısı ve mevcut yıl/ay/raporlarla iki yönlü tarih bağlantısı hazırdır. Yıllık kaynaklar/hesap motoru/bilimsel yöntem değiştirilmedi.

## Yerel kontroller

`node --test web/tests/comparison.test.mjs web/tests/trace.test.mjs`: **37 test / 274,7103 ms** geçti. Yedi yeni test exact değer/input korunumu, sıfır/null ve yıl sınırları, bozuk/eksik/sırasız yıllar, kaynak/sınır/zaman/hücre/işlem farkı, tüketilen yüzey bağımlılığı, kullanılmayan değişiklikler ve gerçek A/B parent kayıtlarındaki 288 maskesiz değerin aynen aktarılmasını denetler. Yeni küçük metadata/politika fixture'ları teknik ve sentetiktir; gerçek maske hesabı kanıtı değildir.

Yerel web/serve.py ve optional Playwright ile `node web/tests/browser.cjs`: **65 senaryo grubu**, JS hatası 0/dış runtime isteği 0. Gerçek 24 yıllık katalogda üç politika × iki pencere × 288 değer, tablodaki altı ondalık biçimiyle eşleşti; path kayıt/geçerli sayıları 288. Yıllar boyunca çizilen değerlerde yeni ortalama/seyreltme yok. Önceki rapor/hücre/akış/yıl seçimi senaryoları da geçti.

End/sağ ok ile yıl sınırından geçiş, odağın korunması, üst yıl/aydan işaretçi güncelleme, eski rapordan doğru uzun dönem aya dönme, boş/tek pencere, policy değişimi ve uyumsuz tek pencereyi kaldırınca kalan pencerenin çalışması denetlendi. Sentetik Aralık 2001/Ocak 2002 eksikliği A çizgisini iki parçaya ayırdı; 286/288 ve “Veri yok” görüldü. Gerçek kayıtlarda bu eksiklik yok; yapay tarayıcı denemesidir. Fraksiyon sürüm farkı maskeli geçmişi engelledi, maskesizi engellemedi; işlem sürümü farkında uzun dönem kapanırken yıllık ekran kaldı.

İlk tarayıcı denemesinde kapalı details içindeki innerText boş döndüğü için test, tabloyu kullanıcı gibi açacak şekilde düzeltildi; son tam koşu yukarıda başarılıdır. 1440×1100 / 390×844 viewport, history-desktop.png ve history-mobile.png görüntüleri incelendi; yatay taşma yok. Dosyalar ignored web/artifacts içinde; gerçek telefon/Mac doğrulaması değildir.

`analysis` kendi venv Python ile depo kökünden `scripts/workspace.py check`: **201 Windows analiz testi**, nokta/alignment/A alan/B tile, eski iki yıllık ve yeni 24 yıllık A/B replay, gerçek fraksiyon dönüşümleri ve iki beş düğümlü akış geçti. Ardından **37 JS / 196,2855 ms**, syntax ve son tam builder başarılı. NumPy deprecation ve kasıtlı duplicate ZIP test uyarısı sonuçları etkilemedi. Analiz test sayısı değişmedi; kaynak hesabı değişmeden mevcut tam suite yeniden çalıştırıldı.

`scripts/workspace.py package` son kaynakları yeniden derledi; **6.754.353 byte** ZIP, SHA-256 `18cd20f004c67233bd1d9f966e675f4d0bb81f8d18aa7ca5a90f08e3f1436978` doğrulandı. Önceki gerçek 24 yıllık ZIP de verifier ile geçti; yeni ZIP'teki altı dosya son build ile byte aynı. İki ZIP'in data/results.json byte'ları eşleşti. Paket ignored web/artifacts içinde, yayımlanmadı. Yeni ayrı son ZIP iki kez üretilmiş sayılmaz; mevcut analiz suite builder tekrarlanabilirliğini ayrıca denetler.

## Korunan kayıt ve paylaşım

data/results.json **6.649.872 byte**, SHA-256 `58cbad9e6951c648501a33a9f0bda71e589d09dd6bfb38f3de1727498ed75fdb`; yeni geliştirmeden önceki katalogla aynıdır. Web 0.4.0/annual 0.3.0/rapor 0.1.0/manifest 0.3.0 ve altı genel dosya korunur. Mevcut raw fixture'lar/satır sonları değişmedi. Yeni API/token isteği, istatistik/yıllık özet/anomali/eğilim veya bilimsel profil kabulü yok. Yeni Mac/Linux/Docker/ARM64/uzak CI çalıştırılmadı. T-02/U-02/H-M1-020 yerel M1 incelemesi; M2 kabulü veya R-A05/R-B05 analiz tamamlanması değil. Push/main/Pages/Sites/dış mesaj yok.

QA sunucusu durduruldu; 8873 TCP bağlantısı kapalı doğrulandı. open_in_codex queued döndü; kullanıcıya görünür açılış teyidi değildir. Yeniden açma komutları kılavuzda. Portal kendi venv Python ile `portal/scripts/portal.py check` geçti; bu içerik/bağlantı doğrulamasıdır, NASA bilimsel sonucu değildir.
