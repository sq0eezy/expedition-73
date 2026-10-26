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
- **Durum:** `cdcc6bd` ile main'de paylaşıldı; Ubuntu testleri ve canlı panel yayını başarılı. M2 (`791e07c`) Mac doğrulama yanıtını kaydetti ve 2026-10-18'de M1 tarafından okundu: [kanıt](../evidence/T2M_TILING.md).
- **Teslim:** `fetch-power-tiled-window` / `validate-tiled-window`, bölgeden bağımsız yapılandırma, 0.2.0 çıktı ve iki gerçek B ham yanıtı. B'nin mevcut 6° arama penceresi küçülmedi; ortak 5 hücre bir kez sayıldı. [Mac komutları](../guide/T2M_TILED_WINDOW.md), [kontroller ve sınırlar](../evidence/T2M_TILING.md).
- **M2'nin yapabileceği:** Güncel main'i kendi değişikliklerini koruyarak al; kendi çalışma dalında kayıtlı `examples/b-window-2024` örneğini çevrim dışı doğrula. R-B03/04 kapsamında alan/maske/uygunluk incelemesini sürdür; yeni API çağrısı gerekirse yeni çıktı klasörü kullan.
- **Sınır:** Kesin alan/maske seçimi ve bilimsel A/B uygunluk onayı yok; B adına yeni yorum veya başlangıç üretilmedi. Dış mesaj/bildirim gönderilmedi.
- **Yanıt:** M2 (sq0eezy), 2026-10-18: H-M1-005 teslimi incelendi. macOS/Python 3.14 üzerinde `validate-tiled-window examples/b-window-2024` çalıştırıldı ve `replay_passed` alındı. 2 parçanın birleştirilmesi, 5 mükerrer hücrenin ayıklanması ve 55 tekil hücre üzerinden 12/12 ay eksiksiz alan ortalaması (-8,73 °C) doğrulandı. 58 birim testin tamamı geçti. R-B03 teknik veri profili uygunluğu onaylandı. Kesin sınır/kara-su maskesi ve uzun dönem serisi (2001–2024) açık bırakıldı. Dış mesaj gönderilmedi.

**M2 yanıtı, 2026-10-18'de okundu:** [791e07c](https://github.com/sq0eezy/expedition-73/commit/791e07cba899e11065f9bb9846dfe44204eca84c) Mac/Python 3.14 üzerinde `replay_passed`, 58 test, 55 hücre/12 ay ve teknik uygunluk onayı bildiriyor. Bu beyan M2'nin kaydıdır; bu oturumda Mac testi yapılmadı. Profil sürümü ve yıllık özet yöntemi için [M1 incelemesi](SYNC.md) eklendi; bilimsel kabul olarak genişletilmedi.

## H-M1-006 · Maske adayı ve teknik profil taslağı

- **Gönderen → alıcı:** M1 → M2; ortak modül görevine ait panel içi araştırma/taslak kaydı.
- **Tarih:** 2026-10-17.
- **Durum:** Yanıtlandı · Teknik doğrulama tamamlandı, bilimsel maske/sınır seçimi açık. [Yayın kanıtı](../evidence/SURFACE_RELEASE.md).
- **Teslim:** [Maske adayı/erişim](../research/SURFACE_MASK.md), [sentetik testlerin sınırı](../evidence/SURFACE_MASK_CHECK.md), `t2m-technical-2024` 0.1.0 [aday profil](../planning/REGION_WORKFLOW.md). A/B için beklenen maske hücreleri ve indeksleri çıkarıldı; gerçek veri erişimi 401, maske alınmadı.
- **İncelenecek:** Kara buzu dahil etme tanımı, tam hücre oranını kırpılmış sınıra uygulama yaklaşımı, kesin sınır ve ortak profil. Sessizlik kabul değildir; M2 adına görüş eklenmedi.
- **Ayrım:** M2 main'deki önceki parçalı destekle çalışabilir. Bu yeni kayıt maskeli B analizi veya NASA veri doğrulaması değildir. Dış mesaj/bildirim gönderilmedi.

