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
- **Durum:** Yanıtlandı · İnceleme bekliyor; M2 başlangıç ve ilk erişim denemesini tamamladı.
- **Beklenen ilk çıktı:** [B görevlerinden](../planning/REGION_B.md) R-B01/R-B02: kaynaklı sınır önerisi ve gerçek küçük T2M API yanıtı/erişim engeli özeti. [B fişine](../research/regions/REGION_B_PROFILE.md) yaz.
- **M1’in teslim edeceği:** Sürümlü modül girdi/çıktısı, örnek çağrı ve uygunluk koşulları; MOD-01/03.
- **Yanıt:** M2 (sq0eezy), 2026-10-16: R-B01 ve R-B02 tamamlandı. Aday pencere GeoJSON'u (`b-candidate-window.geojson`), konfigürasyonu (`b-point-2024.config.json`) ve gerçek 2024 POWER verisi (`analysis/examples/b-point-2024/`) üretildi. [B fişine](../research/regions/REGION_B_PROFILE.md) işlendi. `check-alignment` ile A ve B 12 ay eşleşti (`aligned_point_series`). M1'den beklenen: 6° genişlik için parçalı bölgesel adaptör desteği veya ortak sınır revizyonu. Dış mesaj gönderilmedi.

**H-M1-002 takip kontrolü · 2026-10-17, M1 oturumu:** M2'nin `4ad9448` katkısı ve yanıtı okundu/alındı. B örneği ham yanıttan yeniden üretildi; Windows'ta 43 test, iki nokta şema doğrulaması, A/B 12 eşleşen ay ve mevcut A alan örneği geçti. `inference_allowed=false`; bu teknik kontrol bölgesel bilimsel uygunluk incelemesi değildir. M2'nin 6° pencereyi bölgesel işleme beklentisi sıradaki modül işine taşındı. [Dal düzeni](../decisions/ADR-007-FEATURE-BRANCHES.md). M2 adına yeni niyet/başlangıç eklenmedi, dış mesaj gönderilmedi.

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

## H-M1-005 · B genişliği için parçalı erişim desteği

- **Gönderen → alıcı:** M1 → M2; kullanıcının ortak modülü main'de paylaşma talebi kapsamında panel içi teslim.
- **Tarih:** 2026-10-17.
- **Durum:** `cdcc6bd` ile main'de paylaşıldı; Ubuntu testleri ve canlı panel yayını başarılı. M2 inceleme/çalıştırma sonucu bekleniyor: [kanıt](../evidence/T2M_TILING.md).
- **Teslim:** `fetch-power-tiled-window` / `validate-tiled-window`, bölgeden bağımsız yapılandırma, 0.2.0 çıktı ve iki gerçek B ham yanıtı. B'nin mevcut 6° arama penceresi küçülmedi; ortak 5 hücre bir kez sayıldı. [Mac komutları](../guide/T2M_TILED_WINDOW.md), [kontroller ve sınırlar](../evidence/T2M_TILING.md).
- **M2'nin yapabileceği:** Güncel main'i kendi değişikliklerini koruyarak al; kendi çalışma dalında kayıtlı `examples/b-window-2024` örneğini çevrim dışı doğrula. R-B03/04 kapsamında alan/maske/uygunluk incelemesini sürdür; yeni API çağrısı gerekirse yeni çıktı klasörü kullan.
- **Sınır:** Kesin alan/maske seçimi ve bilimsel A/B uygunluk onayı yok; B adına yeni yorum veya başlangıç üretilmedi. Dış mesaj/bildirim gönderilmedi.

## H-M1-006 · Maske adayı ve teknik profil taslağı

- **Gönderen → alıcı:** M1 → M2; ortak modül görevine ait panel içi araştırma/taslak kaydı.
- **Tarih:** 2026-10-17.
- **Durum:** M1 geliştirme dalında, inceleme bekliyor; main'e veya canlı panele aktarılmış sayılmaz.
- **Teslim:** [Maske adayı/erişim](../research/SURFACE_MASK.md), [sentetik testlerin sınırı](../evidence/SURFACE_MASK_CHECK.md), `t2m-technical-2024` 0.1.0 [aday profil](../planning/REGION_WORKFLOW.md). A/B için beklenen maske hücreleri ve indeksleri çıkarıldı; gerçek veri erişimi 401, maske alınmadı.
- **İncelenecek:** Kara buzu dahil etme tanımı, tam hücre oranını kırpılmış sınıra uygulama yaklaşımı, kesin sınır ve ortak profil. Sessizlik kabul değildir; M2 adına görüş eklenmedi.
- **Ayrım:** M2 main'deki önceki parçalı destekle çalışabilir. Bu yeni kayıt maskeli B analizi veya NASA veri doğrulaması değildir. Dış mesaj/bildirim gönderilmedi.

**Erişim adımı güncellemesi · 2026-10-17:** Kayıt adımı tamamlandı bilgisi geldi; programatik erişim henüz doğrulanmadı. [Yerel metadata kontrolü](../guide/EARTHDATA_ACCESS.md) hazır; kullanıcı token'ı kendi terminalinde gizli girer. Başarılı gerçek yanıt gelene kadar fraksiyon veya maske doğrulaması yapılmış sayılmaz.

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
