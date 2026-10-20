---
status: Validating
updated: "2026-10-19"
phase: Kayıtlı verilerle ilk yerel sonuç ekranı
review_summary: "Kabul edilen mimari yön, seçilen pilot ve henüz açık olan veri kararları."
change_summary: "İlk web ekranı yerelde çalışıyor; 162 analiz testi ve on Chrome senaryosu geçti. Nihai profil/yığın ve barındırma açık."
---
# Mevcut durum

**İlk pilot seçildi: 2 metre hava sıcaklığının zaman serisi ve eğilimi.** Kullanıcı modüle özel bilimsel hesap + ortak sonuç adaptörü yaklaşımını kabul etti; alt modüller ve modüller arası veri bağlantıları istedi. Sonuçları inceleten bir web uygulaması sunulacak. [ADR-004](decisions/ADR-004-MODULES-AND-PILOT.md).

## Hazır olanlar

- **İlk yerel web ekranı çalışıyor:** A/B seçimi, aylık grafik, üç yüzey ağırlığı, ay kartları/farkı, alan kapsamı, kaynak ayrıntısı, tablo ve JSON indirme hazır. Builder kayıtlı girdileri yeniden doğrular, yalnız dört genel çıktı dosyası üretir; tarayıcı NASA/token kullanmaz. Dokuz yeni testle 162 analiz testi, gerçek veri tekrarları ve on Chrome senaryosu geçti; mobil/masaüstü görseller incelendi. [Kullanım ve sınırlar](product/RESULTS_PREVIEW.md), [gerçek kanıt](evidence/RESULTS_PREVIEW_CHECK.md). `web/` teknik prototiptir; nihai teknoloji veya bilimsel profil kabulü yok. M1 dalında yerel, main/Pages değişmedi.

- **Kaynak AREA uygunluğu kontrol edildi:** Seçili granülün tam DMR'si yeniden HTTP 200 ile okundu; eski hash'le aynı ve AREA sayısal bildirimi yok. Şartname ile başka NASA README tablosu arasındaki fark kaydedildi. `check-source-area` bu durumu çevrim dışı açıkça raporlar; değer/alan karşılaştırması yapılmadı. Yedi yeni test, toplam 153 test ve gerçek veri tekrarları başarılı. [Esas inceleme](research/SOURCE_AREA.md), [erişim/komut kanıtı](evidence/SOURCE_AREA_CHECK.md). Yeni sonuç M1 dalında yerel; maske/profil kabulü yok.

- **Kesilmiş hücreler için alan denetimi:** `audit-surface-support` kayıtlı gerçek girdileri yeniden doğrulayıp iki aday yüzey için koşullu alt/homojen/üst alan raporu verir. 12 yeni testle toplam 146 test başarılı; eski sıcaklık örnekleri değişmedi. Aralıklar güven aralığı veya sıcaklık hata payı değildir; kaynak AREA/alan ölçüsü uyumu doğrulanmadı. [Yöntem](research/SURFACE_SUPPORT.md), [gerçek sonuç](evidence/SURFACE_SUPPORT_CHECK.md). Yeni çalışma M1 dalında yerel; önceki canlı teslim aşağıda.

- **M2 macOS üzerinde 134 testi ve Bölge B aday yüzey akışını doğruladı:** `origin/main` (`6da0103`), `codex/m2-region-b` dalına alındı; macOS/Python 3.14 (`netCDF4 1.7.2`, `numpy 2.5.4`) üzerinde 134 birim testin tamamı (0 atlanan), 55 hücrelik `b-surface-fractions` NetCDF dönüşüm tekrarı ve 5 düğümlü `run-surface-workflow` Bölge B akışı (`12/12 ay`) doğrulandı. [B fişi](research/regions/REGION_B_PROFILE.md), [M2 notu](team/members/M2.md), [H-M1-008 yanıtı](team/HANDOFFS.md). Nihai bilimsel maske/sınır seçimi açık.

