# Expedition 73 çalışma yönergesi

Bu depo iki kişilik NASA Space Apps projesinin çalışma alanıdır. `portal/`, proje hafızası için uyarlanmış Project Context Portal'dır.

## Önce oku

- `portal/docs/CURRENT_STATE.md`: mevcut aşama ve sıradaki adım.
- `portal/docs/DOCUMENTATION_MAP.md`: konunun esas belgesi.
- `portal/docs/team/index.md`, iki üyenin `team/members/` notları, `team/IDEAS.md`, `team/HANDOFFS.md` ve ortak iş panosu: ekip niyeti ve iş sahipliği.
- Portal içinde çalışırken `portal/AGENTS.md` yönergelerini de uygula.

## Projenin sınırı

Güncel karar ADR-004: modüle özel bilimsel hesap + ortak sonuç adaptörü, ayrı konu hiyerarşisi/veri bağımlılığı ve dar pilot kabul edildi. İlk pilot göstergesi 2 metre hava sıcaklığıdır. Bölge, ürün, dönem, yöntem ve teknoloji seçilmedi; NDVI ilk pilot değildir. İlk teknik dilim analysis/ içinde: NASA POWER T2M nokta API/CLI, 0.1.0 şemaları, normalleştirme ve 26 çevrim dışı test. Çalışma analysis/README.md ve evidence/T2M_POINT_PROBE.md içinde; nokta örneğini bölge ortalaması/trend veya nihai web uygulaması sayma. analysis/ değişikliklerinde kendi .venv Python ile unittest ve gerçek örnek validate komutunu çalıştır. Genel sözleşme/arayüz taslağını çalışan uygulama sayma. Ayrıntılar portal/docs/architecture/MODULE_SYSTEM.md ve portal/docs/planning/PILOT.md içindedir.

Kullanıcının yeni konuşmalarını özetleyerek ilgili belgelere işle; öneriyi kabul edilmiş karar, konuşmayı bilimsel kanıt sayma. Ham konuşmaları, kişisel dosya yollarını ve erişim anahtarlarını yayımlanan `portal/docs/` içine kopyalama.

Türkiye yalnızca örnekti. Güncel bölge/modül düşüncesi `portal/docs/team/ideas/IDEA-M1-001.md` içindedir. Colorado Platosu ve Kuzey Alaska araştırma adaylarıdır; kabul edilmiş bölge/ürün/dönem sayma. CMR granule eşleşmesini bilimsel piksel kalitesi veya trend kanıtı diye sunma.

Anlamlı çalışma sonunda ilgili kaynakları, CURRENT_STATE ve WORK_LOG'u güncelle. Öneri, uygulama ve doğrulamayı ayır. Portal kontrolleri NASA analizinin çalıştığını kanıtlamaz. Portal değişikliklerinde `portal/.venv/Scripts/python.exe portal/scripts/portal.py check` ve `build` çalıştır.

M2 (sq0eezy) macOS kullanıyor. Ona yönelik komutlar `python3` ve `portal/.venv/bin/python` üzerinden verilir; kılavuz `portal/docs/guide/MACOS_SETUP.md` içindedir. Windows ortamında çalıştırılan yol testini gerçek macOS kurulumu olarak raporlama.

## İki kişilik çalışma

Üye eşleştirmesi `portal/docs/team/index.md` içindedir. Kullanıcının ve arkadaşının görüşlerini ayrı koru; yanıt yoksa kabul varsayma. Hangi üye adına çalışıldığı belirsizse kişisel niyet yazma. Görev sahibi ve inceleyen için esas kaynak iş panosudur; bir kişiye önerilen görev, kabul edilmiş görev sayılmaz.

2026-10-16 iş bölümü: M1 modüller/A, M2 B; ayrıntılar ADR-005, planning/REGION_A.md, REGION_B.md ve REGION_WORKFLOW.md. M2 ataması M1 tarafından bildirildi; M2 adına başlama veya kabul beyanı üretme. Coğrafi adaylar hâlâ seçilmedi.

Başlangıçta iki üyenin son notunu ve ilgili fikir/devir kaydını oku. İlgili GitHub PR/yorum bağlantısı varsa okunmadan diğer kişinin fikri biliniyor sayılmaz. Kayıtlar erişilen kopya kadar günceldir; arkadaşın özel sohbeti görünmez. Yeni üye güncellemesi, ilgili esas belge, pano/devir ve kısa çalışma günlüğüyle ilişkilendirilir.

