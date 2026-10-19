# İlk T2M modül dilimi · v0.1.0

NASA POWER Monthly API'den **aday bir noktaya** ait aylık 2 metre hava sıcaklığını alır; doğrular ve sürümlü ortak JSON çıktısına çevirir. `examples/a-point-2024/` gerçek API yanıtı ve çıktısıdır. Bu sürüm **bölge ortalaması, trend, p-değeri veya nedensellik hesabı yapmaz**. POWER, MERRA-2 tabanlı bir servistir; yanıt doğrudan `M2TMNXSLV` 5.12.4 dosyası diye etiketlenmez.

Kapsam: MOD-01/02/03'ün ilk aktarım/adaptör dilimi ve R-A02'nin erişim sınaması. Nokta profiline ek olarak maskesiz aday dikdörtgen için deneysel alan ağırlıklı seri çalışıyor; B uygunluğu ve istatistikler sonraki işlerdir.

## Yeni: sınır hücrelerinde koşullu alan denetimi

Kaynak alanı ön kontrolü: `.venv\Scripts\python.exe -X utf8 -m expedition73 check-source-area --metadata examples/a-surface-fractions/metadata.dmr.xml`; Mac/Linux'ta `.venv/bin/python` kullanılır. Gerçek seçili granül metaverisinde AREA yok; kaynak sayısal alanı ile karşılaştırma yapılmadı. Çıkış 0 kontrolün tamamlandığı anlamındadır; `comparison_status` alanı sonucu bildirir. Metadata'da ileride AREA görülmesi de değer/birim/geometri onayı değildir. [Gerçek kaynak kontrolü](../portal/docs/evidence/SOURCE_AREA_CHECK.md).

`analysis` içinde Windows CMD: `.venv\Scripts\python.exe -X utf8 -m expedition73 audit-surface-support --window-run examples/b-window-2024 --fraction-run examples/b-surface-fractions`. Mac/Linux aynı argümanlarla `.venv/bin/python -X utf8 -m expedition73 ...`; `requirements-mask.txt` gerekir. Kaynaklar çevrim dışı yeniden doğrulanır; iki aday için tam hücre oranının kırpılan parçadaki bilinmeyen yerleşimine bağlı alt/homojen/üst alan hesaplanır. JSON stdout'a gelir; dosya veya NASA isteği üretmez. [Yöntem/varsayımlar](../portal/docs/research/SURFACE_SUPPORT.md), [gerçek sonuç/12 test](../portal/docs/evidence/SURFACE_SUPPORT_CHECK.md). Kayıtlı ortak özet `examples/surface-support-summary.json`. Koşullu alan aralığı güven aralığı veya sıcaklık hata payı değildir; maske seçilmez, kaynak AREA doğrulaması hâlâ açık.

## Yeni: çok girdili yürütme denemesi

Gerçek kayıtlı T2M ve fraksiyon işlemleri de artık motora bağlandı: `analysis` içinde Windows CMD ile `.venv\Scripts\python.exe -m expedition73 run-surface-workflow --window-run examples/b-window-2024 --fraction-run examples/b-surface-fractions --output-dir artifacts/b-surface-new-run`. Mac/Linux'ta `.venv/bin/python` kullanılır; `requirements-mask.txt` kurulu olmalı. [Akış, iki aday politika, kaynaklar ve sınırlar](../portal/docs/evidence/SURFACE_WORKFLOW.md). A ve B için 12 ay hesaplandı; maskesiz örnekler değiştirilmedi. Bu komut ağ/token istemez, mevcut küçük kayıtları tekrar doğrular. Başarısız girdide bağımlı işler engellenir ve aday sonuç yazılmaz.

`analysis` içinde Windows CMD: `.venv\Scripts\python.exe -m expedition73 demo-workflow`. Mac/Linux: `.venv/bin/python -m expedition73 demo-workflow`. Yapay A→B, A+B→C grafiğini çalıştırır; C=12, A parametresi değişince yeni çalıştırmada C=21 üretir. Ortak A bir kez hesaplanır, girdi kimlikleri/ata izi ve hata/engelli durumları korunur; eski/yeni A karışımı reddedilir. İstek şeması 0.1.0, örnek `examples/workflow-demo.json`. [Kanıt, komut ve sınırlar](../portal/docs/evidence/WORKFLOW_ENGINE.md). Bu komut yapay örnektir; gerçek kayıtların ayrı akışı yukarıdadır. Kalıcı cache, otomatik kaynak izleme ve web arayüzü yok.

