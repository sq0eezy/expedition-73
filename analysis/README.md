# İlk T2M modül dilimi · v0.1.0

NASA POWER Monthly API'den **aday bir noktaya** ait aylık 2 metre hava sıcaklığını alır; doğrular ve sürümlü ortak JSON çıktısına çevirir. `examples/a-point-2024/` gerçek API yanıtı ve çıktısıdır. Bu sürüm **bölge ortalaması, trend, p-değeri veya nedensellik hesabı yapmaz**. POWER, MERRA-2 tabanlı bir servistir; yanıt doğrudan `M2TMNXSLV` 5.12.4 dosyası diye etiketlenmez.

Kapsam: MOD-01/02/03'ün ilk aktarım/adaptör dilimi ve R-A02'nin erişim sınaması. Nokta profiline ek olarak maskesiz aday dikdörtgen için deneysel alan ağırlıklı seri çalışıyor; B uygunluğu ve istatistikler sonraki işlerdir.

## Yeni: maskesiz dikdörtgen denemesi

Mac/Linux, `analysis` klasöründe kurulu ortamla:

```sh
.venv/bin/python -m expedition73 validate-window examples/a-window-2024
.venv/bin/python -m expedition73 fetch-power-window --config examples/a-window-2024.config.json --output-dir artifacts/a-window-new-run
```

Windows'ta `.venv/bin/python` yerine `& .\.venv\Scripts\python.exe` kullanılır. İlk komut çevrim dışıdır; ikinci komut NASA API'ye bağlanır. [Yöntem, sınırlar ve kurulum](../portal/docs/guide/T2M_WINDOW.md), [gerçek kanıt](../portal/docs/evidence/T2M_WINDOW_PROBE.md).

`monthly_window_series` nokta çıktısından ayrı türdür. Yarım hücre payı içeren istek, MERRA2 0,625°×0,5° ızgarası, orta noktadan kurulan hücre kenarları, dikdörtgen kesişimi ve küresel alan ağırlıkları kullanılır. Tek ayda eksik hücre değeri varsa ortalama null kalır; coğrafi hücre eksikse yanıt reddedilir. Ham yanıt, hücre tanıları ve yıllık sağlayıcı özetleri saklanır. `validate-window RUN_DIR` tüm hesabı yeniden yapar; `check-alignment` yalnızca eski nokta profilini kabul eder.

Kara/su maskesi, kesin coğrafi bölge, keyfî poligon ve çıkarım yoktur. Pilot sınırı: yarım hücre payı dahil en fazla 5°/eksen ve iki yıl; tarih çizgisi/kutup aşımı veya parçalama yok. B'nin mevcut 6° arama penceresi bu komutun kapsamını aşar; B sessizce küçültülmez. Mevcut B nokta erişimi bu sınırlamadan etkilenmez. JSON şemaları `schemas/window-request.schema.json`, `schemas/monthly-window-series.schema.json`; gerçek A örneği `examples/a-window-2024/` altında.

## Mac / Linux

Depo kökünden Python 3.11+ ile:

~~~sh
cd analysis
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m expedition73 validate examples/a-point-2024/result.json
~~~

Kaydedilmiş örneğin doğrulaması ve testler NASA'ya ağ isteği yapmaz. Gerçek bir API denemesi için yeni bir çıktı klasörü seç:

~~~sh
.venv/bin/python -m expedition73 fetch-power-point --config examples/a-point-2024.config.json --output-dir artifacts/a-point-new-run
~~~

Komut önce yapılandırmayı doğrular; sonra tek API isteği yapar. Başarılı yanıtta `request.json`, `response.json` ve `result.json` oluşturur. Var olan çıktı klasörünün üzerine yazmaz. Her yeni çağrı NASA'ya gerçek istek gönderir; tekrar gerekmiyorsa kaydedilmiş örneği kullan. `artifacts/` yerel/ignored alandır.

## Windows

Python 3.11+ ile `analysis/` içinde ortam oluştur. Bu çalışma alanında mevcut Python kullanılarak `analysis/.venv` zaten oluşturuldu. Ortamı olan PowerShell'de:

~~~powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m expedition73 validate examples/a-point-2024/result.json
.\.venv\Scripts\python.exe -m expedition73 fetch-power-point --config examples/a-point-2024.config.json --output-dir artifacts/a-point-new-run
~~~

Yeni Windows bilgisayarında Python kuruluysa `py -3 -m venv .venv` ve `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` ile yerel ortam hazırlanabilir. Global paket kurulumu gerekmez.

## B için kullanım

`examples/a-point-2024.config.json` dosyasını yeni bir B yapılandırmasına kopyala. `region_id`, açıklama, aday pencere/sürümü ve onun içindeki deneme noktası değiştirilir; gösterge T2M, durum `candidate` kalır. Dönem/sıklık/sağlayıcıyı ortak çalışma profiliyle eşleştir. Bu araç sonradan seçilecek gerçek analiz poligonunu veya bölgesel seriyi henüz desteklemiyor. B görevinin yerine A değerleri yazılmaz.

`check-alignment LEFT.json RIGHT.json` sözleşme, kaynak/yöntem, zaman ve eşleşen geçerli ayları kontrol eder. `aligned_point_series` **yalnızca aktarım/zaman uyumu** demektir; çıktı her zaman `inference_allowed: false` taşır. Bu kontrolden bölgesel eğilimlerin farklılığı sonucu çıkarılamaz. Uyumsuz durumda çıkış kodu 2, geçersiz veride 1 olur.

## Sözleşme ve doğrulamalar

- `schemas/point-request.schema.json`: aday pencere, nokta, dönem ve sürüm.
- `schemas/monthly-point-series.schema.json`: ilk **T2M nokta-serisi profili**, bütün gelecekteki modüllerin nihai şeması değil.
- `expedition73/power.py`: kaynak kontrolü, normalleştirme, anlamsal tutarlılık ve uyum denetimi.
- `regions/a-candidate-window.geojson`: önceki araştırma dikdörtgeninin yeniden üretilebilir geometrisi; kabul edilmiş ekolojik/analiz sınırı değil.

Yinelenen JSON anahtarları, sonlu olmayan sayılar, yanlış birim/tanım/konum/dönem ve şema dışı sonuçlar reddedilir. Dönmeyen ay ile sağlayıcının dolgu değeri ayrı `null` durumlarıdır; gerçek 0 °C geçerlidir. POWER'ın `YYYY13` yıllık özeti aylık seriye katılmaz; özel ayrıntıda korunur. Seri takvim kapsamının tam olması bilimsel/piksel kalite onayı değildir. API'nin kaynak/versiyon, zaman standardı, mesaj ve parametre metaverisi ile ham yanıt SHA-256 özeti saklanır; piksel kalite bayrağı varmış gibi üretilmez.

Kaynaklar: [POWER aylık API](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/), [meteoroloji yöntemi](https://power.larc.nasa.gov/docs/methodology/meteorology/). Görevler ve gerçek bulgular `portal/docs` içindedir; bu kılavuz bilimsel sonuç yerine geçmez.
