---
review_summary: "A aday dikdörtgeni için gerçek bölgesel POWER yanıtı ve alan hesabının doğrulama sınırları."
change_summary: "56 hücre ve 12 ay alındı; sınır kesişimi ve bağımsız Ocak hesabı doğrulandı."
---
# Gerçek T2M bölgesel erişim ve alan hesabı

**Tarih/ortam:** 2026-10-16, Windows, Python 3.12.14, proje içi `analysis/.venv`. M1'in modül/A görevine devam talebi kapsamında yapıldı. Aday arama sınırı değişmedi: `[-113,36,-109,39]`, `search-window-0.1.0`; kabul edilmiş analiz alanı değildir. [Kullanım ve yöntem](../guide/T2M_WINDOW.md).

## Gerçek API gözlemi

İlk sınır isteği 42 hücre merkezi döndürdü. Merkezleri çevreleyen hücrelerin pencereyle kesişimleri, doğu ve batıda toplam %6,25 alanı dışarıda bırakıyordu. Uç noktanın merkez seçimi bütün sınır alanını sağladığı varsayılmadı. İkinci isteğe enlemde 0,25°, boylamda 0,3125° pay eklendi.

| Alan | Gerçek kayıt |
|---|---|
| Uç nokta | [POWER aylık bölgesel T2M isteği](https://power.larc.nasa.gov/api/temporal/monthly/regional?parameters=T2M&community=SB&longitude-min=-113.3125&longitude-max=-108.6875&latitude-min=35.75&latitude-max=39.25&format=JSON&start=2024&end=2024) |
| Erişim | 2026-10-16 08:19:19 UTC / 11:19:19 Türkiye |
| Yanıt | 17.786 bayt, GeoJSON FeatureCollection, 56 hücre merkezi |
| Kaynak | API v2.10.0, kaynak `MERRA2`; doğrudan M2TMNXSLV dosya sürümü iddiası yok |
| Gerçek koordinatlar | 8 boylam: -113,125…-108,75, adım 0,625°; 7 enlem: 36…39, adım 0,5° |
| Değişken/zaman | T2M, `C`, Temperature at 2 Meters; 2024-01…2024-12, LST |
| Dolgu/yıllık özet | -999; hücrelerin `202413` kayıtları aylara katılmadı |
| SHA-256 | `c38efad91ac280448589c68494d61d3749a499db9d72dcc6a710759e7a76b39c` |
| Dosyalar | [Yapılandırma, ham yanıt ve sonuç](https://github.com/sq0eezy/expedition-73/tree/main/analysis/examples/a-window-2024) |

[POWER aylık belge](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/) bölgesel örneğinde 0,5×0,5° ifadesi geçiyor; bu yanıtın boylam adımı gerçekte 0,625°. [POWER meteoroloji yöntemi](https://power.larc.nasa.gov/docs/methodology/meteorology/) ve [NASA MERRA-2 dosya şartnamesi §4.1, PDF sayfa 15](https://ntrs.nasa.gov/api/citations/20150019760/downloads/20150019760.pdf#page=15) MERRA-2 çıktı ızgarasını 0,625×0,5°, başlangıcı 180°B/90°G olarak tanımlar. Adaptör kaynağı ve gerçek koordinatları denetler; genel örnekteki sayıyı körlemesine kullanmaz.

## Hesap ve bağımsız karşılık

Orta noktayla kurulan hücre kenarları dikdörtgenle kesiştirildi. Küresel alan yaklaşımıyla toplam alan **117.698,095 km²**; bu sayı resmî plato alanı değildir. Her ay 56/56 hücre sayısal döndü ve geçerli alan oranı 1 oldu. Bu kapsam kontrolü piksel kalitesi veya fiziksel doğruluk ölçüsü değildir.

| Teknik örnek | Maskesiz aday dikdörtgen ortalaması |
|---|---|
| Ocak 2024 | -0,3911184860434411 °C |
| Temmuz 2024 | 26,52282408687593 °C |

Görünen çok basamak hesap denetimi içindir; kaynak verinin iki ondalığından daha yüksek bilimsel hassasiyet iddiası taşımaz. Tek yıl mevsimsel değişimdir; uzun dönem ısınma/soğuma sonucu değildir.

Ocak için üretim kodunun alan/ızgara yardımcıları kullanılmadan ikinci hesap yapıldı: her enlem satırında sekiz boylamın ağırlıkları `[3,10,10,10,10,10,10,1]/64`; enlem bantları sırasıyla `[36,36.25]`, `[36.25,36.75]`, …, `[38.75,39]` ve ağırlıkları `sin(kuzey)−sin(güney)`. Satır ortalamalarının bu bantlarla toplamı üretim Ocak sonucuyla 12 ondalıkta eşleşti. Bu kontrol hesap doğrulamasıdır; bağımsız gözlemle bilimsel doğrulama değildir.

## Doğrulama

`analysis` klasöründe:

```powershell
& .\.venv\Scripts\python.exe -m unittest discover -s tests -v
& .\.venv\Scripts\python.exe -m expedition73 validate examples/a-point-2024/result.json
& .\.venv\Scripts\python.exe -m expedition73 validate-window examples/a-window-2024
```

Windows'ta ilk tam koşuda **41 test geçti** (109,946 s). Platformlar arası son basamak farkı için dar tolerans eklendikten sonra ilgili dört yeniden hesaplama testi geçti (21,582 s); yeni tolerans testiyle toplam 42 ayrı test doğrulandı. Eski nokta örneği doğrulaması ve yeni alan örneğinin çevrim dışı yeniden hesabı geçti. Testler NASA'ya ağ çağrısı yapmaz. Sınır kesişimi, bağımsız Ocak hesabı, bilinen yarımküre alanı, sabit/gerçek sıfır alanı, dolgu/eksik ay, bütün ayın eksikliği, yıllık özeti ayırma, eksik/tekrar coğrafi hücre, ızgara/birim/kaynak hatası, sıralama, yeniden hesaplamayla değiştirilmiş çıktıyı yakalama ve üzerine yazmama denetlenir. Ubuntu CI sonucu yayın sonrasında ayrıca kontrol edilecek; gerçek Mac doğrulaması yok.

## Açık sınırlar

Kara/su maskesi yok; hücre kenarları yanıtta sunulmadığı için orta nokta varsayımı var. Sonuç maskesiz aday dikdörtgene aittir. Kesin alan, B uygunluğu, ortak dönem/ürün/yöntem, trend ve p-değeri kararı verilmedi. Bölgesel sonuçlar için karşılaştırma kapısı ve gerçek web uygulaması henüz yok. M2'nin başladığı veya Mac üzerinde doğrulandığı varsayılmadı.

## Uzak doğrulama · 2026-10-16

Kod `b6fa5d405990be7f841efec1a3b0d69652acd2b2` ile main'e gönderildi. [Ubuntu T2M adapter checks](https://github.com/sq0eezy/expedition-73/actions/runs/38874227150) başarılı: 42 test, eski nokta örneği doğrulaması ve yeni alan örneğinin yeniden hesabı. Bu uzak Linux kontrolüdür; gerçek Mac kurulumu değildir. [Canlı kanıt sayfası](https://sq0eezy.github.io/expedition-73/evidence/T2M_WINDOW_PROBE/) HTTP 200 ve yeni yanıt SHA-256'sını içeren içerikle doğrulandı. Yerel portal check/strict build ve yedi HTTP yol/içerik kontrolü de geçti; geçici sunucu kapatıldı.

Kod commit'inin [GitHub Pages işi](https://github.com/sq0eezy/expedition-73/actions/runs/38874227002) de başarılı tamamlandı. Panelin yayımlanması yukarıdaki bilimsel sınırlamaları kaldırmaz.
