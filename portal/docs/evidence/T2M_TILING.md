---
review_summary: "B aday penceresinde iki gerçek API isteği, beş ortak hücrenin çıkarılması ve parçalı erişim kontrolleri."
change_summary: "B'nin 6° sınırı korunarak 55 benzersiz hücre/12 ay hesaplandı; eski örnekler korundu."
---
# Parçalı T2M erişimi · Gerçek modül denemesi

**2026-10-17 · Windows/Python 3.12.14, `analysis/.venv`.** M1, M2'nin beklediği parçalı bölgesel desteğin geliştirilip main'de paylaşılmasını istedi. Çalışma ayrı M1 dalında geliştirildi. [M2'nin beklentisi](../team/HANDOFFS.md), [Mac/Windows kılavuzu](../guide/T2M_TILED_WINDOW.md).

## Gerçek kaynak ve istekler

M2'nin mevcut B aday dikdörtgeni `[-156,68,-150,70]` değişmedi. Bu sınır nihai bilimsel alan seçimi değildir. Ortak modülün teknik örneği için iki küçük [NASA POWER Monthly regional](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/) T2M isteği yapıldı; bütün arşiv indirilmedi. API v2.10.0, kaynak `MERRA2`, `C`, Temperature at 2 Meters, 2024, LST, -999 dolgu. Gerçek koordinatlar 0,625° boylam × 0,5° enlem ızgarasında.

| Parça | İstek bbox: west/south/east/north | UTC erişim | Ham SHA-256 |
|---|---|---|---|
| tile-001 | -156,3125 / 67,75 / -152,6875 / 70,25 | 2026-10-17 08:53:25 | `368c1795d022f7d26055474237f08f699e5acd1540dd4cece0208d4d64f92484` |
| tile-002 | -153,3125 / 67,75 / -149,6875 / 70,25 | 2026-10-17 08:53:26 | `0681c57fb4c68f774ae99e18115b14eeaad53f1f38f9161fbd185616105b7d1f` |

Türkiye saatleri 11:53:25 ve 11:53:26. Tam URL/zaman/hash [manifestte](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-window-2024/manifest.json); ham yanıtlar, istek ve sonuç [aynı klasörde](https://github.com/sq0eezy/expedition-73/tree/main/analysis/examples/b-window-2024).

## Gözlenen sonuç

İki yanıtta 30'ar hücre kaydı vardı; 5 ortak hücre aynı içerikle döndü ve tekilleştirildi. **55 benzersiz hücre**, 12/12 ay, her ay tam geçerli kesişim alanı. Küresel alan yaklaşımıyla aday dikdörtgen **53.169,124 km²**. Ocak 2024 yaklaşık **-24,13 °C**, Temmuz **9,70 °C**; bunlar maskesiz aday dikdörtgenin teknik örnek ortalamalarıdır. M2'nin tek nokta değerlerinin yerine yazılmadı.

Hücreleri birleştirdikten sonra asıl dikdörtgenle alan kesişimi bir kez hesaplandı; parça ortalamaları kullanılmadı. Ocak ikinci yolla kontrol edildi: 11 boylam genişliğinin oranları `[1,10,10,10,10,10,10,10,10,10,5]/96`, beş enlem bandı için `sin(kuzey)−sin(güney)` ağırlıkları. Üretim alan/ızgara yardımcıları kullanılmadan satır ortalamalarından hesaplanan sonuç 12 ondalıkta eşleşti. Bu, hesap kontrolüdür; bağımsız gözlemle fiziksel doğrulama değildir.

## Komutlar ve kontroller

`analysis` klasöründe:

```powershell
& .\.venv\Scripts\python.exe -m unittest discover -s tests -v
& .\.venv\Scripts\python.exe -m expedition73 validate examples/a-point-2024/result.json
& .\.venv\Scripts\python.exe -m expedition73 validate examples/b-point-2024/result.json
& .\.venv\Scripts\python.exe -m expedition73 validate-window examples/a-window-2024
& .\.venv\Scripts\python.exe -m expedition73 validate-tiled-window examples/b-window-2024
```

Son tam koşuda **58 test geçti (31,590 s)**; dört parçalı iki yönlü birleşim de buna dahil. Eski A/B nokta ve A alan örnekleri ile yeni B parçalı örneğinin çevrim dışı doğrulaması geçti. A/B nokta uyumu 12 eşleşen ay ve `inference_allowed=false` verdi. Şema derleyicisi işlem boyunca önbelleğe alındı; hücre denetimleri korunuyor, her hücrede aynı şema tekrar derlenmiyor. Portal check ve strict build geçti; bunlar bilimsel hesap kontrolünün yerine geçmez.

Test kapsamı: gerçek B ham parçalarını yeniden hesaplama, eksik/tekrar hücre, tutarsız örtüşen değer/yükselti/ay, API/kaynak/zaman metaverisi uyumsuzluğu, dosya yolu/URL/hash/zaman bozulması, kayıp/fazla/sırası değişmiş parça, parça sınırı değişse de aynı ağırlık/sonuç, tek parçalı A geriye uyumu, eksik ayda null, iki yönde plan ve birleşim, başarısız istekte sahte tamamlanma üretmeme. Yeni testler ağ çağrısı yapmaz; iki gerçek yanıt kaydedilmiştir. CI de yalnızca kayıtlı örnekleri kullanır.

## Yorum ve paylaşım sınırı

Maske, kesin alan, ortak bilimsel profil ve uzun dönem yöntem seçilmedi. Hücre kenarları orta noktadan kurulur, küresel alan yaklaşımı açıkça kaydedilir. Bu destek R-B04'ün teknik engelini kaldırır; M2'nin kendi nihai alan hesabı/yorumunu bitirdiği veya bu sürümü Mac'te çalıştırdığı varsayılmaz. Kullanıcı test sonrası main'e gönderilmesini istedi.

## Paylaşım yolu

Kod M1 dalına `0413622` ile gönderildi. Bağlı entegrasyonun PR açma isteği `403 Resource not accessible by integration` döndürdü; PR oluşmadı. Yerel inceleme ve 58 test sonrası, kullanıcının açık main paylaşım yetkisiyle Git merge yolu uygulanıyor; sonraki geliştirme ayrı dalda sürecek. Canlı yayın/uzak test sonuçları tamamlanınca kayda eklenecek. Yerel portal check/strict build, git diff --check ve altı HTTP yol/içerik kontrolü geçti; geçici sunucu kapatıldı.
