---
review_summary: "NASA POWER'dan gerçek 2024 T2M nokta örneği, kod/şema kontrolleri ve bilimsel sınırlar."
change_summary: "İlk sayısal API erişimi ve çalışan nokta adaptörü kaydedildi; bölgesel/trend sonucu üretilmedi."
---
# T2M · İlk gerçek API ve adaptör denemesi

**Tarih:** 2026-10-16 · **Ortam:** Windows, Python 3.12.14, `analysis/.venv`, jsonschema 4.25.1. Kullanıcı M1 görevlerine başlamamızı istedi. Kapsam: R-A01/02 ve MOD-01/02/03'ün ilk teknik dilimi; [ADR-006](../decisions/ADR-006-T2M-POINT-ADAPTER.md).

## Gerçek erişim

Önce küçük bir elle kodlanmış HTTP sınaması, ardından yeni CLI ile bir çağrı yapıldı. Ana örnek CLI çağrısının yanıtıdır. `analysis/` içinde çalıştırılan komut:

~~~text
.venv/Scripts/python.exe -m expedition73 fetch-power-point --config examples/a-point-2024.config.json --output-dir examples/a-point-2024
~~~

| Bilgi | Gözlenen |
|---|---|
| API | NASA POWER Monthly and Annual API · v2.10.0 |
| Kaynak etiketi | MERRA2; doğrudan M2TMNXSLV dosyası değil |
| İstek | T2M, community SB, lon -111.0, lat 37.5, start/end 2024, format JSON |
| Erişim zamanı | 2026-10-16T07:57:51+00:00; Türkiye saati 10:57:51 |
| Sayısal yanıt | 12 aylık T2M değeri ve `202413` yıllık özeti |
| Birim / değişken | `C` / Temperature at 2 Meters; çıktı birim etiketi `degC` |
| Dolgu / zaman standardı | -999.0 / LST; yerel güneş zamanı |
| Örnek kayıtlar | Ocak 0,60 °C; Temmuz 28,31 °C; Aralık 2,39 °C |
| Aylık kapsam | Beklenen 12, geçerli 12, eksik 0; bu piksel kalite onayı değil |
| Yıllık özet | 13,57 °C; aylık seriden ayrılıp özel ayrıntıda korundu |
| Kaynak yanıt SHA-256 | `e79f6a2d1dba78fbbfff0d9f03584ee8c9c02ad1223f51bd432f099ddb06b8c6` |

[İstek yapılandırması](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/a-point-2024/request.json), [ham API yanıtı](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/a-point-2024/response.json), [normalleştirilmiş çıktı](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/a-point-2024/result.json). Ham yanıtın servis işlem süreleri değişebileceği için yeni çağrının byte özeti farklı olabilir; kaydedilmiş örneğin özeti yukarıdadır.

## Uygulananlar

İstek/sonuç için v0.1.0 JSON Schema ve anlamsal tutarlılık kontrolü; T2M tanımı/birimi, konum, dönem, aday pencere, kaynak ve sürüm izi; eksik/dolgu/gerçek sıfır ayrımı; aylık sıralama; yıllık özeti ayrı tutma. Özel kaynak metaverisi ve küçük ham yanıt korunur. Uyum kontrolü yalnızca nokta serilerinin aktarım/zaman uygunluğunu söyler; istatistik çıkarımına izin vermez.

## Gerçek kontroller

- `analysis/.venv/Scripts/python.exe -m unittest discover -s tests -v` (`analysis/` içinde): **26 test geçti**. Kaydedilmiş gerçek yanıtın yeniden üretilmesi; eksik/dolgu/sıfır, yıllık özet, bozuk JSON, uygunsuz konum/dönem/birim, kaynak tutarsızlığı ve uyumsuz seriler sınandı. Testler NASA'ya çağrı yapmaz.
- `-m expedition73 validate examples/a-point-2024/result.json`: şema ve anlamsal kontrol geçti.
- `-m expedition73 check-alignment` ile kaydedilmiş örnek kendi kopyasıyla sınandı: 12 eşleşen ay, `aligned_point_series`, `inference_allowed: false`. Bu A/B testi değildir.
- Nokta yanıtı ve kod Windows üzerinde çalıştırıldı; gerçek Mac kurulumu henüz sınanmadı. Ayrı Ubuntu CI kontrolü hazırlandı; bu kayıt yazılırken uzak sonuç henüz görülmedi.

## Ne doğrulanmadı?

Deneme noktası aday pencere içindedir; pencere veya nokta kesin analiz alanı değildir. Nokta servisi grid tabanlı tahmin döndürür; istasyon ölçümü veya bütün alanın ortalaması sayılmaz. Alan/kesişim ağırlıkları, kara maskesi, uzun dönem seri, istatistik yöntemi, trend/p-değeri ve B verisi henüz yok. Genel modül grafiği ve nihai web uygulaması geliştirilmedi. [Sonraki görevler](../planning/REGION_A.md).

Kaynaklar: [NASA POWER aylık API](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/), [meteoroloji yöntemi](https://power.larc.nasa.gov/docs/methodology/meteorology/).