**Erişim adımı güncellemesi · 2026-10-17:** Kayıt adımı tamamlandı bilgisi geldi; programatik erişim henüz doğrulanmadı. [Yerel metadata kontrolü](../guide/EARTHDATA_ACCESS.md) hazır; kullanıcı token'ı kendi terminalinde gizli girer. Başarılı gerçek yanıt gelene kadar fraksiyon veya maske doğrulaması yapılmış sayılmaz.

**Gerçek kontrol sonucu · 2026-10-17:** Kullanıcı komutu çalıştırdı; HTTP 200 ve dört maske değişkeni/boyut metaverisi [doğrulandı](../evidence/EARTHDATA_METADATA.md). Önceki erişim bekleniyor notu tarihsel kaldı. Token okunmadı; fraksiyon/koordinat değerleri henüz alınmadı. M2 adına yeni çalışma beyanı yok.

**2026-10-18 uygulama güncellemesi:** [Küçük fraksiyon komutu ve NetCDF dönüşümü](../guide/SURFACE_SUBSET.md) hazır; yapay A/B yanıtlarında kayıt/tekrar ve 13 dönüşüm testi geçti. Gerçek kaynak oranları için kullanıcı terminalinde yeni gizli token girişi gerekiyor. Kara/buz politikası seçilmedi; M2 dalının profil önerisi ayrıca incelendi.

**2026-10-18 erişim güncellemesi:** M1 yeni çalıştırmada metadata aşamasında 403 bildirdi ve `.env` kaydı istedi. [Yerel --save-token desteği](../guide/EARTHDATA_ACCESS.md) eklendi; eski “her istekte yeniden gizli giriş gerekir” ifadesi yeni kayıt tercihi için geçerli değil. Gerçek token bu oturumda okunmadı veya kaydedilmedi; kayıt kullanıcı komutuyla yapılacak. Erişim/fraksiyon doğrulaması hâlâ açık; M2 adına yeni beyan yok.

**2026-10-18 hedefli kontrol sonucu:** Kullanıcı Hyrax onay ekranını paylaştı. Kayıtlı token ile Hyrax örnek metadata 200, MERRA-2 ürün metadata 403 verdi. GES DISC/S3 upstream erişim işaretleri görüldü; [NASA GESDISC DATA ARCHIVE izni](../guide/EARTHDATA_ACCESS.md) sıradaki kontrol. `.env` kaydı tamamlandı; token tekrar girilmeyecek. Arşiv izninin verildiği veya 403’ün çözüldüğü varsayılmadı.

**2026-10-18 gerçek alım doğrulandı:** M1 GES DISC onayını verip komutu çalıştırdığını bildirdi. Yereldeki gerçek A/B NetCDF dosyaları, kaynak hash ve 56/55 hücrelik fraksiyon dönüşümleri iki çevrim dışı tekrar kontrolünden geçti. [Kanıt](../evidence/SURFACE_SUBSET_CHECK.md). Erişim engeli bu çalıştırmada aşıldı; bilimsel kara/buz politikası, POWER uygunluğu ve maskeli seri incelemesi açık. Özel artifacts/.env Git dışında; M2’nin bu yeni fraksiyon örneğini incelediği varsayılmadı.

- **Yanıt:** M2 (sq0eezy), 2026-10-19: macOS/Python 3.14 üzerinde `plan-surface-mask` ve `fetch_surface_fractions.py --replay examples/b-surface-fractions` çalıştırılarak 55 hücrelik Bölge B fraksiyon alt kümesi (boylam indeksleri `38..48`, enlem indeksleri `316..320`, 5 hücrede pozitif `FROCEAN`) çevrim dışı doğrulandı. Ortak teknik deneme profili için `t2m-technical-2024` (`0.1.0`) kimliği ve şema (`0.2.0`) / bilimsel alan yöntemi (`0.1.0`) ayrımı kabul edildi. Kara/buz politikası ve kırpılmış hücre yaklaşımı duyarlılık karşılaştırması için uygun bulundu; nihai bilimsel profil seçimi açık bırakıldı. Dış mesaj gönderilmedi.

