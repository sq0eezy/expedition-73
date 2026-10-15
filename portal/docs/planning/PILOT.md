---
review_summary: "Tek göstergeli ilk deney: 2 metre hava sıcaklığı, ortak çıktı ve webde inceleme."
change_summary: "Kullanıcı T2M pilotunu seçti; veri/analiz/arayüz için doğrulanabilir küçük adımlar belirlendi."
---
# Pilot · 2 metre hava sıcaklığı

**Kabul edilen:** Tek göstergeyle deneme; zaman serisi, eğilim ve sonuçları inceleten web uygulaması. [ADR-004](../decisions/ADR-004-MODULES-AND-PILOT.md). Bilimsel veri indirilmedi; uygulama kodu henüz yok.

## Soru ve aday girdiler

Seçilecek ortak dönemde iki tanımlı kara alanındaki 2 metre hava sıcaklığı nasıl değişiyor; eğilimler ve farkları ne kadar belirsiz? Zıt yönlü eğilim şart koşulmaz. Pilot küresel ısınmanın bütün neden/etkilerini hesaplamaz.

**Ürün adayı:** MERRA-2 `M2TMNXSLV` 5.12.4, aylık `T2M`. [NASA ürün açıklaması](https://gmao.gsfc.nasa.gov/gmao-products/merra-2/wmo-data-access_merra-2/). Gösterge seçildi; ürün/indirme yolu kesinleşmedi. [CMR eşleşmesi](../research/REGION_CANDIDATES.md) sayısal dosya erişimi kanıtı değildir.

**Alan/dönem adayları:** Colorado Platosu çevresi ve Kuzey Alaska; 2001–2024. Henüz onaylanmadı. Arama dikdörtgeni gerçek analiz poligonu sayılmaz. Nokta örneği erişim sınamasında kullanılırsa bölge ortalaması diye sunulmaz.

## Adımlar ve çıkış koşulları

| Adım | Çıkış koşulu |
|---|---|
| Gerçek örneğe eriş | Küçük sayısal örnek, kaynak/sürüm, tanım, birim, zaman ve eksik değerler kaydedilmiş |
| Alan/dönem belirle | Sürümlü sınır, kara maskesi, hücre/tarih kapsamı açıklanmış; uygun değilse gerekçe kaydedilmiş |
| Seri üret | Küçük örnekte alan ağırlıklı hesap bağımsız doğrulanmış; ortak dönem serileri ve kapsam raporu üretilmiş |
| İstatistiği sına | Mevsimsellik, zaman bağımlılığı ve eksikliğe uygun yöntem seçilmiş; eğim/aralık ve A–B eğilim farkı hesaplanmış |
| Adaptörü sına | Ortak sözleşme, kaynak izleri, özel ayrıntı ve uyumsuz çıktı reddi doğrulanmış |
| Webde göster | İki alan, uyumlu seri/karşılaştırma, kalite ve yöntem kartları; eksik/belirsiz durumlar görünür |

Önce az sayıda tarih/hücreyle erişim ve hesap kontrol edilir. Birkaç aylık örnekten uzun dönem eğilim/anlamlılık sonucu çıkarılmaz. İkinci bilimsel modül, bu akış çalıştıktan sonra ele alınır.

## Yöntem ve doğrulama planı

Aylık seride zaman eğilimi + takvim ayı etkileri ve zaman bağımlılığını dikkate alan belirsizlik hesabı adaydır. Theil–Sen/uygun Mann–Kendall yaklaşımı duyarlılık karşılaştırması olabilir; seçim yapılmadı. [Bilimsel kontrol noktaları](../research/SCIENCE_NOTES.md).

Doğrulama: bilinen eğimli/eğimsiz kontrollü seriler, mevsim döngüsü, ardışık bağımlılık, eksik ay, iki bölgede aynı serinin kullanılması ve uyumsuz birim/dönem/alan. Sentetik sonuçlar NASA bulgusu sayılmaz. Gerçek örnekte ara hesap bağımsız araçla karşılaştırılır; aralığın kapsamadığı ürün/model belirsizlikleri açıklanır.

A/B sorumluluğu düşünülen düzendir; kişi/bölge eşleştirmesi yok. İki kişi aynı modül/sözleşme sürümünü kullanır ve bölgesel hesapları çapraz inceler. Yöntem değişirse iki alanın sonucu aynı analiz sürümüne getirilir.

Teslim: tekrarlanabilir çalışma, sürümlü sonuçlar ve bunları gösteren küçük web deneyimi. [Ekran kapsamı](../product/index.md) · [Görevler](WORK_BOARD.md).
