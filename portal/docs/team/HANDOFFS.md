---
review_summary: "Bir üyeden diğerine aktarılan iş, soru, engel ve yanıtlar."
---
# Devir ve yanıt bekleyenler

Buraya yazmak tek başına bildirim göndermez; alıcı ortak depodan güncel kayıtları alır.

## H-M1-001 · Bölge ve modül önerisini inceleme

- **Gönderen → alıcı:** M1 → M2; kullanıcı “diğer arkadaş da baksın” dediği için bu oturumda kayda geçirildi.
- **Tarih:** 2026-10-15.
- **Durum:** Yanıt bekliyor; görüldü veya kabul edildi sayılmadı.
- **Konu:** [IDEA-M1-001](ideas/IDEA-M1-001.md).
- **Beklenen:** Colorado Platosu/Kuzey Alaska adaylarını ve güncel [tek göstergeli T2M pilotunu](../planning/PILOT.md), açık sınır/kalite sorularını inceleyip M2 görüşünü fikir kartına ekle. Önceki iki göstergeli pilot daraltıldı.
- **Eldeki çıktı:** [Araştırma ve katalog sorguları](../research/REGION_CANDIDATES.md), [mimari önerisi](../architecture/REGIONAL_MODULE_PROPOSAL.md).
- **Yanıt:** Henüz yok. Dış mesaj veya otomatik bildirim gönderilmedi.

## H-M1-002 · Bölge B görevlerine başlangıç

- **Gönderen → alıcı:** M1 → M2; kullanıcı panele eklenmesini ve arkadaşının buradan bakmasını istedi.
- **Tarih:** 2026-10-16.
- **Durum:** Yanıt bekliyor; B ataması M1 tarafından bildirildi, M2 başlangıcı yok.
- **Beklenen ilk çıktı:** [B görevlerinden](../planning/REGION_B.md) R-B01/R-B02: kaynaklı sınır önerisi ve gerçek küçük T2M API yanıtı/erişim engeli özeti. [B fişine](../research/regions/REGION_B_PROFILE.md) yaz.
- **M1’in teslim edeceği:** Sürümlü modül girdi/çıktısı, örnek çağrı ve uygunluk koşulları; MOD-01/03.
- **Yanıt:** Henüz yok. Yeni yanıtta görev kimliği, fiş/çıktı bağlantısı, gerçek durum ve M1’den beklenen girdi yazılacak. Dış mesaj veya bildirim gönderilmedi.

## H-M1-003 · İlk nokta adaptörü ve sözleşme ara teslimi

- **Gönderen → alıcı:** M1 → M2; mevcut ortak modül görevinin panel içi ara teslimi.
- **Tarih:** 2026-10-16.
- **Durum:** İnceleme bekliyor; M2’nin okuduğu/kabul ettiği varsayılmadı.
- **Teslim:** `analysis/` içinde v0.1.0 nokta CLI, istek/sonuç JSON şemaları, gerçek A örneği ve çevrim dışı testler. [Mac çalıştırma ve B’ye uyarlama](../guide/T2M_ADAPTER.md).
- **Beklenen:** Önce kaydedilmiş örneği doğrula; R-B01/02 kapsamında kendi B yapılandırman/denemenle gerçek sonucu fişine ekle. Bölgesel entegrasyon henüz desteklenmiyor.
- **Sınır:** Aktarım/zaman uyumu istatistik onayı değil; B verisi, bölgesel ağırlıklar ve trend hesabı henüz yok. Dış mesaj/bildirim gönderilmedi.

## H-M1-004 · Maskesiz alan hesabı ara teslimi

- **Gönderen → alıcı:** M1 → M2; mevcut ortak modül görevinin panel içi ara teslimi.
- **Tarih:** 2026-10-16.
- **Durum:** İnceleme bekliyor; M2 okuması/kabulü varsayılmadı.
- **Teslim:** Ayrı `monthly_window_series` profili; 56 hücreli A aday penceresi, kenar kesişimleri/alan ağırlıkları, eksik ayı null bırakma ve ham yanıttan yeniden hesaplama. [Mac/Windows komutları](../guide/T2M_WINDOW.md), [kanıt](../evidence/T2M_WINDOW_PROBE.md).
- **Beklenen:** Kaydedilmiş alan örneğini çevrim dışı incele; B fişindeki kendi sınır/API çalışmanı sürdür. Nokta adaptörü çalışmaya devam ediyor. B arama penceresi 6° olduğu için bu tek istekli alan pilotuna doğrudan sığmıyor; B'yi küçültmeden parçalama/veri yolu geliştirmesi gerekiyor.
- **Açık:** Kara/su maskesi, kesin alanlar ve ortak bilimsel uygunluk; çıktı trend veya kara ortalaması değildir. Dış mesaj/bildirim gönderilmedi.

## Bir kayıt için gerekenler

| Alan | İçerik |
|---|---|
| Kimlik | Örneğin `H-M1-001`; oluşturulan gerçek kaydın kimliği |
| Gönderen → alıcı | M1 → M2 veya M2 → M1 |
| Tarih | Gerçek paylaşım tarihi |
| Konu | İlgili görev/fikir bağlantısı |
| Beklenen | Somut soru, inceleme veya yapılacak iş |
| Eldeki çıktı | Dosya, araştırma veya doğrulama bağlantısı |
| Durum | Yanıt bekliyor / Görüldü / Yanıtlandı / Çözüldü |
| Yanıt | Yanıtlayan kişi, tarih ve gerçek yanıt |

Görev durumu burada kopyalanmaz; [iş panosuna](../planning/WORK_BOARD.md) bağlantı verilir. “Görüldü” veya tarayıcıdaki “Okudum” işareti karar onayı anlamına gelmez. Çözülmüş kaydı silmeyin; yanıtını ve sonucunu koruyun.

Kaynak şablon: `templates/TEAM_HANDOFF.md`.