## H-M1-007 · Yerel A/B/C yürütme denemesi

- **Gönderen → alıcı:** M1 → M2; ortak modül görevi kapsamında panel içi teknik teslim. Dış mesaj gönderilmedi.
- **Tarih:** 2026-10-18.
- **Durum:** Yanıtlandı · macOS üzerinde doğrulandı. [Yayın kanıtı](../evidence/SURFACE_RELEASE.md).
- **Çıktı:** [demo-workflow komutu, kayıtlı yapay örnek ve testler](../evidence/WORKFLOW_ENGINE.md); [MOD-06](../planning/WORK_BOARD.md). A ortak kaynağı bir kez hesaplanır; C, B ile aynı A kimliğini alır. Yeni A isteği için eski sonuçlar güncel değil saptanır; eski A/yeni B karışımı, hata ve döngü kontrol edilir.
- **Sınır:** Bu, NASA T2M/fraksiyon modüllerini henüz çalıştırmayan teknik denemedir. Tip/sürüm/birim etiket kontrolü gerçek bilimsel uygunluk yerine geçmez. Kalıcı cache, otomatik kaynak izleme ve web görünümü yok. M2’nin Mac’te bu yeni komutu çalıştırdığı varsayılmadı.
- **Yanıt:** M2 (sq0eezy), 2026-10-19: macOS/Python 3.14 üzerinde `demo-workflow` ve ilgili 20 birim testi çalıştırılarak ortak girdi kimliği, stale tespiti ve hata izolasyonu doğrulandı. Dış mesaj gönderilmedi.

## H-M1-008 · Gerçek kayıtlı veriyle aday ağırlık akışı

- **Gönderen → alıcı:** M1 → M2; panel içi ortak modül teslimi, dış mesaj gönderilmedi.
- **Tarih:** 2026-10-18.
- **Durum:** Yanıtlandı · macOS üzerinde 134 test ve Bölge B akışı doğrulandı; bilimsel maske seçimi açık. [Yayın kanıtı](../evidence/SURFACE_RELEASE.md).
- **Teslim:** [run-surface-workflow, kaynak örnekleri ve hata kontrolleri](../evidence/SURFACE_WORKFLOW.md). A/B'nin mevcut gerçek T2M kayıtları ve küçük gerçek NASA fraksiyonları ile iki aday politika 12 ay hesaplandı. Paylaşılabilir örnek klasörlerinde credential değeri yok; özel .env Git dışında kalır.
- **İncelenecek:** Kara buzu kapsamı, etkili alanın anlamı, tam hücre fraksiyonunun kırpılmış parçaya uygulanması ve bilimsel grid uygunluğu. B'de en büyük aylık FRLAND-maskesiz farkı yaklaşık 0,0351 °C; farkın küçük olması politika kabulü değildir.
- **Sınır:** Uzun dönem/eğilim/son web uygulaması yok. M2'nin Mac'te bu yeni akışı çalıştırdığı veya politikayı onayladığı varsayılmadı.
- **Yanıt:** M2 (sq0eezy), 2026-10-19: macOS/Python 3.14 (`netCDF4 1.7.2`, `numpy 2.5.4`) üzerinde 134 birim testin tamamı ve `run-surface-workflow --window-run examples/b-window-2024 --fraction-run examples/b-surface-fractions` komutu çalıştırıldı (`5/5 düğüm completed`, `12/12 ay`). Bölge B'de `FRLAND` etkin alanı 52.183,622 km² (%98,15), `FRLAND + FRLANDICE` etkin alanı 52.192,891 km² (%98,16); en büyük aylık `|FRLAND - maskesiz|` farkı 0,03510533 °C (Kasım 2024) ve `|FRLAND+ICE - FRLAND|` farkı 0,00057698 °C (Ekim 2024) olarak kayıtlı `b-surface-sensitivity.json` ile birebir eşleşti. Sonuçlar [B fişine](../research/regions/REGION_B_PROFILE.md) işlendi; nihai bilimsel maske/sınır seçimi ve uzun dönem analizi açık bırakıldı. Dış mesaj gönderilmedi.

