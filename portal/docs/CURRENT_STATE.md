---
status: Validating
updated: "2026-10-16"
phase: İlk T2M nokta API ve adaptör denemesi
review_summary: "Kabul edilen mimari yön, seçilen pilot ve henüz açık olan veri kararları."
change_summary: "NASA POWER gerçek nokta örneği alındı; ilk CLI/JSON şeması/adaptör ve 26 çevrim dışı test hazır."
---
# Mevcut durum

**İlk pilot seçildi: 2 metre hava sıcaklığının zaman serisi ve eğilimi.** Kullanıcı modüle özel bilimsel hesap + ortak sonuç adaptörü yaklaşımını kabul etti; alt modüller ve modüller arası veri bağlantıları istedi. Sonuçları inceleten bir web uygulaması sunulacak. [ADR-004](decisions/ADR-004-MODULES-AND-PILOT.md).

## Hazır olanlar

- [Modül sistemi](architecture/MODULE_SYSTEM.md), [sistem haritası](architecture/SYSTEM_MAP.md), [ortak sonuç taslağı](architecture/DATA_AND_FLOWS.md), [dar pilot planı](planning/PILOT.md) ve [web deneyimi](product/index.md) güncellendi. İlk teknik dilim `analysis/` içinde çalışıyor: T2M nokta-serisi JSON şemaları, API/CLI, normalleştirme ve uygunluk denetimi. Genel modül grafiği/bölgesel analiz henüz yok. [Çalıştırma](guide/T2M_ADAPTER.md), [gerçek kanıt](evidence/T2M_POINT_PROBE.md), [teknik seçim](decisions/ADR-006-T2M-POINT-ADAPTER.md).
- Yönetim portalı **[GitHub Pages'te açık](https://sq0eezy.github.io/expedition-73/)**. Yayın işi başarılı; başlangıç sayfası ve okuma kataloğu HTTP 200 ile doğrulandı. [Yayın kaydı](evidence/PAGES_SETUP.md), [kullanım](guide/WEB_PORTAL.md).
- [İki kişilik ekip alanı](team/index.md), üye notları, fikir/devir kayıtları ve [iş panosu](planning/WORK_BOARD.md) mevcut. M1 modüller ve A’yı üstlendi; B’yi M2’ye atadı: [ADR-005](decisions/ADR-005-TEAM-OWNERSHIP.md). [A görevleri](planning/REGION_A.md), [B görevleri](planning/REGION_B.md) ve [ortak profil](planning/REGION_WORKFLOW.md) hazır. M2’nin kendi başlangıç/görüş kaydı henüz yok.
- [İki aday alan](research/REGION_CANDIDATES.md) için NASA CMR metaverisi sorgulandı. Katalog eşleşmesi gerçek piksel, kalite veya analiz doğrulaması değildir. Türkiye yalnızca örnekti.
- M2 macOS kullanıyor; yerel geliştirme için [Mac kılavuzu](guide/MACOS_SETUP.md) var. Webden okumak için kurulum/pull gerekmez. Yerel kaynaklarla çalışan kişinin/yapay zekânın güncel kaydı alması gerekir.

## Açık kalanlar

Kesin iki bölge/sınır, ürün/sürüm/erişim yolu, dönem, istatistik yöntemi, teknoloji yığını, genel web arayüzü sorumlusu, teslim tarihi ve nihai uygulama adı seçilmedi. MERRA-2 aylık T2M, Colorado Platosu çevresi/Kuzey Alaska ve 2001–2024 adaydır; seçilmiş sayılmaz.

NASA POWER API’den A aday penceresindeki tek deneme noktası için 2024’ün 12 aylık T2M değeri alındı ve küçük yanıt örneği saklandı. 26 test ve gerçek yanıtın yeniden üretimi geçti. Bu nokta örneği bölge ortalaması değildir. Bölgesel seri, trend/p-değeri, modüller arası gerçek tüketim ve sunulacak web uygulaması henüz yok. Portalın yayında olması bilimsel ürünün tamamlandığını göstermez.

## Sıradaki küçük adım

M1’in [A fişi](research/regions/REGION_A_PROFILE.md) ve ilk nokta denemesi hazır. M2 [kılavuzla](guide/T2M_ADAPTER.md) kaydedilmiş örneği çevrim dışı doğrulayıp kendi B API denemesini yapabilir. B örneği ve gerçek sınır/maske/ızgara kapsamıyla [ortak profili](planning/REGION_WORKFLOW.md) kesinleştir; bölgesel ağırlık/alan hesabına bundan sonra geç. Sınır/dönem uygunluğu sonrasında küçük bağımsız hesapla seri üretimini doğrula; ardından istatistik ve web görünümüne geç. Yeni konuşmalar [işleme akışıyla](guide/AI_WORKFLOW.md) kaydedilir.