- **Mevcut M1 dilimi ortak panelde paylaşıldı:** Kullanıcının açık talebiyle geliştirme dalı korundu, incelenmiş sürüm main'e birleştirildi. `96815c5` için Ubuntu'da 134 test, gerçek A/B aday akışları ve Pages başarılı; canlı yeni belgeler/katalog HTTP 200. İlk CI'da saptanan Windows/Linux satır sonu kaynak hash farkı, örnek baytlarını koruyan Git ayarı ve yeniden üretimle giderildi. PR API yetkisi olmadığı için normal Git merge kullanıldı. M2'nin ayrı dalı korunur; yeni kabul beyanı yok. [Yayın/CI kanıtı](evidence/SURFACE_RELEASE.md).

- **Gerçek girdiler motorla bağlandı:** [Kayıtlı T2M → fraksiyon uygunluğu → iki aday önizleme → duyarlılık raporu](evidence/SURFACE_WORKFLOW.md) A ve B için tamamlandı; her ikisinde 12/12 ay. Ortak kaynaklar bir kez doğrulanıyor, bozuk/yanlış bölge girdisinde bağımlı hesap engelleniyor; eksik ay null kalıyor. 13 yeni entegrasyon testi, toplam 134 test geçti. Küçük açık NASA fraksiyon örnekleri artık analysis/examples altında tekrar üretilebilir; özel .env kopyalanmadı. İki politika adaydır; bilimsel maske seçilmedi.


- **İlk bağımlılık motoru çalışıyor:** M1'in A→B, A+B→C örneği `demo-workflow` ile sıralı yürütüldü; ortak A tek hesaplandı, aynı girdi kimliği/ata izi ve hata/engelli durumları doğrulandı. A parametresi değişince eski A/B/C güncel değil olarak saptandı; eski A + yeni B karışımı reddedildi. 20 yeni test ve toplam 121 test geçti. [Kanıt/komut](evidence/WORKFLOW_ENGINE.md). Bu ilk komut yapay denemedir; sonraki gerçek girdi akışı üsttedir. Kalıcı cache/otomatik kaynak izleme/web ürünü yok. [MOD-06](planning/WORK_BOARD.md) Validating.

- **Yerel token kaydı eklendi:** Kullanıcı `.env` kaydı istedi; iki erişim komutu `--save-token` ile gizli girişten kaydeder, sonraki çalıştırmalar proje `.env` değerini kullanır. Kullanıcı yerel kaydı tamamladı; kayıtlı değer ekrana çıkarılmadan isteklerde kullanıldı. Önceki Hyrax 200 / ürün 403 ayrımından sonra kullanıcı GES DISC arşiv onayını tamamladı; yeni gerçek A/B veri çıktısı doğrulandı. [Erişim geçmişi](guide/EARTHDATA_ACCESS.md).


- **Küçük fraksiyon aktarımı hazır:** [Yerel gizli-token komutu](guide/SURFACE_SUBSET.md), A/B için sınırlı DAP4 sorgusu, NetCDF dönüşümü ve çevrim dışı tekrar denetimi eklendi. Yeni 13 test yapay veriyle geçti; gerçek metadata giriş kontrolü başarılı. Gerçek A/B fraksiyon alt kümeleri alındı; 56/55 hücre, koordinatlar, dolgu, hash ve yeniden dönüşüm geçti. [Kanıt ve sınırlar](evidence/SURFACE_SUBSET_CHECK.md). Kabul edilmiş maskeli seri yok; iki fraksiyon ağırlık seçeneği yalnız aday önizleme olarak hesaplandı.
- **M2 yeni katkısı okundu ve birleştirildi:** `codex/m2-region-b` dalındaki `791e07c` ve 2026-10-19 güncellemesiyle Mac üzerinde B tekrar kontrolü, 134 test başarısı ve `t2m-technical-2024` (`0.1.0`) teknik deneme profili uzlaşması kaydedildi. [İnceleme notu](team/SYNC.md); nihai bilimsel profil hâlâ açık.

