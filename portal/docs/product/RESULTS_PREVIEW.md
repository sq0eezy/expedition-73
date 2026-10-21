---
status: Validating
updated: "2026-10-22"
review_summary: "Gerçek kayıtlı sıcaklık sonuçlarını inceleten ilk yerel ekran; bilimsel ve ürün sınırları."
change_summary: "İki pencere için teknik eşleşme koşulları, yönlü aylık fark grafiği/tablosu ve geçerli çift sayıları eklendi; bilimsel profil kabulü yok."
---
# İlk sonuç ekranı · Yerel teknik prototip

M1, ilk ekran önerisinden sonra devam istedi. Bu dilimde `web/` altında çalışan bir teknik prototip hazırlandı; nihai ürün teknolojisi, genel web sorumlusu veya bilimsel profil seçimi değildir. Yönetim portalı proje hafızasıdır; yeni ekran kayıtlı hesap sonuçlarını inceletir. [Gerçek tarayıcı/test kanıtı](../evidence/RESULTS_PREVIEW_CHECK.md).

## Çalışan deneyim

| Eylem | Gözlenen davranış |
|---|---|
| Pencere seç | A/B birlikte veya tek görünür; hiçbir pencere seçilmezse açık boş durum |
| Yüzey ağırlığını seç | Bütün pencere, FRLAND, FRLAND+FRLANDICE; grafik/kart/tablo/kapsam aynı seçimden beslenir |
| Ayı değiştir | 12 aylık seri korunur; işaret ve sıcaklık kartları seçili ayı gösterir |
| İki pencereyi incele | Seçili ayın mekânsal farkı gösterilir; trend/iklim etkisi diye adlandırılmaz |
| Ağırlıkları kıyasla | Aynı ayın üç sonucu; iki ikili farkın işaretli ay değeri, yıllık en büyük mutlak farkı/ayı ve her çiftin eşleşen ay sayısı görünür |
| Hücreye in | A/B hücre şeması, ayın grid T2M rengi, tam/kesilmiş sınır; tıklama ve ok tuşlarıyla seçilen hücrenin sıcaklığı, dört fraksiyonu ve etkin alanı görünür |
| Kapsama bak | Hücre sayıları, kesilmiş sınır parçaları veya iki adayın koşullu alan sınırları görünür; güven aralığı denmez |
| Kaynağı aç | Grid sıcaklığı tanımı, dönem/zaman standardı, aday bbox, kaynak kayıt zamanı/URL/hash görünür; AREA karşılaştırmasının yokluğu ve hesaplanmamış eğilim belirtilir |
| Tablo / indirme | Sayısal tablo 12 ayı gösterir; JSON seçili pencere, ay, politika ve kaynak izlerini korur |

Başlangıçta maskesiz görünüm açıktır; bu, bilimsel maske kabulü anlamına gelmez. Eksik sıcaklık null kalır, grafik boşluğu birleştirilmez, o ayın farkı üretilmez. Kaynak yüklenemez veya sözleşme uymazsa sonuç kartları gizlenir, hata ve yeniden deneme görünür.

## Hücre incelemesi · 2026-10-20

Aday sınırla kesişen 56/55 hücre gösterilir. Renk ölçeği bütün kayıtlı hücre/aylardan ortak kurulur; pencere/ay seçimiyle ölçek değişmez. Gri, eksik sıcaklıktır. Yüzey seçimi hücre sıcaklığını değiştirmez; etkin alanı ve geçerli aylık alan payını değiştirir. Eksik sıcaklıklı hücrenin geçerli katkısı sıfır gösterilir; analizdeki eksik veri kuralı korunur.

Dikdörtgen şema enlem/boylam düzlemindedir, alan koruyan bir harita veya kıyı çizgisi değildir. Hücre kenarları mevcut orta nokta yaklaşımına dayanır; tam hücre fraksiyonunun kesişimde homojenliği ve kaynak AREA eksikliği aynı sınırlar olarak kalır. Web aktarımı `recorded_temperature_web_preview` 0.2.0 gerekli hücre alanlarını ekler; kaynak çıktı şemaları/bilimsel yöntem/teknik profil değişmedi. Eski web verisini yeni arayüzle kullanmak yerine builder tekrar çalıştırılır. [Yeni doğrulama](../evidence/SPATIAL_PREVIEW_CHECK.md).

## Aday ağırlıkları yan yana inceleme · 2026-10-20

