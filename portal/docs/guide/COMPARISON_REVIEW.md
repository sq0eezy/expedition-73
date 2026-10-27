---
status: Validating
updated: "2026-10-22"
review_summary: "Aynı veri kaydıyla karşılaştırma seçimini paylaşma ve yeniden hesaplayarak açma."
change_summary: "Kaynak kimlikli 0.1.0 rapor indirilebilir; bütün alanlar yeniden hesaplamayla eşleşmeden seçimler uygulanmaz."
---
# Karşılaştırma inceleme raporu

İki kişinin aynı pencere çifti, yön, ay ve yüzeyi incelemesi için yerel ekran küçük bir JSON raporu indirir. Bu bir inceleme kaydıdır; yazar imzası, M2 kabulü veya bilimsel yöntem kararı değildir. [Gerçek kontrol](../evidence/COMPARISON_REVIEW_CHECK.md).

## Kullanım

1. Windows depo kökünde `scripts\start-preview.cmd`, Mac'te `sh scripts/start-preview.sh` ile aç; sonra localhost 8873. [Kurulum](DEV_PACKAGE.md).
2. İki uyumlu pencereyi, yönü, ayı ve yüzeyi seç. **Karşılaştırma raporunu indir** düğmesi `expedition73-comparison-review.json` verir.
3. Raporu kendi seçtiğin yolla diğer kişiye iletebilirsin; uygulama otomatik göndermez. Diğer kişi aynı veri kaydıyla çalışan güncel ekranında **Raporu aç ve doğrula** alanından seçer.
4. Tam veri JSON byte SHA-256 kimliği, kaynak context/hedef iş tanımı kimlikleri ve yeniden hesaplanan bütün rapor alanları eşleşirse seçimler açılır. Gereken iki pencere görünür yapılır; diğer görünür pencereler kapatılmaz.
5. Kaynak/biçim/içerik uyuşmazsa seçimler değiştirilmez. Aynı sayısal değerleri taşısa bile farklı kaynak JSON byte kaydı reddedilir. Aynı rapor tekrar açılabilir.

Dosya yalnız tarayıcıda okunur; sunucuya yüklenmez. En fazla 131.072 byte rapor kabul edilir. Web Crypto yoksa rapor düğmeleri kapatılır, grafikler kullanılabilir. Rapor açmak için NASA hesabı/token veya Node gerekmez.

## Ayrı rapor sözleşmesi

`recorded_comparison_review` **0.1.0**, karşılaştırma uygulaması **0.1.0**. Annual kaynak web verisi 0.3.0 ve altı genel dosya korunur. Yeni dış yıl kataloğu 0.4.0, demo manifesti 0.3.0; eski bağımsız 0.3.0 da desteklenir. Önceki genel JSON indirme düğmesi bölge girdilerini aktarmaya devam eder; bu raporun yerine geçmez.

- `dataset`: kaynak şeması ve **seçili yılın 0.3.0 snapshot byte kaydının** SHA-256 kimliği; yalnız seçilen iki kayıtla sınırlı değildir. Eski bağımsız ekranda bu data/results.json dosyasının tamamıdır; yeni katalogda ilgili snapshots girdisinin data_json metninin UTF-8 byte kaydıdır. Başka yıl eklenmesi aynı yıllık raporu bozmaz.
- `selection`: left_id, right_id, policy, month.
- `source_definitions`: iki kaydın context ve Sensitivity hedef tanım kimlikleri; rastgele run/artifact kimlikleri değildir.
- `result`: teknik koşullar, 12 ayın sol/sağ/farkları, geçerli çift sayısı, maksimum |fark|/tüm bağ ayları. `selected_month` seçilen satırı taşır. Eksik değerler null kalır.
- Aday/kayıttan çalışma, inference_performed=false, scientific_acceptance=not_performed ve identity_authentication=not_performed zorunludur. Ek alanlar reddedilir. Serbest not, kişisel ad/yol/tarih, özel parametre/context veya ham dosya kopyalanmaz.

Saf `createComparisonReview`/`verifyComparisonReview` mevcut comparison.mjs içindedir; `datasetDigest` Web Crypto kullanır. Doğrulama JSON anahtar sırasından bağımsızdır. Sonuç değiştirilirse yeniden hesaplamaya uymaz; baştan tutarlı başka rapor üretilebilir. Kimin yazdığını doğrulayan imza yoktur.

Bu işlem normalleştirilmiş kayıttaki **JS pencere farkını** tekrarlar; NASA ham API/NetCDF dönüşümünü tarayıcıda yeniden yapmaz. Onlar builder kaynak tekrarında doğrulanır. Trend/ısınma etkisi/güven aralığı veya bilimsel maske/sınır/uzun dönem seçimi eklenmedi. [H-M1-017](../team/HANDOFFS.md) M2 incelemesi bekler; yeni kod yerel M1 dalındadır.

Yıllar arası rapor açılışında seçilen ayın yılı katalogda bulunmalıdır. Önce o snapshot ve bütün sonuçlar doğrulanır, sonra yıl değiştirilir. [Çok yıllı kaynak/yıl kılavuzu](T2M_HISTORY.md).

2026-10-26: [Uzun dönem işaretçisi](T2M_TIMELINE.md) de doğrulanan raporun ayına gider. Rapor hâlâ tek yıllık snapshot'a bağlıdır; bütün 288 ayın istatistik raporu eklenmedi.
