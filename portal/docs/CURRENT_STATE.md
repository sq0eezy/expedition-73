---
status: Proposed
updated: "2026-10-15"
phase: Fikir karşılaştırması ve veri keşfi
review_summary: "Kesinleşenler, açık seçimler ve sıradaki küçük adım."
change_summary: "M2'nin Mac kullandığı kaydedildi; ayrı macOS kurulum kılavuzu ve açılış adımları eklendi."
---

# Mevcut durum

Kullanıcı 2026-10-15 tarihinde **henüz değişken seçmediklerini, fikirleri karşılaştırdıklarını** doğruladı.

## Bilinenler

- İki kişilik ekip NASA Space Apps için çalışıyor.
- Paylaşılan challenge metni NASA ölçümlerinde veya model çıktılarında zaman içindeki değişimi, yerini, miktarını ve istatistiksel anlamlılığını incelemeyi istiyor.
- Etkileşimli web uygulaması ve animasyonlu görselleştirme düşünülüyor.
- Proje hafızası için Project Context Portal kullanılacak: [ADR-001](decisions/ADR-001-PORTAL.md).

## Hazırlananlar

M2'nin Mac kullandığı bilgisine göre [macOS kurulum kılavuzu](guide/MACOS_SETUP.md) eklendi. Kodun Mac ortam yolu zaten mevcut; gerçek Mac kurulum sonucu M2'den bekleniyor.

Portal GitHub `main` üzerinden paylaşıldı; uzak commit eşleşmesi doğrulandı. Arkadaşın kendi bilgisayarında pull/kurulum sonucu henüz bildirilmedi.

[İki kişilik ekip alanı](team/index.md) hazır. Emeç Yıldız (`emecyildiz`) ve depo sahibi `sq0eezy` için ayrı çalışma notları; fikir alışverişi, devir listesi ve sorumlu/inceleyen alanlı iş panosu var. Bilimsel görevler henüz kişilere atanmadı. Kullanıcı GitHub `main` aktarımını istedi: [ADR-002](decisions/ADR-002-GITHUB-SHARING.md). Arkadaşın üç uzak commit'i çakışmasız birleştirildi; kurulum adımları [paylaşım kılavuzunda](team/SYNC.md), aktarımın gerçek sonucu [kanıt kaydında](evidence/GITHUB_SHARE.md).

Türkçe portal, fikir karşılaştırması, kaynak listesi, öneri mimarisi ve iş panosu hazırlandı. Portal içerik/derleme kontrolleri ve kaynak aracın testleri geçti; yerel erişim doğrulandı. Gerçek sonuçlar ve sınırlar [portal kanıt kaydında](evidence/PORTAL_SETUP.md) tutulur. Projenin genel aşaması hâlâ fikir karşılaştırmasıdır.

## Açık kararlar

Değişken, veri ürünü, iki bölge, tarih aralığı, istatistik yöntemi, teknoloji yığını, görev sahipleri, teslim tarihi ve nihai uygulama adı seçilmedi. “Expedition 73” çalışma alanının adıdır.

NASA verisi indirilmedi; trend veya p-değeri hesaplanmadı. Portalın çalışması bilimsel uygulamanın tamamlandığını göstermez.

## Sıradaki küçük adım

Arkadaşın [kurulum adımlarıyla](team/SYNC.md) main'i alıp yerel portalını açsın; ardından iki kişi üye notlarına niyetlerini yazıp ilk görevleri üstlensin. Bilimsel keşifte [fikir karşılaştırmasından](discovery/IDEA_COMPARISON.md) iki adayı küçük veri örnekleriyle değerlendirme adımı bekliyor. Yeni konuşmalar [işleme akışıyla](guide/AI_WORKFLOW.md) kaydedilir.
