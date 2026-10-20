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
