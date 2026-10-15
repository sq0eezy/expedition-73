# Bilimsel kontrol noktaları

Bu sayfa analiz sonucu içermez. İlk konuşmadaki kesin ifadeleri daraltır ve yöntem seçimi için araştırma soruları tutar.

## İlk konuşmayı okurken

- **Bölgesel örnekler henüz bulgu değil.** Kuzey bölgelerinin her yerde yeşerdiği veya Amazon/Sahel'in her dönemde aynı yönde değiştiği varsayılmadı. Aynı yöntemle seçilmiş bölge ve dönem incelenecek.
- **NDVI değişimi için neden ayrıca araştırılmalı.** Yeşillik eğiminden tek başına çölleşme veya iklim kaynaklı nedensellik sonucu üretmeyelim. Ek kanıt ihtiyacı kaydedilecek.
- **GRACE etiketini doğru seçelim.** Karasal su depolaması ile yalnızca yeraltı suyu aynı çıktı değildir. Ek bileşen gereksinimi [JPL açıklamasında](https://grace.jpl.nasa.gov/applications/groundwater/) ele alınıyor.
- **Zıtlık keşif sorusu olsun.** Baştan zıt eğim vaadi vermek yerine artan, azalan, belirsiz ve veri yetersiz sonuçlarına açık bir deney tasarlayalım.

## Yöntem seçilmeden önce cevaplanacaklar

| Konu | Araştırma sorusu |
|---|---|
| Veri kalitesi | Dolgu değerleri ve kalite bayrakları nasıl uygulanacak? |
| Zaman | Ortak dönem nedir; aylık mı, mevsimlik mi, yıllık mı karşılaştıracağız? |
| Mevsimsellik | Yıllık döngünün trend sanılmasını nasıl önleyeceğiz? |
| Otokorelasyon | Ardışık gözlemler bağımsız mı; yöntem bunu nasıl ele alacak? |
| Uzay | Bölge ortalaması hangi ağırlık ve maskeyle hesaplanacak? |
| Eğilim | Doğrusal veya monoton trend varsayımı bu değişkene uygun mu? |
| Belirsizlik | Eğim aralığı, örnek sayısı ve eksiklik nasıl gösterilecek? |
| Anlamlılık | Test, sıfır hipotezi ve eşik ne olacak; p-değeri nasıl anlatılacak? |
| Çoklu karşılaştırma | Birçok bölge/piksel denenirse seçilim ve çoklu test etkisi nasıl ele alınacak? |

Yalnızca `p < 0,05` etiketi üretmek kabul ölçütü yapılmadı. Yöntemin birincil kaynağı seçildikten sonra bu sayfaya eklenecek; henüz istatistik kütüphanesi veya test belirlenmedi.

## Taslak analiz çıktısı

Her sonuçta ürün/sürüm, bölge sınırı, dönem, birim, kullanılan örnek sayısı, eksiklik, ön işleme ve yöntem bilgisi bulunması öneriliyor. Eğim, belirsizlik ve varsa p-değeri bu bağlamla sunulmalı. Üretilecek gerçek sayılar [kanıt kaydına](../evidence/index.md) dayanmalı.

## T2M pilotu için konuşulan yöntem adayları

İlk gösterge T2M olarak seçildi; yöntem henüz seçilmedi. Her modül kendi bilimsel yöntemini yönetir; ortak sözleşme tek test zorunluluğu değildir.

- Aylık sıcaklıkta zaman eğilimi + takvim ayı etkileri; belirsizlik için zaman bağımlılığını dikkate alan HAC/Newey–West yaklaşımı adaydır. [Statsmodels koşulları](https://www.statsmodels.org/stable/generated/statsmodels.stats.sandwich_covariance.cov_hac.html) ardışık/eşit aralıklı zaman varsayar; eksik ayları silip ardışık saymak doğru değildir.
- Theil–Sen ve uygun Mann–Kendall yaklaşımı alternatif/duyarlılık incelemesidir. Standart test mevsimsellik ve zaman bağımlılığını kendiliğinden çözmez. [USGS yöntem araştırması](https://www.usgs.gov/publications/techniques-trend-analysis-monthly-water-quality-data-0).
- A'da anlamlı, B'de anlamsız sonuç çıkması A/B eğilimlerinin farklılığını kanıtlamaz. Ortak tarihlerde fark serisi veya uygun ortak modelle fark ayrıca sınanır.
- Çok sayıda modül/piksel testinde soru ailesi ve bağımlılık yapısına uygun çoklu test kontrolü gerekir; [FDR yöntemleri](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.fdrcorrection.html) adaydır.
- Eğim, aralık, kalite ve kapsam birlikte gösterilir; p-değeri değişimin doğru olma olasılığı değildir. Anlamsız sonuç kesin değişim yokluğu sayılmaz. İstatistiksel aralık bütün ürün/model belirsizliklerini kapsamaz.

Girdi/çıktı türü, analiz profili, varsayımlar ve özel tanılar [sonuç sözleşmesinde](../architecture/DATA_AND_FLOWS.md) korunacak. Bunlar tasarım tartışmasıdır; çalıştırılmış analiz değildir.
