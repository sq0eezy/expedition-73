# İş panosu

Görevler eldeki kanıta göre güncellenir. Araştırma ve uygulama görevlerinin sahipleri, inceleyenleri ve teslim tarihleri henüz atanmadı. Üye kimlikleri [ekip dizinindedir](../team/index.md). `Verified` portal işleri uygulamanın doğrulandığını göstermez.

| ID | İş | Durum | Sorumlu | Üstlenme | İnceleyen | Tamamlanma ölçütü / kanıt |
|---|---|---|---|---|---|---|
| P-01 | Portalı projeye uyarla | Verified | Önceki yapay zekâ oturumu | Tamamlandı | Üye incelemesi kaydı yok | [Portal doğrulaması](../evidence/PORTAL_SETUP.md) |
| P-02 | İlk konuşmayı özetle | Implemented | Önceki yapay zekâ oturumu | Tamamlandı | Üye incelemesi kaydı yok | [Bağlam](../PROJECT_CONTEXT.md), [fikirler](../discovery/IDEA_COMPARISON.md) |
| P-03 | İki kişilik ekip alanını hazırla | Verified | Bu yapay zekâ oturumu | Kullanıcı talebi | Üye incelemesi bekliyor | [Ekip alanı](../team/index.md), [teknik kontrol](../evidence/TEAM_SETUP.md) |
| S-01 | Yerel portalı uzak değişiklikleri koruyarak main'e gönder | Verified | Bu yapay zekâ oturumu | Kullanıcı talebi | Uzak commit eşleşmesi doğrulandı | [Aktarım kaydı](../evidence/GITHUB_SHARE.md); GitHub main'de paylaşıldı |
| S-02 | Main'i alıp kendi Mac bilgisayarında portalı kur | Proposed | M2 | Önerildi | Atanmadı | [Mac kurulumu](../guide/MACOS_SETUP.md); M2'nin kendi ortamında açılış sonucu |
| S-03 | Pull gerektirmeyen ortak web yayını hazırla | Verified | Bu yapay zekâ oturumu | Kullanıcı talebi | Başarılı yayın ve HTTP doğrulaması | [Pages kaydı](../evidence/PAGES_SETUP.md); portal açık |
| S-04 | Pages kaynağını GitHub Actions seç ve ilk yayını aç | Verified | Depo hesabı | Kullanıcı ayarı yaptığını bildirdi | Bu oturum: yayın/HTTP kontrolü | [Başarılı çalışma](../evidence/PAGES_SETUP.md), canlı site HTTP 200 |
| R-01 | İki adayı kısa listeye al | Proposed | Atanmadı | Atanmadı | Atanmadı | Her aday için seçim kartı |
| R-02 | Sayısal veri erişimini sına | Proposed | Atanmadı | Atanmadı | Atanmadı | Gerçek küçük dosya, indirme yöntemi, sürüm ve birim |
| R-03 | İki bölge ve ortak dönem adayını araştır | Implemented | Bu yapay zekâ oturumu | Kullanıcı talebi | M1/M2 görüşü bekleniyor | [İki aday](../research/REGION_CANDIDATES.md); gerekçeler ve katalog kontrolü hazır, seçim yapılmadı |
| R-04 | Adaylarda küçük bilimsel alt kümeyi ve kaliteyi incele | Proposed | Atanmadı | Atanmadı | Atanmadı | Veri erişimi, geçerli ay/piksel oranı ve maske; bölge/ürün pilot kararı bekliyor |
| D-01 | Araştırma sorusu ve kapsamı seç | Kısmen kararlaştırıldı | M1 yönlendirmesi | Tek gösterge seçildi; alan/ürün/dönem açık | M2 görüşü bekleniyor | [ADR-004](../decisions/ADR-004-MODULES-AND-PILOT.md) ve [pilot](PILOT.md) |
| A-02 | Modül ilişkileri ve sonuç sözleşmesini taslaklaştır | Implemented | Bu yapay zekâ oturumu | Kullanıcı talebi | Teknik uygulama/üye incelemesi bekleniyor | [Modül sistemi](../architecture/MODULE_SYSTEM.md); hiyerarşi ve veri bağımlılığı ayrı |
| P-04 | Dar T2M pilotunu uçtan uca gerçekleştir | Proposed | Atanmadı | Dar kapsam kullanıcı tarafından kabul edildi | Atanmadı | [Pilotun veri, hesap, adaptör ve web çıkış koşulları](PILOT.md) |
| A-01 | İstatistik yöntemini belirle | Proposed | Atanmadı | Atanmadı | Atanmadı | Kaynak, varsayımlar ve örnek doğrulama planı |
| U-01 | Etkileşim taslağını belirle | Proposed | Atanmadı | Atanmadı | Atanmadı | Harita/grafik/tarih akışı; kapsam seçimine bağlı |
| C-01 | Yeni konuşmaları özetleyerek işle | Proposed | Atanmadı | Atanmadı | Atanmadı | Yeni bilginin esas belgede yer alması |

Bir görev önerildiğinde “Sorumlu: M1/M2, Üstlenme: Önerildi” yazılır. İlgili kişi üstlenince “Kabul edildi” olur. Kişi başlamadan işi `Validating` saymayın; bittiğinde gerçek sonucu ve inceleme ihtiyacını kaydedin. İnceleyen adı yazmak, incelemenin yapılmış olduğunu göstermez.

Henüz uygulama geliştirme görevi başlatılmadı. [Açık sorular](../discovery/index.md) yanıtlandıkça işler somutlaştırılacak.
