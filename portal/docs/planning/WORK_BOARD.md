# İş panosu

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
| C-01 | Yeni konuşmaları özetleyerek işle | Proposed | Atanmadı | Atanmadı | Atanmadı | Yeni bilginin esas belgede yer alması |

## Modül ve bölge görevleri

**2026-10-16 ikinci ara teslim:** MOD-01/03 için nokta profiline ayrı `monthly_window_series` şeması/CLI eklendi. MOD-02 ve R-A04 için maskesiz aday dikdörtgenin 56 hücre/12 aylık alan hesabı ve bağımsız Ocak kontrolü çalışıyor. Kesin sınır/maske, ortak B profili ve istatistik açık; R-A04 tamamlandı sayılmadı. [Kanıt ve sınırlar](../evidence/T2M_WINDOW_PROBE.md). **2026-10-17 güncellemesi:** M2'nin B nokta katkısı ve 6° pencere için parçalama beklentisi okundu; nokta uyumu kontrol edildi, bölgesel uygunluk henüz açık.

Görevlerin ayrıntıları: [M1 · A ve modüller](REGION_A.md), [M2 · B](REGION_B.md), [ortak profil ve sıra](REGION_WORKFLOW.md). `Proposed` henüz çalıştırılmadığını gösterir; sorumluluk ataması ayrı sütundadır.

| ID | İş | Durum | Sorumlu | Üstlenme / atama kaynağı | İnceleyen | Bitiş ölçütü / çıktı |
|---|---|---|---|---|---|---|
| MOD-01 | Girdi/çıktı sözleşmesi ve çağrı örneği | Validating | M1 | M1 üstlendi | M2 (planlanan) | Sürümlü şema taslağı ve A/B API örnekleriyle uyumlu girdi/çıktı |
| MOD-02 | T2M modülü ve bilimsel hesap | Validating | M1 | M1 üstlendi | M2 (planlanan) | Ortak profilde seri/analiz; bağımsız küçük hesap ve yöntem kontrolleri |
| MOD-03 | Adaptör, uygunluk ve sürümlü modül teslimi | Validating | M1 | M1 üstlendi | M2 (planlanan) | Örnek çalıştırma, sürüm, hata/eksiklik davranışı ve B yapılandırma girdileri |
| MOD-04 | Geniş pencere için parçalı API ve hücre birleştirme | Verified | M1 | M1'in 2026-10-17 geliştirme/main talebi | M2 (kullanım incelemesi bekleniyor) | [İki gerçek B isteği, 55 tekil hücre, bağımsız Ocak ve hata kontrolleri](../evidence/T2M_TILING.md); [Mac kılavuzu](../guide/T2M_TILED_WINDOW.md). Nihai bölgesel bilimsel uygunluk değildir. |
| MOD-05 | Maske kaynağı ve aday fraksiyon ağırlık altyapısı | Validating | M1 | Modül/A kapsamında devam talebi | M2 (tanım/uygunluk incelemesi bekleniyor) | [İlk hazırlık](../evidence/SURFACE_MASK_CHECK.md), [yerel token ile HTTP 200 metadata](../evidence/EARTHDATA_METADATA.md); gerçek fraksiyon/koordinat alt kümesi ve dönüşüm açık. Sentetik hesap testleri NASA veri doğrulaması değildir. |
| R-A01 | A tanımı ve sınır önerisi | Implemented | M1 | M1 üstlendi | M2 (planlanan) | [A fişi](../research/regions/REGION_A_PROFILE.md): kaynaklı aday/poligon ve sınır sürümü |
| R-A02 | A küçük API erişimi | Verified | M1 | M1 üstlendi | M2 (planlanan) | [Gerçek nokta API ve 26 test](../evidence/T2M_POINT_PROBE.md); 12/12 ay, bölge ortalaması değil |
| R-A03 | A/B ortak veri profilini kaydet | Validating | M1 | M1 üstlendi | M2 (B uygunluk incelemesi) | [Teknik deneme taslağı](REGION_WORKFLOW.md) `t2m-technical-2024` 0.1.0 hazır; nihai bilimsel profil ve M2 incelemesi açık |
| R-A04 | A örnek hesap ve entegrasyon | Validating | M1 | M1 üstlendi | M2 (planlanan) | [Maskesiz aday dikdörtgende bağımsız hesap geçti](../evidence/T2M_WINDOW_PROBE.md); ortak profil/kesin sınır/maske entegrasyonu açık; MOD-02/03 gerekir |
| R-A05 | A tam dönem seri/kalite/analiz | Proposed | M1 | M1 üstlendi | M2 (planlanan) | Gerçek dönem çıktıları ve geçerli alan/zaman kapsamı; R-A04 gerekir |
| R-A06 | A bulgusu ve web kontrolü | Proposed | M1 | M1 üstlendi | M2 (planlanan) | Kaynak/belirsizlikle yorum ve arayüz seçim eşleşmesi; R-A05 gerekir |
| R-B01 | B tanımı ve sınır önerisi | Implemented | M2 | M2 üstlendi | M1 (planlanan) | [B fişi](../research/regions/REGION_B_PROFILE.md): b-candidate-window.geojson ve arama penceresi |
| R-B02 | B küçük API erişimi | Verified | M2 | M2 üstlendi | M1 (planlanan) | [Gerçek nokta API ve 43 test](../research/regions/REGION_B_PROFILE.md); 12/12 ay, -8,29 °C yıllık ortalama |
| R-B03 | B'nin ortak veri profiline uygunluğu | Proposed | M2 | M2 üstlendi | M1 (planlanan) | Ortak ürün/dönem/yöntemle B uyumu ve engeller; R-A03 ile eşleşir |
| R-B04 | B örnek hesap ve entegrasyon | Proposed | M2 | Atandı; bu alt işte başlangıç kaydı yok | M1 (planlanan) | Küçük bağımsız alan hesabı modülle karşılaştırılmış; MOD-02/03 gerekir |
| R-B05 | B tam dönem seri/kalite/analiz | Proposed | M2 | Atandı; bu alt işte başlangıç kaydı yok | M1 (planlanan) | Gerçek dönem çıktıları ve geçerli alan/zaman kapsamı; R-B04 gerekir |
| R-B06 | B bulgusu ve web kontrolü | Proposed | M2 | Atandı; bu alt işte başlangıç kaydı yok | M1 (planlanan) | Kaynak/belirsizlikle yorum ve arayüz seçim eşleşmesi; R-B05 gerekir |

Bir görev önerildiğinde “Sorumlu: M1/M2, Üstlenme: Önerildi” yazılır. İlgili kişi üstlenince “Kabul edildi” olur. Kişi başlamadan işi `Validating` saymayın; bittiğinde gerçek sonucu ve inceleme ihtiyacını kaydedin. İnceleyen adı yazmak, incelemenin yapılmış olduğunu göstermez.

M1'in nokta aktarımı ve maskesiz aday dikdörtgen hesabı çalışıyor; M2'nin B nokta örneği de mevcut. Kesin analiz alanının bölgesel hesabı, uzun dönem istatistik ve web uygulaması açık. [Açık sorular](../discovery/index.md) yanıtlandıkça işler somutlaştırılacak.

2026-10-17: MOD-04, R-B04'ün 6° genişlikte erişim engelini kaldırıyor. R-B03/04 yine Proposed; M2'nin kendisinin yeni çalıştırma/alan yorumu yapmış olduğu varsayılmadı. [H-M1-005 teslimi](../team/HANDOFFS.md).
