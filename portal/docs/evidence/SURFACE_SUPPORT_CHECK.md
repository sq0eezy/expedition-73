---
status: Validating
updated: "2026-10-19"
review_summary: "Gerçek kayıtlı A/B verileriyle koşullu yüzey alanı sınırı; analitik ve entegrasyon testleri."
change_summary: "Yeni audit-surface-support komutu, 12 test ve toplam 146 test başarılı; B sınır parçalarının varsayım etkisi sayısallaştırıldı."
---
# Sınır hücreleri · Gerçek girdili alan denetimi

**Tarih/ortam:** 2026-10-19, Windows, analysis sanal ortamı, Python 3.12.14. M1'in devam talebi kapsamında kendi dalında geliştirme. Fetch sonrası main ve M2 dalında yeni katkı yok; M2 `791e07c` kaydı değişmedi. Yeni NASA veri isteği, token okuma, Git push, main birleştirmesi veya Pages yayını yapılmadı.

## Yöntem ve gerçek girdiler

`surface_support.py` mevcut `surface_workflow.run` üzerinden girdileri bir kez sabitleyip T2M/fraksiyon replay'lerini ve kaynak uygunluğunu denetler. Başarısız kaynakta rapor vermez. Sonra [koşullu alan korunumu hesabını](../research/SURFACE_SUPPORT.md) iki aday politika için yapar. Bu, yeni bilimsel gösterge veya kabul edilmiş ortak çıktı sözleşmesi değildir; mevcut sıcaklık/maskesiz sonuçlar değişmedi.

Girdiler: `analysis/examples/a-window-2024`, `b-window-2024` ve `a-surface-fractions`, `b-surface-fractions`. Önceki [kaynak/ham veri doğrulaması](SURFACE_SUBSET_CHECK.md) geçerli. Yeni rapor her kaynak dosyasının byte SHA-256 izini korur. Ortak özet `analysis/examples/surface-support-summary.json`; tam hücreli yerel raporlar ignored `analysis/artifacts/surface-support-20261019T083759Z/a-audit.json` ve `b-audit.json` içinde. Özel .env/artifacts yayımlanan belgeye kopyalanmadı.

## Gözlenen sonuç

Aşağıdaki yüzdeler pencere alanına oranlardır. Alt/üst, yalnız fraksiyonlar pilotun küresel alan ölçüsünde kesin kabul edilirse ve hücre içi yerleşim serbestse geçerli **koşullu yerleşim sınırlarıdır**. Fiziksel ölçüm doğruluğu veya güven aralığı değildir.

| Pencere/politika | Koşullu alt (%) | Homojen tahmin (%) | Koşullu üst (%) | Yerleşimi belirsiz kesilmiş hücre |
|---|---:|---:|---:|---:|
| A · FRLAND | 99,9401 | 99,9623 | 99,9845 | 2 |
| A · FRLAND+FRLANDICE | 99,9401 | 99,9623 | 99,9845 | 2 |
| B · FRLAND | 97,0233 | 98,1465 | 99,0593 | 24 |
| B · FRLAND+FRLANDICE | 97,0697 | 98,1639 | 99,0603 | 24 |

A'da 56 hücrenin 26'sı kesiliyor; bu parçalar pencere alanının %21,8723'ü. B'de 55 hücrenin 28'i kesiliyor; %29,6859. Kesilmiş her hücre belirsiz değildir: f=0/1 olduğunda alan yerleşimi değişmez. FRLAND koşullu toplam aralık genişliği A'da yaklaşık 52,21 km², B'de 1082,56 km². B'nin aralığı bu aday sınır/ölçü varsayımına aittir; tüm Alaska veya kaynak verinin istatistiksel belirsizliği değildir.

Bu aralıklardan sıcaklık sapması, p-değeri veya iklim etkisi türetilmedi. T2M hâlâ grid sıcaklığıdır. Kaynağın AREA değişkeni ve daha ince yüzey geometrisi doğrulanmadı; maske/bölge/profil kabulü yapılmadı.

## Tekrar çalıştırma

`analysis` içinde Windows CMD, kurulu requirements-mask ortamıyla:

```cmd
.venv\Scripts\python.exe -X utf8 -m expedition73 audit-surface-support --window-run examples/a-window-2024 --fraction-run examples/a-surface-fractions
.venv\Scripts\python.exe -X utf8 -m expedition73 audit-surface-support --window-run examples/b-window-2024 --fraction-run examples/b-surface-fractions
```

Mac/Linux'ta aynı argümanlarla `.venv/bin/python -X utf8 -m expedition73 audit-surface-support ...`; ortam oluşturmak gerekirse `python3 -m venv .venv`. Bu yeni komut gerçek Mac'te çalıştırılmadı. JSON stdout'a verilir, kendiliğinden dosya yazmaz; `-X utf8` Windows yönlendirme/alt süreç kaydında Türkçe etiketleri korur. Ağ veya credential gerektirmez.

## Kontroller

- `.venv/Scripts/python.exe -m unittest discover -s tests`: **146 test / 11,773 saniye, başarılı**. Yeni 12 test: bilinen alan hesabı, sekiz eşit alt hücrede bütün yüzey yerleşimlerini bağımsız tarama, tam/boş/saf hücre, tamamlayıcı pay korunumu, geçersiz girdiler, A/B alan toplamı, mevcut ağırlık önizlemesiyle eşleşme, değişmez kaynak, tek replay/ağ-token kullanmama, CLI/hata, yanlış bölge/geometri ve kayıtlı özetin yeniden üretimi.
- İki gerçek nokta `validate`, A `validate-window`, B `validate-tiled-window` başarılı; iki gerçek fraksiyon `--replay` 56/55 hücreyle geçti. İki yeni CLI gerçek girdilerden JSON üretti; maskesiz/sıcaklık örnek dosyaları değiştirilmedi.
- Önceden var olan NumPy 2.5 NetCDF sentetik yazım uyarıları hata üretmedi. Uzak Ubuntu CI veya Mac çalıştırması bu yeni dilim için yapılmadı.

Portal check/strict build ve git diff --check geçti; bunlar NASA analiz doğrulamasının yerine geçmez. Sonraki adım: AREA/alan tanımı incelemesi ve ortak yüzey hedefini değerlendirmek; M2'nin yeni görüşü beklenir.