## Aday maske altyapısı · Gerçek fraksiyon erişimi doğrulandı

Metadata kontrolü, depo kökünde Windows PowerShell: `& .\analysis\.venv\Scripts\python.exe .\analysis\scripts\check_earthdata_access.py`. Mac: `analysis/.venv/bin/python analysis/scripts/check_earthdata_access.py`. Proje `.env` kaydı okunur; açık `--save-token` ile gizli girişten kaydedilir. Script yalnız metadata ister; sonuç `analysis/artifacts/earthdata-access-...` altında kalır. [Token/uygulama yetkisi](../portal/docs/guide/EARTHDATA_ACCESS.md). GES DISC onayı sonrası gerçek A/B fraksiyon alt kümeleri de alınıp yeniden doğrulandı: [kanıt](../portal/docs/evidence/SURFACE_SUBSET_CHECK.md).

`plan-surface-mask --config examples/b-window-2024.config.json` beklenen kaynak hücrelerini ve sıfır tabanlı indeksleri çevrim dışı listeler. `preview-surface-mask --run RUN_DIR --mask MASK.json --components FRLAND` önce sıcaklık run'ını yeniden doğrular, sonra `schemas/surface-fractions.schema.json` girdisini kontrol edip ayrı `candidate_surface_weight_preview` üretir. Kara buzu dahil olacaksa açıkça `--components FRLAND FRLANDICE` denir; varsayılan bilimsel politika yoktur.

M2C0NXASM 5.12.4 aday kaynağına ilk oturumsuz istek 401 vermişti; erişim kaydı `resources/merra2-mask-access.json` tarihseldir. Güncel `surface_source.py` NetCDF dönüştürücüsü ve yerel komutla alınan gerçek A/B alt kümeleri 56/55 hücreyle doğrulandı; özel yanıtlar Git dışında `artifacts/` içinde. Türetilmiş `examples/*-surface-mask-plan.json` dosyaları ilk istek planlarıdır; veri sonucu değildir. Testteki yapay oranlar açık `--allow-synthetic` olmadan önizlemeye alınmaz. [Araştırma/yöntem sınırları](../portal/docs/research/SURFACE_MASK.md).

Oranlar tüm kaynak hücresine aittir; sınırla kesişen parçaya aynı oranı uygulamak yaklaşık bir yöntemdir. Yeniden ağırlıklandırma, hücre T2M'sini ayrı bir kara yüzey sıcaklığına dönüştürmez. Bu araç mevcut maskesiz örnekleri veya seçilmiş analiz profilini değiştirmez.

## Yeni: B'nin geniş penceresi için parçalı erişim

`analysis` içinde kurulu ortamla, Mac/Linux:

```sh
.venv/bin/python -m expedition73 validate-tiled-window examples/b-window-2024
.venv/bin/python -m expedition73 fetch-power-tiled-window --config examples/b-window-2024.config.json --output-dir artifacts/b-window-new-run
```

İlk komut çevrim dışıdır; ikincisi sıralı NASA API istekleri yapar. Windows'ta Python yolu `& .\.venv\Scripts\python.exe`. [Tam kılavuz](../portal/docs/guide/T2M_TILED_WINDOW.md), [gerçek kanıt](../portal/docs/evidence/T2M_TILING.md). B'nin 6° sınırı korunur; iki yanıttaki 5 ortak hücre çıkarılıp 55 benzersiz hücreyle asıl alan bir kez hesaplanır. Çakışan değerler hata verir, parça ortalamaları ortalanmaz. Eksik veri kuralları eski alan yöntemiyle aynıdır.

