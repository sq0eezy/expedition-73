---
status: Validating
updated: "2026-10-20"
review_summary: "Kayıtlı grid hücrelerinin ekranda incelenmesi ve bölgesel sonuçla tutarlılığı."
change_summary: "A/B 56/55 hücre, ay/politika seçimi, klavye ve hata durumları doğrulandı; 164 analiz testi ve 18 Chrome senaryosu geçti."
---
# Hücre görünümü · Yerel doğrulama

2026-10-20, Windows / Python 3.12.14, M1 geliştirme dalı. [Ürün kapsamı ve çalıştırma](../product/RESULTS_PREVIEW.md). Bu bir bilimsel profil/maske kabulü veya canlı yayın kanıtı değildir.

## Kaynak ve hesap

`analysis/scripts/build_web_preview.py`, kayıtlı `a-window-2024` / `b-window-2024` ve eşleşen `*-surface-fractions` girdilerini mevcut workflow ile tekrar doğruladı. A 56, B 55 hücre; her biri 12 ay. Kaynak JSON/NetCDF/metadata örnekleri değiştirilmedi. Yeni NASA isteği veya token erişimi yapılmadı.

Web aktarımı `recorded_temperature_web_preview` **0.2.0** oldu: her hücre için doğrulanmış aylık T2M, dört tam-hücre fraksiyonu, mevcut denetimdeki tam/kesilmiş dikdörtgen ve üç etkin alan ağırlığı taşınır. Bilimsel yöntem, T2M kaynak çıktı şemaları ve `t2m-technical-2024` 0.1.0 değişmedi. Eski web paketi yeni arayüzle karıştırılırsa hata gösterilir; yeniden derleme gerekir.

İki yeni entegrasyon testi, tüm hücrelerin değer/fraksiyon/kesişimlerini replay girdileriyle eşleştirir. Üç politikanın hücre alanı toplamları mevcut kapsamı, **2 pencere × 3 politika × 12 ay** ağırlıklı hesapları mevcut serileri 8 ondalık basamakta yeniden üretir. Nokta/alan hesap algoritması değiştirilmedi.

## Gerçek kontroller

Depo kökünde builder; `analysis` içinde kendi sanal ortamıyla:

```text
python -m unittest discover -s tests
python -m expedition73 validate examples/a-point-2024/result.json
python -m expedition73 validate examples/b-point-2024/result.json
python -m expedition73 validate-window examples/a-window-2024
python -m expedition73 validate-tiled-window examples/b-window-2024
python scripts/fetch_surface_fractions.py --replay examples/a-surface-fractions
python scripts/fetch_surface_fractions.py --replay examples/b-surface-fractions
```

Gerçek sonuç: **164 test / 19,000 saniye / OK**; iki nokta, A alan, B parçalı alan (2 istek kaydı, 5 tekrar çıkarılmış), 56/55 fraksiyon dönüşümü başarılı. Önceden var olan NumPy deprecation uyarısı hata üretmedi. Bunlar yeni bir Mac/Ubuntu koşusu değildir; M2'nin ayrı 134 testlik macOS beyanı [paylaşım kaydında](../team/SYNC.md).

`node --check web/src/app.js` geçti. Yerel `web/serve.py` yalnız `web/dist` sunarak HTTP 200 verdi; Codex panelinde açma isteği queued döndü. Bağımsız Playwright/yüklü Chrome headless ile `node web/tests/browser.cjs`: **18 senaryo grubu başarılı**, ana sayfa JS hatası 0, dış origin runtime isteği 0.

Yeni kontroller: 56/55 hücre, dokunma/tıklama ve ok tuşlarıyla odak/ayrıntı seçimi; ayın gerçek T2M ile eşleşmesi; politika değişirken rengin sabit ve etkin alanın doğru kalması; pencere kaldırılınca diğerine geçiş; boş seçimde eski hücrelerin temizlenmesi; eksik sıcaklıkta gri/null/sıfır geçerli katkı; yanlış ağırlık/geometri/hücre kapsamı/tarih ve eski web sürümünde sonuçların gizlenmesi. Önceki grafik, kaynak, indirme, HTTP hata/tekrar ve birim/zaman uyumsuzluğu kontrolleri de geçti.

1440×1100 masaüstü ve 390×844 mobil viewport ekran görüntüleri ile A/B hücre panelleri incelendi; yatay sayfa taşması yok. Görseller yerel ignored `web/artifacts/` altında. Gerçek telefon, ekran okuyucu veya macOS web doğrulaması yapılmadı.

Portal `check`, strict `build` ve `git diff --check` geçti; NASA hesaplarını doğrulayan kontrollerden ayrıdır. QA sunucusu kapatıldı ve loopback adresinin yanıt vermediği doğrulandı.

## Yorumlama sınırı

Şema enlem/boylam düzlemindedir; alanı koruyan harita, uydu görüntüsü, kıyı çizgisi veya kabul edilmiş ekolojik sınır değildir. Tam hücre kenarları mevcut orta nokta yaklaşımından kurulur. Renk tüm kayıtlı hücre/aylar için ortak, sabit yıllık ölçekle grid T2M'yi gösterir; politika sıcaklığı değiştirmez. Alan payı, seçili ayda geçerli sıcaklığı olan hücrelerin seçili ağırlığı üzerinden gösterilir; eksik hücre sıfır geçerli katkı alır, mevcut analiz eksik veri kuralı değiştirilmez.

Fraksiyonlar tam hücreye aittir; kesilmiş parçada homojen kabul edilir. Alan, pilotun tanımlı küresinde hesaplanır; kaynak AREA ile doğrulanmış değildir. Ayrı kara sıcaklığı, hücre içi kara/su yerleşimi, belirsizlik veya trend çıkarılmaz. Main/Pages'e yeni yayın yapılmadı; yeni ekran M2 tarafından incelenmiş sayılmaz.
