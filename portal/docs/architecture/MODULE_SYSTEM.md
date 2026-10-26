---
review_summary: "Konu ağacı, modüle özel hesaplama ve çıktıyla bağlanan modüllerin sorumlulukları."
change_summary: "İlk yerel bağımlılık motoru ve yapay A/B/C örneği çalışıyor; 20 test eklendi. NASA modülleri, kalıcı cache ve web bağlantısı henüz yok."
---
# Modüller, alt modüller ve bağlantılar

**Yön kabul edildi:** [ADR-004](../decisions/ADR-004-MODULES-AND-PILOT.md). Genel bilimsel kimlikler ve sözleşme uygulama taslağıdır. Ayrı bir 0.1.0 yerel teknik yürütme denemesi ve istek şeması artık çalışıyor: [kanıt](../evidence/WORKFLOW_ENGINE.md). Bu, tüm bilimsel modüllerin entegrasyonu veya kalıcı kayıt sistemi değildir.

## İki ayrı ilişki

2026-10-26: [Yıllık ağırlık denetimi](../guide/T2M_ANNUAL_WEIGHTING.md), mevcut recorded_window_history 0.1.0 çıktısını ham kaynakları tekrar doğrulayarak tüketen ayrı bir Python modülüdür. Kendi iki aday hesabı ve candidate_annual_weighting_audit 0.1.0 şeması vardır. Bu ilk CLI henüz beş düğümlü yüzey motorunda kayıtlı yeni bir işlem veya web kataloğu değildir; [hedef/yöntem kabulü](../research/TEMPORAL_AGGREGATION.md) ve adaptör/akış entegrasyonu ayrı kalır.

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

## Birden çok girdiyi aynı çalıştırmada birleştirme · 2026-10-18 taslağı

M1, B'nin A'dan değer aldığı; C'nin de hem A hem B çıktısını beklediği örneğe hazır olup olmadığımızı sordu. Aşağıdaki A/B/C **modül adlarıdır**, coğrafi A/B bölgeleri değildir. Bu bölüm açıklığa kavuşturulmuş uygulama gereksinimi taslağıdır; devam talebiyle yapılan ilk teknik uygulamanın durumu aşağıdadır. Ayrıntılar iki üye tarafından ortak bilimsel yöntem olarak kabul edilmiş sayılmaz.

~~~mermaid
flowchart LR
    A[A modülü - çıktı a1] --> B[B modülü - a1 girdisiyle çıktı b1]
    A --> C[C modülü - a1 ve b1 birlikte]
    B --> C
~~~

1. C istendiğinde zorunlu girdileri ve onların girdileri bulunur. Eksik tanım/çıktı bağlantısı, desteklenmeyen sürüm ve döngü **hesap başlamadan** denetlenir. Üreticiden tüketiciye sıra bu örnekte A → B → C'dir; bağımsız dallar varsa birlikte çalıştırılabilir, zorunlu değildir.
2. Aynı bölge/sınır, dönem, kaynak, bilimsel profil ve parametreler için A çıktısı bir kez üretilir veya tamamen aynı girdilerle doğrulanmış kayıt kullanılır. Aynı modülün farklı bölge/dönem isteği ayrı çalışma kimliğidir; yanlış paylaşılmaz.
3. B, A'nın adını veya sadece sürümünü değil, **değişmez çıktı kimliğini ve veri özetini** alır. Örneğin B'nin kaydı `b1 consumes a1` olur; kaynak izinde bu bağ korunur.
4. C, `a1 + b1` çiftiyle çalışır. B `a1` ile hesaplanmışken C'ye yeni `a2` verilmez. C'nin girdi tanımı bu paylaşılan A kaynağında eşitlik ister; iki dalın bölge/zaman/birim/kalite/yöntem uygunluğu da ayrıca denetlenir. Farklı A kaynakları gerçekten amaçlanıyorsa ayrı adlandırılmış girdiler ve açık yöntem gerekçesi gerekir.
5. A değişince B ve C'nin önceki sonuçları güncel değil sayılır. Yeni a2 için önce b2, ardından `a2+b2` kullanan c2 oluşturulur. Devam eden eski çalıştırmanın girdileri değiştirilmez; eski sonuç kendi kaynak iziyle korunur, yeni seçimde güncel diye gösterilmez.
6. A başarısızsa B ve C **girdi nedeniyle engelli** kalır. B başarısızsa A sonucu korunur, C engelli kalır. Bir modülün teknik çalışmasını bitirmesi yeterli değildir: çıktı, alıcının kabul koşullarından geçmelidir. Kısmi hesap yalnız modülün yönteminde önceden tanımlıysa mümkündür; eksik değer sıfır diye tamamlanmaz.

Önerilen görünür durumlar: bekliyor, çalışıyor, tamamlandı, başarısız, girdi nedeniyle engelli ve güncel değil. Web uygulaması C'nin neden beklediğini, hangi kaynağı beklediğini ve girdi çıktı kimliklerini gösterebilir. Canlı durum geçişleri henüz arayüzde uygulanmadı; 2026-10-21 görünümü yalnız derlemede tamamlanan gerçek akışı gösterir.

