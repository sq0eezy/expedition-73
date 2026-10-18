---
status: Accepted
date: "2026-10-17"
review_summary: "M1'in doğrudan main yerine ayrı geliştirme dalında çalışma kararı."
change_summary: "M1 modül/A çalışması codex/m1-modules-region-a dalına taşındı; ortak main güncellemeleri korunacak."
---
# ADR-007 · Ayrı geliştirme dalları

## Bağlam ve karar kaynağı

M1, iki kişinin doğrudan main üzerinde çalışmasının çakışmalara yol açabileceğini belirterek ayrı dalda devam edilmesini ve GitHub'daki M2 katkısının kontrol edilip gerekirse alınmasını istedi. Bu karar önceki [main üzerinden ilk paylaşımın](ADR-002-GITHUB-SHARING.md) sonraki geliştirme düzenini değiştirir. M2'nin kendi dalını açtığı varsayılmadı.

## Karar

M1 modüller/A çalışması **`codex/m1-modules-region-a`** dalında sürdürülür. Dal, M2'nin `4ad9448` katkısını içeren güncel main'den açıldı. Yeni geliştirme doğrudan main'e gönderilmez; paylaşım geliştirme dalı üzerinden, ortak sürüme geçiş pull request incelemesi ve birleştirmeyle yapılır. Her push otomatik birleştirme yetkisi vermez.

M2 için de kendisine ait `codex/` önekli bir dal kullanılması önerilir; adını ve açılışını M2 belirler. İki kişi aynı geliştirme dalını paylaşmaz.

## Sonuçlar

- İşe başlamadan `git status`, `git fetch origin` ve yerel/uzak fark incelenir. Korunmamış çalışma saklanmadan dal değişimi veya pull yapılmaz.
- Main, temiz çalışma alanında `git pull --ff-only origin main` ile alınır. Geliştirme dalına main güncellemeleri önce incelenip `git merge origin/main` ile taşınabilir; çakışmada iki katkı korunur. Reset/force ile katkı silinmez.
- GitHub Pages mevcut workflow ile main'den yayımlanır. **Yalnızca geliştirme dalına push etmek canlı paneli güncellemez.** İnceleme için GitHub dalındaki belgeler veya yerel portal kullanılır; main'e birleştikten sonra başarılı yayınla ortak URL güncellenir.
- Yerel main'in eski `origin/master` izleme ayarı bu geçişte `origin/main` olarak düzeltildi. Eski uzak master silinmedi.

İşlem kaydı ve komutlar [paylaşım kılavuzunda](../team/SYNC.md), gerçek kontroller [çalışma günlüğünde](../control-center/WORK_LOG.md). Bilimsel kapsam, alan seçimi veya yöntem kararı değişmedi.

## 2026-10-17 · Bu modül tesliminin birleştirme yolu

M1, parçalı T2M desteğinin test sonrası main'de paylaşılmasını açıkça istedi. Bağlı GitHub entegrasyonunun PR oluşturma çağrısı `403 Resource not accessible by integration` döndürdü; PR oluşmadı. Bu teslim için ayrı dalda geliştirme, yerel kod incelemesi ve testlerden sonra yerel Git merge ile main'e aktarım uygulanır. Bu, sonraki geliştirmelerde ayrı dal veya mümkün olduğunda PR kullanımını kaldırmaz. [Gerçek sonuç kaydı](../evidence/T2M_TILING.md).

## 2026-10-18 · Aday fraksiyon/modül tesliminin canlı paylaşımı

M1 mevcut çalışmanın dal düzeni korunarak canlıya gönderilmesini açıkça istedi. PR oluşturma yeniden aynı API 403 sonucunu verdi; bu teslimde de ayrı M1 dalı, yerel inceleme/test ve normal Git merge/push kullanıldı. M2'nin `791e07c` dalı birleştirilmedi veya değiştirilmedi. Yayında saptanan CI düzeltmesi de M1 dalında hazırlanır. Bu yetki sonraki işleri otomatik main'e taşımaz. [Yayın ve CI kanıtı](../evidence/SURFACE_RELEASE.md).
