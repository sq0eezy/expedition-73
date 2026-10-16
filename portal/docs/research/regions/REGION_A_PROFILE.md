---
review_summary: "A aday penceresinin ilk kaynak/sınır önerisi ve gerçek 2024 T2M nokta API denemesi."
change_summary: "R-A01 sınır önerisi yazıldı; R-A02 gerçek nokta erişimi ve ilk adaptör doğrulandı."
---
# Bölge A · Çalışma fişi

M1'in ilk çalışma kaydı, **2026-10-16**. Görev durumu [panoda](../../planning/WORK_BOARD.md), kullanım [T2M kılavuzunda](../../guide/T2M_ADAPTER.md). Alanın kesin seçimi yapılmadı; bu fiş ilk teknik incelemedir.

| Alan | Kayıt |
|---|---|
| Soru | Seçilecek bu kara alanında 2 metre hava sıcaklığının ortak uzun dönemdeki eğilimi nedir? Bu deneme yalnızca erişim/biçim sınar. |
| Aday alan | Colorado Platosu çevresindeki önceki [araştırma penceresi](../REGION_CANDIDATES.md); bütün plato veya resmî ekolojik sınır değil |
| Sınır önerisi/sürümü | Proje tarafından tanımlı arama dikdörtgeni: west/south/east/north = -113,36,-109,39; `search-window-0.1.0`. Kabul edilmiş analiz poligonu değil. |
| Geometri | [GeoJSON aday penceresi](https://github.com/sq0eezy/expedition-73/blob/main/analysis/regions/a-candidate-window.geojson); boylam/enlem sırasıyla kapanan dikdörtgen |
| Bölgesel gerekçe | Kurak ve yüksekliği değişen kara çevresi sıcaklık sorusu için aday: [NASA bölge tanımı](https://modis.gsfc.nasa.gov/gallery/individual.php?db_date=2021-04-13). Koordinatlar bu kaynaktan türetilmiş resmî sınır değil, önceki proje arama önerisi. |
| Kara/su, yükselti ve grid kapsamı | Poligon içindeki kara/su maskesi, hücre sayısı ve alan ağırlıkları henüz incelenmedi. Nokta yanıtı bunların yerine geçmez. |
| Deneme noktası | 37,5°K / 111°B; arama penceresinin içindeki teknik erişim noktası, temsili bölge ortalaması değil |
| Sağlayıcı/API | NASA POWER Monthly and Annual API v2.10.0; point/T2M/community SB/2024/JSON |
| Kaynak ve sürüm ayrımı | Yanıtta kaynak `MERRA2`; bu, doğrudan `M2TMNXSLV` 5.12.4 dosyası veya nihai iki-bölge ürünü diye etiketlenmedi |
| Gerçek yanıt | 12 aylık kayıt; `C`, Temperature at 2 Meters; -999 dolgu; LST zaman standardı. `202413` yıllık özet ayrı korundu. |
| Kapsam/kalite | Deneme yılında 12/12 ay sayısal; piksel kalite bayrağı yok. Bu sayım bilimsel kalite veya tüm alan kapsamı değildir. |
| Sözleşme/modül | İlk nokta-serisi profili ve CLI `0.1.0`; alan ortalaması/harita/istatistik çıktısı henüz yok |
| Bağımsız hesap | Bölgesel alan hesabı yapılmadı; gerçek yanıtın çevrim dışı yeniden normalleştirilmesi ve şema/tutarlılık kontrolleri geçti |
| Ortak profil/B uygunluğu | B erişim örneği henüz yok; A/B ortak ürün/dönem/yöntem seçilmedi |
| Sonuç dosyaları | [İstek](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/a-point-2024/request.json), [API yanıtı](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/a-point-2024/response.json), [çıktı](https://github.com/sq0eezy/expedition-73/blob/main/analysis/examples/a-point-2024/result.json) |
| Bulgular | Gerçek API erişimi/aktarım başarılı. Bölgesel trend, p-değeri ve iklim etkisi bulgusu yok. |
| Sonraki adım | B denemesiyle ortak profili eşleştir; gerçek analiz poligonu/maske ve bölgesel alt küme yolunu incele; sonra alan hesabını küçük örnekle doğrula. |

## 2026-10-16 · Erişim ve ilk adaptör

M1 görevlerine başlama talebiyle nokta örneği alındı; küçük ham yanıt kaynak iziyle saklandı. Deneme yılı 2024, uzun dönem önerisi 2001–2024'ün kabulü değildir. 26 çevrim dışı test ve gerçek örnek doğrulaması geçti. Kaynak URL'si, UTC/Türkiye erişim saati, SHA-256, API metaverisi, komutlar ve sınırlar [kanıt kaydında](../../evidence/T2M_POINT_PROBE.md).