“Büyük/küçük konu” otomatik hesap bağımlılığı oluşturmaz. Küresel ısınma bir gezinme başlığı olabilir; hesap yapacaksa göstergesi, yöntemi ve girdi tanımı ayrıca yazılır. Toprak nemi gelecekte NASA'dan doğrudan alınan ayrı bir gösterge olabilir; sırf sıcaklıkla ilişkili diye onu sıcaklıktan hesaplayan bağlantı kurulmaz. Sıcaklık–toprak nemi ilişki analizi ise iki seriyi tüketen ayrı bir modül olarak tanımlanabilir. Bilimsel ilişki/nedensellik ile çalıştırma bağımlılığı birbirinin yerine geçmez; bu örnekler kabul edilmiş yeni modül/veri seçimi değildir.

Fiziksel geri besleme gerektiren model gelecekte gündeme gelirse A ↔ B'yi bu sıraya doğrudan eklemek yerine zaman adımı veya yakınsama koşulları açıkça belirlenmiş ayrı bir birleşik hesap gerekir. İlk çalıştırma taslağı döngüleri reddeder; böyle bir çözücü henüz tasarlanıp uygulanmadı.

**Uygulama durumu · 2026-10-18:** `analysis/expedition73/workflow.py` içinde sıralı planlayıcı, aynı çalıştırmada ortak üreticiyi tek hesaplama, kayıtlı işlem sürümü/çıktı etiketi kontrolü, çıktı kimliği/ata izi, callback kopya izolasyonu ve hata/engelli durumu çalışıyor. `demo-workflow` tamamen yapay A/B/C ile ilk C=12, A değişince C=21 üretti. Eski A + yeni B karışımı reddedildi. `compare_snapshot` açık çağrıldığında tanımlı değişiklik için bağımlı sonuçları güncel değil olarak bulur; canlı otomatik izleme veya kalıcı cache değildir. [20 yeni test ve çalışma kanıtı](../evidence/WORKFLOW_ENGINE.md), [MOD-06](../planning/WORK_BOARD.md).

İlk sürüm tek context, düğüm başına tek `result` portu ve sıralı çalışma kullanır. Kayıtlı gerçek T2M/fraksiyon adaptörleri artık ayrı `run-surface-workflow` ile bağlandı: kaynak tekrar hesabı, bölge/sınır/koordinat ve çıktı tanımı kontrol ediliyor. İki açık aday ağırlık seçeneği hesaplanıyor; bu, tam bilimsel profil/kalite kabulü değildir. [Gerçek verili kanıt](../evidence/SURFACE_WORKFLOW.md). Dış kaynak revizyonu isteğe kaydedilmelidir. Genel bilimsel sonuç zarfı, çoklu çıktı portları, kalıcı iş deposu, kaynak değişimini izleme, tekrar çalıştırmalar arasında cache, paralel işler ve canlı iş görünümü sonraki kapsamdır. İlk yapay deneme bilimsel modül doğrulaması değildir; sonraki gerçek kayıt akışı da ikinci bilimsel gösterge veya kabul edilmiş maske analizi sayılmaz.

## İlk pilot ve genişleme

**İlk yerel görünüm · 2026-10-19:** [Sonuç prototipi](../product/RESULTS_PREVIEW.md) kayıtlı gerçek T2M/fraksiyon akışını derlemede doğrular ve yalnız toplu veriyi tarayıcıya verir. Bölge listesi aynı T2M işlemlerine yeni uygun kayıt bağlayabilir; konu ağacı/data dependency ayrımı korunur. Bu, genel modül editörü veya hesap sunucusu değildir; nihai bilimsel/yığın kararı açık.

İlk analiz modülü **2 metre hava sıcaklığı** olacak; konu grubu altında gösterilecek. İki bölgenin çıktıları karşılaştırma bileşenine bağlanarak tek göstergede yeniden kullanım sınanır. İkinci bilimsel modül geldiğinde modüller arası gerçek tüketim ayrıca denenir; çizim entegrasyon kanıtı değildir.

Yeni modül: gereksinimler + özel hesap + adaptör + ayrıntı görünümü + örnek doğrulama. Yeni bölge: sürümlü sınır + veri/kalite kapsamı + uygunluk sonucu. [Pilot koşulları](../planning/PILOT.md).

**Kayıtlı akış görünümü · 2026-10-21:** Sonuç ekranı aynı gerçek yüzey çalıştırmasının beş düğüm/sekiz bağını gösterir. Genel projeksiyondan önce artifact/girdi/ata/context tutarlılığı ve her adımın bir kez çalışması doğrulanır. Ekrandaki kararlı kimlik bir **tanım parmak izidir**; motorun rastgele çalıştırma UUID'sine bağlı değişmez artifact kimliği ile aynı değildir. Özel parametre/context/payload dışarı kopyalanmaz. Bu, canlı yürütme veya kalıcı cache uygulaması değildir. [Ürün kapsamı](../product/RESULTS_PREVIEW.md), [kanıt](../evidence/WORKFLOW_TRACE_CHECK.md).