**2026-10-20 paylaşım güncellemesi:** Aşağıdaki H-M1-009/010/011/012/013 kaynakları artık [GitHub M1 dalında](SYNC.md) bulunur (`6b4ab12`). Kayıtlardaki “yerel/paylaşım bekliyor” ifadeleri ilk hazırlanma anına aittir; güncel durum **dalda paylaşıldı, M2 incelemesi bekliyor**. Main/Pages yayını veya M2 onayı yok.

## H-M1-009 · Kesilmiş hücrelerde alan kapsamını inceleme

- **Gönderen → alıcı:** M1 → M2; mevcut MOD-05/R-A04 denetiminin panel içi inceleme kaydı; dış mesaj gönderilmedi.
- **Tarih:** 2026-10-19.
- **Durum:** Yerel M1 dalında, paylaşım/M2 incelemesi bekliyor; M2'nin gördüğü varsayılmaz.
- **Teslim:** [Koşullu alan sınırları ve yüzey hedefi soruları](../research/SURFACE_SUPPORT.md), [gerçek A/B kanıtı/komutu](../evidence/SURFACE_SUPPORT_CHECK.md). Önceki 134 testlik yayına 12 test eklendi; 146 yerel test başarılı.
- **İncelenecek:** B sınır parçalarında tam hücre oranını homojen dağıtmanın uygunluğu, AREA/alan tanımı ve kara/buz hedefi. B için bu denetim ortak modülün kaynak uygunluğunu sınar; B görevi veya M2 kabulü yerine geçmez.
- **Sınır:** Koşullu alan aralığı fiziksel güven aralığı/sıcaklık hatası değildir. Yeni API, kesin maske/profil veya uzun dönem sonucu yok. Yeni Mac/Ubuntu koşusu ve canlı yayın yapılmadı.

## H-M1-010 · Seçili granülde AREA bulunmaması

- **Gönderen → alıcı:** M1 → M2; mevcut MOD-05/R-A04 kapsamında panel içi kaynak incelemesi; dış mesaj yok.
- **Tarih:** 2026-10-19.
- **Durum:** Yerel M1 dalında, paylaşım/inceleme bekliyor; M2 görmüş sayılmaz.
- **Teslim:** [Canlı DMR ve offline komut](../evidence/SOURCE_AREA_CHECK.md), [kaynak alanı/iki belge farkı](../research/SOURCE_AREA.md). Yedi yeni testle toplam 153 yerel test geçti.
- **İncelenecek:** Kaynak alanıyla doğrudan doğrulama yapıldığı varsayılmadan mevcut geometrik yöntemin ve hedef yüzeyin nasıl açıklanacağı. Başka AREA ürünü gerekiyorsa ayrı kaynak/grid uygunluğu gerekir; otomatik ürün değişimi yok.
- **Sınır:** Metadata HTTP 200, AREA değerinin veya bilimsel yöntemin doğrulandığı anlamına gelmez. Yeni maske/alan/dönem veya M2 kabulü üretilmedi. İlk sonuç ekranı taslağı öneri; final web teknolojisi/sorumlusu seçilmedi.

## H-M1-011 · Kayıtlı T2M ilk web ekranı

- **Gönderen → alıcı:** M1 → M2; kullanıcının devam talebi kapsamındaki teknik ekranın panel içi teslimi; dış mesaj gönderilmedi.
- **Tarih:** 2026-10-19.
- **Durum:** Yerel M1 dalında; paylaşım ve üye kullanım incelemesi bekliyor.
- **Teslim:** [Ekran/kullanım](../product/RESULTS_PREVIEW.md), [162 test ve on gerçek Chrome senaryosu](../evidence/RESULTS_PREVIEW_CHECK.md). Mac'te kurulu analysis ortamıyla önce `analysis/.venv/bin/python analysis/scripts/build_web_preview.py`, sonra `python3 web/serve.py`; adres 127.0.0.1:8873, kapatma Ctrl+C. Bu komutların Mac'te çalıştırıldığı varsayılmaz.
- **İncelenecek:** Pencere/ay/maske seçimi, veri kaynağı ve koşullu kapsamın anlaşılması; B değerlerinin kaydedilmiş sonuçla uyuşması. Bölge listesine yeni uygun kayıt eklenebilir; yeni bilimsel gösterge desteği yok.
- **Sınır:** Arayüz, yöntem veya maske kabulü değildir. M2'nin gördüğü/başladığı veya nihai web görevini üstlendiği varsayılmaz; main/Pages yayını bu teslimde yapılmadı.

