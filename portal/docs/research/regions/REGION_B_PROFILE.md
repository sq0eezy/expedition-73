---
review_summary: "B aday penceresinin ilk kaynak/sınır önerisi ve gerçek 2024 T2M nokta API denemesi."
change_summary: "Bölge B için kırpılmış hücre alan sınırları (audit-surface-support), 2001–2024 (288 ay) geçmiş serisi ve yıllık ağırlık akışı macOS üzerinde doğrulandı."
---
# Bölge B · Çalışma fişi

sq0eezy'nin ilk çalışma kaydı, **2026-10-16** (son güncelleme **2026-10-28**). Görev durumu [panoda](../../planning/WORK_BOARD.md), kullanım [T2M kılavuzunda](../../guide/T2M_ADAPTER.md). Alanın kesin seçimi yapılmadı; bu fiş teknik inceleme, çok yıllı seri ve aday ağırlık doğrulama kaydıdır.

| Alan | Kayıt |
|---|---|
| Soru | Soğuk Arktik kara ekosisteminde (Brooks Range / North Slope) 2 metre hava sıcaklığının zaman serisi ve eğilimi nedir? Bu deneme yalnızca erişim/biçim sınar. |
| Aday alan | Kuzey Alaska, Brooks Range–North Slope çevresindeki önceki [araştırma penceresi](../REGION_CANDIDATES.md); bütün Arktik veya resmî ekolojik sınır değil |
| Sınır önerisi/sürümü | Proje tarafından tanımlı arama dikdörtgeni: west/south/east/north = -156,68,-150,70; `search-window-0.1.0`. Kabul edilmiş analiz poligonu değil. |
| Geometri | [GeoJSON aday penceresi](https://github.com/sq0eezy/expedition-73/blob/main/analysis/regions/b-candidate-window.geojson); boylam/enlem sırasıyla kapanan dikdörtgen |
| Bölgesel gerekçe | Soğuk mevsim, tundra/orman geçişi ve bitki tepkisi için aday: [NASA saha araştırması](https://science.nasa.gov/blogs/notes-from-the-field/2021/10/05/unraveling-the-mysteries-of-arctic-greening-and-browning/). Koordinatlar bu kaynaktan türetilmiş resmî sınır değil, önceki proje arama önerisi. |
| Kara/su, yükselti ve grid kapsamı | `M2C0NXASM` 5.12.4 alt kümesi (55 hücre: boylam `38..48`, enlem `316..320`, 28 kırpılmış sınır hücresi [%29,69 alan]) doğrulandı; 5 kaynak hücresinde pozitif `FROCEAN` var, granülde `AREA` bildirimi yok (`check-source-area`). Koşullu alan sınırları (`audit-surface-support`): `FRLAND` alt/homojen/üst `51.586,416` / `52.183,622` / `52.668,980 km²` (%97,02 / %98,15 / %99,06); `FRLAND+FRLANDICE` `51.611,105` / `52.192,891` / `52.669,508 km²` (%97,07 / %98,16 / %99,06). Nihai kara/buz maske politikası ve yükselti düzeltmesi açık. |
| Deneme noktası | 69,0°K / 153,0°B (yükselti 304,58 m); arama penceresinin içindeki teknik erişim noktası, temsili bölge ortalaması değil |
| Sağlayıcı/API | NASA POWER Monthly and Annual API v2.10.0 (`MERRA2` T2M) ve NASA GES DISC OPeNDAP (`M2C0NXASM` 5.12.4 yüzey fraksiyonları) |
| Kaynak ve sürüm ayrımı | POWER yanıtında kaynak `MERRA2`; bu, doğrudan `M2TMNXSLV` 5.12.4 dosyası veya nihai iki-bölge ürünü diye etiketlenmedi |
| Gerçek yanıt | 2024 tek yıl (12/12 ay) ve 2001–2024 çok yıllı geçmiş (`288/288 ay`, 55 hücre); `C`, Temperature at 2 Meters; -999 dolgu; LST zaman standardı. |
| Kapsam/kalite | 2001–2024 döneminde 288/288 ay ve 24/24 tam yıl sayısal; piksel kalite bayrağı yok. Bu sayım bilimsel kalite veya tüm alan kapsamı değildir. |
| Sözleşme/modül | Nokta (`v0.1.0`), parçalı alan (`v0.2.0`), çok yıllı geçmiş (`v0.1.0`), aday yüzey duyarlılığı (`v0.1.0`) ve yıllık ağırlık denetimi (`v0.1.0`) şemaları macOS üzerinde 238 Python testiyle doğrulandı. |
| Bağımsız hesap | Nokta (2024): Ocak -22,89 °C, Temmuz 10,92 °C, Yıllık -8,29 °C. Parçalı maskesiz alan (2024, 55 hücre): Ocak -24,13 °C, Temmuz 9,70 °C; eşit ay yıllık `-8,7264 °C`, takvim günü ağırlıklı `-8,6992 °C` (`fark: +0,0272 °C`), sağlayıcı yıllık `-8,6995 °C`. 2001–2024 (24 yıl) en büyük `|takvim günü - eşit ay|` farkı `0,1401 °C` (2021). Aday `FRLAND` (2024): `|FRLAND - maskesiz|` maks aylık fark `0,0351 °C` (Kasım 2024). |
| Ortak profil/A uygunluğu | `t2m-technical-2024` (`0.1.0`) teknik deneme profili, 2001–2024 288 aylık geçmiş ve 2 adımlı yıllık akış (`History → AnnualWeighting`) A ve B için macOS'ta doğrulandı (238 Python testi). Nihai bilimsel profil, maske ve yıllık hedef seçimi açık. |
| Sonuç dosyaları | [Nokta çıktısı](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-point-2024/result.json), [Parçalı alan çıktısı](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-window-2024/result.json), [Yüzey fraksiyonları](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-surface-fractions/fractions.json), [Duyarlılık raporu](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-surface-sensitivity.json), [2001–2024 geçmişi](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-history-2001-2024/result.json), [Yıllık ağırlık denetimi](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/b-annual-weighting-audit.json) |
| Bulgular | Nokta, 55 hücreli parçalı alan, `M2C0NXASM` fraksiyon/alan sınırları, 2001–2024 (288 ay) serisi ve 24 yıllık ağırlık akışı macOS üzerinde doğrulandı. Bölgesel trend, p-değeri, nihai maske ve yıllık ağırlık kabulü yok. |
| Sonraki adım | Teknik doğrulamalar (`H-M1-009..024`) tamamlandı; sırada kesin sınır/maske/yıllık özet uzlaşması ve 2001–2024 uzun dönem eğilim analizi (`R-B05`) var. |

## 2026-10-28 · Koşullu alan sınırları, 2001–2024 (288 ay) geçmişi ve yıllık ağırlık akışı macOS doğrulaması

M2 (`sq0eezy`) olarak `origin/main` (`271cd9e` / `6db86b2` ilk konsolidasyon paketi) `codex/m2-region-b` dalına alındı ve macOS (`Python 3.14.8`, `jsonschema 4.25.1`, `netCDF4 1.7.2`, `numpy 2.5.4`) üzerinde **238 birim testin tamamı** (0 atlanan) ile Bölge B'nin yeni modül/veri çıktıları çevrim dışı doğrulandı:
- **Kırpılmış hücre alan sınırları (`audit-surface-support` & `check-source-area`):** Seçili `M2C0NXASM` granülünde `AREA` değişkeni bulunmadığı (`not_available_in_selected_granule`) teyit edildi. 53.169,124 km²'lik B penceresindeki 55 hücrenin 28'i sınır tarafından kırpılmıştır (kesişim alanının %29,69'u; 24 hücrede alt-hücre yerleşim belirsizliği). `FRLAND` koşullu alanı alt sınırda `51.586,416 km²` (%97,02), homojen dağıtımda `52.183,622 km²` (%98,15), üst sınırda `52.668,980 km²` (%99,06; yerleşim aralığı `1.082,564 km²`) olarak doğrulandı.
- **2001–2024 çok yıllı geçmiş (`validate-window-history`):** `b-history-2023-2024` (24/24 ay) ve `b-history-2001-2024` (288/288 ay, 55 tekil hücre) ham parça yanıtlarından yeniden hesaplanarak doğrulandı (`history_replay_passed`).
- **Yıllık ağırlık denetimi ve bağımlılık akışı (`validate-annual-weighting` & `run-annual-workflow`):** 2001–2024 dönemindeki 24 tam maskesiz yıl için `History → AnnualWeighting` iki adımlı akışı `completed` verdi. 2024 yılında eşit ay ortalaması `-8,726417 °C`, takvim günü ağırlıklı ortalama `-8,699213 °C` (`takvim - eşit = +0,027204 °C`), sağlayıcı yıllık hücre ortalaması `-8,699471 °C` (`sağlayıcı - takvim = -0,000259 °C`); 24 yıl genelinde en büyük `|takvim günü - eşit ay|` farkı `0,140113 °C` (2021) olarak teyit edildi.
- **Web önizleme paketi (`scripts/workspace.py package` & `smoke_preview.py`):** 7 genel dosya (`manifest.json` `0.5.0`) derlenip yerel HTTP 200 smoke testiyle (`127.0.0.1:8873`) doğrulandı. Bu doğrulama teknik tekrar kanıtıdır; nihai maske, yıllık özet yöntemi ve `R-B05` eğilim/belirsizlik kararı açık kalır.

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
