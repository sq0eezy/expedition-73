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
| Sözleşme/modül | Nokta-serisi profili v0.1.0 ve parçalı alan profili v0.2.0 tam uyumlu (`validate-tiled-window` ile `replay_passed` alındı; 55 hücre tekilleştirildi). |
| Bağımsız hesap | Nokta (12 ay): Ocak -22,89 °C, Temmuz 10,92 °C, Yıllık -8,29 °C. Parçalı alan (55 hücre): Ocak -24,13 °C, Temmuz 9,70 °C, Yıllık -8,73 °C. |
| Ortak profil/A uygunluğu | R-B03 onaylandı: A ile aynı sağlayıcı (NASA POWER/MERRA-2), aynı gösterge (T2M, degC), aynı takvim (2024) ve LST standardı. Çevrim dışı testler (58 test) ve şema kontrolleri tam uyumlu. |
| Sonuç dosyaları | [Nokta çıktısı](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-point-2024/result.json), [Parçalı alan çıktısı](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-window-2024/result.json) |
| Bulgular | Gerçek API erişimi/aktarım başarılı. Geniş 6° aday penceresinde 55 hücre tekilleştirilerek -8,73 °C yıllık sıcaklık hesaplandı; nokta verisiyle (-8,29 °C) yüksek tutarlılık sağlandı. Bölgesel trend, p-değeri ve iklim etkisi bulgusu yok. |
| Sonraki adım | R-B03 tamamlandı; R-B04 doğrulandı. Sırada kara/su maskesi araştırması ve 2001–2024 uzun dönem serisinin hazırlanması var. |

## 2026-10-18 · Bölge B parçalı alan doğrulaması ve R-B03 uygunluğu

M2 (sq0eezy) olarak Emeç'in `H-M1-005` ile sunduğu parçalı bölgesel alan çıktısı (`analysis/examples/b-window-2024`) macOS üzerinde `validate-tiled-window` komutuyla doğrulandı. 55 tekil MERRA-2 hücresi üzerinden hesaplanan 53.169,1 km²'lik aday arama penceresinde 12/12 ay eksiksiz alan ağırlıklı ortalamalar alındı.

2024 yılı aylık alan ağırlıklı ortalamalar:
- Ocak: -24,13 °C, Şubat: -21,53 °C, Mart: -21,46 °C
- Nisan: -10,19 °C, Mayıs: -3,19 °C, Haziran: 8,85 °C
- Temmuz: 9,70 °C, Ağustos: 7,19 °C, Eylül: 1,63 °C
- Ekim: -9,44 °C, Kasım: -19,55 °C, Aralık: -22,61 °C
- **Yıllık alan ortalaması:** -8,73 °C (Nokta örneğindeki -8,29 °C ile tutarlı ve geniş soğuk Arktik alanı yansıtıyor).

R-B03 ortak veri profili uygunluğu onaylandı: İki bölge de aynı NASA POWER / MERRA-2 altyapısını, T2M parametresini, Celsius birimini ve LST standardını kullanmaktadır. Region B için açık kalan tek teknik gereksinim, Arktik Okyanusu kıyı hücrelerinin ayıklanması için Faz 2'de uygulanacak kara/su maskesidir.

## 2026-10-16 · Bölge B ilk erişim ve nokta adaptörü

**M1 modül teslimi · 2026-10-17:** Aşağıdaki M2 nokta kaydı korunuyor. M1, mevcut 6° B penceresini değiştirmeden parçalı erişim desteğini iki gerçek API isteğiyle sınadı; 55 benzersiz hücre/12 ay örneği hazır. Bu M2'nin bölgesel analizini tamamladığı anlamına gelmez. [Yeni kılavuz](../../guide/T2M_TILED_WINDOW.md), [modül kanıtı](../../evidence/T2M_TILING.md), [H-M1-005](../../team/HANDOFFS.md).

M2 (sq0eezy) olarak ilk görev çalışması yapıldı. Aday pencere GeoJSON'u (`b-candidate-window.geojson`) ve yapılandırması (`b-point-2024.config.json`) oluşturuldu. 69,0°K / 153,0°B noktasından gerçek 2024 POWER T2M yanıtı çekildi. 12/12 ay geçerli değer elde edildi; `test_saved_real_b_example_replays_and_aligns` testi dahil tüm çevrim dışı testler (43 test) ve A/B `check-alignment` denetimi başarıyla geçti.
