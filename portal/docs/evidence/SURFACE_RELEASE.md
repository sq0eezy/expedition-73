---
status: Validating
updated: "2026-10-18"
review_summary: "Mevcut M1 aday maske/modül akışının dal düzeni korunarak ortak canlı panele paylaşılması."
change_summary: "Kullanıcı canlı paylaşımı istedi; branch ve main bütünleştirme/yayın doğrulaması hazırlanıyor."
---
# Aday maske ve modül akışı · Canlı paylaşım

**Talimat kaynağı:** M1, 2026-10-18'de mevcut çalışmanın dal düzeni korunarak canlıya gönderilmesini istedi. Bu kayıt ilk hazırlık durumudur; branch/merge/CI/Pages sonuçları gözlendikçe aşağıya eklenecek. Yayın yapılmış sayılmaz.

Kapsam: [gerçek fraksiyon alt kümeleri](SURFACE_SUBSET_CHECK.md), [yerel bağımlılık motoru](WORKFLOW_ENGINE.md), [gerçek verili aday akış](SURFACE_WORKFLOW.md), yerel token kaydı ve ortak panel belgeleri. NASA'dan yeni veri alınmayacak. Son bilimsel maske/alan/dönem/istatistik veya final web uygulaması seçilmedi.

## Dal ve katkıların korunması

- Başlangıç: M1 `codex/m1-modules-region-a` / `14a16ba`, main/origin-main `1172824`.
- Fetch sonrası M2 `codex/m2-region-b` / `791e07c` değişmemişti. Kaydı okundu; bu dal mevcut yayına birleştirilmeyecek. M2'ye mesaj veya onun dalına yazım yapılmaz.
- Pages workflow'u main'den derleyip yalnız `portal/site` artifact'ını yükler. Geliştirme dalına push tek başına canlı adresi değiştirmez.
- Önce M1 dalında commit/push, mümkünse PR üzerinden incelenmiş main birleştirmesi uygulanır. Sonraki geliştirme ayrı M1 dalında sürer; genel otomatik merge yetkisi verilmedi.

## Kontroller

Önceki yerel kanıt: Windows/Python 3.12.14'te 134 test; gerçek nokta/alan/fraksiyon replay ve aday A/B akışı başarılı. Yayın öncesi kontrollerin son sonucu, kaynak commit ve uzak yayın iş bağlantıları aşağıda kaydedilecek. `.env`, sanal ortam, özel artifacts ve kişisel dosyalar paylaşım dışında tutulur. A/B küçük NASA alt kümelerinde yalnız beşer açık kaynak/üretim dosyası var; token değeri yoktur.
