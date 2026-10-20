---
status: Validating
updated: "2026-10-20"
review_summary: "Gerçek kayıtlı sıcaklık sonuçlarını inceleten ilk yerel ekran; bilimsel ve ürün sınırları."
change_summary: "Hücre şeması, gerçek hücre sıcaklığı/fraksiyonu ve etkin alan incelemesi eklendi; web aktarımı 0.2.0. 164 test ve 18 Chrome senaryosu geçti."
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
| Hücreye in | A/B hücre şeması, ayın grid T2M rengi, tam/kesilmiş sınır; tıklama ve ok tuşlarıyla seçilen hücrenin sıcaklığı, dört fraksiyonu ve etkin alanı görünür |
| Kapsama bak | Hücre sayıları, kesilmiş sınır parçaları veya iki adayın koşullu alan sınırları görünür; güven aralığı denmez |
| Kaynağı aç | Grid sıcaklığı tanımı, dönem/zaman standardı, aday bbox, kaynak kayıt zamanı/URL/hash görünür; AREA karşılaştırmasının yokluğu ve hesaplanmamış eğilim belirtilir |
| Tablo / indirme | Sayısal tablo 12 ayı gösterir; JSON seçili pencere, ay, politika ve kaynak izlerini korur |

Başlangıçta maskesiz görünüm açıktır; bu, bilimsel maske kabulü anlamına gelmez. Eksik sıcaklık null kalır, grafik boşluğu birleştirilmez, o ayın farkı üretilmez. Kaynak yüklenemez veya sözleşme uymazsa sonuç kartları gizlenir, hata ve yeniden deneme görünür.

## Hücre incelemesi · 2026-10-20

Aday sınırla kesişen 56/55 hücre gösterilir. Renk ölçeği bütün kayıtlı hücre/aylardan ortak kurulur; pencere/ay seçimiyle ölçek değişmez. Gri, eksik sıcaklıktır. Yüzey seçimi hücre sıcaklığını değiştirmez; etkin alanı ve geçerli aylık alan payını değiştirir. Eksik sıcaklıklı hücrenin geçerli katkısı sıfır gösterilir; analizdeki eksik veri kuralı korunur.

Dikdörtgen şema enlem/boylam düzlemindedir, alan koruyan bir harita veya kıyı çizgisi değildir. Hücre kenarları mevcut orta nokta yaklaşımına dayanır; tam hücre fraksiyonunun kesişimde homojenliği ve kaynak AREA eksikliği aynı sınırlar olarak kalır. Web aktarımı `recorded_temperature_web_preview` 0.2.0 gerekli hücre alanlarını ekler; kaynak çıktı şemaları/bilimsel yöntem/teknik profil değişmedi. Eski web verisini yeni arayüzle kullanmak yerine builder tekrar çalıştırılır. [Yeni doğrulama](../evidence/SPATIAL_PREVIEW_CHECK.md).

## Hesap ve arayüz ayrımı

`analysis/scripts/build_web_preview.py` / `expedition73.web_preview`, her kaynağı mevcut gerçek workflow ile bir kez doğrular. Yüzey kapsamı aynı doğrulanmış girdilerden hesaplanır; AREA metadata hash'i snapshot ile eşleştirilir. Ekran yeni bilimsel yöntem çalıştırmaz; yalnız hazır serileri gösterir ve seçili ayın aritmetik farkını hesaplar. [Hesap akışı](../evidence/SURFACE_WORKFLOW.md), [koşullu kapsam](../research/SURFACE_SUPPORT.md), [AREA yeterliliği](../research/SOURCE_AREA.md).

`web/regions.json` bir kaynak listesidir; yeni uygun bölge aynı T2M işlemlerine buradan bağlanır. Prototip aynı takvim yılını paylaşan 1–8 kayıtlı pencereyi destekler; gösterge, zaman standardı ve sağlayıcı/sürüm metaverisi eşleşmelidir. Bu teknik kontrol bilimsel karşılaştırma onayı değildir. Kaynak değişince yeniden derleme gerekir. Desteklenmeyen gösterge, serbest poligon, anlık NASA sorgusu, kalıcı işler veya genel modül editörü eklenmedi.

## Yerel çalıştırma ve paylaşım

Depo kökünde Windows CMD:

```cmd
analysis\.venv\Scripts\python.exe analysis\scripts\build_web_preview.py
analysis\.venv\Scripts\python.exe web\serve.py
```

Mac/Linux: `analysis/.venv/bin/python analysis/scripts/build_web_preview.py`, ardından `python3 web/serve.py`. Analysis ortamı için requirements-mask paketleri gerekir. Adres `http://127.0.0.1:8873/`; kapatma terminalde Ctrl+C. Dosyaya çift tıklamak yerine HTTP adresi kullanılır. Gerçek macOS koşusu yapılmadı.

Builder yalnız üç uygulama dosyası ve doğrulanmış seri/hücre JSON dosyası üretir; sunucu yalnız `web/dist` klasörünü sunar. Token/özel .env/ham özel artifacts tarayıcıya verilmez; tarayıcı çalışırken dış veri isteği yapmaz. Ayrı Node/Playwright yalnız isteğe bağlı QA içindir.

Yeni kod M1 dalında yerel. Main/Pages güncellenmedi; mevcut Pages işi yalnız portalı derler. Web ekranının barındırılması, uzun dönem istatistik ve nihai bilimsel A/B karşılaştırması açık. Sonraki küçük adım, bu ekran akışının ekipçe incelenmesi ve gösterilecek yüzey/dönem/kapsamın netleştirilmesidir.
