---
status: Validating
updated: "2026-10-17"
phase: Maske hazırlığı ve aday ortak teknik profil
review_summary: "Kabul edilen mimari yön, seçilen pilot ve henüz açık olan veri kararları."
change_summary: "Yerel token ile NASA metadata erişimi HTTP 200; dört maske değişkeni/boyut metaverisi doğrulandı, sayısal fraksiyonlar henüz alınmadı."
---
# Mevcut durum

**İlk pilot seçildi: 2 metre hava sıcaklığının zaman serisi ve eğilimi.** Kullanıcı modüle özel bilimsel hesap + ortak sonuç adaptörü yaklaşımını kabul etti; alt modüller ve modüller arası veri bağlantıları istedi. Sonuçları inceleten bir web uygulaması sunulacak. [ADR-004](decisions/ADR-004-MODULES-AND-PILOT.md).

## Hazır olanlar

- **Earthdata metadata erişimi doğrulandı:** Kullanıcının yerel terminalde gizli token ile çalıştırdığı kontrol HTTP 200 verdi. Dört maske değişkeni, Float32/birim/boyut sırası ve dolgu metaverisi okundu; XML hash'i raporla eşleşti. Token okunmadı/kaydedilmedi. [Gerçek kanıt](evidence/EARTHDATA_METADATA.md). Sayısal fraksiyon/koordinat değerleri ve gerçek maskeli seri henüz alınmadı.

- **Geliştirme dalında maske hazırlığı:** [MERRA-2 sabit fraksiyonları](research/SURFACE_MASK.md) aday kaynak olarak bulundu; güncel OPeNDAP metadata isteği oturumsuz 401 verdi. Gerçek oranlar alınmadı. A/B için 56/55 hücrelik istek planları ve ayrı aday maske ağırlık önizlemesi hazır. 72 test geçti; 14 yeni test sentetik verilerle hesabı denetliyor. [Kapsam ve gerçek erişim kanıtı](evidence/SURFACE_MASK_CHECK.md). Mevcut gerçek T2M örnekleri maskesiz kaldı.
- [Ortak teknik deneme profili](planning/REGION_WORKFLOW.md) `t2m-technical-2024` 0.1.0 taslağı gerçek örneklerle dolduruldu. Bu, nihai ürün/alan/dönem/maske/istatistik seçimi veya M2 kabulü değildir.

- **M2'nin 6° pencere için beklediği teknik destek main'de:** [parçalı T2M komutu](guide/T2M_TILED_WINDOW.md) iki gerçek isteği birleştirdi; 5 tekrar çıkarılıp 55 hücre/12 ay hesaplandı. B aday sınırı değişmedi. Yeni çıktı profili 0.2.0; eski 0.1.0 örnekler çalışıyor, bilimsel alan yöntemi değişmedi. `cdcc6bd` main birleştirmesinde 58 testlik Ubuntu CI ve Pages yayını başarılı; canlı kılavuz HTTP 200. [Kanıt](evidence/T2M_TILING.md). Sonraki geliştirme ayrı M1 dalında sürer.

- M2'nin [B geometri/API katkısı](research/regions/REGION_B_PROFILE.md) `4ad9448` ile main'e geldi ve yerel kopyaya çakışmasız alındı. M2 başlangıç/üstlenme kaydı artık var: [M2 notu](team/members/M2.md), [H-M1-002 yanıtı](team/HANDOFFS.md). M1 çalışması `codex/m1-modules-region-a` dalında devam ediyor: [ADR-007](decisions/ADR-007-FEATURE-BRANCHES.md). Geliştirme dalı push'u canlı paneli güncellemez; Pages main'e birleştirme sonrası yayımlanır.

