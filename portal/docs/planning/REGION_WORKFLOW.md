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

## Ortak veri profili · Henüz doldurulmadı

R-A03/R-B03 bu tabloda adayları kaynaklı biçimde kesinleştirir. Değişiklikte profil sürümü ve gerekçesi yazılır; sonuçlar kullandıkları sürüme bağlanır.

| Alan | Güncel kayıt |
|---|---|
| Profil kimliği/sürümü | Henüz yok |
| Gösterge | 2 metre hava sıcaklığı; pilot seçildi |
| Sağlayıcı/ürün/sürüm ve API yolu | İki bölge için seçilmedi; A erişim denemesi NASA POWER Monthly v2.10.0 point API ile başarılı. [Kanıt](../evidence/T2M_POINT_PROBE.md). Doğrudan MERRA-2 ürünüyle eşit sayılmaz |
| A ve B sınır kimliği/sürümü | Seçilmedi; [A fişi](../research/regions/REGION_A_PROFILE.md), [B fişi](../research/regions/REGION_B_PROFILE.md) |
| Ortak dönem/sıklık | Seçilmedi; 2001–2024 ve aylık sıklık önceki adaylar |
| Birim/ölçek/eksik değer kuralı | Ürüne göre doğrulanacak |
| Kara/su maskesi ve alan/kesişim ağırlığı | Tanımlanmadı; coğrafyaya uygun ama karşılaştırılabilir kurallar gerek |
| Referans dönem/mevsim tanımı | Gerekliyse açıkça seçilecek |
| Analiz profili/sürümü ve varsayımlar | Seçilmedi |
| Modül/sözleşme sürümü ve örnek çağrı | İlk nokta profili/CLI 0.1.0 hazır: [çalıştırma](../guide/T2M_ADAPTER.md). Bölgesel profil henüz yok |
| Gözlenen uyumluluk/engeller | A nokta API erişimi doğrulandı. B örneği, bölgesel kapsam ve ortak yöntem henüz yok; A/B uyumu doğrulanmadı |

API kullanımı bütün arşivi elle indirmek zorunda olmak değildir. Öncelik gerekli küçük alt kümeye programla erişmek; sorgu, yanıt ve üretim izini korumaktır. [NASA POWER aylık API](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/) bir seçenektir; nokta yanıtı bölge ortalaması sayılmaz. POWER yanıtı doğrudan MERRA-2 dosyasıyla aynı ürün/sürüm diye etiketlenmez. Sağlayıcı değişikliği önce uygunluk kontrolünden geçer.

## Bir iş tamamlandığında

Kendi fişine gerçek sonuç ve kaynak ekle; panoda ilgili görev satırını güncelle. Diğer kişiden istenen girdiyi [devir listesine](../team/HANDOFFS.md), kısa niyet/özeti kendi üye notuna yaz. İnceleyen adı incelemenin yapıldığı anlamına gelmez. Dış bildirim gönderilmez; ortak sitede görünmesi için değişiklik GitHub main'e ulaşmalı.