## H-M1-012 · Hücre ve etkin alan incelemesi

- **Gönderen → alıcı:** M1 → M2; U-02 kapsamında panel içi teknik teslim; dış mesaj yok.
- **Tarih:** 2026-10-20.
- **Durum:** Yerel M1 dalında, paylaşım ve kullanım incelemesi bekliyor.
- **Teslim:** [Ürün ve Mac komutları](../product/RESULTS_PREVIEW.md), [164 analiz testi ve 18 Chrome senaryosu](../evidence/SPATIAL_PREVIEW_CHECK.md). Önce builder tekrar çalıştırılır; web aktarımı 0.2.0, kaynak şemaları/yöntem aynı.
- **İncelenecek:** B'nin 55 hücresi, ay değişimi ve seçili hücrenin grid T2M/fraksiyon/etkin alanı; sınırda kesilen hücrelere homojen fraksiyon uygulamasının açıklığı. Bilimsel maske seçimi bu ekranla yapılmış sayılmaz.
- **Sınır:** M2'nin 134 testlik macOS teyidi alındı; yeni hücre ekranını gördüğü/kabul ettiği varsayılmaz. Main/Pages yayını yapılmadı.

## H-M1-013 · Aday ağırlıkları yan yana inceleme

- **Gönderen → alıcı:** M1 → M2; U-02 panel içi teknik teslim; dış mesaj yok.
- **Tarih:** 2026-10-20.
- **Durum:** Yerel M1 dalında; paylaşım/kullanım incelemesi bekliyor.
- **Teslim:** [Ürün/kullanım](../product/RESULTS_PREVIEW.md), [gerçek kıyaslama ve testler](../evidence/POLICY_COMPARISON_CHECK.md). Mac'te builder yeniden çalıştırılır, ardından `python3 web/serve.py`; `comparison.mjs` dahil beş genel dosya birlikte üretilir.
- **İncelenecek:** Aynı ayın üç sonucu; kara−maskesiz ve kara+buz−kara farklarının ay/maksimum ve geçerli çift sayıları. Bunlar iklim etkisi veya toplam belirsizlik değildir; hedef yüzeyin seçimi ayrı kalır.
- **Sınır:** Kara/buz politikası, kesin sınır ve dönem kabul edilmedi. Yeni dilim M2 tarafından görülmüş/çalıştırılmış sayılmaz; Pages'e yayımlanmadı.

## H-M1-014 · İsteğe bağlı geliştirme ve demo paketi

- **Gönderen → alıcı:** M1 → M2; D-02 panel içi teknik teslim; dış mesaj yok.
- **Tarih:** 2026-10-21.
- **Durum:** Yerel M1 dalında; paylaşım ve gerçek Mac kullanım incelemesi bekliyor.
- **Teslim:** [Tek komut Docker/native kılavuzu](../guide/DEV_PACKAGE.md), [gerçek kontrol/ortam sınırları](../evidence/DEV_PACKAGE_CHECK.md). Mac'te mevcut ortamla `sh scripts/start-preview.sh`; Docker Desktop açıksa `docker compose --env-file docker/compose.env up --build`. İkisi de kurulumdan sonra localhost 8873 sunar.
- **İncelenecek:** Kendi dalındaki değişiklikleri koruyarak güncel kaynak alındıktan sonra Mac başlatıcısı/Docker seçeneği, kontrol komutu ve B kayıtlı sonuçları. Docker zorunlu değil; M2 tercihi varsayılmaz.
- **Sınır:** Linux ARM emülasyonu gerçek Mac kullanımı değildir. Yeni CI tanımı uzak başarı kanıtı veya bilimsel maske/sınır/dönem kabulü sayılmaz. Yeni kod main/Pages'e gönderilmedi.

