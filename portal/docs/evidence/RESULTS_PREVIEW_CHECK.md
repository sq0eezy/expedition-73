---
status: Validating
updated: "2026-10-19"
review_summary: "Kayıtlı gerçek verili ilk web ekranının Python, HTTP ve gerçek Chrome kontrolleri."
change_summary: "162 analiz testi, gerçek veri tekrarları ve on tarayıcı senaryosu geçti; mobil/masaüstü görüntüler incelendi."
---
# İlk sonuç ekranı · Gerçek doğrulama

**Tarih/ortam:** 2026-10-19, Windows, analysis Python 3.12.14, yüklü Chrome'un headless çalıştırması. M1 devam talebi, kendi dalı. Fetch'te main/M2 değişimi yok; `4759a51` ve `c0c79e2` yerel commit'leri korundu. Bu oturumda yeni NASA isteği/token okuma veya Git push/main/Pages yayını yapılmadı. [Esas ürün kaydı](../product/RESULTS_PREVIEW.md).

## Girdi ve derleme

`web/regions.json` mevcut A/B pencere ve fraksiyon kayıtlarını seçti. `analysis/scripts/build_web_preview.py` ile kaynaklar yeniden hesaplandı; metadata hash'i aynı snapshot ile eşleşti. Builder dört dosya üretti: index.html, styles.css, app.js, data/results.json. Yalnız kayıtlı toplu veriler; canlı NASA isteği yok. Kaynak JSON, çıktının aday durumunu ve inference_performed=false alanını korur. Ham kaynak hash'leri mevcut kanıtlara bağlıdır.

**Python:** analysis sanal ortamında `-m unittest discover -s tests`: **162 test / 16,218 saniye, başarılı.** Dokuz yeni veri aktarımı/uygunluk testi: gerçek seri/kaynak eşitliği, tek B kaydıyla genişletilebilirlik, geçersiz registry/kimlik, yol kapsamı, ağ-token kullanmama, replay sonrası metadata değişimi, zaman standardı/sağlayıcı sürümü uyumsuzluğu, başarısız kaynak/dönemde kısmi yeni çıktı üretmeme ve sadece dört genel dosyanın tekrar üretimi. İki nokta validate, A pencere, B parçalı pencere, A/B fraksiyon replay'leri geçti. Eski NumPy deprecation uyarısı hata üretmedi.

## HTTP ve tarayıcı

Yerel loopback HTTP adresi `http://127.0.0.1:8873/` **200** döndürdü; tarayıcı paneline açma isteği iletildi (uygulama `queued` döndürdü). Gerçek browser QA bundan bağımsız Chrome ile yapıldı. Sunulan kök yalnız generated web/dist; depo kökü veya .env sunulmadı.

Yeni `web/serve.py` ile başlangıç, CSS, JS ve sonuç JSON yolları HTTP 200; `.env` ve analysis içindeki ham örnek yolu HTTP 404 verdi. Sunucu yalnız 127.0.0.1'e bağlandı.

Playwright paketiyle `node web/tests/browser.cjs`: **10 kontrol grubu geçti**, JavaScript hatası 0, tarayıcının dış origin veri isteği 0:

1. Başlangıç A/B iki çizgi, 12 tablo satırı ve kartlar kaynak JSON ile eşleşiyor. Ocak A ≈ −0,39 °C, B ≈ −24,13 °C; mekânsal A−B ≈ 23,74 °C.
2. Temmuz seçimi ve FRLAND değişimi kaynak değerlerine eşit; koşullu kapsam uyarısı görünür.
3. JSON indirme ay/politika/aday durumunu ve kaynakları koruyor.
4. Tek pencere ve boş seçim; boşta indirme kapalı, eski kaynak durumu gösterilmiyor.
5. Kaynak ayrıntısında gerçek ham hash görülüyor; runtime dış istek ve JS hatası yok.
6. 390×844 mobil görünüm yatay taşmıyor; dar SVG görünümüyle eksen yazıları okunuyor.
7. Yalnız UI hata testi için taklit edilen eksik ayda kart/fark “Veri yok”, çizgi iki ayrı parçaya ayrılıyor. Bu taklit NASA kaynak dosyalarına yazılmadı.
8. Taklit HTTP 503'te sonuç gizli; yeniden deneme gerçek yerel JSON ile toparlanıyor.
9. Taklit yanlış birim K, sözleşme hatası olarak sonuçları göstermiyor.
10. B'nin zaman standardı yalnız UI hata testi için UTC yapılınca A ile eşlenmiyor; sonuçlar gizleniyor. Kaynaklar aynı ayları taşısa da farklı zaman standardı veya sağlayıcı sürümüyle builder da eşleme yapmıyor. Bu teknik uygunluk, bilimsel profil kabulü değildir.

Masaüstü 1440×1100 ve mobil ekran görüntüleri alınıp görsel olarak incelendi. İlk mobil incelemede SVG metinleri fazla küçülüyordu; dar viewBox ve seyrek eksen etiketleriyle düzeltildi, on kontrol yeniden geçti. QA paketinin varsayılan Chromium binary'si kurulu değildi; yeni tarayıcı indirilmeden yüklü Chrome kullanıldı. Görüntüler ignored `web/artifacts/desktop.png` ve `mobile.png` altında. Bunlar gerçek Mac veya uzaktaki Ubuntu çalıştırması değildir.

Portal check/strict build ve git diff --check geçti. Başarılı arayüz testi maske/sınır/bilimsel kalite veya eğilim testi onayı değildir. Prototip nihai sunum uygulaması sayılmaz; aynı veri türündeki ilk çalışan görünümüdür. Önizleme QA sunucusu kapatıldı; loopback adresinin artık yanıt vermediği denetlendi. Yeniden açma komutları ürün kaydındadır.