- **Earthdata metadata erişimi doğrulandı:** Kullanıcının yerel terminalde gizli token ile çalıştırdığı kontrol HTTP 200 verdi. Dört maske değişkeni, Float32/birim/boyut sırası ve dolgu metaverisi okundu; XML hash'i raporla eşleşti. Token okunmadı/kaydedilmedi. [Gerçek kanıt](evidence/EARTHDATA_METADATA.md). Bu ilk metadata kontrolünden sonra sayısal A/B fraksiyon/koordinat değerleri de alındı; iki aday ağırlık önizlemesi de sonraki gerçek veri akışında hesaplandı, bilimsel politika kabulü yok.

- **Geliştirme dalında maske hazırlığı:** [MERRA-2 sabit fraksiyonları](research/SURFACE_MASK.md) aday kaynak olarak bulundu; güncel OPeNDAP metadata isteği oturumsuz 401 verdi. İlk hazırlıkta gerçek oranlar yoktu; 2026-10-18 alımı üstteki kanıtla doğrulandı. A/B için 56/55 hücrelik istek planları ve ayrı aday maske ağırlık önizlemesi hazır. 72 test geçti; 14 yeni test sentetik verilerle hesabı denetliyor. [Kapsam ve gerçek erişim kanıtı](evidence/SURFACE_MASK_CHECK.md). Mevcut gerçek T2M örnekleri maskesiz kaldı.
- [Ortak teknik deneme profili](planning/REGION_WORKFLOW.md) `t2m-technical-2024` 0.1.0 taslağı gerçek örneklerle dolduruldu. Bu, nihai ürün/alan/dönem/maske/istatistik seçimi değildir. M2 ayrı dalında teknik uygunluk onayı ve farklı profil kimliği önerdi; teknik kimlik ayrımı 2026-10-19 M2 kaydıyla uzlaştırıldı; bilimsel profil açık.

- **M2'nin 6° pencere için beklediği teknik destek main'de:** [parçalı T2M komutu](guide/T2M_TILED_WINDOW.md) iki gerçek isteği birleştirdi; 5 tekrar çıkarılıp 55 hücre/12 ay hesaplandı. B aday sınırı değişmedi. Yeni çıktı profili 0.2.0; eski 0.1.0 örnekler çalışıyor, bilimsel alan yöntemi değişmedi. `cdcc6bd` main birleştirmesinde 58 testlik Ubuntu CI ve Pages yayını başarılı; canlı kılavuz HTTP 200. [Kanıt](evidence/T2M_TILING.md). Sonraki geliştirme ayrı M1 dalında sürer.

- M2'nin [B geometri/API katkısı](research/regions/REGION_B_PROFILE.md) `4ad9448` ile main'e geldi ve yerel kopyaya çakışmasız alındı. M2 başlangıç/üstlenme kaydı artık var: [M2 notu](team/members/M2.md), [H-M1-002 yanıtı](team/HANDOFFS.md). M1 çalışması `codex/m1-modules-region-a` dalında devam ediyor: [ADR-007](decisions/ADR-007-FEATURE-BRANCHES.md). Geliştirme dalı push'u canlı paneli güncellemez; Pages main'e birleştirme sonrası yayımlanır.

