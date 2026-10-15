---
review_summary: "Konu ağacı, modüle özel hesaplama ve çıktıyla bağlanan modüllerin sorumlulukları."
change_summary: "Kabul edilen yaklaşım; contains/consumes ilişkileri, çıktı türleri ve genişleme kurallarıyla tanımlandı."
---
# Modüller, alt modüller ve bağlantılar

**Yön kabul edildi:** [ADR-004](../decisions/ADR-004-MODULES-AND-PILOT.md). Teknik kimlikler ve kurallar uygulama taslağıdır; çalışan kayıt sistemi veya doğrulanmış şema değildir.

## İki ayrı ilişki

| İlişki | Anlamı | Örnek |
|---|---|---|
| `contains` | Konuları ve alt modülleri düzenli gösterir | İklim göstergeleri → Hava sıcaklığı |
| `consumes` | Hesabın başka bir çıktıya ihtiyacını belirtir | Sıcaklık–yeşillik ilişkisi → sıcaklık serisi + NDVI serisi |

Konu ağacı gezinmeyi, veri bağımlılık grafiği çalıştırma sırasını belirler; ayrı saklanırlar. Aynı modül farklı konu görünümlerine bağlantıyla eklenebilir; hesap/veri kopyalanmaz. Alt modül üst başlıktan istatistik yöntemi devralmaz.

~~~mermaid
flowchart TB
    C[İklim göstergeleri] -. alt modül .-> T[2 metre hava sıcaklığı]
    E[Ekosistem göstergeleri] -. alt modül .-> V[Bitki yeşilliği - daha sonra]
    T --> TS[Sıcaklık zaman serisi]
    V --> VS[NDVI zaman serisi]
    TS --> R[İlişki analizi - daha sonra]
    VS --> R
    TS --> P[A ve B sıcaklık karşılaştırması]
~~~

Kesik oklar gezinme, düz oklar veri ilişkisidir; bilimsel nedensellik göstermez. “Küresel ısınma” geniş bir konu başlığı olabilir; sıcaklık modülü tek başına insan kaynaklı neden atfetmez. Üst başlık alt modül eğimlerini/p-değerlerini ortalayıp skor üretmez. Hesap yapan üst modülün girdisi, yöntemi ve çıktısı ayrıca tanımlanır.

## Modülün içi ve dışı

1. **Kaynak uyarlayıcı:** Ürün/sürüm, ölçek, birim, dosya ve kalite alanlarını okur.
2. **Özel hesap:** Göstergenin bilimsel tanımına uygun hazırlık, alan/zaman özeti ve analiz yapar.
3. **Sonuç adaptörü:** [Ortak sözleşmeyi](DATA_AND_FLOWS.md) üretir; özel tanı ve ayrıntıları saklar.
4. **Uygunluk kontrolü:** Sonucun alıcı modülün girdi gereksinimini karşılayıp karşılamadığını denetler.
5. **Sunum:** Ortak grafikler ve modüle özel ayrıntılar çıktılardan okunur.

Dosya okuma, alan ağırlığı ve doğrulama yardımcıları paylaşılabilir. Bütün değişkenlere tek test zorunlu tutulmaz. Yeni bölge mevcut modülün bölge/kalite tanımıyla eklenir; bölgeye özgü hesap kopyası açılmaz.

## Bir modül diğerinin girdisi olduğunda

Bağlantı, modül adından öte adlandırılmış ve sürümlü çıktıyı seçer. Örnek taslak:

`temperature_air_2m.monthly_series → temperature_vegetation_relation.temperature_input`

Çıktı tek sayı, seri, harita veya kalite raporu olabilir; alıcı beklediği türü açıklar. Harita girdisine eğim özeti verilemez. Hava/yüzey sıcaklığı eşitlenmez. Birim dönüşümünün kuralı saklanır; farklı dönem/maske/yöntemde gerekirse yeniden hesaplanır.

Kaynak çıktı kimliği/sürümü, üretim çalışması ve veri özeti korunur. Kaynak değişince bağımlı sonuç **güncel değil** sayılır; yeniden hesaplanmadan güncel gibi gösterilmez. Zorunlu girdi eksikse alıcı gerekçeli durur. Çalıştırma grafiğinde döngüye izin verilmez; fiziksel geri beslemeler pilotta kendiliğinden çift yönlü hesap oklarına dönüşmez.

## İlk pilot ve genişleme

İlk analiz modülü **2 metre hava sıcaklığı** olacak; konu grubu altında gösterilecek. İki bölgenin çıktıları karşılaştırma bileşenine bağlanarak tek göstergede yeniden kullanım sınanır. İkinci bilimsel modül geldiğinde modüller arası gerçek tüketim ayrıca denenir; çizim entegrasyon kanıtı değildir.

Yeni modül: gereksinimler + özel hesap + adaptör + ayrıntı görünümü + örnek doğrulama. Yeni bölge: sürümlü sınır + veri/kalite kapsamı + uygunluk sonucu. [Pilot koşulları](../planning/PILOT.md).
