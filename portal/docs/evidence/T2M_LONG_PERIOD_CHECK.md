---
status: Validating
updated: "2026-10-24"
review_summary: "Gerçek 24 yıllık NASA POWER erişimi, kaynak tekrarı ve yıl kataloğu kontrolü."
change_summary: "A/B 288/288 ay, 201 Windows test/30 JS/53 Chrome geçti. Yeni Mac/Linux/CI/yayın yok; bilimsel eğilim ve profil açık."
---
# 2001–2024 gerçek kontrol kaydı

Tarih 2026-10-24, ortam Windows/PowerShell, analysis kendi .venv Python. Başlangıç temiz cfaf9d2, dal codex/m1-modules-region-a. Fetch sonrası main a1a83d5, uzak M1/M2 6047c42; yeni katkı yok. [Kapsam/komutlar](../guide/T2M_LONG_PERIOD.md).

## Gerçek kaynak erişimi

Mevcut history.collect, tek yıllık request ve fetch_missing=True ile 2001–2022'de A için 22 tek istek, B için 44 tile isteği yaptı. İstekler seri yürütüldü; hata/otomatik tekrar olmadı. Her tamamlanmış yıl artifacts/annual-2001-2024 altında ayrı doğrulandı. Kayıtlı 2023/2024 açık seed olarak korundu; 24 yıl parent history.collect ile birleştirilip validate_run ile tekrarlandı. Operasyon yardımcıları ignored artifacts içinde; tekrar kullanılacak esas araç [history CLI](../guide/T2M_HISTORY.md).

| Sonuç | A | B |
|---|---|---|
| Aylık seri | 288/288 | 288/288 |
| Hücre | 56 | 55 |
| Hücre-ay | 16.128 | 15.840 |
| Bütün aylarda bütün hücrelerin varlığı | Evet, alan oranı 1 | Evet, alan oranı 1 |
| Kaynak dosyaları | 75; 2.883.390 byte | 123; 2.961.617 byte |
| 2023/2024 byte korunumu | Aynı | Aynı |

Her yıl NASA POWER v2.10.0 / MERRA2, aylık LST; ortak grid/alan yöntemi/sınır eşleşti. Parent manifest SHA-256 A `fdbce4939cc4010dc230a6207b28aff840ee71931d4fe328c59004600d7e9b09`, B `942ee939084a15786e499906c0e486b06109cb468660a7e406f03b1184165bb7`. Küçük kaynaklar analysis/examples/a-history-2001-2024 ve b-history-2001-2024 içinde. Kalite sayımları parent series.valid_cells/valid_area_fraction, quality ve dosya byte toplamlarından ayrıca çıkarıldı; replay kontrollerinin yerine sayılmadı.

NASA resmi [Monthly API belgesi](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/) bu tarihte tekrar okundu: meteoroloji MERRA-2 tabanlı ve 1981'den önceki yıla kadar tarif edilir. 2001–2024 proje aday dönemi; NASA genel sınırı değildir. Gerçek erişim kanıtı doküman kapsamından ayrı yukarıdaki ham yanıt/tekrar kayıtlarıdır.

## Yerel doğrulama

Depo kökünde kendi venv Python ile `scripts/workspace.py check`: **201 test / 388,815 s**, 0 hata/atlanan; eski nokta/alan/parçalı örnekler, eski iki yıllık ve yeni 24 yıllık A/B replay, gerçek fraksiyon dönüşümleri ve iki beş düğümlü surface akışı geçti. Node iki test dosyasında **30 test / 414,5819 ms**, syntax ve 24 yıllık builder geçti. Bilimsel yöntem/hesap değişmedi. Beklenen NumPy deprecation ve kasıtlı duplicate ZIP test uyarısı dışında hata yok.

Yeni test_long_history.py gerçek 288 ay/tüm kesişen hücreler, eski 2023/2024 kaynak byte korunumu, 24 annual katalog/hash, önceki rapor kimlikleri ve her ihraç edilen maskesiz ayın yeniden hesaplanan kaynakla eşleşmesini kontrol eder. İlk iki yıllık testler ayrıca korundu.

Katalog **6.649.872 byte**, 8 MB sınırının altında; web 0.4.0/annual 0.3.0/rapor 0.1.0/manifest 0.3.0/altı genel dosya korunur. Eski annual SHA-256 2023 `f4c23871f99661d75e99102208ac9cb15b17f33e373c1ee18bc75a14d941fa5b`, 2024 `d4ce2e87783af79ccee855a6a8040845cfd19776a405b52dc829c88c766e7169` aynı.

`python web/serve.py` ve mevcut optional Playwright/kurulu Chrome ile `node web/tests/browser.cjs`: **53 senaryo grubu**, JS hatası 0, dış runtime isteği 0. 2001/2012/2024 seçimleri gerçek yıllık değerlerle eşleşti; yeni 2001 raporu kendi yılına döndü, 2023/2024 raporları korundu. Bozuk annual hash/yıl sırası/yinelenen yıl/eksik varsayılan katalog reddedildi. Mevcut klavye/mobil/hücre/akış/karşılaştırma kontrolleri geçti. Masaüstü 1440×1100 ve mobil 390×844 viewport; gerçek telefon/Mac koşusu değil. Screenshot'lar ignored web/artifacts altında. open_in_codex queued döndü; kullanıcıya görünür açılış teyidi değildir.

HTTP index 200, .mjs text/javascript; .env/analysis kaynak yolu/portal kaynak yolu 404. Git staging sonrası **198 yeni kaynak dosyasının tamamı** çalışma dosyasıyla byte aynı kontrol edildi; önceki T2M/fraksiyon kaynaklarına değişiklik yapılmadı. .gitattributes byte koruması aynen kaldı.

`scripts/workspace.py package` kataloğu tekrar derledi ve altı genel dosyalı **6.740.603 byte** ZIP'i doğruladı; SHA-256 `f89b2b2012e395e9002bf20d54540ca8d5e60bb18fe989a1612fd09c4894921b`. Önceki gerçek iki yıllık ZIP de verifier ile açıldı; yeni ZIP'teki altı dosyanın son build ile byte aynı olduğu kontrol edildi. Paket yalnız ignored web/artifacts içinde; yayımlanmadı. Full suite mevcut builder'ın aynı kaynaklarla iki üretiminde byte eşitliğini de denetledi; bu dilimde iki ayrı son ZIP üretildiği iddia edilmez.

QA sunucusu durduruldu; 8873 TCP bağlantısının kapalı olduğu doğrulandı. Tekrar açma komutları kılavuzdadır.

Portal kendi venv Python ile `portal/scripts/portal.py check` ve `build` başarılı (ilk strict build 8,94 s); bu içerik/bağlantı kontrolüdür, NASA bilimsel doğrulaması değildir. Git diff/staged diff whitespace kontrolleri geçti.

## Sınırlar ve paylaşım

Eksiksiz aylık kayıt piksel QA'sı, model doğruluğu veya bilimsel uygunluk değildir. Sabit fraksiyon örnekleri bütün yıllarda yalnız aday duyarlılık; tarihsel maske doğrulanmadı. Yeni eğilim/istatistik veya dönem/sınır/yüzey kararı yok. Yeni Mac/Linux/Docker/ARM64/uzak CI koşusu yapılmadı. M2'nin ekran/bilimsel profil kabulü yok; R-A05/R-B05 bilimsel analiz tamamlandı sayılmaz. Yerel M1 dalında; push/main/Pages/Sites/dış mesaj yok.