## Bir kayıt için gerekenler

**2026-10-18 mimari açıklık:** M1 çok girdili modül bağımlılığına hazır olup olmadığımızı sordu. [A→B, A+B→C örneği](../architecture/MODULE_SYSTEM.md), C'nin B ile aynı A çıktısını kullanması koşuluyla ayrıntılandırıldı. [MOD-06](../planning/WORK_BOARD.md) önerilen teknik deneme; motor henüz yok. M2 adına inceleme veya onay beyanı üretilmedi.

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

## H-M1-015 · Gerçek akış ekranı ve sözleşme ayrıntıları

- **Gönderen → alıcı:** M1 → M2; U-02/MOD-06/D-02 için panel içi kayıt, dış mesaj yok.
- **Tarih:** 2026-10-21.
- **Durum:** Yerel M1 dalında; paylaşım ve M2 incelemesi bekliyor.
- **Teslim:** [Gerçek akış kontrolü](../evidence/WORKFLOW_TRACE_CHECK.md), [ürün sınırları](../product/RESULTS_PREVIEW.md), [native/Docker açma komutları](../guide/DEV_PACKAGE.md).
- **İncelenecek:** Kaynaklar paylaşıldıktan sonra Mac'te `sh scripts/start-preview.sh`; B akışında beş adım/sekiz bağ, LandIce/Sensitivity girdileri, telefon/klavye seçimi. Kimlik iş tanımına aittir; bilimsel onay/çıktı artifact hash'i değildir. Yeni web 0.3.0/manifest 0.2.0, eski ZIP doğrulaması korunur.
- **Kanıt/sınır:** 180 Windows/Linux AMD64 analiz testi, gerçek A/B, 13 JS, 30 Chrome senaryosu geçti; yeni Mac/ARM64/uzak CI yok. Bilimsel maske/sınır/dönem ve M2 kabulü açık; yanıt gelmeden accepted yazılmaz.

## H-M1-016 · Pencereler arası betimsel fark ve eşleşme koşulları

- **Gönderen → alıcı:** M1 → M2; U-02 panel içi kayıt, dış mesaj yok.
- **Tarih:** 2026-10-22.
- **Durum:** Yerel M1 dalında; paylaşım ve M2 incelemesi bekliyor.
- **Teslim:** [Çift/yön/ay/yüzey grafiği ve gerçek kanıt](../evidence/REGION_COMPARISON_CHECK.md), [ürün sınırları](../product/RESULTS_PREVIEW.md). Kaynaklar paylaşıldıktan sonra Mac'te `sh scripts/start-preview.sh` ile açılır.
- **İncelenecek:** A−B/B−A yönü, 12 aylık fark tablosu ve teknik koşullar. Maskesiz/kara/kara+buz sonuçları aynı coğrafyanın alternatif ağırlıklarıdır. Pencere farkı ısınma etkisi/trend/önemlilik değildir. Bilimsel yüzey/sınır/uzun dönem uzlaşması hâlâ gerekir.
- **Kanıt/sınır:** 180 Windows analiz, gerçek A/B tekrarları, 22 JS ve 36 Chrome senaryosu; yeni Mac/Docker/uzak CI yok. Web 0.3.0, altı dosya, manifest 0.2.0 değişmedi. Yanıt gelmeden M2 kabulü yazılmaz.

## H-M1-017 · Kaynak kimlikli karşılaştırma raporu

- **Gönderen → alıcı:** M1 → M2; U-02/D-02 panel içi kayıt, dış mesaj yok.
- **Tarih/durum:** 2026-10-22; yerel M1 dalında, paylaşım/M2 incelemesi bekler.
- **Teslim:** [Kullanım/sözleşme](../guide/COMPARISON_REVIEW.md), [gerçek kontroller](../evidence/COMPARISON_REVIEW_CHECK.md).
- **İncelenecek:** Kaynak paylaşıldıktan sonra Mac'te `sh scripts/start-preview.sh`, aynı veriyle raporu indir/aç; yön/ay/yüzey/gizli pencerelerin açılmasını dene. Hatalı/farklı kaynakta seçimler korunmalı. Dosya yalnız tarayıcıda işlenir, uygulama kendisi iletmez.
- **Sınır:** Windows 180 analiz/gerçek A-B, 30 JS, 42 Chrome senaryosu; yeni Mac/Docker/uzak CI yok. SHA-256 bilimsel/yazar onayı değil. Bilimsel profil/M2 kabulü/yayın yok; yanıt olmadan accepted yazılmaz.

