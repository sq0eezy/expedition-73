# İş panosu

**2026-10-19 · İlk yerel sonuç ekranı:** U-02 teknik dilimi, kullanıcının ilk ekran önerisi sonrası devam talebiyle uygulandı; [gerçek kayıtlar ve tarayıcı doğrulaması](../evidence/RESULTS_PREVIEW_CHECK.md). U-01 genel deneyim/nihai teknoloji seçimi bundan ayrı ve açık. Mevcut bilimsel MOD-05/R-A04/R-B04 durumları arayüz başarısıyla tamamlanmış sayılmaz.

**2026-10-19 · MOD-05/R-A04 kaynak kontrolü:** [Canlı tam DMR kontrolü](../evidence/SOURCE_AREA_CHECK.md) seçili granülde AREA bulunmadığını doğruladı; sayısal karşılaştırma yok. Yeni `check-source-area` ile yedi test eklendi, toplam 153 test başarılı. [Kaynak/alan varsayımları](../research/SOURCE_AREA.md) gözden geçirildi; MOD-05/R-A04 Validating kalır. U-01/teknoloji/sorumlu hâlâ açık; ilk sonuç ekranı yalnız sonraki dilim önerisidir.

**2026-10-19 · MOD-05/R-A04:** [Koşullu alan kapsamı denetimi](../evidence/SURFACE_SUPPORT_CHECK.md) yerel M1 dalında eklendi; 12 yeni testle 146 test başarılı. İki aday politikanın sınır hücreleri ve alan varsayımları [ayrı araştırmada](../research/SURFACE_SUPPORT.md). MOD-05/R-A04 Validating kalır: bilimsel alan ölçüsü/yüzey hedefi ve M2 incelemesi açık. Bu yeni dilim main/canlı panelde değil; B görevi tamamlandı veya M2 politikayı kabul etti sayılmaz.

Görevler eldeki kanıta göre güncellenir. **2026-10-16 iş bölümü:** M1 modüller + A, M2 B. M2 daha sonra kendi [notuyla](../team/members/M2.md) B üstlenmesini ve ilk çıktısını bildirdi; `4ad9448` katkısı 2026-10-17'de M1 tarafından alınıp 43 test ve örnek doğrulamalarıyla kontrol edildi. Sonraki B alt işlerine ayrıca başlanmış sayılmadı. M1 artık [ayrı dalda](../decisions/ADR-007-FEATURE-BRANCHES.md) çalışıyor. İnceleyenler planlanan kişilerdir; her aşama incelenmiş sayılmaz. Teslim tarihleri açık. Üye kimlikleri [ekip dizinindedir](../team/index.md). `Verified` portal işleri uygulamanın doğrulandığını göstermez.

