---
review_summary: "B aday penceresinin ilk kaynak/sınır önerisi ve gerçek 2024 T2M nokta API denemesi."
change_summary: "M2 için B arama penceresi GeoJSON'u, b-point-2024 config/yanıt/çıktı dosyaları ve ilk NASA POWER denemesi eklendi."
---
# Bölge B · Çalışma fişi

sq0eezy'nin ilk çalışma kaydı, **2026-10-16**. Görev durumu [panoda](../../planning/WORK_BOARD.md), kullanım [T2M kılavuzunda](../../guide/T2M_ADAPTER.md). Alanın kesin seçimi yapılmadı; bu fiş ilk teknik inceleme ve API erişim kaydıdır.

| Alan | Kayıt |
|---|---|
| Soru | Soğuk Arktik kara ekosisteminde (Brooks Range / North Slope) 2 metre hava sıcaklığının zaman serisi ve eğilimi nedir? Bu deneme yalnızca erişim/biçim sınar. |
| Aday alan | Kuzey Alaska, Brooks Range–North Slope çevresindeki önceki [araştırma penceresi](../REGION_CANDIDATES.md); bütün Arktik veya resmî ekolojik sınır değil |
| Sınır önerisi/sürümü | Proje tarafından tanımlı arama dikdörtgeni: west/south/east/north = -156,68,-150,70; `search-window-0.1.0`. Kabul edilmiş analiz poligonu değil. |
| Geometri | [GeoJSON aday penceresi](https://github.com/sq0eezy/expedition-73/blob/main/analysis/regions/b-candidate-window.geojson); boylam/enlem sırasıyla kapanan dikdörtgen |
| Bölgesel gerekçe | Soğuk mevsim, tundra/orman geçişi ve bitki tepkisi için aday: [NASA saha araştırması](https://science.nasa.gov/blogs/notes-from-the-field/2021/10/05/unraveling-the-mysteries-of-arctic-greening-and-browning/). Koordinatlar bu kaynaktan türetilmiş resmî sınır değil, önceki proje arama önerisi. |
| Kara/su, yükselti ve grid kapsamı | Kara/su maskesi (Arktik gölleri/kıyı şeridi), kutup gecesi ve yükselti açık. Genişlik 6° olduğu için mevcut tek istekli alan adaptörüne (5° sınırı) doğrudan girmez; nokta API üzerinden sınandı. |
| Deneme noktası | 69,0°K / 153,0°B (yükselti 304,58 m); arama penceresinin içindeki teknik erişim noktası, temsili bölge ortalaması değil |
| Sağlayıcı/API | NASA POWER Monthly and Annual API v2.10.0; point/T2M/community SB/2024/JSON |
| Kaynak ve sürüm ayrımı | Yanıtta kaynak `MERRA2`; bu, doğrudan `M2TMNXSLV` 5.12.4 dosyası veya nihai iki-bölge ürünü diye etiketlenmedi |
| Gerçek yanıt | 12 aylık kayıt; `C`, Temperature at 2 Meters; -999 dolgu; LST zaman standardı. `202413` yıllık özet (-8,29 °C) ayrı korundu. |
| Kapsam/kalite | Deneme yılında 12/12 ay sayısal; piksel kalite bayrağı yok. Bu sayım bilimsel kalite veya tüm alan kapsamı değildir. |
| Sözleşme/modül | Nokta-serisi profili v0.1.0 tam uyumlu (`check-alignment` ile A ve B 12/12 ay eşleşti). Bölgesel alan hesabı için istek parçalama planlanıyor. |
| Bağımsız hesap | 12 ayın değerleri: Ocak -22,89 °C, Şubat -21,67 °C, Mart -21,49 °C, Nisan -9,69 °C, Mayıs -2,88 °C, Haziran 9,30 °C, Temmuz 10,92 °C, Ağustos 8,16 °C, Eylül 2,48 °C, Ekim -8,77 °C, Kasım -19,71 °C, Aralık -23,62 °C. |
| Ortak profil/A uygunluğu | A ile aynı sağlayıcı (NASA POWER), aynı değişken (T2M, degC), aynı takvim (2024) ve LST standardı. `check-alignment` sonucu: `aligned_point_series`. |
| Sonuç dosyaları | [İstek](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-point-2024/request.json), [API yanıtı](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-point-2024/response.json), [çıktı](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-point-2024/result.json) |
| Bulgular | Gerçek API erişimi/aktarım başarılı. Nokta verisi Arktik soğuk kış (-23 °C bandı) ve kısa ılıman yaz (10 °C bandı) dinamiklerini beklenen şekilde yansıtıyor. Bölgesel trend, p-değeri ve iklim etkisi bulgusu yok. |
| Sonraki adım | B fişi tamamlandı; R-B01/R-B02 doğrulandı. 6°'lik pencere için parçalı bölgesel istek ya da odaklanmış alt bölge sınırını Emeç ile netleştir. |

## 2026-10-16 · Bölge B ilk erişim ve nokta adaptörü

M2 (sq0eezy) olarak ilk görev çalışması yapıldı. Aday pencere GeoJSON'u (`b-candidate-window.geojson`) ve yapılandırması (`b-point-2024.config.json`) oluşturuldu. 69,0°K / 153,0°B noktasından gerçek 2024 POWER T2M yanıtı çekildi. 12/12 ay geçerli değer elde edildi; `test_saved_real_b_example_replays_and_aligns` testi dahil tüm çevrim dışı testler (43 test) ve A/B `check-alignment` denetimi başarıyla geçti.
