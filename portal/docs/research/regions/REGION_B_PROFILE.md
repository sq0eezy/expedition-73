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
| Kara/su, yükselti ve grid kapsamı | `M2C0NXASM` 5.12.4 alt kümesi (55 hücre: boylam `38..48`, enlem `316..320`) alınıp doğrulandı; 5 kaynak hücresinde pozitif `FROCEAN` oranı var. `FRLAND` etkin alanı 52.183,622 km² (%98,15), `FRLAND+FRLANDICE` 52.192,891 km² (%98,16). Nihai kara/buz maske politikası ve yükselti düzeltmesi açık. |
| Deneme noktası | 69,0°K / 153,0°B (yükselti 304,58 m); arama penceresinin içindeki teknik erişim noktası, temsili bölge ortalaması değil |
| Sağlayıcı/API | NASA POWER Monthly and Annual API v2.10.0 (`MERRA2` T2M) ve NASA GES DISC OPeNDAP (`M2C0NXASM` 5.12.4 yüzey fraksiyonları) |
| Kaynak ve sürüm ayrımı | POWER yanıtında kaynak `MERRA2`; bu, doğrudan `M2TMNXSLV` 5.12.4 dosyası veya nihai iki-bölge ürünü diye etiketlenmedi |
| Gerçek yanıt | 12 aylık kayıt; `C`, Temperature at 2 Meters; -999 dolgu; LST zaman standardı. `202413` yıllık özet (-8,29 °C) ayrı korundu. |
| Kapsam/kalite | Deneme yılında 12/12 ay sayısal; piksel kalite bayrağı yok. Bu sayım bilimsel kalite veya tüm alan kapsamı değildir. |
| Sözleşme/modül | Nokta (`v0.1.0`), parçalı alan (`v0.2.0`) ve aday yüzey duyarlılığı (`v0.1.0`) şemaları tam uyumlu (`validate-tiled-window`, `fetch_surface_fractions.py --replay` ve `run-surface-workflow` macOS'ta geçti). |
| Bağımsız hesap | Nokta (12 ay): Ocak -22,89 °C, Temmuz 10,92 °C, Yıllık -8,29 °C. Parçalı maskesiz alan (55 hücre): Ocak -24,13 °C, Temmuz 9,70 °C (12 ay eşit ağırlıklı ortalama -8,73 °C). Aday `FRLAND` ağırlıklı: Ocak -24,13 °C, Temmuz 9,70 °C, Kasım -19,59 °C (`|FRLAND - maskesiz|` maks fark: 0,0351 °C). |
| Ortak profil/A uygunluğu | `t2m-technical-2024` (`0.1.0`) teknik deneme profili doğrulandı: A ve B aynı sağlayıcı/gösterge/takvim ve 5 düğümlü aday yüzey akışıyla çalışıyor (134 test geçti). Nihai bilimsel profil ve maske seçimi açık. |
| Sonuç dosyaları | [Nokta çıktısı](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-point-2024/result.json), [Parçalı alan çıktısı](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-window-2024/result.json), [Yüzey fraksiyonları](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-surface-fractions/fractions.json), [Duyarlılık raporu](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-surface-sensitivity.json) |
| Bulgular | Nokta, 55 hücreli parçalı alan ve gerçek `M2C0NXASM` fraksiyonlarıyla 5 düğümlü aday duyarlılık akışı macOS üzerinde doğrulandı. En büyük aylık `|FRLAND - maskesiz|` farkı 0,0351 °C, `|FRLAND+ICE - FRLAND|` farkı 0,00058 °C. Bölgesel trend, p-değeri ve nihai maske kabulü yok. |
| Sonraki adım | Teknik doğrulamalar tamamlandı; sırada kesin sınır/maske politikası uzlaşması ve 2001–2024 uzun dönem serisi hazırlığı var. |

## 2026-10-19 · Bölge B yüzey fraksiyonları ve 5 düğümlü aday duyarlılık doğrulaması

M2 (sq0eezy) olarak `origin/main` (`6da0103`) ile gelen gerçek `M2C0NXASM` 5.12.4 yüzey fraksiyonu alt kümesi (`analysis/examples/b-surface-fractions`) ve `run-surface-workflow` modül akışı macOS/Python 3.14 (`netCDF4 1.7.2`, `numpy 2.5.4`) üzerinde çevrim dışı doğrulandı. 134 birim testin tamamı (0 atlanan) geçti.

Bölge B aday duyarlılık özeti (`analysis/examples/b-surface-sensitivity.json`):
- **Maskesiz aday pencere alanı:** 53.169,124 km² (55 tekil hücre, 5 hücrede pozitif `FROCEAN` okyanus oranı).
- **`FRLAND` (yalnız kara) etkin alanı:** 52.183,622 km² (pencerenin %98,15'i).
- **`FRLAND + FRLANDICE` (kara + kara buzu) etkin alanı:** 52.192,891 km² (pencerenin %98,16'sı).
- **Maskesiz ile `FRLAND` arasındaki en büyük aylık mutlak fark:** `0,03510533 °C` (Kasım 2024: maskesiz `-19,5501 °C`, `FRLAND` `-19,5852 °C`).
- **`FRLAND + FRLANDICE` ile `FRLAND` arasındaki en büyük aylık mutlak fark:** `0,00057698 °C` (Ekim 2024).

Bu sonuçlar iki aday yüzey politikasının teknik duyarlılık karşılaştırmasıdır; nihai bilimsel maske/sınır seçimi veya uzun dönem trend kanıtı değildir.

## 2026-10-18 · Bölge B parçalı alan doğrulaması ve R-B03 teknik uygunluğu

M2 (sq0eezy) olarak Emeç'in `H-M1-005` ile sunduğu parçalı bölgesel alan çıktısı (`analysis/examples/b-window-2024`) macOS üzerinde `validate-tiled-window` komutuyla doğrulandı. 55 tekil MERRA-2 hücresi üzerinden hesaplanan 53.169,124 km²'lik aday arama penceresinde 12/12 ay eksiksiz alan ağırlıklı ortalamalar alındı.

2024 yılı aylık maskesiz alan ağırlıklı ortalamalar:
- Ocak: -24,13 °C, Şubat: -21,53 °C, Mart: -21,46 °C
- Nisan: -10,19 °C, Mayıs: -3,19 °C, Haziran: 8,85 °C
- Temmuz: 9,70 °C, Ağustos: 7,19 °C, Eylül: 1,63 °C
- Ekim: -9,44 °C, Kasım: -19,55 °C, Aralık: -22,61 °C
- **12 ay eşit ağırlıklı ortalama:** -8,73 °C (Nokta örneğindeki -8,29 °C ile tutarlı; kabul edilmiş yıllık zaman ağırlıklandırması henüz seçilmedi).

Ortak teknik deneme profili (`t2m-technical-2024` `0.1.0`) kapsamında iki bölgenin de aynı NASA POWER / MERRA-2 altyapısını, T2M parametresini, Celsius birimini ve LST standardını kullandığı doğrulandı.

## 2026-10-16 · Bölge B ilk erişim ve nokta adaptörü

**M1 modül teslimi · 2026-10-17:** Aşağıdaki M2 nokta kaydı korunuyor. M1, mevcut 6° B penceresini değiştirmeden parçalı erişim desteğini iki gerçek API isteğiyle sınadı; 55 benzersiz hücre/12 ay örneği hazır. Bu M2'nin bölgesel analizini tamamladığı anlamına gelmez. [Yeni kılavuz](../../guide/T2M_TILED_WINDOW.md), [modül kanıtı](../../evidence/T2M_TILING.md), [H-M1-005](../../team/HANDOFFS.md).

M2 (sq0eezy) olarak ilk görev çalışması yapıldı. Aday pencere GeoJSON'u (`b-candidate-window.geojson`) ve yapılandırması (`b-point-2024.config.json`) oluşturuldu. 69,0°K / 153,0°B noktasından gerçek 2024 POWER T2M yanıtı çekildi. 12/12 ay geçerli değer elde edildi; `test_saved_real_b_example_replays_and_aligns` testi dahil tüm çevrim dışı testler (43 test) ve A/B `check-alignment` denetimi başarıyla geçti.