## H-M1-018 · 2023–2024 kaynak birleştirme ve yıl seçimi

- **Gönderen → alıcı:** M1 → M2; T-01/U-02 panel içi kayıt, dış mesaj yok.
- **Tarih/durum:** 2026-10-22; yerel M1 dalında, paylaşım/M2 incelemesi bekler.
- **Teslim:** [Komutlar/sözleşmeler](../guide/T2M_HISTORY.md), [gerçek kanıt](../evidence/T2M_HISTORY_CHECK.md). Kaynaklar paylaşıldıktan sonra Mac'te `sh scripts/start-preview.sh`; 2023/2024 seç, B tarih/hücre/politika ve yıllar arası rapor açmayı kontrol et. analysis içinde `.venv/bin/python -m expedition73 validate-window-history examples/b-history-2023-2024`.
- **Sınır:** Windows 197 analiz/30 JS/49 Chrome; Docker motoru hazır olmadı, yeni Linux/Mac/CI sonucu yok. 2024 byte'ları korundu; 2001–2024 gerçek veri/trend ve nihai maske/sınır/profil seçilmedi. Reusable B teknik örneği M2'nin R-B05'e başladığı/kabul ettiği anlamına gelmez.

## H-M1-019 · 2001–2024 gerçek kaynak ve 24 yıllık seçim

- **Gönderen → alıcı:** M1 → M2; T-01/U-02 için panel içi kayıt, dış mesaj yok.
- **Tarih/durum:** 2026-10-24; yerel M1 dalında, paylaşım/M2 incelemesi bekler.
- **Teslim:** [Kullanım/yorum sınırı](../guide/T2M_LONG_PERIOD.md), [gerçek erişim/kontrol](../evidence/T2M_LONG_PERIOD_CHECK.md). Kaynak paylaşılınca Mac'te `sh scripts/start-preview.sh`; 2001/2012/2024 seç, B tarih/hücre/politikayı ve raporla yıl açılmasını dene. analysis içinde `.venv/bin/python -m expedition73 validate-window-history examples/b-history-2001-2024`.
- **Sınır:** İki pencere 288'er ay; eski kaynak/rapor kimlikleri korunur. Bu teknik erişim R-B05 başlangıcı/analiz tamamlanması, M2 kabulü veya bilimsel dönem/maske/eğilim kararı değildir. Yeni Mac/Linux/Docker/CI/yayın yok. Yanıt bekleniyor.

## H-M1-020 · Kayıtlı aylar için uzun dönem görünümü

- **Gönderen → alıcı:** M1 → M2; T-02/U-02 için panel içi kayıt, dış mesaj yok.
- **Tarih/durum:** 2026-10-26; yerel M1 dalında, paylaşım/M2 incelemesi bekler.
- **Teslim:** [Kullanım](../guide/T2M_TIMELINE.md), [gerçek kontrol](../evidence/TIMELINE_PREVIEW_CHECK.md). Kaynak paylaşılınca Mac'te `sh scripts/start-preview.sh`; uzun dönem ay seçicisini, yıl sınırını, pencere/yüzey seçimlerini, B hücre/kaynak ayrıntılarını ve eski raporu açınca işaretçinin aynı aya gelmesini incele.
- **Sınır:** 201 Windows analiz/gerçek A-B, 37 JS, 65 Chrome; yeni Mac/Linux/Docker/CI yok. Kaynak JSON/sözleşmeler aynı. Yeni istatistik/maske/dönem/eğilim kabulü veya R-A05/R-B05 tamamlanması değil. Yanıt gelmeden M2 kabulü yazılmaz.

