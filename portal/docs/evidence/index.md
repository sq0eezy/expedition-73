# Kanıtlar

| Kayıt | Kapsam |
|---|---|
| [Gerçek modül akışı ekranı](WORKFLOW_TRACE_CHECK.md) | Aynı çalıştırmadan 5/8 bağlantı, kimlik/girdi/ata doğrulama, Windows/Linux 180 test, 13 JS/30 Chrome ve paket uyumu |
| [Portal kurulumu ve doğrulama](PORTAL_SETUP.md) | Bu oturumdaki belge portalı kontrolleri |
| [Ekip alanı doğrulaması](TEAM_SETUP.md) | İki üyeli belge yapısı, GitHub kimlik incelemesi ve paylaşım sınırı |
| [GitHub main aktarımı](GITHUB_SHARE.md) | Uzak katkıların korunması, gönderim ve kurulum takibi |
| [Mac kurulum hazırlığı](MACOS_SETUP.md) | macOS kılavuzu, ortam yolu kontrolü ve gerçek Mac doğrulama sınırı |
| [Bölge adayları araştırması](REGION_RESEARCH.md) | Resmî kaynaklar, 21 CMR metadata isteği ve sınırlar |
| [GitHub Pages hazırlığı](PAGES_SETUP.md) | Otomatik yayın akışı, erişim yetkisi ve ilk etkinleştirme sınırı |
| [Modül ve pilot tasarımı](MODULE_DESIGN.md) | Kullanıcı kararı, konu/veri ilişkileri ve tek göstergeli pilot belgelerinin kontrolü |
| [Çok girdili yürütme denemesi](WORKFLOW_ENGINE.md) | Yapay A→B, A+B→C, aynı kaynak kimliği, hata/döngü ve güncellik kontrolleri; NASA modül entegrasyonu değildir |
| [Gerçek verili modül akışı](SURFACE_WORKFLOW.md) | Kayıtlı NASA T2M ve fraksiyonlarının motorla bağlanması; iki aday politikanın 12 aylık duyarlılığı ve hata kontrolleri |
| [Aday maske/modül paylaşımı](SURFACE_RELEASE.md) | Kullanıcının canlı talebi, dal/main bütünleştirmesi ve gerçek yayın kontrolü |
| [Koşullu alan kapsamı denetimi](SURFACE_SUPPORT_CHECK.md) | Kesilmiş hücrelerin yüzey yerleşim sınırları, iki gerçek pencere ve analitik testler; güven aralığı değildir |
| [Kaynak AREA uygunluğu](SOURCE_AREA_CHECK.md) | Canlı tam DMR HTTP 200: seçili granülde AREA yok; çevrim dışı yeterlilik kontrolü, sayısal karşılaştırma yapılmadı |
| [Geliştirme paketi](DEV_PACKAGE_CHECK.md) | Docker/native başlatıcı, 171 analiz + 8 JS testi, Docker HTTP/22 Chrome senaryosu ve sınırlı demo ZIP; uzak CI sonucu değildir |
| [Aday ağırlık kıyaslaması](POLICY_COMPARISON_CHECK.md) | Aynı ayın üç sonucu ve eşleşen çiftlerde yıllık en büyük fark/ayı; 164 analiz + 8 JS testi ve 22 Chrome senaryosu |
| [Hücre görünümü](SPATIAL_PREVIEW_CHECK.md) | 56/55 hücre, mevcut alan/aylık sonuçları yeniden üretme, 164 analiz testi ve 18 Chrome senaryosu; yeni yayın yok |
| [İlk yerel sonuç ekranı](RESULTS_PREVIEW_CHECK.md) | Gerçek kayıtlı grafik/ay/maske seçimi, 162 analiz testi ve on Chrome senaryosu; bilimsel profil kabulü değildir |
| [Gerçek T2M API ve adaptör](T2M_POINT_PROBE.md) | 2024 tek nokta yanıtı, 26 test ve bilimsel sınırlar |
| [Gerçek T2M alan hesabı](T2M_WINDOW_PROBE.md) | 56 hücre/12 ay, kenar kesişimleri, bağımsız hesap ve kapsam sınırları |
| [Parçalı T2M erişimi](T2M_TILING.md) | B'nin 6° penceresinde iki istek, 55 tekil hücre ve kaynak/hata kontrolleri |
| [Maske hazırlığı](SURFACE_MASK_CHECK.md) | Gerçek 401 erişim sonucu, hücre planı ve yalnızca sentetik maske hesabı testleri |
| [Earthdata metadata erişimi](EARTHDATA_METADATA.md) | Yerel kullanıcı isteğinde HTTP 200, dört değişken, boyut/birim ve dosya hash doğrulaması |
| [Küçük fraksiyon dönüştürücüsü](SURFACE_SUBSET_CHECK.md) | Gerçek A/B fraksiyon alt kümeleri 56/55 hücreyle yeniden doğrulandı; yapay hata testleri ayrı |
| [Araştırma kaydı](../research/index.md) | İncelenen sayfalar ve erişim sınırları |

NASA POWER sayısal nokta erişimi için [ilk kanıt](T2M_POINT_PROBE.md), maskesiz aday dikdörtgenin küçük alan hesabı için [yeni kanıt](T2M_WINDOW_PROBE.md) var. Kesin analiz bölgesinin uzun dönem serisi/trend/anlamlılık hesabı, performans ölçümü veya kullanıcı denemesi için henüz kanıt yok.

Yeni kanıtta tarih/ortam, gerçek komut veya gözlem yöntemi, girdi, sonuç, çıktı dosyası ve sınırlama bulunmalı. Portal testleri uygulama analizi yerine sayılmaz. Kaynak aracın eski `verification/` kayıtları bu projenin sonuçları değildir.