- [Modül sistemi](architecture/MODULE_SYSTEM.md), [sistem haritası](architecture/SYSTEM_MAP.md), [ortak sonuç taslağı](architecture/DATA_AND_FLOWS.md), [dar pilot planı](planning/PILOT.md) ve [web deneyimi](product/index.md) güncellendi. `analysis/` içinde ilk nokta adaptörüne ayrı türle maskesiz aday dikdörtgen hesabı eklendi: gerçek bölgesel API, kenar hücrelerini içeren istek, alan kesişimi/ağırlıklar, eksik veri kuralı ve çevrim dışı yeniden hesaplama. Genel modül grafiği ve bilimsel A/B karşılaştırması henüz yok. [Alan kılavuzu](guide/T2M_WINDOW.md), [gerçek alan kanıtı](evidence/T2M_WINDOW_PROBE.md), [ilk nokta kılavuzu](guide/T2M_ADAPTER.md), [teknik seçim](decisions/ADR-006-T2M-POINT-ADAPTER.md).
- Yönetim portalı **[GitHub Pages'te açık](https://sq0eezy.github.io/expedition-73/)**. Yayın işi başarılı; başlangıç sayfası ve okuma kataloğu HTTP 200 ile doğrulandı. [Yayın kaydı](evidence/PAGES_SETUP.md), [kullanım](guide/WEB_PORTAL.md).
- [İki kişilik ekip alanı](team/index.md), üye notları, fikir/devir kayıtları ve [iş panosu](planning/WORK_BOARD.md) mevcut. M1 modüller ve A’yı üstlendi; B’yi M2’ye atadı: [ADR-005](decisions/ADR-005-TEAM-OWNERSHIP.md). M2 daha sonra B'yi üstlenip R-B01/02 çıktısını paylaştı; adayların kesin seçimini yaptığı varsayılmadı. [A görevleri](planning/REGION_A.md), [B görevleri](planning/REGION_B.md) ve [ortak profil](planning/REGION_WORKFLOW.md) hazır.
- [İki aday alan](research/REGION_CANDIDATES.md) için NASA CMR metaverisi sorgulandı. Katalog eşleşmesi gerçek piksel, kalite veya analiz doğrulaması değildir. Türkiye yalnızca örnekti.
- M2 macOS/Python 3.14 ortamında testleri geçirdiğini kendi [üye notunda](team/members/M2.md) bildirdi; bu oturum Mac'te çalışmadı. Yerel geliştirme için [Mac kılavuzu](guide/MACOS_SETUP.md) var. Webden okumak için kurulum/pull gerekmez. Yerel kaynaklarla çalışan kişinin/yapay zekânın güncel kaydı alması gerekir.

## Açık kalanlar

Kesin iki bölge/sınır, ürün/sürüm/erişim yolu, dönem, istatistik yöntemi, teknoloji yığını, genel web arayüzü sorumlusu, teslim tarihi ve nihai uygulama adı seçilmedi. MERRA-2 aylık T2M, Colorado Platosu çevresi/Kuzey Alaska ve 2001–2024 adaydır; seçilmiş sayılmaz.

NASA POWER API’den A aday dikdörtgeniyle kesişen 56 hücre için 2024'ün 12 ayı alındı. Maskesiz alan ağırlıklı seri ve bağımsız Ocak hesabı doğrulandı; küçük ham yanıt saklandı. Bu sonuç kabul edilmiş coğrafi bölgenin veya yalnızca kara alanının sonucu değildir. Hücre kenarları orta noktadan kuruluyor; küresel alan yaklaşımı açıkça kayıtlı. Kara/su maskesi, kesin sınır, B profili, uzun dönem/trend/p-değeri, modüller arası gerçek tüketim ve sunulacak web uygulaması açık. Portalın yayında olması bilimsel ürünün tamamlandığını göstermez.

## Sıradaki küçük adım

Metadata erişimi tamamlandı; sırada küçük A/B fraksiyon/koordinat alt kümesi ve kaynak dönüşümünü doğrulama var. Kaynak dolgu değeri POWER T2M'den farklı; ayrı uygulanmalı. Henüz NetCDF dönüştürücü veya gerçek maskeli seri yok. Kara/buz tanımı ve tam hücre oranının kırpılmış alana uygulanma yaklaşımı iki üye tarafından değerlendirilecek. Token kalıcı tutulmadığı için yeni authenticated istek yine yerel giriş gerektirir. Yeni maske/erişim çalışması ayrı M1 dalında; main'e aktarılmış sayılmaz.