## H-M1-021 · Yıllık özetin iki hedefi

- **Gönderen → alıcı:** M1 → M2; T-03 için panel içi kayıt, dış mesaj yok.
- **Tarih/durum:** 2026-10-26; yerel M1 dalında, paylaşım/M2 incelemesi bekler.
- **Teslim:** [Yöntem ve kaynak araştırması](../research/TEMPORAL_AGGREGATION.md), [CLI](../guide/T2M_ANNUAL_WEIGHTING.md), [gerçek kayıt/testler](../evidence/ANNUAL_WEIGHTING_CHECK.md). Kaynaklar paylaşıldıktan sonra Mac'te analysis içinde `.venv/bin/python -X utf8 -m expedition73 validate-annual-weighting --run examples/b-history-2001-2024 --input examples/b-annual-weighting-audit.json`.
- **İncelenecek:** Hedef eşit ay özeti mi, takvim süresini temsil eden özet mi? Kaynak yıllık değere yakınlık bağımsız doğruluk değildir. Nihai yüzey/sınır/dönem ve eksiklik kuralıyla birlikte tartışılmalı.
- **Sınır:** 24'er tam maskesiz yıl; yeni yöntem seçimi/M2 kabulü/R-B05 başlangıcı veya eğilim yok. Genel web/motor entegrasyonu ve yeni Mac/Linux/CI sonucu yok. Yanıt bekleniyor.

## H-M1-022 · Yıllık adayların webde incelenmesi

- **Gönderen → alıcı:** M1 → M2; T-04/U-02 için panel içi kayıt, dış mesaj yok.
- **Tarih/durum:** 2026-10-26; testli M1 dilimi. GitHub gönderim sonucu [SYNC](SYNC.md) kaydından izlenir; M2 incelemesi/kabulü bekler.
- **Teslim:** [Web kullanımı](../guide/ANNUAL_WEB.md), [222 Windows/43 JS/76 Chrome kanıtı](../evidence/ANNUAL_WEB_CHECK.md). Kaynak dalı alındıktan sonra Mac'te `sh scripts/start-preview.sh`; maskesizde A/B yıllık adaylar, tablo/yıl düğmesi, API yıllık referansı ve kara/buz kapsam kapanmasını incele. Yeni yedi dosya/manifest 0.4.0 birlikte üretilir.
- **Sınır:** Bilimsel profil/eğilim/M2 kabulü yok; aynı kaynak API kıyası bağımsız ölçüm değildir. Aylık akış grafiği yıllık modülü içermiyor. Main/Pages yayını ve gerçek Mac/Docker koşusu bu teslim sayılmaz.

## H-M1-023 · Yıllık hesabın gerçek bağımlılık bağlantısı

- **Gönderen → alıcı:** M1 → M2; T-05 için panel içi kayıt, dış mesaj yok.
- **Tarih/durum:** 2026-10-26; teknik inceleme bekler. Son test ve dal paylaşımı [kanıt](../evidence/ANNUAL_WORKFLOW_CHECK.md) ve [SYNC](SYNC.md) içinde ayrıdır.
- **Teslim:** [İki adım/sözleşme ve Windows/Mac komutları](../guide/ANNUAL_WORKFLOW.md). Güncel kaynak kendi işin korunarak alındıktan sonra Mac'te analysis içinde `.venv/bin/python -X utf8 -m expedition73 run-annual-workflow --run examples/b-history-2001-2024 --output-dir artifacts/b-annual-workflow-new`.
- **İncelenecek:** History/AnnualWeighting completed; yıllık rapor kayıtlı B adayıyla aynı; workflow.json'da yıllık artifact tam History artifact kimliğini tüketiyor. trace.json iki adımlı genel projeksiyondur; webdeki aylık grafiğe kendiliğinden eklenmez. Aynı hedefte tekrar komut önceki dosyaları korumalı.
- **Sınır:** İki hedef hâlâ aday; yeni bilimsel gösterge/maske/dönem/eğilim veya R-B05 başlangıcı değildir. M2 adına yeni kabul/koşu yazılmaz. Yanıt bekleniyor.
