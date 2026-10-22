---
status: Validating
updated: "2026-10-22"
review_summary: "Kaynak byte kimliği, yeniden hesaplama ve seçimleri yalnız doğrulama sonrası uygulama."
change_summary: "180 Windows analiz/gerçek A-B, 30 JS ve 42 Chrome senaryosu geçti; kaynak veri ve bilimsel profil değişmedi."
---
# Karşılaştırma raporu · Gerçek kontrol

M1 devam istedi. Durum/harita, iki üye, fikir/devir/pano/sync okundu. Temiz başlangıç `fdaf166`; fetch sonrası uzak M1 `6047c42`, main/M2 `a1a83d5`, yeni katkı yok. M2'nin macOS/B kaydı okundu; yeni ekran/rapor/ortam veya bilimsel politika kabulü çıkarılmadı.

[Esas kullanım ve sözleşme](../guide/COMPARISON_REVIEW.md): tam web JSON byte SHA-256 kimliği, çift/yön/ay/yüzey, context/hedef tanım kimlikleri ve mevcut fonksiyonla yeniden hesaplanan bütün alanlar eşleşir. Yalnız doğrulamadan sonra seçimler uygulanır; farklı snapshot/bozuk içerikte korunur. Daha yeni dosya okuması veya kaynak sayfası yüklemesi eski asenkron okumanın seçim uygulamasını engeller. Anahtar sırası değişebilir; bu rapor byte imzası değildir. Dosya yüklenmez/loglanmaz; 128 KiB sınırı ve Web Crypto yoksa yalnız raporları kapatma yolu vardır.

Yeni rapor/karşılaştırma 0.1.0; web 0.3.0, altı genel dosya, manifest 0.2.0, analiz/motor/teknik profil değişmedi. Genel JSON indirme korundu. Kaynak data/results.json önceki ZIP ile byte aynı.

## Gerçek kontroller · 2026-10-22

- Windows/Python 3.12.14, `analysis\.venv\Scripts\python.exe scripts/workspace.py check`: **180 test / 20,711 s**, atlama/hata yok. Gerçek A/B nokta/uyum, A alan/B tiled-window (2 tile/5 tekrar/55 hücre), 56/55 fraksiyon replay ve iki gerçek 5 düğümlü akış geçti. Mevcut NetCDF/NumPy deprecation ve bilerek bozuk ZIP uyarıları çıktı; başarısız test yok.
- Aynı komutta **30 JS testi / 184,479 ms**, üç JS syntax kontrolü ve builder geçti. Sekiz yeni test: bilinen SHA-256 vektörü/byte ve boyut sınırı, yön/ay/politika/context round trip, sonuç/kaynak/seçim/sürüm/ek alan/onay bozulması, farklı snapshot, anahtar sırası, geçersiz kayıt/seçim, eksik çiftlerin null kalması ve özel alanların dışlanması.
- Kurulu Chrome headless/Playwright ile `node web/tests/browser.cjs`: **42 senaryo grubu**, JS hatası/dış runtime isteği 0, ana sayfada GET dışı runtime isteği yok. Gerçek B−A/kara+buz/Ekim raporu indirildi; kaynak hash'i bağımsız Node SHA-256 ile eşleşti. Ekim farkı -24,55507353066377 °C. İki pencere gizlenip raporla seçimler geri açıldı; aynı dosya yeniden seçildi. Bozuk sonuç/hash/seçim/onay/ek alan/JSON ve büyük dosyada seçimler değişmedi. Yalnız görünen ad değiştiğinde bile farklı byte snapshot'ında eski rapor reddedildi. Web Crypto olmadan grafikler çalıştı ve rapor düğmeleri kapandı. 1440×1100 ve 390×844 görüntüler incelendi; yatay taşma yok.
- Gerçek üç politikanın B−A/Ekim raporu ayrıca create + JSON serialization + verify ile doğrulandı; her biri 12/12 geçerli çift. Kaynak SHA-256 `d4ce2e87783af79ccee855a6a8040845cfd19776a405b52dc829c88c766e7169`. 4.619 byte örnek yalnız ignored web/artifacts altında, yeni genel örnek değildir.
- HTTP smoke: altı dosya 200, .mjs JavaScript MIME, .env/analiz kaynağı yolları 404. Codex panel açma çağrısı queued; kullanıcının sayfayı gördüğü varsayılmadı.
- Demo iki kez paketlendi: **341.998 byte**, SHA-256 `fae25cc92a5b49b150ba0e1c0d679dde6cdb9b25961d2c92e722ddd6024b75ba`; aynı byte/hash ve manifest doğrulandı. Rapor/özel artifacts eklenmedi; yalnız altı genel dosya.

## Sınırlar ve teslim

Doğrulama normalleştirilmiş kaydın JS farkını tekrarlar; NASA ham dönüşümü, bilimsel kalite veya yazar kimliğini doğrulamaz. Yeni tutarlı rapor üretilebilir; SHA-256 imza/bilimsel onay değildir. Bilimsel maske/sınır/uzun dönem ve nihai yığın/hosting açık. Kalıcı cache/iş kuyruğu/sunucu depolaması/otomatik ekip senkronizasyonu eklenmedi.

Yeni Mac/Docker/Linux/ARM64/uzak CI koşusu yok. U-02/D-02 Validating, [H-M1-017](../team/HANDOFFS.md) panel içi inceleme; M2 kabulü değil. Yerel M1 dalında; push/main/Pages/Sites veya dış mesaj yok. Portal kontrolleri bilimsel analiz kabulü değildir.

QA sunucusu kapatıldı; 8873 TCP bağlantısı kapalı doğrulandı. Örneklerde Git farkı yok, diff --check ve portal içerik kontrolü geçti. Yeniden açma komutları rapor kılavuzundadır.
