---
status: Validating
updated: "2026-10-19"
review_summary: "Gerçek kayıtlı sıcaklık sonuçlarını inceleten ilk yerel ekran; bilimsel ve ürün sınırları."
change_summary: "A/B seçimi, üç ağırlık görünümü, aylık grafik/kart/tablo, kaynak/kapsam ve JSON indirme çalışıyor."
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
| Kapsama bak | Hücre sayıları, kesilmiş sınır parçaları veya iki adayın koşullu alan sınırları görünür; güven aralığı denmez |
| Kaynağı aç | Grid sıcaklığı tanımı, dönem/zaman standardı, aday bbox, kaynak kayıt zamanı/URL/hash görünür; AREA karşılaştırmasının yokluğu ve hesaplanmamış eğilim belirtilir |
| Tablo / indirme | Sayısal tablo 12 ayı gösterir; JSON seçili pencere, ay, politika ve kaynak izlerini korur |

Başlangıçta maskesiz görünüm açıktır; bu, bilimsel maske kabulü anlamına gelmez. Eksik sıcaklık null kalır, grafik boşluğu birleştirilmez, o ayın farkı üretilmez. Kaynak yüklenemez veya sözleşme uymazsa sonuç kartları gizlenir, hata ve yeniden deneme görünür.

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

Builder yalnız üç uygulama dosyası ve toplu JSON üretir; sunucu yalnız `web/dist` klasörünü sunar. Token/özel .env/ham özel artifacts tarayıcıya verilmez; tarayıcı çalışırken dış veri isteği yapmaz. Ayrı Node/Playwright yalnız isteğe bağlı QA içindir.

Yeni kod M1 dalında yerel. Main/Pages güncellenmedi; mevcut Pages işi yalnız portalı derler. Web ekranının barındırılması, uzun dönem istatistik ve nihai bilimsel A/B karşılaştırması açık. Sonraki küçük adım, bu ekran akışının ekipçe incelenmesi ve gösterilecek yüzey/dönem/kapsamın netleştirilmesidir.
