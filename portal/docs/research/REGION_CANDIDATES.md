---
review_summary: "NASA'nın coğrafi veri düzeni, seçim ölçütleri ve gerekçeli iki bölge adayı."
change_summary: "Colorado Platosu ve Kuzey Alaska, kaynak ve CMR sorgularıyla tartışma adayı olarak eklendi."
---
# Bölge seçimi ve iki aday

<div class="portal-hero" markdown>

## Adaylar araştırıldı; seçim yapılmadı

**Durum: Proposed · Tarih: 2026-10-15.** Kullanıcı Türkiye'nin yalnızca örnek olduğunu açıkladı. Bölge ve modüllerin NASA verilerine göre seçilmesini, iki gerekçeli adayın arkadaşının incelemesine açılmasını istedi.

**Araştırma önerisi:** Colorado Platosu çevresindeki bir kara alanı ile Kuzey Alaska'daki bir kara alanında, sıcaklık ve bitki örtüsü eğilimlerini ortak ürünlerle incelemek. Zıt trend veya iklim kaynaklı neden sonucu henüz yok.

</div>

## NASA verileri ülkelere göre mi ayrılıyor?

NASA'nın tek bir ülke temelli bölgeleme sistemi yok. Earthdata'da veri **konu, görev/algılayıcı, ürün ve sürüm** üzerinden bulunur; zaman ve coğrafya ayrıca filtrelenir. Bir collection ürün koleksiyonunu, granule ise o ürünün bir dosya/veri birimini ifade eder. [Earthdata Search](https://search.earthdata.nasa.gov/), [arama açıklaması](https://forum.earthdata.nasa.gov/viewtopic.php?t=5121).

| Ürünün coğrafi düzeni | Ne anlama gelir? | Bölgeyi nasıl alırız? |
|---|---|---|
| Küresel enlem-boylam ızgarası | Örneğin MERRA-2 düzenli bir dünya ızgarasında model/yeniden analiz alanları sunar | Bölgeyle kesişen hücreleri ve istenen değişkeni seçeriz |
| Karolara bölünmüş ızgara | MODIS'in birçok kara ürünü sinusoidal `h/v` karolarındadır; bunlar ülke sınırı değildir | İlgili karoları bulup birleştirir, poligonla keseriz |
| Küresel Climate Modeling Grid | Bazı MODIS ürünleri 0,05° enlem-boylam ızgarasındadır | Küresel dosyanın ilgili alanını çıkarırız |
| Yörünge/geçiş verisi | Bazı ürünler uydu geçişi boyunca ölçümler içerir | Alan ve zamanla kesişen geçişleri seçip örnekleme kapsamını inceleriz |

Izgara örneklerinin dayanağı: [MODIS kara ızgaraları](https://modis-land.gsfc.nasa.gov/MODLAND_grid.html), [MERRA-2 ürünleri](https://gmao.gsfc.nasa.gov/gmao-products/reanalysis-products/).

**Türkiye seçilseydi:** küresel ürünlerde Türkiye sınırıyla kesişen hücreleri çıkarabilirdik; ayrı bir “Türkiye paketi” bulunması gerekmez. Önce dikdörtgenle dosya aranabilir; ülke analizi için gerçek sınır poligonu, kara/su maskesi ve piksel ağırlıkları gerekir. Dikdörtgen komşu ülkeleri veya denizi içerebilir. Bu oturum Türkiye için ayrı dosya/piksel kontrolü yapmadı.

[CMR](https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html) alanla kesişen dosyaları bulur. [AppEEARS](https://appeears.earthdatacloud.nasa.gov/) desteklediği ürünlerde nokta/poligon, zaman ve katman alt kümeleri ile kalite alanları sunar. Katalogda dosya bulmak ile poligon içinden geçerli sayısal piksel çıkarmak ayrı adımlardır. Her ürün aynı alt küme servisini desteklemeyebilir.

## Adayları hangi ölçütlerle çıkardık?

1. Aynı ölçümün iki yerde de aynı ürün/sürümle incelenebilmesi.
2. Uzun ve örtüşen bir dönemin araştırılabilmesi; başlangıç önerisi **2001–2024**, henüz kabul edilmedi.
3. İki alanın da kara olması ve bitki örtüsü karşılaştırmasına elverişli olması.
4. Farklı çevresel koşulların kaynaklı bir araştırma sorusu oluşturması.
5. Bölgeyi yeniden bulabileceğimiz açık bir coğrafi tanım.
6. Kar, bulut, çıplak zemin, sulama ve yangın gibi karıştırıcıların görünür tutulması.

Sayısal başarı puanı veya garanti edilen zıt eğim üretilmedi. Aşağıdaki dikdörtgenler **ön arama pencereleridir**; NASA'nın resmî ekolojik sınırları değildir. Veri kalitesinden sonra gerekçeli poligon seçimi yapılmalı; istenen eğimi elde etmek için sınır kaydırılmamalı.

## Aday A · Colorado Platosu çevresi, güneybatı ABD

**Ön arama penceresi:** 113°B–109°B, 36°K–39°K (`west,south,east,north = -113,36,-109,39`). Colorado Platosu'nun tamamını temsil ettiği iddia edilmez. Utah/kuzey Arizona çevresinde sınırlı bir pilot araştırma alanıdır.

**Neden aday?** NASA'nın bölge anlatımı, kurak çalı/ot alanları ile yüksek kesimlerdeki ormanları birlikte gösteriyor. NASA arşivindeki güncel araştırma, güneybatı ABD kuraklığını ısınma ve dolaşım değişkenliği bağlamında inceliyor. Bu iki kaynak, sıcaklıkla birlikte suya duyarlı bitki örtüsünü araştırmak için gerekçe sunuyor; bu dikdörtgende NDVI'nın azaldığını kanıtlamıyor. [NASA bölge tanımı](https://modis.gsfc.nasa.gov/gallery/individual.php?db_date=2021-04-13), [NASA NTRS araştırması](https://ntrs.nasa.gov/citations/20250007013).

**Soru:** Bu kara alanında sıcaklık eğilimi ve bitki yeşilliğinin mevsimsel/yıllar arası değişimi nasıl görünüyor?

**Zorluk:** Çıplak kaya/zemin, yükselti, sulanan alanlar ve yangınlar ayrı incelenmeli. Düşük NDVI doğrudan çölleşme veya iklim etkisi diye adlandırılmamalı.

## Aday B · Kuzey Alaska, Brooks Range–North Slope çevresi

**Ön arama penceresi:** 156°B–150°B, 68°K–70°K (`west,south,east,north = -156,68,-150,70`). Kuzey Kutbu noktası veya bütün Arktik değildir. Dağ/etek/tundra kara alanı için pilot arama penceresidir.

**Neden aday?** NASA destekli Brooks Range çalışmaları bu çevredeki tundra/orman geçişini ve hem yeşillenme hem kahverengileşmenin nedenlerine ilişkin açık soruları ele alıyor. Bu, “ısınan yerde bitki tepkisi her zaman aynı mıdır?” sorusu için kaynaklı bir bağlam sunuyor. [NASA saha araştırması](https://science.nasa.gov/blogs/notes-from-the-field/2021/10/05/unraveling-the-mysteries-of-arctic-greening-and-browning/).

**Soru:** Soğuk kara ekosisteminde sıcaklık eğilimi, büyüme mevsimi ve yeşillik göstergeleri nasıl birlikte değişiyor?

**Zorluk:** Uzun kar mevsimi, kutup gecesi, bulut, göller ve yüksek arazi kalite filtresi gerektirir. Her kış ayındaki geçersiz NDVI sıfır sayılamaz; yıllık ortalama ile büyüme mevsimi göstergesi ayrı değerlendirilmelidir.

## İkisini neden birlikte öneriyoruz?

İkisi de Kuzey Yarımküre kara alanı; aynı NASA ürün ailesiyle çalışılabilir. Su kısıtı araştırmasına uygun bir kurak bölge ile soğuk mevsim koşulları belirgin bir kuzey bölgesi karşılaştırılır. **Farklı tepkiler bir hipotezdir.** İkisi de aynı yönde değişebilir veya anlamlı trend çıkmayabilir. Aynı ülke sınırları içinde olmaları, iki ayrı coğrafi/ekolojik bölge oldukları gerçeğini değiştirmez; teknik seçim ülke sayısına dayanmıyor.

## Ortak modül adayları ve gerçek katalog kontrolü

| Modül / ürün | Coğrafi yapı | A: 2001–2024 eşleşme | B: 2001–2024 eşleşme | Karar öncesi kontrol |
|---|---|---|---|---|
| 2 m hava sıcaklığı · MERRA-2 `M2TMNXSLV` 5.12.4 | Küresel 0,5° × 0,625° ızgara | 288 granule | 288 granule | T2M, birim, bölge hücreleri, aylık bütünlük |
| Bitki örtüsü · MODIS `MOD13A3` 061 | Aylık 1 km sinusoidal karolar | 576 granule | 2258 granule | Karo kesişimi, NDVI/EVI ölçeği, kalite, geçerli piksel/mevsim |
| Kar · MODIS `MOD10CM` 61 | Aylık küresel 0,05° CMG | 284 granule | 284 granule | Aylık kapsam, eksik/çakışan kayıt, karanlık/bulut; koşullu ek modül |

Ürün tanımları: [MERRA-2 T2M](https://gmao.gsfc.nasa.gov/gmao-products/merra-2/wmo-data-access_merra-2/), [MOD13A3](https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/MOD13A3), [MOD10CM](https://nsidc.org/data/mod10cm/versions/61).

**Ne sınandı?** NASA CMR koleksiyon ve granule metaverisi. Her ürün/alan için 2001–2024 aralığı, Temmuz 2001 ve Temmuz 2024 sorgulandı; iki örnek ayda da kayıt eşleşmesi bulundu. Tam URL ve örnek dosya kimlikleri [JSON kaydında](REGION_CATALOG_CHECK.json).

**Ne sınanmadı?** Bilimsel dosya indirme/oturum, gerçek pikseller, bütün ayların kapsaması, kalite bayrakları ve trend. MODIS dosya sayıları karo ve zaman aralığı kesişimlerinden etkilenir; B'nin daha çok dosyası olması daha çok geçerli gözlem olduğu anlamına gelmez. Kar sorgusunda 288 yerine 284 kayıt çıkması kapsam kontrolü gerektirir; hangi ayların eksik/çakışan olduğu henüz belirlenmedi. Sorgular metaveri aralıklarıyla kesiştiği için bir aya birden fazla kayıt dönebilir.

## Karar için küçük pilot

Önce iki alan için aynı ürünlerden küçük sayısal alt kümeler alalım. Kara, bitki örtüsü ve kalite maskeleriyle geçerli piksel/ay oranlarını raporlayalım. Ortak dönem ve mevsim tanımını bundan sonra seçelim. Bir aday uygun değilse reddetme gerekçesini saklayıp başka alan araştırabiliriz.

Sıcaklık kendi birimiyle, NDVI kendi birimiyle karşılaştırılır. Ortak referans dönem ve uygun mevsim/alan ağırlığı açıklanır; iki farklı değişkenin ham eğimleri birbirine eşitmiş gibi çizilmez. Eğim, belirsizlik ve anlamlılık için yöntem ayrıca seçilecek. Nüfus, geniş “toprak kalitesi” başlığı ve yeni modüller bu pilotun kapsamına otomatik eklenmedi.

[Bölge + modül önerisi](../architecture/REGIONAL_MODULE_PROPOSAL.md) · [Ekip tartışma kartı](../team/ideas/IDEA-M1-001.md) · [Kontrol kanıtı](../evidence/REGION_RESEARCH.md)