Parçalı çıktı `monthly_window_series` şema/modül 0.2.0; eski nokta/tek istekli 0.1.0 profilleri korunur. Bilimsel alan yöntemi 0.1.0 değişmedi. Plan 4° gövdeler ve yarım hücre payı, en çok 16 istek ve iki yıl kullanır. Kara maskesi, keyfî poligon, tarih çizgisi/kutup geçişi veya trend çıkarımı yoktur. Her ham parçanın URL/zaman/SHA-256'sı `manifest.json` ve sonuçta tutulur; `validate-tiled-window` bütün planı ve hücre birleşimini yeniden hesaplar. Yapılandırma bölgeden bağımsızdır; M2'nin örneği nihai bölge seçimi değildir.

## Yeni: maskesiz dikdörtgen denemesi

Mac/Linux, `analysis` klasöründe kurulu ortamla:

```sh
.venv/bin/python -m expedition73 validate-window examples/a-window-2024
.venv/bin/python -m expedition73 fetch-power-window --config examples/a-window-2024.config.json --output-dir artifacts/a-window-new-run
```

Windows'ta `.venv/bin/python` yerine `& .\.venv\Scripts\python.exe` kullanılır. İlk komut çevrim dışıdır; ikinci komut NASA API'ye bağlanır. [Yöntem, sınırlar ve kurulum](../portal/docs/guide/T2M_WINDOW.md), [gerçek kanıt](../portal/docs/evidence/T2M_WINDOW_PROBE.md).

`monthly_window_series` nokta çıktısından ayrı türdür. Yarım hücre payı içeren istek, MERRA2 0,625°×0,5° ızgarası, orta noktadan kurulan hücre kenarları, dikdörtgen kesişimi ve küresel alan ağırlıkları kullanılır. Tek ayda eksik hücre değeri varsa ortalama null kalır; coğrafi hücre eksikse yanıt reddedilir. Ham yanıt, hücre tanıları ve yıllık sağlayıcı özetleri saklanır. `validate-window RUN_DIR` tüm hesabı yeniden yapar; `check-alignment` yalnızca eski nokta profilini kabul eder.

Kara/su maskesi, kesin coğrafi bölge, keyfî poligon ve çıkarım yoktur. Tek istekli komutun sınırı: yarım hücre payı dahil en fazla 5°/eksen ve iki yıl. B'nin mevcut 6° arama penceresi için yukarıdaki yeni parçalı komut kullanılır; B sessizce küçültülmez. Mevcut B nokta erişimi etkilenmez. JSON şemaları `schemas/window-request.schema.json`, `schemas/monthly-window-series.schema.json`; gerçek A örneği `examples/a-window-2024/` altında.

## Deneysel: gerçek sabit fraksiyon alt kümesi

Yerel NASA komutları proje kökündeki Git dışında tutulan `.env` içinden `EARTHDATA_TOKEN` okur. Açık `--save-token` seçeneği token'ı gizli girişten bu anahtara kaydeder/değiştirir; sonraki çalıştırmalarda tekrar sorulmaz. CMD/PowerShell ayrımı, 403 uygulama yetkisi ve kayıt adımları [erişim kılavuzunda](../portal/docs/guide/EARTHDATA_ACCESS.md). Token değerini komut argümanına veya paylaşılan belgelere yazma.

Gerçek A/B fraksiyon alt kümeleri 2026-10-18’de alındı ve 56/55 hücre için çevrim dışı yeniden doğrulandı; bilimsel maske seçimi ve maskeli seri açık. Küçük alt kümeyi gizli token ile alan ve yerel NetCDF yanıtını ortak maske girdisine dönüştüren yardımcı komut hazır. Ek bağımlılıklar `requirements-mask.txt` içinde; mevcut nokta/alan araçlarının temel kurulumu değişmez. [Windows/Mac komutları ve sınırlar](../portal/docs/guide/SURFACE_SUBSET.md), [sentetik dönüşüm testleri](../portal/docs/evidence/SURFACE_SUBSET_CHECK.md). `--replay REGION_DIRECTORY` ağ/token olmadan ham yanıtı tekrar dönüştürür. Kara/buz politikası seçilmez, sıcaklık serisi değiştirilmez.

## Temel ortam · Mac / Linux

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