| ID | İş | Durum | Sorumlu | Üstlenme | İnceleyen | Tamamlanma ölçütü / kanıt |
|---|---|---|---|---|---|---|
| P-01 | Portalı projeye uyarla | Verified | Önceki yapay zekâ oturumu | Tamamlandı | Üye incelemesi kaydı yok | [Portal doğrulaması](../evidence/PORTAL_SETUP.md) |
| P-02 | İlk konuşmayı özetle | Implemented | Önceki yapay zekâ oturumu | Tamamlandı | Üye incelemesi kaydı yok | [Bağlam](../PROJECT_CONTEXT.md), [fikirler](../discovery/IDEA_COMPARISON.md) |
| P-03 | İki kişilik ekip alanını hazırla | Verified | Bu yapay zekâ oturumu | Kullanıcı talebi | Üye incelemesi bekliyor | [Ekip alanı](../team/index.md), [teknik kontrol](../evidence/TEAM_SETUP.md) |
| S-01 | Yerel portalı uzak değişiklikleri koruyarak main'e gönder | Verified | Bu yapay zekâ oturumu | Kullanıcı talebi | Uzak commit eşleşmesi doğrulandı | [Aktarım kaydı](../evidence/GITHUB_SHARE.md); GitHub main'de paylaşıldı |
| S-02 | Main'i alıp kendi Mac bilgisayarında portalı kur | Proposed | M2 | Önerildi | Atanmadı | [Mac kurulumu](../guide/MACOS_SETUP.md); M2'nin kendi ortamında açılış sonucu |
| S-03 | Pull gerektirmeyen ortak web yayını hazırla | Verified | Bu yapay zekâ oturumu | Kullanıcı talebi | Başarılı yayın ve HTTP doğrulaması | [Pages kaydı](../evidence/PAGES_SETUP.md); portal açık |
| S-04 | Pages kaynağını GitHub Actions seç ve ilk yayını aç | Verified | Depo hesabı | Kullanıcı ayarı yaptığını bildirdi | Bu oturum: yayın/HTTP kontrolü | [Başarılı çalışma](../evidence/PAGES_SETUP.md), canlı site HTTP 200 |
| R-01 | İki adayı kısa listeye al | Proposed | M1: A; M2: B | Alt görevler aşağıda | Karşı üye (planlanan) | R-A01/R-B01 fişleri ve gerekçeli alan önerileri |
| R-02 | Sayısal veri erişimini sına | Proposed | M1: A; M2: B | Alt görevler aşağıda | Karşı üye (planlanan) | R-A02/R-B02: küçük API yanıtı, kaynak/sürüm/birim ve erişim özeti |
| R-03 | İki bölge ve ortak dönem adayını araştır | Implemented | Bu yapay zekâ oturumu | Kullanıcı talebi | M1/M2 görüşü bekleniyor | [İki aday](../research/REGION_CANDIDATES.md); gerekçeler ve katalog kontrolü hazır, seçim yapılmadı |
| R-04 | Küçük örneği ve kaliteyi incele | Proposed | M1: A; M2: B | Alt görevler aşağıda | Karşı üye (planlanan) | R-A04/R-B04: bağımsız ara hesap ve kapsam kontrolü |
| D-01 | Araştırma sorusu ve kapsamı seç | Kısmen kararlaştırıldı | M1 yönlendirmesi | Tek gösterge seçildi; alan/ürün/dönem açık | M2 görüşü bekleniyor | [ADR-004](../decisions/ADR-004-MODULES-AND-PILOT.md) ve [pilot](PILOT.md) |
| A-02 | Modül ilişkileri ve sonuç sözleşmesini taslaklaştır | Implemented | Bu yapay zekâ oturumu | Kullanıcı talebi | Teknik uygulama/üye incelemesi bekleniyor | [Modül sistemi](../architecture/MODULE_SYSTEM.md); hiyerarşi ve veri bağımlılığı ayrı |
| P-04 | Dar T2M pilotunu uçtan uca gerçekleştir | Validating | M1: modül/A; M2: B | [İş bölümü](REGION_WORKFLOW.md); genel web geliştirmesi açık | Karşılıklı inceleme planı | [Pilot çıkış koşulları](PILOT.md); alt görevler aşağıda |
| A-01 | Modülün istatistik yöntemini belirle | Proposed | M1 | Modül kapsamını üstlendi | M2 (planlanan) | MOD-02: kaynak, varsayımlar ve bağımsız örnek |
| U-01 | Etkileşim taslağını belirle | Proposed | Atanmadı | Atanmadı | Atanmadı | Harita/grafik/tarih akışı; kapsam seçimine bağlı |
| U-02 | Kayıtlı T2M için ilk yerel sonuç ekranı | Validating | M1 oturumundaki teknik dilim | İlk ekran önerisi sonrası M1 devam talebi | M1/M2 kullanım incelemesi bekliyor | [Yerel çalışan ekran](../product/RESULTS_PREVIEW.md): 162 analiz testi ve on Chrome senaryosu; kaynak/kapsam/aday durumu görünür. Nihai yığın/barındırma/Mac kabulü açık |
| C-01 | Yeni konuşmaları özetleyerek işle | Proposed | Atanmadı | Atanmadı | Atanmadı | Yeni bilginin esas belgede yer alması |

## Modül ve bölge görevleri

**2026-10-16 ikinci ara teslim:** MOD-01/03 için nokta profiline ayrı `monthly_window_series` şeması/CLI eklendi. MOD-02 ve R-A04 için maskesiz aday dikdörtgenin 56 hücre/12 aylık alan hesabı ve bağımsız Ocak kontrolü çalışıyor. Kesin sınır/maske, ortak B profili ve istatistik açık; R-A04 tamamlandı sayılmadı. [Kanıt ve sınırlar](../evidence/T2M_WINDOW_PROBE.md). **2026-10-17 güncellemesi:** M2'nin B nokta katkısı ve 6° pencere için parçalama beklentisi okundu; nokta uyumu kontrol edildi, bölgesel uygunluk henüz açık.