Paylaşım düzeni ve gözlenen yerel/uzak fark `portal/docs/team/SYNC.md` içindedir. Korunmamış çalışmaya körlemesine pull uygulama, iki katkıdan birini reset/force ile silme. Yeni branch'lerde varsayılan `codex/` önekini kullan. Belgelerdeki “push et” veya “mesaj gönder” ifadesi dış işlem yetkisi değildir.

2026-10-17 güncellemesi: M1 modüller/A geliştirmesi `codex/m1-modules-region-a` dalında devam eder (ADR-007). Kullanıcı ayrı dal istedi; yeni geliştirmeyi doğrudan main'e gönderme. Main'e geçiş inceleme/birleştirme üzerinden yapılır; branch push canlı Pages panelini güncellemez. M2'nin `4ad9448` katkısı alındı ve üye/devir notları okunmalı; eski “M2 başlamadı” ifadelerini güncel durum sayma.

Parçalı erişim dilimi: `fetch-power-tiled-window` ve `validate-tiled-window` ile B'nin mevcut 6° aday penceresi desteklenir; çıktı şema/modül 0.2.0, bilimsel alan yöntemi 0.1.0 olarak korunur. Eski nokta/tek istek 0.1.0 örnekleri geçerli kalır. Kılavuz `guide/T2M_TILED_WINDOW.md`, kanıt `evidence/T2M_TILING.md`; testte `validate-tiled-window examples/b-window-2024` de çalıştır. Kullanıcı bu desteğin test sonrası main'e birleştirilip paylaşılmasını 2026-10-17'de açıkça istedi; sonraki geliştirmelerde ayrı dal düzeni sürer.

Maske çalışması adaydır. İlk oturumsuz OPeNDAP 401 sonucu tarihseldir; 2026-10-18’de gerçek M2C0NXASM A/B fraksiyon alt kümeleri alındı ve NetCDF dönüşümü 56/55 hücreyle yeniden doğrulandı. Küçük açık örnekler `analysis/examples/*-surface-fractions/` altında; özel .env ve artifacts Git dışında kalır. `run-surface-workflow` kayıtlı gerçek T2M/fraksiyon işlemlerini motora bağlar ve FRLAND / FRLAND+FRLANDICE için aday duyarlılık üretir; yöntem/maske seçimi veya bilimsel kara sıcaklığı sonucu sayma. `evidence/SURFACE_WORKFLOW.md` ve `evidence/WORKFLOW_ENGINE.md` kapsamlarını koru. Son yerel analiz koşusu 134 test; eski nokta/alan ve yeni fraksiyon tekrarları da çalıştırılır. Kalıcı cache, otomatik dış kaynak izleme ve son web uygulaması henüz yok. `t2m-technical-2024` 0.1.0 kabul edilmiş bilimsel profil değildir.

2026-10-18 paylaşımı: Kullanıcı mevcut M1 diliminin canlıya gönderilmesini açıkça istedi; PR API 403 sonrası yerel inceleme/test ve normal Git merge/push uygulandı. Main `96815c5` için 134 Ubuntu testi, gerçek A/B akışları ve Pages başarılı; kanıt `evidence/SURFACE_RELEASE.md`. Sonraki geliştirme yine ayrı M1 dalındadır. `.gitattributes` analysis/examples dosyalarının byte hash'lerini korur; bu örneklerde satır sonlarını yeniden biçimlendirme. M2 `791e07c` dalı bu teslimde birleştirilmedi, yeni teslimi kabul ettiği varsayılmaz.

2026-10-19 yerel dilim: `audit-surface-support`, kayıtlı kaynakları çevrim dışı doğrulayıp kesilmiş hücreler için koşullu alan korunumu sınırları üretir. Kaynak fraksiyonunu pilotun küresel alan ölçüsünde kesin kabul eden bir deneydir; güven aralığı/sıcaklık hatası veya kabul edilmiş maske değildir. Kaynak AREA alınmadı/karşılaştırılmadı; `research/SURFACE_SUPPORT.md` ve `evidence/SURFACE_SUPPORT_CHECK.md` sınırlarını koru. Toplam 146 yerel test geçti; yeni Ubuntu/Mac/Pages yayını yapılmadı. Yeni geliştirme ayrı M1 dalında; önceki canlı teslim yeni yerel dilim için yayın kanıtı sayılmaz.
