---
review_summary: "A aday penceresinin ilk kaynak/sınır önerisi ve gerçek 2024 T2M nokta API denemesi."
change_summary: "Aday dikdörtgen için 56 hücre/12 ay alındı; maskesiz alan hesabı ve bağımsız kontrol eklendi."
---
# Bölge A · Çalışma fişi

M1'in ilk çalışma kaydı, **2026-10-16**. Görev durumu [panoda](../../planning/WORK_BOARD.md), kullanım [T2M kılavuzunda](../../guide/T2M_ADAPTER.md). Alanın kesin seçimi yapılmadı; bu fiş ilk teknik incelemedir.

**2026-10-19 · R-A04 kontrolü:** Kayıtlı 56 hücrenin 26'sı sınırdan kesiliyor; iki hücrede seçili yüzeyin kesilen parçadaki yerleşimi bilinmiyor. [Koşullu alan denetimi](../../evidence/SURFACE_SUPPORT_CHECK.md) ve [alan ölçüsü varsayımları](../SURFACE_SUPPORT.md) eklendi. Kaynak AREA karşılaştırması, kesin sınır ve bilimsel maske seçimi hâlâ açık; yeni bir sıcaklık/trend bulgusu değildir.

| Alan | Kayıt |
|---|---|
| Soru | Seçilecek bu kara alanında 2 metre hava sıcaklığının ortak uzun dönemdeki eğilimi nedir? Bu deneme yalnızca erişim/biçim sınar. |
| Aday alan | Colorado Platosu çevresindeki önceki [araştırma penceresi](../REGION_CANDIDATES.md); bütün plato veya resmî ekolojik sınır değil |
| Sınır önerisi/sürümü | Proje tarafından tanımlı arama dikdörtgeni: west/south/east/north = -113,36,-109,39; `search-window-0.1.0`. Kabul edilmiş analiz poligonu değil. |
| Geometri | [GeoJSON aday penceresi](https://github.com/sq0eezy/expedition-73/blob/main/analysis/regions/a-candidate-window.geojson); boylam/enlem sırasıyla kapanan dikdörtgen |
| Bölgesel gerekçe | Kurak ve yüksekliği değişen kara çevresi sıcaklık sorusu için aday: [NASA bölge tanımı](https://modis.gsfc.nasa.gov/gallery/individual.php?db_date=2021-04-13). Koordinatlar bu kaynaktan türetilmiş resmî sınır değil, önceki proje arama önerisi. |
| Kara/su, yükselti ve grid kapsamı | Kara/su maskesi ve yükselti düzeltmesi açık. Aday dikdörtgenle kesişen 56 hücre gerçek bölgesel yanıttan alındı; 0,625° boylam × 0,5° enlem. Orta nokta kenar varsayımıyla sınır kesişimleri ve küresel alan ağırlıkları hesaplandı. |
| Deneme noktası | 37,5°K / 111°B; arama penceresinin içindeki teknik erişim noktası, temsili bölge ortalaması değil |
| Sağlayıcı/API | NASA POWER Monthly and Annual API v2.10.0; point/T2M/community SB/2024/JSON |
| Kaynak ve sürüm ayrımı | Yanıtta kaynak `MERRA2`; bu, doğrudan `M2TMNXSLV` 5.12.4 dosyası veya nihai iki-bölge ürünü diye etiketlenmedi |
| Gerçek yanıt | 12 aylık kayıt; `C`, Temperature at 2 Meters; -999 dolgu; LST zaman standardı. `202413` yıllık özet ayrı korundu. |
| Kapsam/kalite | Deneme yılında 12/12 ay sayısal; piksel kalite bayrağı yok. Bu sayım bilimsel kalite veya tüm alan kapsamı değildir. |
| Sözleşme/modül | Nokta-serisi profiline ayrı `monthly_window_series` v0.1.0 eklendi; maskesiz dikdörtgen çıktısı ve CLI çalışıyor. Harita/istatistik özeti yok. |
| Bağımsız hesap | 56 hücre kesişimi toplamı aday pencere alanını kapsıyor. Ocak için açık boylam ağırlıkları ve enlem bantlarıyla ikinci hesap, üretim sonucuyla 12 ondalıkta eşleşti: [alan kanıtı](../../evidence/T2M_WINDOW_PROBE.md). |
| Ortak profil/B uygunluğu | B nokta/parçalı örneği mevcut. [Ortak teknik profil](../../planning/REGION_WORKFLOW.md) 0.1.0 taslağı dolduruldu; bilimsel uygunluk, maske ve nihai ürün/dönem/yöntem seçilmedi |
| Sonuç dosyaları | [İstek](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/a-point-2024/request.json), [API yanıtı](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/a-point-2024/response.json), [çıktı](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/a-point-2024/result.json) |
| Bulgular | Gerçek API erişimi/aktarım başarılı. Bölgesel trend, p-değeri ve iklim etkisi bulgusu yok. |
| Sonraki adım | Parçalama desteği hazır. Gerçek analiz sınırı/kara-su maskesini ve kimlik doğrulamalı küçük maske alt kümesini incele; [maske araştırması](../SURFACE_MASK.md). Küçük teknik hesabı nihai alan/profilde yeniden doğrula. |

## 2026-10-16 · Maskesiz aday dikdörtgen denemesi

Kenar hücrelerini de içeren bölgesel istek 56 hücre/12 ay döndürdü; 12 ayın tamamında tüm kesişim alanı sayısal değer taşıyor. Küresel alan yaklaşımıyla pencere 117.698,095 km²; Ocak ortalaması yaklaşık -0,39 °C, Temmuz 26,52 °C. Bunlar yalnızca 2024 maskesiz arama dikdörtgeni sonuçlarıdır; plato geneli, kara ortalaması veya uzun dönem iklim bulgusu değildir. [Ham yanıt/kaynak/bağımsız hesap](../../evidence/T2M_WINDOW_PROBE.md), [yöntem ve çalıştırma](../../guide/T2M_WINDOW.md). B için işlem yapılmadı.

## 2026-10-16 · Erişim ve ilk adaptör

M1 görevlerine başlama talebiyle nokta örneği alındı; küçük ham yanıt kaynak iziyle saklandı. Deneme yılı 2024, uzun dönem önerisi 2001–2024'ün kabulü değildir. 26 çevrim dışı test ve gerçek örnek doğrulaması geçti. Kaynak URL'si, UTC/Türkiye erişim saati, SHA-256, API metaverisi, komutlar ve sınırlar [kanıt kaydında](../../evidence/T2M_POINT_PROBE.md).