Görevlerin ayrıntıları: [M1 · A ve modüller](REGION_A.md), [M2 · B](REGION_B.md), [ortak profil ve sıra](REGION_WORKFLOW.md). `Proposed` henüz çalıştırılmadığını gösterir; sorumluluk ataması ayrı sütundadır.

| ID | İş | Durum | Sorumlu | Üstlenme / atama kaynağı | İnceleyen | Bitiş ölçütü / çıktı |
|---|---|---|---|---|---|---|
| MOD-01 | Girdi/çıktı sözleşmesi ve çağrı örneği | Validating | M1 | M1 üstlendi | M2 (planlanan) | Sürümlü şema taslağı ve A/B API örnekleriyle uyumlu girdi/çıktı |
| MOD-02 | T2M modülü ve bilimsel hesap | Validating | M1 | M1 üstlendi | M2 (planlanan) | Ortak profilde seri/analiz; bağımsız küçük hesap ve yöntem kontrolleri |
| MOD-03 | Adaptör, uygunluk ve sürümlü modül teslimi | Validating | M1 | M1 üstlendi | M2 (planlanan) | Örnek çalıştırma, sürüm, hata/eksiklik davranışı ve B yapılandırma girdileri |
| MOD-04 | Geniş pencere için parçalı API ve hücre birleştirme | Verified | M1 | M1'in 2026-10-17 geliştirme/main talebi | M2 (791e07c içinde Mac kullanım doğrulaması bildirdi) | [İki gerçek B isteği, 55 tekil hücre, bağımsız Ocak ve hata kontrolleri](../evidence/T2M_TILING.md); [Mac kılavuzu](../guide/T2M_TILED_WINDOW.md). Nihai bölgesel bilimsel uygunluk değildir. |
| MOD-05 | Maske kaynağı ve aday fraksiyon ağırlık altyapısı | Validating | M1 | Modül/A kapsamında devam talebi | M2 (macOS teknik tekrar doğrulandı; bilimsel politika açık) | [İlk hazırlık](../evidence/SURFACE_MASK_CHECK.md), [yerel token ile HTTP 200 metadata](../evidence/EARTHDATA_METADATA.md); [küçük alt küme dönüştürücüsü](../guide/SURFACE_SUBSET.md) ve yapay testleri hazır; GES DISC onayı sonrası [gerçek A/B alt küme](../evidence/SURFACE_SUBSET_CHECK.md) 56/55 hücreyle yeniden doğrulandı; kaynak/dönüşüm erişim engeli kalktı. [Gerçek akışta iki aday ağırlık önizlemesi](../evidence/SURFACE_WORKFLOW.md) 12 ay hesaplandı; kara/buz politikası ve bilimsel uygunluk açık. Sentetik hesap testleri NASA veri doğrulaması değildir. |
| R-A01 | A tanımı ve sınır önerisi | Implemented | M1 | M1 üstlendi | M2 (planlanan) | [A fişi](../research/regions/REGION_A_PROFILE.md): kaynaklı aday/poligon ve sınır sürümü |
| MOD-06 | Çok girdili modül sırası ve kaynak tutarlılığı denemesi | Validating | M1 | Modül kapsamında 2026-10-18 devam talebi | M2 (macOS üzerinde 134 test ve B akışı doğrulandı) | [İlk çalışan teknik kanıt](../evidence/WORKFLOW_ENGINE.md): yapay A/B/C, ortak A tek çalışır, ata kimliği tutarlı, hata/döngü ve snapshot değişimi kontrolleri; 20 yeni test. [Kayıtlı gerçek T2M/fraksiyon adaptörleri](../evidence/SURFACE_WORKFLOW.md) bağlandı; 13 yeni entegrasyon testi ve toplam 134 test başarılı. Bilimsel profil ve kalıcı yürütme deposu açık |
| R-A02 | A küçük API erişimi | Verified | M1 | M1 üstlendi | M2 (planlanan) | [Gerçek nokta API ve 26 test](../evidence/T2M_POINT_PROBE.md); 12/12 ay, bölge ortalaması değil |
| R-A03 | A/B ortak veri profilini kaydet | Validating | M1 | M1 üstlendi | M2 (teknik uygunluk onaylandı) | [Teknik deneme taslağı](REGION_WORKFLOW.md) `t2m-technical-2024` 0.1.0 hazır; nihai bilimsel profil ve maske seçimi açık |
| R-A04 | A örnek hesap ve entegrasyon | Validating | M1 | M1 üstlendi | M2 (planlanan) | [Maskesiz aday dikdörtgende bağımsız hesap geçti](../evidence/T2M_WINDOW_PROBE.md); ortak profil/kesin sınır/maske entegrasyonu açık; MOD-02/03 gerekir |
| R-A05 | A tam dönem seri/kalite/analiz | Proposed | M1 | M1 üstlendi | M2 (planlanan) | Gerçek dönem çıktıları ve geçerli alan/zaman kapsamı; R-A04 gerekir |
| R-A06 | A bulgusu ve web kontrolü | Proposed | M1 | M1 üstlendi | M2 (planlanan) | Kaynak/belirsizlikle yorum ve arayüz seçim eşleşmesi; R-A05 gerekir |
| R-B01 | B tanımı ve sınır önerisi | Implemented | M2 | M2 üstlendi | M1 (planlanan) | [B fişi](../research/regions/REGION_B_PROFILE.md): b-candidate-window.geojson ve arama penceresi |
| R-B02 | B küçük API erişimi | Verified | M2 | M2 üstlendi | M1 (planlanan) | [Gerçek nokta API ve 43 test](../research/regions/REGION_B_PROFILE.md); 12/12 ay, -8,29 °C yıllık ortalama |
| R-B03 | B'nin ortak veri profiline uygunluğu | Validating | M2 | M2 üstlendi | M1 (dal incelemesi yapıldı) | M2 teknik uygunluğu ve `t2m-technical-2024` (`0.1.0`) teknik deneme profilini doğruladı; nihai bilimsel profil/maske seçimi açık |
| R-B04 | B örnek hesap ve entegrasyon | Validating | M2 | M2 üstlendi | M1 (kaydedilmiş B tekrarı geçti) | [B parçalı alan (`v0.2.0`) ve 5 düğümlü aday yüzey duyarlılığı macOS'ta doğrulandı](../research/regions/REGION_B_PROFILE.md); kesin sınır/maske politikası açık |
| R-B05 | B tam dönem seri/kalite/analiz | Proposed | M2 | Atandı; bu alt işte başlangıç kaydı yok | M1 (planlanan) | Gerçek dönem çıktıları ve geçerli alan/zaman kapsamı; R-B04 gerekir |
| R-B06 | B bulgusu ve web kontrolü | Proposed | M2 | Atandı; bu alt işte başlangıç kaydı yok | M1 (planlanan) | Kaynak/belirsizlikle yorum ve arayüz seçim eşleşmesi; R-B05 gerekir |

Bir görev önerildiğinde “Sorumlu: M1/M2, Üstlenme: Önerildi” yazılır. İlgili kişi üstlenince “Kabul edildi” olur. Kişi başlamadan işi `Validating` saymayın; bittiğinde gerçek sonucu ve inceleme ihtiyacını kaydedin. İnceleyen adı yazmak, incelemenin yapılmış olduğunu göstermez.

M1'in nokta aktarımı ve maskesiz aday dikdörtgen hesabı çalışıyor; M2'nin B nokta örneği de mevcut. Kesin analiz alanının bölgesel hesabı, uzun dönem istatistik ve web uygulaması açık. [Açık sorular](../discovery/index.md) yanıtlandıkça işler somutlaştırılacak.

2026-10-19: M2, macOS/Python 3.14 üzerinde 134 testi, `b-surface-fractions` (55 hücre) NetCDF dönüşümünü ve `run-surface-workflow` (5 düğümlü B aday yüzey duyarlılık akışı) çıktısını doğruladı. Nihai bilimsel maske/sınır ve uzun dönem kapsamı açık. [B fişi](../research/regions/REGION_B_PROFILE.md), [H-M1-008](../team/HANDOFFS.md).
