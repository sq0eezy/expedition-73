---
review_summary: "M1: modüller ve A; M2: B. Paralel başlanacak işler, ortak profil ve karşılıklı teslimler."
change_summary: "Kullanıcının iş bölümü talebi görev sırası ve ortak veri profiliyle somutlaştırıldı."
---
# İki bölge için iş bölümü

**2026-10-16:** Kullanıcı kendisinin modülleri ve A'yı, arkadaşının B'yi yapacağını belirtti: [ADR-005](../decisions/ADR-005-TEAM-OWNERSHIP.md). M2 adına bağımsız kabul/başlama beyanı yazılmadı. Atama, görüş ve gerçek ilerleme ayrı kaydedilir. Görev durumlarının esas kaynağı [iş panosudur](WORK_BOARD.md).

| Kişi | Sorumluluk | İlk açacağı sayfa |
|---|---|---|
| Emeç · M1 | Ortak modüller, sözleşme/adaptör ve Bölge A | [A ve modül görevleri](REGION_A.md) |
| sq0eezy · M2 | Bölge B girdileri, veri uygunluğu, hesap/sonuç kontrolü | [B görevleri](REGION_B.md) |

İlk pilot tek gösterge: 2 metre hava sıcaklığı. A/B iş kimlikleridir; mevcut Colorado Platosu/Kuzey Alaska adaylarının kesin seçildiği anlamına gelmez. Ürün, dönem ve analiz yöntemi de açık.

## Çalışma sırası

1. **Paralel:** İki kişi kendi bölge fişini ve küçük API erişim denemesini hazırlar (R-A01/02, R-B01/02). M1 ayrıca MOD-01 sözleşme taslağını hazırlar.
2. **Birlikte eşleştir:** A/B özetleriyle M1 önce ortak profil taslağını paylaşır (R-A03); M2 B'nin uygunluğunu inceler (R-B03); sonra profilin kullanılacak sürümü kaydedilir. M2'nin incelemeye başlaması için R-A03'ün bütünüyle bitmesi gerekmez. Eksik alan veya erişim sorunu varsa gerekçesiyle karar güncellenir.
3. **Ortak modülü teslim et:** M1 MOD-02/03'ü doğrulanabilir örnek ve sürümle hazırlar; M2 B'nin yapılandırmasını bu arayüze bağlar.
4. **Küçük hesabı çapraz kontrol et:** R-A04/B04'te tek tarih/az sayıda hücreyle ara hesap incelenir; hatayı tam dönem sonuç üretmeden yakala.
5. **Aynı sürümle iki alan:** R-A05/B05 tam seri, kapsam ve analiz üretir. R-A06/B06 yorum ve web kontrolünü tamamlar. A–B farkı için ayrıca uygun analiz gerekir.

## Ortak veri profili · 2026-10-18 (R-A03 / R-B03)

R-A03 ve R-B03 kapsamında A ve B aday alanlarının veri uyumu incelendi ve doğrulandı.

| Alan | Güncel kayıt |
|---|---|
| Profil kimliği/sürümü | `common-profile-t2m-0.2.0` |
| Gösterge | 2 metre hava sıcaklığı (T2M) · Pilot gösterge |
| Sağlayıcı/ürün/sürüm ve API yolu | NASA POWER Monthly and Annual API v2.10.0 (MERRA-2 tabanlı servis). Nokta API ve Parçalı Bölgesel API yolları |
| A ve B sınır kimliği/sürümü | Bölge A: `[-113, 36, -109, 39]` (`search-window-0.1.0`), Bölge B: `[-156, 68, -150, 70]` (`search-window-0.1.0`) |
| Ortak dönem/sıklık | 2024 (aylık sıklık, 12/12 ay eksiksiz doğrulandı); uzun dönem adayı: 2001–2024 |
| Birim/ölçek/eksik değer kuralı | Celsius (°C), dolgu değeri `-999.0` (seriye katılmıyor, eksik değer durumunda ay `null` kalır); 2024 denemelerinde eksik veriyle karşılaşılmadı |
| Kara/su maskesi ve alan/kesişim ağırlığı | MERRA-2 0,625° × 0,5° ızgara hücre orta noktalarından kenar kurma ve küresel dikdörtgen kesişim integrali (`R=6.371.008,8 m`). Kara/su maskesi henüz uygulanmadı; Region B kıyı hücreleri için Faz 2'de maske eklenecek |
| Referans dönem/mevsim tanımı | Henüz tanımlanmadı; tam dönem serisinde (2001–2024) belirlenecek |
| Analiz profili/sürümü ve varsayımlar | `spherical_midpoint_cell_intersection` 0.1.0; hücre içi değer sabit kabul edilir |
| Modül/sözleşme sürümü ve örnek çağrı | Nokta sözleşmesi v0.1.0 (`monthly_point_series`), Parçalı alan sözleşmesi v0.2.0 (`monthly_tiled_window_series`). CLI komutları: `fetch-power-point`, `fetch-power-tiled-window` |
| Gözlenen uyumluluk/engeller | A ve B nokta serileri `check-alignment` ile 12 ay eksiksiz eşleşti. B'nin 6° genişliği parçalı API motoruyla (`MOD-04`) çözüldü; 55 tekil hücre integrali doğrulandı. Kalan tek engel: Region B kıyı hücreleri için kara/su maskesi gereksinimi |

API kullanımı bütün arşivi elle indirmek zorunda olmak değildir. Öncelik gerekli küçük alt kümeye programla erişmek; sorgu, yanıt ve üretim izini korumaktır. [NASA POWER aylık API](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/) bir seçenektir; nokta yanıtı bölge ortalaması sayılmaz. POWER yanıtı doğrudan MERRA-2 dosyasıyla aynı ürün/sürüm diye etiketlenmez. Sağlayıcı değişikliği önce uygunluk kontrolünden geçer.

## Bir iş tamamlandığında

Kendi fişine gerçek sonuç ve kaynak ekle; panoda ilgili görev satırını güncelle. Diğer kişiden istenen girdiyi [devir listesine](../team/HANDOFFS.md), kısa niyet/özeti kendi üye notuna yaz. İnceleyen adı incelemenin yapıldığı anlamına gelmez. Dış bildirim gönderilmez; ortak sitede görünmesi için değişiklik GitHub main'e ulaşmalı.