- [Modül sistemi](architecture/MODULE_SYSTEM.md), [sistem haritası](architecture/SYSTEM_MAP.md), [ortak sonuç taslağı](architecture/DATA_AND_FLOWS.md), [dar pilot planı](planning/PILOT.md) ve [web deneyimi](product/index.md) güncellendi. `analysis/` içinde ilk nokta adaptörüne ayrı türle maskesiz aday dikdörtgen hesabı eklendi: gerçek bölgesel API, kenar hücrelerini içeren istek, alan kesişimi/ağırlıklar, eksik veri kuralı ve çevrim dışı yeniden hesaplama. Yerel grafiğe kayıtlı T2M/fraksiyon işlemleri de bağlandı; bilimsel A/B karşılaştırması henüz yok. [Alan kılavuzu](guide/T2M_WINDOW.md), [gerçek alan kanıtı](evidence/T2M_WINDOW_PROBE.md), [ilk nokta kılavuzu](guide/T2M_ADAPTER.md), [teknik seçim](decisions/ADR-006-T2M-POINT-ADAPTER.md).
- Yönetim portalı **[GitHub Pages'te açık](https://sq0eezy.github.io/expedition-73/)**. Yayın işi başarılı; başlangıç sayfası ve okuma kataloğu HTTP 200 ile doğrulandı. [Yayın kaydı](evidence/PAGES_SETUP.md), [kullanım](guide/WEB_PORTAL.md).
- [İki kişilik ekip alanı](team/index.md), üye notları, fikir/devir kayıtları ve [iş panosu](planning/WORK_BOARD.md) mevcut. M1 modüller ve A’yı üstlendi; B’yi M2’ye atadı: [ADR-005](decisions/ADR-005-TEAM-OWNERSHIP.md). M2 daha sonra B'yi üstlenip R-B01/02 çıktısını paylaştı; adayların kesin seçimini yaptığı varsayılmadı. [A görevleri](planning/REGION_A.md), [B görevleri](planning/REGION_B.md) ve [ortak profil](planning/REGION_WORKFLOW.md) hazır.
- [İki aday alan](research/REGION_CANDIDATES.md) için NASA CMR metaverisi sorgulandı. Katalog eşleşmesi gerçek piksel, kalite veya analiz doğrulaması değildir. Türkiye yalnızca örnekti.
- M2 macOS/Python 3.14 ortamında testleri geçirdiğini kendi [üye notunda](team/members/M2.md) bildirdi; bu oturum Mac'te çalışmadı. Yerel geliştirme için [Mac kılavuzu](guide/MACOS_SETUP.md) var. Webden okumak için kurulum/pull gerekmez. Yerel kaynaklarla çalışan kişinin/yapay zekânın güncel kaydı alması gerekir.

## Açık kalanlar

Kesin iki bölge/sınır, ürün/sürüm/erişim yolu, dönem, istatistik yöntemi, teknoloji yığını, genel web arayüzü sorumlusu, teslim tarihi ve nihai uygulama adı seçilmedi. MERRA-2 aylık T2M, Colorado Platosu çevresi/Kuzey Alaska ve 2001–2024 adaydır; seçilmiş sayılmaz.

NASA POWER API’den A aday dikdörtgeniyle kesişen 56 hücre için 2024'ün 12 ayı alındı. Maskesiz alan ağırlıklı seri ve bağımsız Ocak hesabı doğrulandı; küçük ham yanıt saklandı. Bu sonuç kabul edilmiş coğrafi bölgenin veya yalnızca kara alanının sonucu değildir. Hücre kenarları orta noktadan kuruluyor; küresel alan yaklaşımı açıkça kayıtlı. Kara/su maskesi, kesin sınır, B profili, uzun dönem/trend/p-değeri, genel çok göstergeli entegrasyon ve sunulacak web uygulaması açık. Kayıtlı T2M/fraksiyon işlemleri arasındaki ilk gerçek tüketim artık çalışıyor. Portalın yayında olması bilimsel ürünün tamamlandığını göstermez.

## Sıradaki küçük adım

İlk sonuç ekranı gerçek 2024 kayıtlarıyla yerelde çalışıyor; sırada ekipçe ay/pencere/maske etkileşimini ve gösterilen kapsam açıklamalarını incelemek, yüzey hedefi/ortak profil kararlarını netleştirmek var. [Çalıştırma ve ekran kapsamı](product/RESULTS_PREVIEW.md). Harita, uzun dönem/trend, ikinci gösterge ve nihai barındırma/yığın hâlâ açık. AREA bulunmayan granülden alan karşılaştırması üretilecek sayılmaz. Önceki 134 testlik akış main/canlı portalda; 162 testlik güncel yerel dilimler henüz paylaşılmadı. Yeni geliştirme ayrı M1 dalında sürer.
