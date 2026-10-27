---
status: Validating
updated: "2026-10-26"
review_summary: "Gerçek maskesiz A/B T2M yıllarında iki ağırlık adayının ve API yıllık hücre özetinin kıyası."
change_summary: "216 Windows analiz/37 JS, gerçek A/B rapor tekrarları ve builder geçti; 48 aday yıl, yeni web/istatistik profili kabulü yok."
---
# Yıllık ağırlık adayları · Gerçek kontrol

Tarih 2026-10-26; Windows, analysis kendi .venv Python. Başlangıç temiz 4a1d3dc, codex/m1-modules-region-a. Ekip/durum/fikir/devir/pano okundu. Fetch sonrası main a1a83d5, uzak M1/M2 6047c42; yeni katkı yok. [Yöntem/kaynak yorumu](../research/TEMPORAL_AGGREGATION.md), [CLI](../guide/T2M_ANNUAL_WEIGHTING.md).

## Gerçek kayıt sonuçları

Yeni NASA isteği yok. Mevcut 2001–2024 history/raw kayıtları tekrarlandı; aynı kesişen alanlar korunarak 24'er tam aylık yıl ve API'nin her yıldaki yıllık hücre değerleri değerlendirildi. Kaydedilmiş çıktılar analysis/examples/a-annual-weighting-audit.json ve b-annual-weighting-audit.json; sağlayıcı yıllık değerler kaynak yanıttaki yıl+13 anahtarından gelir.

| Deneysel sonuç · °C | A | B |
|---|---|---|
| 2024 eşit ay | 12,189302625 | −8,726416617 |
| 2024 takvim günleri | 12,221020987 | −8,699212570 |
| 2024 API yıllık hücrelerinin alan özeti | 12,221245094 | −8,699471419 |
| 24 yılda en büyük iki aday farkının mutlak değeri | 0,079697566 · 2003 | 0,140113109 · 2021 |
| En büyük mutlak API−eşit ay farkı | 0,080099891 | 0,140118380 |
| En büyük mutlak API−gün ağırlığı farkı | 0,001461704 | 0,000935168 |

Her pencerede 24/24 yıl ve yıllık referansta 56/55 hücre tam. Bu 48 bölge-yılın tamamında gün ağırlığı API yıllık özetine daha yakın çıktı; bu **bu kayıtların gözlemidir**, NASA algoritmasının evrensel doğrulanması değildir. Aynı MERRA-2 kaynaklarının kıyası bağımsız doğruluk/güven aralığı sayılmaz. Artıkların kaynağı ayrıştırılmadı; tolerans/ölçüm doğruluğu eşiği seçilmedi. NASA kısa işleme tablosunda ağırlıklar açık olmadığından eşit ay yorumunu tablodan kesin çıkarma varsayımı sürdürülmedi.

## Doğrulama

İlk 13 hedef test geçti (59,225 s); sonrasında ham kayıtla üretilmiş eksik ay/yıl denemesi geçti (17,431 s). Kaynak kimliğinin yeniden hesaplanan float'lar yerine kayıtlı parent byte'larına bağlanması sırasında ilk devam eden tam check durduruldu; final suite bu düzeltmeden sonra yeniden başlatıldı. Önceki koşu final başarı diye sayılmaz.

Yeni testler Gregoryen 2000/2024 artık ve 2100 artık-olmayan yıl, Şubat 28/29 ağırlığı, null/sıfır, eksik sağlayıcı hücresi, taşma, bozuk/tekrarlı ay ve statü, gerçek A/B bütün yıllarında bağımsız Decimal aritmetiği, kaynak byte değişimi ve rapor/CLI tekrarını kapsar. Sentetik eksik ay denemesinde sağlayıcı yıllık değer hazır olsa da aday yıllık değerler null kaldı; gerçek 2001–2024 kayıtlarında eksik ay yok.

Son `scripts/workspace.py check` alt süreç kaydı: **216 test / 338,606 s**, OK, 0 atlanan/hata; **37 JS / 196,2935 ms**, syntax ve tam builder başarılı. Eski nokta/alignment/A alan/B tile, iki yıllık/24 yıllık A-B history tekrarları, gerçek fraksiyon dönüşümleri, iki beş düğümlü akış ve yeni iki `validate-annual-weighting` geçti. 15 yeni test vardır. NumPy deprecation ve kasıtlı duplicate ZIP test uyarısı dışında ürün kontrol hatası yok.

Sonuçları dosyaya yazan ignored yardımcı, başarılı alt süreç bittikten sonra log sonunu CP1254 stdout'a basarken UnicodeEncodeError verdi; onun çıkış kodu 1'dir. Ürün check kaydında 216/OK, 37 JS ve nihai başarı işareti ayrı okunarak doğrulandı. Yardımcı UTF-8 çıktıyla yalnız kayıt okuma modunda düzeltildi; bu bir yeni tam check koşusu sayılmadı. Kayıt ignored analysis/artifacts/annual-weighting-final-check.log içindedir.

A aday rapor SHA-256 `8e306f1b6d2dc91226f0bc554ac00b61744192433e461d6fc7a7f54b9caf35fb`; B `f0beb02708646b61e40ac5cb172b80d329a1a04ac9deddf65d2d5c0264141a9d`. Parent raw result kimliği ve bütün yıllık kaynak hash'leri raporda tutulur. İki rapor sayısı/aday bayrakları/kaynak kimliği ve yeniden hesaplanan değerleri denetlendi; kendi hash'leri bilimsel onay değildir.

Genel webin altı dosyası son builder sonrasında önceki gerçek timeline ZIP'iyle byte aynı doğrulandı; eski paket verifier geçti, yeni paket/yayın yapılmadı. Yeni tarayıcı/Mac/Linux/Docker/ARM64/uzak CI sonucu yok; önceki 65 Chrome bu yeni CLI için test diye sayılmaz.

Portal kendi venv Python ile check ve strict build geçti (ilk build 3,94 s). Portal denetimi içerik/bağlantı kontrolüdür, aday yıllık hesabın bilimsel doğrulaması değildir. Git diff kontrolleri ve yeni iki raporun staged byte korunumu teslimde ayrıca denetlenir.

## Sınırlar

İki hedef de adaydır; yalnız maskesiz mevcut pencere kullanılır. Raporlar 0.1.0 yeni ayrı türdür; bilimsel maske/sınır/dönem/istatistik kabulü, yıllık anomali, eğilim/p-değeri veya iklim normali üretmez. Yeni CLI henüz genel web/motor akışına eklenmedi. M2'nin kabulü/R-B05 başlangıcı veya R-A05/R-B05 analiz tamamlanması yok. Yeni kayıt/kod yerel M1 dalında; push/main/Pages/Sites/dış mesaj yok.
