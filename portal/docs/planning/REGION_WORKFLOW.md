---
review_summary: "M1: modüller ve A; M2: B. Paralel başlanacak işler, ortak profil ve karşılıklı teslimler."
change_summary: "İki bölgenin gerçek 2024 örnekleriyle ortak teknik deneme profili dolduruldu; bilimsel profil/maske seçimi açık."
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

## Ortak teknik deneme profili · 0.1.0, aday

**Kimlik:** `t2m-technical-2024`, sürüm `0.1.0`, durum **Candidate / M2 incelemesi bekleniyor**. Bu tablo eldeki teknik denemelerin ortak özelliklerini kaydeder; nihai ürün/alan/dönem/maske veya istatistik kabulü değildir. Kodun bu profil belgesini çalışma zamanında otomatik tükettiği varsayılmadı. R-A03 taslağı hazırlandı; R-B03 bilimsel uygunluk incelemesi açık. Sonraki değişiklikte sürüm/gerekçe yazılacak.

| Alan | Güncel kayıt |
|---|---|
| Profil kimliği/sürümü | `t2m-technical-2024` / `0.1.0`; kabul edilmemiş teknik deneme taslağı |
| Gösterge | 2 metre hava sıcaklığı; pilot seçildi |
| Sağlayıcı/ürün/sürüm ve API yolu | İki küçük örnekte NASA POWER Monthly and Annual API v2.10.0, kaynak `MERRA2`, monthly/point ve regional; nihai ürün seçilmedi. Doğrudan MERRA-2 dosya sürümüyle eşit sayılmaz. [Parçalı deneme kanıtı](../evidence/T2M_TILING.md) |
| A ve B sınır kimliği/sürümü | İki proje arama dikdörtgeni; `search-window-0.1.0`. A `[-113,36,-109,39]`, B `[-156,68,-150,70]`; kabul edilmiş analiz sınırı değil. [A fişi](../research/regions/REGION_A_PROFILE.md), [B fişi](../research/regions/REGION_B_PROFILE.md) |
| Ortak dönem/sıklık | Gerçek teknik örnekler 2024-01…2024-12, aylık, Gregoryen, LST. Uzun dönem seçilmedi; 2001–2024 aday |
| Birim/ölçek/eksik değer kuralı | T2M, degC, 2 metre; sağlayıcı C tanımı kontrol ediliyor. -999 dolgu ve dönmeyen ay ayrı null statüleri. Yıllık 13. kayıt aylara karışmıyor. Alan hesabında her pozitif destek hücresi gerekli |
| Kara/su maskesi ve alan/kesişim ağırlığı | Mevcut gerçek örnekler maskesiz; orta nokta hücre kenarı ve küresel dikdörtgen kesişim alanı yöntemi 0.1.0. A 56/B 55 hücre. M2C0NXASM fraksiyonları aday; gerçek erişim 401, maske alınmadı. [Maske araştırması](../research/SURFACE_MASK.md) |
| Referans dönem/mevsim tanımı | Gerekliyse açıkça seçilecek |
| Analiz profili/sürümü ve varsayımlar | Seçilmedi |
| Modül/sözleşme sürümü ve örnek çağrı | Nokta ve tek istek 0.1.0, parçalı pencere 0.2.0. Bilimsel alan yöntemi aynı 0.1.0; farklı şemaları aynı sürümmüş gibi etiketlemeyin. [Çalıştırma](../guide/T2M_TILED_WINDOW.md) |
| Gözlenen uyumluluk/engeller | Nokta A/B aktarım/zaman kontrolünde 12 ay eşleşiyor; `inference_allowed=false`. A tek istek/B parçalı alan örnekleri ayrı yeniden hesaplamalardan geçiyor; bölgesel bilimsel uygunluk onayı yok. Maskenin canlı metadata/değer erişimi ve tanımı açık |

## Bilimsel profil için karar bekleyenler

Kesin alan/poligon, kara/buz dahil etme kuralı, maskenin tam hücre oranını sınır parçasında kullanma yaklaşımı, gerçek maske alt kümesi, ortak uzun dönem, istatistik yöntemi ve belirsizlik incelemesi henüz seçilmedi. `preview-surface-mask` ayrı aday türdür; gerçek bölgesel seri veya nihai profil yerine geçirilmez. M2'nin uygunluk görüşü gelmeden bu teknik tablo bilimsel kabul kaydı sayılmaz.

API kullanımı bütün arşivi elle indirmek zorunda olmak değildir. Öncelik gerekli küçük alt kümeye programla erişmek; sorgu, yanıt ve üretim izini korumaktır. [NASA POWER aylık API](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/) bir seçenektir; nokta yanıtı bölge ortalaması sayılmaz. POWER yanıtı doğrudan MERRA-2 dosyasıyla aynı ürün/sürüm diye etiketlenmez. Sağlayıcı değişikliği önce uygunluk kontrolünden geçer.

## Bir iş tamamlandığında

Kendi fişine gerçek sonuç ve kaynak ekle; panoda ilgili görev satırını güncelle. Diğer kişiden istenen girdiyi [devir listesine](../team/HANDOFFS.md), kısa niyet/özeti kendi üye notuna yaz. İnceleyen adı incelemenin yapıldığı anlamına gelmez. Dış bildirim gönderilmez; ortak sitede görünmesi için değişiklik GitHub main'e ulaşmalı.
