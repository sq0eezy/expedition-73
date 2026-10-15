# Araştırma kaydı

## 2026-10-15 · İstatistik ve benzer araçlar

Önceki tartışmada birincil kaynaklar incelendi: [NASA Giovanni](https://giovanni.gsfc.nasa.gov/giovanni/doc/UsersManualworkingdocument.docx.html), [Worldview karşılaştırması](https://www.earthdata.nasa.gov/learn/blog/introducing-worldviews-comparison-feature?page=18), [Climate Engine](https://climateengine.org/get_started/dive-in-make-a-graph/) ve [CCKP trend/anlamlılık görünümü](https://climateknowledgeportal.worldbank.org/watershed/wca002057/trends-variability-historical). Bölge serileri, görsel karşılaştırma ve trend sunumu için mevcut örnekler var; projenin özgün katkısı henüz kanıtlanmış değildir.

[Earth Engine topluluk örneği](https://developers.google.com/earth-engine/tutorials/community/nonparametric-trends) MODIS EVI üzerinde Mann–Kendall/Sen eğimi kodu gösterir; örneğin mevsimsellik varsayımı ve eski ürün sürümü pilotta körlemesine kopyalanmaz. Araçlarda gerçek proje analizi çalıştırılmadı. [Yöntem adayları ve sınırlar](SCIENCE_NOTES.md), [dar T2M pilotu](../planning/PILOT.md).

## 2026-10-15 · Veriye göre bölge seçimi

Türkiye'nin örnek olduğu kullanıcı tarafından açıklandı. Coğrafi veri düzeni resmî Earthdata/CMR/MODIS/AppEEARS kaynaklarından araştırıldı. Aynı üç ürün için iki alanda tam aralık ve iki örnek ayı kapsayan 18 granule sorgusu çalıştırıldı. [Araştırma](REGION_CANDIDATES.md), [çıktı](REGION_CATALOG_CHECK.json), [yöntem ve sınırlar](../evidence/REGION_RESEARCH.md).

Colorado Platosu çevresi ve Kuzey Alaska **aday** olarak önerildi; bu iki alan için hesaplanmış eğim veya ortak seçim yok. Kullanıcının bölge/modül düşüncesi [öneri taslağında](../architecture/REGIONAL_MODULE_PROPOSAL.md) işlendi. M2 görüşü [fikir kartında](../team/ideas/IDEA-M1-001.md) bekliyor.

## 2026-10-15 · İlk kaynak incelemesi

Kullanıcının ilk yapay zekâ konuşması özetlendi. Challenge açıklaması kullanıcıdan geldi; önerilen değişkenlerin hiçbiri ekip seçimi sayılmadı. Kullanıcı aynı gün fikirlerin hâlâ karşılaştırıldığını doğruladı.

Resmî NASA/GIBS ürün sayfaları tarayıcı araştırmasıyla incelendi; [kaynak tablosunda](DATA_SOURCES.md) hangi sayfanın okunabildiği ve hangi erişimin denenmediği belirtilir. Sayfa okumak veri indirme/analiz kanıtı değildir.

**Çıktı:** [Fikir karşılaştırması](../discovery/IDEA_COMPARISON.md) ve [bilimsel kontrol noktaları](SCIENCE_NOTES.md).

Sonraki araştırmalarda tarih, soru, kaynak, gözlem, yorum ve sınırlamayı birlikte kaydedin. “Bir yapay zekâ önerdi” ifadesi bilimsel atıf yerine geçmez.
