---
status: Proposed
updated: "2026-10-15"
phase: Tek göstergeli T2M pilotunu hazırlama
review_summary: "Kabul edilen mimari yön, seçilen pilot ve henüz açık olan veri kararları."
change_summary: "Modüle özel hesap ve ortak çıktı kabul edildi; T2M pilotu seçildi. Portalın canlı yayını doğrulandı."
---
# Mevcut durum

**İlk pilot seçildi: 2 metre hava sıcaklığının zaman serisi ve eğilimi.** Kullanıcı modüle özel bilimsel hesap + ortak sonuç adaptörü yaklaşımını kabul etti; alt modüller ve modüller arası veri bağlantıları istedi. Sonuçları inceleten bir web uygulaması sunulacak. [ADR-004](decisions/ADR-004-MODULES-AND-PILOT.md).

## Hazır olanlar

- [Modül sistemi](architecture/MODULE_SYSTEM.md), [sistem haritası](architecture/SYSTEM_MAP.md), [ortak sonuç taslağı](architecture/DATA_AND_FLOWS.md), [dar pilot planı](planning/PILOT.md) ve [web deneyimi](product/index.md) güncellendi. Yön kabul edildi; teknik şema ve uygulama henüz yok.
- Yönetim portalı **[GitHub Pages'te açık](https://sq0eezy.github.io/expedition-73/)**. Yayın işi başarılı; başlangıç sayfası ve okuma kataloğu HTTP 200 ile doğrulandı. [Yayın kaydı](evidence/PAGES_SETUP.md), [kullanım](guide/WEB_PORTAL.md).
- [İki kişilik ekip alanı](team/index.md), üye notları, fikir/devir kayıtları ve [iş panosu](planning/WORK_BOARD.md) mevcut. A/B sorumluluğu düşünülüyor; kişi/bölge eşleştirmesi ve bilimsel görev üstlenmeleri henüz yok. M2'nin kendi görüş kaydı gelmedi.
- [İki aday alan](research/REGION_CANDIDATES.md) için NASA CMR metaverisi sorgulandı. Katalog eşleşmesi gerçek piksel, kalite veya analiz doğrulaması değildir. Türkiye yalnızca örnekti.
- M2 macOS kullanıyor; yerel geliştirme için [Mac kılavuzu](guide/MACOS_SETUP.md) var. Webden okumak için kurulum/pull gerekmez. Yerel kaynaklarla çalışan kişinin/yapay zekânın güncel kaydı alması gerekir.

## Açık kalanlar

Kesin iki bölge/sınır, ürün/sürüm/erişim yolu, dönem, istatistik yöntemi, teknoloji yığını, görev sahipleri, teslim tarihi ve nihai uygulama adı seçilmedi. MERRA-2 aylık T2M, Colorado Platosu çevresi/Kuzey Alaska ve 2001–2024 adaydır; seçilmiş sayılmaz.

NASA bilimsel dosyası indirilmedi. Trend/p-değeri, çalışan adaptör, modüller arası gerçek veri aktarımı ve sunulacak uygulama henüz yok. Portalın yayında olması bilimsel ürünün tamamlandığını göstermez.

## Sıradaki küçük adım

[Pilot planındaki](planning/PILOT.md) küçük gerçek T2M örneğine erişip birim, zaman, kalite ve alan kapsamını incele. Sınır/dönem uygunluğu sonrasında küçük bağımsız hesapla seri üretimini doğrula; ardından istatistik ve web görünümüne geç. Yeni konuşmalar [işleme akışıyla](guide/AI_WORKFLOW.md) kaydedilir.