Yeni bölüm her pencerenin üç politikasını aynı ayda gösterir; grafikte seçili politika işaretlenir. İki fark açık adlandırılır: kara−maskesiz ve kara+kara buzu−kara. Bunlar A−B mekânsal farkı değildir. İlgili ikilide eksik olan ay hesaba alınmaz, çiftlerin geçerli sayıları ayrı gösterilir. Hiç geçerli çift yoksa maksimum verilmez; sıfır değer geçerlidir. En büyük mutlak farkın tüm tam eşit ayları korunur.

`comparison.mjs` mevcut aylık değerlerden çıkarma ve maksimum yapar; yuvarlama yalnız gösterimde, altı ondalıktır. Bu ölçüm doğruluğu değildir. Küçük fark bilimsel maske/alan/yüzey tanımını doğrulamaz; sonuç belirsizlik, güven aralığı veya iklim eğilimi değildir. Teknik deneme profili 0.1.0 ve web aktarımı 0.2.0 olarak korunur. [Kayıtlı sonuçlar ve kontroller](../evidence/POLICY_COMPARISON_CHECK.md).

## Hesap ve arayüz ayrımı

`analysis/scripts/build_web_preview.py` / `expedition73.web_preview`, her kaynağı mevcut gerçek workflow ile bir kez doğrular. Yüzey kapsamı aynı doğrulanmış girdilerden hesaplanır; AREA metadata hash'i snapshot ile eşleştirilir. Ekran yeni bilimsel yöntem çalıştırmaz; hazır serileri gösterir, seçili ayın A−B farkını ve aynı pencerenin aday politikaları arasındaki ikili fark/maksimumları hesaplar. [Hesap akışı](../evidence/SURFACE_WORKFLOW.md), [koşullu kapsam](../research/SURFACE_SUPPORT.md), [AREA yeterliliği](../research/SOURCE_AREA.md).

`web/regions.json` bir kaynak listesidir; yeni uygun bölge aynı T2M işlemlerine buradan bağlanır. Prototip aynı takvim yılını paylaşan 1–8 kayıtlı pencereyi destekler; gösterge, zaman standardı ve sağlayıcı/sürüm metaverisi eşleşmelidir. Bu teknik kontrol bilimsel karşılaştırma onayı değildir. Kaynak değişince yeniden derleme gerekir. Desteklenmeyen gösterge, serbest poligon, anlık NASA sorgusu, kalıcı işler veya genel modül editörü eklenmedi.

## Geliştirme paketi · 2026-10-21

Yeni isteğe bağlı [Docker/native geliştirme yolu](../guide/DEV_PACKAGE.md), ortak offline kontrol ve beş genel dosyalı demo ZIP eklenmiştir. Mevcut ekran, bilimsel hesap ve web 0.2.0 sözleşmesi korunur. Docker yalnız localhost'ta statik çıktıyı sunar; NASA/token kullanan API veya web yayını değildir. [Gerçek kontroller](../evidence/DEV_PACKAGE_CHECK.md). Bu yeni dilim M1 dalında yereldir; M2 ortam/arayüz kabulü yok.

## Yerel çalıştırma ve paylaşım

Depo kökünde Windows CMD:

```cmd
analysis\.venv\Scripts\python.exe analysis\scripts\build_web_preview.py
analysis\.venv\Scripts\python.exe web\serve.py
```

Mac/Linux: `analysis/.venv/bin/python analysis/scripts/build_web_preview.py`, ardından `python3 web/serve.py`. Analysis ortamı için requirements-mask paketleri gerekir. Adres `http://127.0.0.1:8873/`; kapatma terminalde Ctrl+C. Dosyaya çift tıklamak yerine HTTP adresi kullanılır. Gerçek macOS koşusu yapılmadı.

Builder yalnız dört uygulama dosyası ve doğrulanmış seri/hücre JSON dosyası üretir; sunucu yalnız `web/dist` klasörünü sunar. Token/özel .env/ham özel artifacts tarayıcıya verilmez; tarayıcı çalışırken dış veri isteği yapmaz. Ayrı Node/Playwright yalnız isteğe bağlı QA içindir.

Yeni kod 2026-10-20 kullanıcı talebiyle [GitHub M1 dalında paylaşıldı](../team/SYNC.md). Main/Pages güncellenmedi; mevcut Pages işi yalnız portalı derler. Web ekranının barındırılması, uzun dönem istatistik ve nihai bilimsel A/B karşılaştırması açık. Sonraki küçük adım, bu ekran akışının ekipçe incelenmesi ve gösterilecek yüzey/dönem/kapsamın netleştirilmesidir.

