---
review_summary: "İlk çalışan T2M API adaptörünü çalıştırma; M2 için Mac komutları ve nokta-serisi sınırı."
change_summary: "Gerçek NASA örneği, v0.1.0 şema/CLI ve çevrim dışı doğrulama kılavuzu eklendi."
---
# İlk T2M adaptörünü çalıştırma

`analysis/` içinde ilk çalışan teknik dilim var: NASA POWER T2M **nokta yanıtı → aylık seri → ortak JSON profili**. Kaynak kod ve ayrıntılı kullanım: [analysis README](https://github.com/sq0eezy/expedition-73/blob/main/analysis/README.md). [Gerçek örnek ve sınırlar](../evidence/T2M_POINT_PROBE.md).

## Mac'te kaydedilmiş örneği doğrula

Güncel kaynaklar alındıktan sonra depo kökünde, Python 3.11+ ile:

~~~sh
cd analysis
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m expedition73 validate examples/a-point-2024/result.json
~~~

Testler ve örnek doğrulaması NASA'ya istek yapmaz. Ortam portalın `.venv` ortamından ayrıdır; bu Mac komutlarının bu oturumda gerçek Mac üzerinde çalıştırıldığı iddia edilmez.

## Yeni küçük API isteği

~~~sh
.venv/bin/python -m expedition73 fetch-power-point --config examples/a-point-2024.config.json --output-dir artifacts/a-point-new-run
~~~

Her çağrı bir gerçek NASA isteğidir. Var olan çıktı klasörünü kullanmaz; yeni ad seç. Başarılı çalışmada istek yapılandırması, küçük ham yanıt ve doğrulanmış sonuç JSON'u yazılır. Windows'ta aynı `analysis/` klasöründe `.venv/bin/python` yerine `.\.venv\Scripts\python.exe` kullanılır.

## M2 kendi B denemesinde ne yapacak?

A örnek yapılandırmasını B'ye özel yeni bir dosyaya kopyala; kimliği/açıklamayı, aday pencere/sürümünü ve içindeki deneme noktasını değiştir. Seçimler [B fişinde](../research/regions/REGION_B_PROFILE.md) kaynaklı kalsın. Dönem/sağlayıcıyı A ile ortak profil üzerinden eşleştir. Bu işlem B'nin sonucunu üretmiş olduğumuz anlamına gelmez; M2 kendi çağrı/inceleme kaydını ekleyecek.

`check-alignment LEFT.json RIGHT.json` kaynak/yöntem/zaman uyumunu ve eşleşen geçerli ayları kontrol eder. `aligned_point_series` sonucu bölgesel karşılaştırma veya istatistik onayı değildir; çıktı `inference_allowed: false` taşır. Harita/alan serisi desteklenmiyor; o girdiler açıkça reddedilir.

## Bilimsel sınır

12 ayın geçerli dönmesi yalnızca takvim kapsamını doğrular. Piksel kalite bayrağı, gerçek bölge ortalaması, uzun dönem trendi, güven aralığı veya p-değeri hesaplanmadı. `YYYY13` yıllık özeti seride 13. ay yapılmaz; özel ayrıntıda saklanır. API metaverisindeki `LST` zaman standardı yerel güneş zamanıdır; T2M değişkeninin yüzey sıcaklığı olduğu anlamına gelmez. [NASA meteoroloji açıklaması](https://power.larc.nasa.gov/docs/methodology/meteorology/).
