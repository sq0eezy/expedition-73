---
status: Proposed
updated: "2026-10-15"
phase: Bölge ve modül adaylarını değerlendirme
review_summary: "Kesinleşenler, açık seçimler ve sıradaki küçük adım."
change_summary: "Pull gerektirmeyen ortak web paneli için Pages akışı hazırlandı; depo sahibinin ilk etkinleştirmesi gerekiyor."
---

# Mevcut durum

Kullanıcı 2026-10-15 tarihinde **henüz değişken seçmediklerini, fikirleri karşılaştırdıklarını** doğruladı.

## Bilinenler

- İki kişilik ekip NASA Space Apps için çalışıyor.
- Paylaşılan challenge metni NASA ölçümlerinde veya model çıktılarında zaman içindeki değişimi, yerini, miktarını ve istatistiksel anlamlılığını incelemeyi istiyor.
- Etkileşimli web uygulaması ve animasyonlu görselleştirme düşünülüyor.
- Proje hafızası için Project Context Portal kullanılacak: [ADR-001](decisions/ADR-001-PORTAL.md).

## Hazırlananlar

Okumak için her iki bilgisayarda pull/kurulum yapma ihtiyacını kaldırmak üzere **GitHub Pages yayın akışı** hazırlandı ve `main` dalına gönderildi: [ADR-003](decisions/ADR-003-WEB-PORTAL.md). İlk GitHub/Ubuntu kontrolü ve derlemesi geçti; yayın işi Pages etkinleştirilmediğinden durdu. Bağlı hesapta depo yönetim yetkisi yok; depo sahibinin [bir kerelik etkinleştirmesi](guide/WEB_PORTAL.md) gerekiyor. Canlı yayın henüz yok; [gerçek kontroller](evidence/PAGES_SETUP.md). Açıldıktan sonra her `main` güncellemesi başarılı derlemeyle yayımlanacak. Belge düzenleme GitHub/dosyalar üzerinden sürer.

Kullanıcı **bölgeyi ve modülleri NASA verilerine göre seçme** fikrini tartışmaya açtı; Türkiye yalnızca örnekti. [Colorado Platosu çevresi ve Kuzey Alaska](research/REGION_CANDIDATES.md) gerekçeli iki aday olarak araştırıldı. NASA CMR'de ürün/bölge/tarih eşleşmeleri sorgulandı; bilimsel dosya ve piksel doğrulaması yapılmadı. [Bölge + modül taslağı](architecture/REGIONAL_MODULE_PROPOSAL.md) ve [IDEA-M1-001](team/ideas/IDEA-M1-001.md) **Proposed** durumunda; M1/M2'nin aday onayı yok. [M2 inceleme kaydı](team/HANDOFFS.md) yanıt bekliyor.

M2'nin Mac kullandığı bilgisine göre [macOS kurulum kılavuzu](guide/MACOS_SETUP.md) eklendi. Kodun Mac ortam yolu zaten mevcut; gerçek Mac kurulum sonucu M2'den bekleniyor.

Portal GitHub `main` üzerinden paylaşıldı; uzak commit eşleşmesi doğrulandı. Arkadaşın kendi bilgisayarında pull/kurulum sonucu henüz bildirilmedi.

[İki kişilik ekip alanı](team/index.md) hazır. Emeç Yıldız (`emecyildiz`) ve depo sahibi `sq0eezy` için ayrı çalışma notları; fikir alışverişi, devir listesi ve sorumlu/inceleyen alanlı iş panosu var. Bilimsel görevler henüz kişilere atanmadı. Kullanıcı GitHub `main` aktarımını istedi: [ADR-002](decisions/ADR-002-GITHUB-SHARING.md). Arkadaşın üç uzak commit'i çakışmasız birleştirildi; kurulum adımları [paylaşım kılavuzunda](team/SYNC.md), aktarımın gerçek sonucu [kanıt kaydında](evidence/GITHUB_SHARE.md).

Türkçe portal, fikir karşılaştırması, kaynak listesi, öneri mimarisi ve iş panosu hazırlandı. Portal içerik/derleme kontrolleri ve kaynak aracın testleri geçti; yerel erişim doğrulandı. Gerçek sonuçlar ve sınırlar [portal kanıt kaydında](evidence/PORTAL_SETUP.md) tutulur. Projenin genel aşaması hâlâ fikir karşılaştırmasıdır.

## Açık kararlar

Değişken, veri ürünü, iki bölge, tarih aralığı, istatistik yöntemi, teknoloji yığını, görev sahipleri, teslim tarihi ve nihai uygulama adı seçilmedi. “Expedition 73” çalışma alanının adıdır.

NASA'nın bilimsel veri dosyaları indirilmedi; yalnızca açık katalog metaverisi sorgulanıp kaydedildi. Trend veya p-değeri hesaplanmadı. Portalın çalışması bilimsel uygulamanın tamamlandığını göstermez.

## Sıradaki küçük adım

Depo sahibi [web yayınını](guide/WEB_PORTAL.md) bir kez açabilir; bundan sonra iki üye aynı siteden okuyabilir. İki üye [fikir kartındaki sorulara](team/ideas/IDEA-M1-001.md) görüşlerini eklesin. Pilot için ürün/alan kararı verilirse küçük sayısal alt kümelerde kalite, maske ve aylık kapsama bakılsın; adaylar bundan sonra kabul veya reddedilsin. M2 yerel düzenleme isterse [Mac kurulumu](guide/MACOS_SETUP.md) geçerlidir. Yeni konuşmalar [işleme akışıyla](guide/AI_WORKFLOW.md) kaydedilir.