## 2026-10-21 · Gerçek modül akışını inceleme

Her seçili aday pencere için derlemede doğrulanan beş adım ve sekiz veri bağlantısı gösterilir. Sıcaklık girdisi bir kez çalışır; fraksiyon kontrolü onu tüketir; kara ve kara+buz hesapları aynı iki girdiyi tüketir; karşılaştırma sıcaklık ile iki ağırlık sonucunu alır. Konu hiyerarşisi bu hesap oklarıyla karıştırılmaz. Bölge seçimi, klavye/tıklama ayrıntısı ve telefon için dikey akış vardır. Adım ayrıntısı gerçek işlem sürümünü, çıktı sözleşmesini, girdi alias/üreticilerini ve iş tanımı kimliğini gösterir.

Önce gerçek çıktı/ata kimlikleri kontrol edilir, sonra küçük genel aktarım üretilir. Tanım parmak izi kaynak snapshot'ı ve işlem tanımına bağlıdır; bilimsel sonuç hash'i veya imza değildir. Rastgele run UUID'leri/özel parametreler aktarılmaz. Yalnız tamamlanmış derleme kaydı gösterilir; bekleyen/çalışan/hatalı işler için canlı izleme, cache veya sunucu eklendiği anlamına gelmez. Yeni uygun bölge aynı kayıttan yapılandırılır; grafik sabit A/B bağlantıları içermez.

**Güncel web aktarımı 0.3.0**, yalnız bu görünüm için zorunlu `workflow_trace` alanı eklendi. Kaynak T2M/fraksiyon şemaları, bilimsel yöntem ve teknik profil 0.1.0 değişmedi. Genel dosya sayısı altı; ZIP manifesti 0.2.0, eski ZIP doğrulaması korunur. [Gerçek kontroller ve sınırlamalar](../evidence/WORKFLOW_TRACE_CHECK.md). U-02/MOD-06 Validating; yeni kod yerel M1 dalında, M2 incelemesi veya main/Pages yayını yok.

## 2026-10-22 · İki pencerenin aynı ay farkı

Görünür adaylardan iki farklı pencere seçilir; sol−sağ farkı, yön değiştirme, seçili ay, üç ortak yüzey ağırlığı, sıfır merkezli fark grafiği/tablosu, en büyük |fark| ve ayrı geçerli ay çifti sayısı incelenir. Tek/boş seçimde eski sonuç temizlenir. Yeni uygun bölge aynı seçim mantığıyla çalışır.

Saf `summarizeRegionDifferences` gösterge/yükseklik/birim, takvim/dönem/zaman standardı, sağlayıcı/ürün/API/kaynak üyeleri, grid/alan yaklaşımı ve kullanılan işlem/sözleşme sürümlerini kontrol eder. Kara seçeneklerinde fraksiyon ürünü/sürümü/DMR hash'i/yerleşim varsayımı da eşleşir. Maskesizde fraksiyon kullanılmıyor gösterilir. Uyumsuzlukta fark hesaplanmaz, koşul tablosu açılır; mevcut üst fark kartı da bu kapıyı kullanır. Eşleşme bilimsel kabul değildir.

Eksik çift null kalır ve çizgi kesilir; sıfır korunur. Maksimum yalnız geçerli aylardan seçilir, tüm eşit maksimum ayları saklanır. Tamamen eksikte sıfır maksimum uydurulmaz. Hesap önce yuvarlanmaz; üç ondalık gösterimi ölçüm doğruluğu veya hata payı değildir. A/B 2024 maskesiz en büyük |fark| Mart'ta yaklaşık 26,185 °C: **iki aday yerin mekânsal sıcaklık farkı**, küresel ısınma etkisinin veya trendlerin farkı değil.

[Gerçek kontrol](../evidence/REGION_COMPARISON_CHECK.md): Windows 180 analiz, gerçek A/B tekrarları, 22 JS ve 36 Chrome senaryosu. Analiz kaynakları ve data/results.json değişmedi; web 0.3.0/manifest 0.2.0/altı dosya korunur. JSON indirme mevcut girdileri sunar, yeni fark özetini eklemez. Yeni kod yerel M1 dalında, M2 kabulü/yayın ve bilimsel maske/sınır/uzun dönem seçimi yok.
