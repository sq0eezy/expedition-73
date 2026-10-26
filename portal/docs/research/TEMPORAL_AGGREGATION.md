---
status: Validating
updated: "2026-10-26"
review_summary: "Aylık T2M'den yıllık özet için iki farklı hedef ve kaynak tanımının sınırı."
change_summary: "Eşit ay/gün sayısı ağırlıkları ve API yıllık hücre karşılığı araştırıldı; yöntem seçilmedi, aday hesap hazır."
---
# T2M · Yıllık özetin neyi temsil edeceği

M1 devam talebi üzerine bilimsel tasarımın ilk dar denemesi, kayıtlı maskesiz aylık T2M'yi iki farklı yıllık özete çevirmektir. **Yöntemler adaydır; bilimsel profil seçilmedi.** [CLI/sözleşme](../guide/T2M_ANNUAL_WEIGHTING.md), [gerçek sayılar ve testler](../evidence/ANNUAL_WEIGHTING_CHECK.md).

## Kaynakların söylediği ve söylemediği

2026-10-26'da [NASA POWER işleme tablosu](https://power.larc.nasa.gov/docs/methodology/data/processing/) okundu: aylık basamak günlerden, yıllık basamak aylardan ortalama olarak açıklanıyor. Bu kısa tablo **aylık ağırlıkları açıkça belirtmiyor**. Buradan yıllık değerin mutlaka 12 eşit ağırlıkla üretildiği sonucu çıkarılamaz. Günlük/saatlik kaynak alınıp tam NASA yıllık algoritması yeniden üretilmedi.

[Xarray aylık ortalamalar örneği](https://docs.xarray.dev/en/stable/examples/monthly-means.html), farklı ay uzunluklarını ve takvimi dikkate alan süre ağırlıklarını mevsimlik ortalama için gösterir. Bunun bir yıla uygulanması burada açık bir hesap adayıdır; Xarray kurulmadı ve bu örnek NASA T2M yıllık ürün algoritmasının doğrulanması sayılmaz.

API'nin kaynak yanıttaki yıl+13 anahtarından gelen yıllık **hücre** değerleri zaten kayıtlıdır. Aynı kesişim alanlarıyla ağırlıklandırılarak iki adayla karşılaştırılır. Bu aynı NASA/MERRA-2 kaynağının kendi özetidir; bağımsız ölçüm, doğruluk veya belirsizlik kanıtı değildir. Görülen artıkların yalnız yuvarlamadan kaynaklandığı da kanıtlanmadı; hiçbir sayısal eşik “NASA doğruluğu” diye tanımlanmadı.

## İki hedef

T_m, mevcut maskesiz aday pencerenin m ayındaki alan ağırlıklı sıcaklığı; d_m Gregoryen takvimde ayın gün sayısı olsun.

| Aday | Hesap | Temsil ettiği hedef |
|---|---|---|
| equal_months | Σ(T_m / 12) | Her ayın aynı katkı yaptığı 12 aylık değer özeti |
| calendar_days | Σ(T_m × d_m / Σd_m) | Aylık ortalamaların takvim süresine göre ağırlıklı özeti |

İkincisinin paydası normal yılda 365, artık yılda 366; 2100 artık yıl değildir. Hesapta ara yuvarlama yapılmaz. API aylık değerlerinin kaynak hassasiyeti nedeniyle çok ondalık üretmek yeni ölçüm doğruluğu kazandırmaz. Gün sayısı ağırlıklı özet, yalnız aylık ortalamalar/eksiklik/alan desteği uygun olduğunda zaman ortalaması hedefini temsil eder; günlük verinin yeniden hesaplanmış sonucu diye sunulmaz.

## Denemenin sınırları

- Yalnız mevcut maskesiz aday pencere geçmişi alınır; kara/kara+buz bilimsel politikası seçilmez.
- Bir ay bile eksikse iki yıllık özet de null kalır. Mevcut aylara yeniden ağırlık dağıtılmaz, API yıllık değeriyle doldurulmaz. Bu katı pilot kuralıdır; evrensel WMO eksiklik kuralı değildir.
- API yıllık hücrelerinden biri eksikse o referansın bölgesel özeti null kalır; kalan hücrelere yeniden alan dağıtılmaz. Aylık yıl tam ise iki aday yine hesaplanabilir.
- Rapor yalnız yıllık değerleri, kullanılan ağırlıkları ve iki yöntemin farkını tutar. En büyük fark toplam belirsizlik, ölçüm hatası veya ısınma miktarı değildir.

[WMO standart normal tanımı](https://wmo.int/wmo-climatological-normals) 1991–2020 gibi 30 yıllık referans dönemlerini kullanır. 2001–2024 penceresi kendi başına böyle bir standart normal dönemi değildir. Bu, 24 yılın incelenemeyeceği veya özel bir referans ortalamasına göre anomali tanımlanamayacağı anlamına gelmez; henüz anomali/baz dönem hesabı yoktur.

**Tartışılacak sonraki karar:** Takvim süresini temsil eden yıllık sıcaklık mı, eşit ay özeti mi hedefleniyor? Zaman ağırlığı, bilimsel yüzey/sınır/dönem ve eksiklik kuralıyla birlikte adlandırılmalı. M2 görüşü/ortak yöntem kabulü bekler; eğilim, otokorelasyon, aralık ve p-değeri ayrı tasarımdır.
