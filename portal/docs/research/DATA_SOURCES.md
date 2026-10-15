---
review_summary: "NASA bağlantıları, veri/görsel ayrımı ve henüz sınanmamış erişim adımları."
change_summary: "Resmî kaynaklara dayanan ilk araştırma listesi eklendi."
---
# NASA veri kaynakları

## Yeni bölge araştırması

NASA'nın coğrafi düzeni ve ülke/poligon alt kümesi [bölge seçimi araştırmasında](REGION_CANDIDATES.md) açıklanır. Bu oturumda `M2TMNXSLV` 5.12.4, `MOD13A3` 061 ve `MOD10CM` 61 için gerçek CMR alan/zaman sorguları yapıldı. [Kaydedilmiş sorgular](REGION_CATALOG_CHECK.json) metadata eşleşmeleridir; sayısal dosya, giriş veya kalite kontrolü değildir. Aşağıdaki MOD13C2/GISTEMP/GRACE seçenekleri önceki alternatifler olarak durur; ürün seçimi yapılmadı.

**İnceleme tarihi: 2026-10-15.** Sayfa içeriğinin okunması, dosya indirmenin veya servis entegrasyonunun çalıştığını göstermez. Hiçbir ürün henüz seçilmedi.

| Kaynak | Burada ne için kullanılır? | İnceleme ve sıradaki sınama |
|---|---|---|
| [Worldview](https://worldview.earthdata.nasa.gov/) | Görsel keşif adayı | Dinamik uygulama adresine ulaşıldı; katman/tarih etkileşimi denenmedi |
| [GIBS görselleştirme belgeleri](https://nasa-gibs.github.io/gibs-api-docs/available-visualizations/) | Harita görüntü katmanlarının nasıl sunulduğunu anlamak | Belge okundu; katman kataloğu sayfada hata verdi. Seçilecek katmanın tarih, projeksiyon ve formatı ayrıca sınanmalı |
| [Giovanni](https://giovanni.gsfc.nasa.gov/giovanni/) | Ön keşif/analiz aracı adayı | Giriş sayfası okundu; veri seçimi, oturum ve dışa aktarım denenmedi |
| [Earthdata Search](https://search.earthdata.nasa.gov/) | Ürün ve dosya bulma | Keşif bağlantısı; ürün bazlı indirme ve kimlik doğrulama henüz sınanmadı |

## Sayısal ürün adayları

### MODIS MOD13C2 V061 · Bitki örtüsü

[NASA ürün kaydı](https://data.nasa.gov/dataset/modis-terra-vegetation-indices-monthly-l3-global-0-05deg-cmg-v061-64885) ve [LAADS ürün sayfası](https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/MOD13C2) incelendi. Aylık 0,05° ızgara üzerinde NDVI/EVI katmanları sunan bir aday. Henüz dosya indirilmedi.

Sonraki inceleme: güncel dosya erişimi, dönem kapsamı, ölçek katsayısı, geçerli değer aralığı, dolgu değerleri ve kalite alanları. Dünya ölçeği için uygunluk değerlendirilirken küçük yerel alanlardaki ayrıntı sınırlaması kontrol edilmeli.

### GRACE / GRACE-FO · Su depolaması

[JPL yeraltı suyu açıklaması](https://grace.jpl.nasa.gov/applications/groundwater/) okundu. Yeraltı suyunu ayıran çalışmalar ek hidrolojik bileşenleri kullanır; bir GRACE su depolaması serisini doğrudan yalnızca yeraltı suyu diye etiketlemeyelim.

Sonraki inceleme: [ürün seçimi rehberi](https://grace.jpl.nasa.gov/data/), ürün sürümü, birim, belirsizlik, eksik aylar ve bölgesel çözünürlük. Ürün veya dosya henüz seçilmedi.

### GISTEMP v4 · Sıcaklık

[NASA GISS sayfası](https://data.giss.nasa.gov/gistemp/) okundu. Aylık yüzey sıcaklık anomalileri ve ızgaralı veri indirme seçenekleri bulunuyor. Bölgesel inceleme için küresel ortalama tablo yerine uygun ızgaralı ürün değerlendirilmeli.

Sonraki inceleme: referans dönem, kapsama alanı, birim, eksiklik ve seçilecek bölge ölçeği. Dosya indirilmedi.

## Görsel ve analiz verisi ayrı kayıtlar

GIBS rasterları ölçümleri renklere eşleyen görsellerdir ([teknik açıklama](https://nasa-gibs.github.io/gibs-api-docs/available-visualizations/)). **Öneri:** trendleri seçilmiş sayısal üründen hesaplayıp, görüntüyü görsel bağlam için kullanalım. Bir görüntü katmanının sorunsuz açılması, analiz verisinin de aynı yolla alınabileceğini kanıtlamaz.

Paylaşılan konuşmadaki genel WMTS adresi doğrudan yapılandırma sayılmadı. Katman kimliği, tile matrix set, uzantı, tarih ve projeksiyon gerçek servis metaverisiyle doğrulanmalı. Erişim/hesap gereksinimi her kaynak için ayrı sınanacak.
