---
status: Verified
updated: "2026-10-18"
review_summary: "Mevcut M1 aday maske/modül akışının dal düzeni korunarak ortak canlı panele paylaşılması."
change_summary: "96815c5 main sürümünde 134 Ubuntu testi, gerçek A/B akışları ve Pages başarılı; canlı belge/katalog HTTP 200."
---
# Aday maske ve modül akışı · Canlı paylaşım

**Talimat kaynağı:** M1, 2026-10-18'de mevcut çalışmanın dal düzeni korunarak canlıya gönderilmesini istedi. Yayın ve analiz kontrolleri başarılı; ilk hata ve düzeltme aşağıda ayrı tutulur. Verified durumu bu teknik teslim/yayın içindir; bilimsel politika kabulü değildir.

Kapsam: [gerçek fraksiyon alt kümeleri](SURFACE_SUBSET_CHECK.md), [yerel bağımlılık motoru](WORKFLOW_ENGINE.md), [gerçek verili aday akış](SURFACE_WORKFLOW.md), yerel token kaydı ve ortak panel belgeleri. NASA'dan yeni veri alınmayacak. Son bilimsel maske/alan/dönem/istatistik veya final web uygulaması seçilmedi.

## Dal ve katkıların korunması

- Başlangıç: M1 `codex/m1-modules-region-a` / `14a16ba`, main/origin-main `1172824`.
- Fetch sonrası M2 `codex/m2-region-b` / `791e07c` değişmemişti. Kaydı okundu; bu dal mevcut yayına birleştirilmeyecek. M2'ye mesaj veya onun dalına yazım yapılmaz.
- Pages workflow'u main'den derleyip yalnız `portal/site` artifact'ını yükler. Geliştirme dalına push tek başına canlı adresi değiştirmez.
- Önce M1 dalında commit/push, mümkünse PR üzerinden incelenmiş main birleştirmesi uygulanır. Sonraki geliştirme ayrı M1 dalında sürer; genel otomatik merge yetkisi verilmedi.

## Kontroller

Windows/Python 3.12.14'te ilk yayın öncesi 134 test / 32,534 saniye; byte düzeltmesi sonrası 134 test / 15,654 saniye başarılı. İki nokta doğrulaması, A pencere, B parçalı pencere ve iki fraksiyon replay'i geçti; portal check/strict build ve git diff --check geçti. `.env`, sanal ortam, özel artifacts ve kişisel dosyalar paylaşım dışında tutulur. Staged içerikte kayıtlı token değerinin bulunmadığı, değeri yazdırılmadan kontrol edildi. A/B küçük NASA alt kümelerinde yalnız beşer açık kaynak/üretim dosyası var; token değeri yoktur.

## İlk main yayını ve CI düzeltmesi · 2026-10-18

- Kaynak [7e50536](https://github.com/sq0eezy/expedition-73/commit/7e505363365614f569ad49d689306b542c155f93) M1 dalına push edildi. PR oluşturma API'si `403 Resource not accessible by integration` döndürdü; PR oluşmadı. Kullanıcının açık yayın talebi ve yerel inceleme/testlerden sonra normal Git merge/push kullanıldı; force/reset yok. [Dal kararı](../decisions/ADR-007-FEATURE-BRANCHES.md).
- Main [1f6b015](https://github.com/sq0eezy/expedition-73/commit/1f6b015b0664d336603e055c518d568b47eb5da5). [İlk Pages işi](https://github.com/sq0eezy/expedition-73/actions/runs/39130172404) başarılı. UTC 13:08:49'da canlı `evidence/SURFACE_WORKFLOW/` HTTP 200 ve `run-surface-workflow` işareti, `assets/reader/catalog.json` HTTP 200 ve yeni belge kaydı görüldü. İlk yayın kaydı da HTTP 200; henüz yazılmamış commit işareti bulunmadı, sürüm kanıtı olarak kullanılmadı.
- [İlk Ubuntu analiz işi](https://github.com/sq0eezy/expedition-73/actions/runs/39130172503) **başarısız**: 134 testte A/B kayıtlı duyarlılık karşılaştırması iki alt testte uyuşmadı; sonraki CLI adımları atlandı. Yerel test başarısı Ubuntu başarısı diye sunulmadı.
- Tanı: Windows `core.autocrlf` JSON dosyalarını CRLF yapmış; Git deposundaki LF baytları Linux'ta farklı kaynak hash'i üretiyor. Metadata byte hash'i de temiz Windows checkout'unda dönüşümden etkilenebilir. Kaynak SHA doğrulaması korunarak `.gitattributes` ile sadece `analysis/examples/**` satır sonu dönüşümü kapatıldı, dosyalar depodaki tam baytlara getirildi ve iki duyarlılık örneği yeniden hesaplandı. Test kaynak hash haritası uyuşmazlığını ayrıca açıkça raporlar. NASA NetCDF/yanıt baytları ve bilimsel yöntem değişmedi; özel artifacts korunur.

## Başarılı düzeltme ve canlı doğrulama

- Düzeltme M1 dalında [75afeeb](https://github.com/sq0eezy/expedition-73/commit/75afeeb) ile kaydedildi/paylaşıldı, main'e [96815c5](https://github.com/sq0eezy/expedition-73/commit/96815c57a765efc988401e9563a18f10aaad7c04) ile normal merge edildi. Sonraki yayın kaydı güncellemesi yalnız belgelerdir; analiz için doğrulanan kaynak bu commit'tir.
- [Ubuntu analiz işi](https://github.com/sq0eezy/expedition-73/actions/runs/39130524169): **başarılı**. Python 3.12, 134 test / 6,372 saniye; gerçek A/B nokta ve eşleşme, A pencere, B parçalı pencere, 56/55 hücre fraksiyon replay'leri başarılı. İki `run-surface-workflow` koşusunda beşer düğüm completed ve 12/12 ay; NASA erişim anahtarı veya canlı API isteği gerekmedi. Bu, gerçek macOS çalıştırması değildir.
- [Pages işi](https://github.com/sq0eezy/expedition-73/actions/runs/39130524210): **başarılı**, strict build ve deploy tamamlandı. UTC **2026-10-18 13:13:27**'de `evidence/SURFACE_WORKFLOW/`, `evidence/SURFACE_RELEASE/` ve `assets/reader/catalog.json` HTTP 200; sırasıyla yeni komut, önceki CI kaydı ve yayın belgesi işaretleri içerikte görüldü.
- [Ortak panel](https://sq0eezy.github.io/expedition-73/) güncellendi; okumak için pull/kurulum gerekmez. Yerel kaynakları kullanan kişinin kendi değişikliklerini koruyarak main'i kendi dalına alması gerekir. M2'nin `791e07c` dalı korunur; bu yeni teslimi incelediği veya Mac'te çalıştırdığı varsayılmaz. M1 yeni geliştirmeye `codex/m1-modules-region-a` üzerinde devam eder.

Paylaşılan site yönetim portalıdır. Maske/buz politikası, bilimsel grid/alan/dönem, uzun dönem istatistik ve son kullanıcı analiz web uygulaması hâlâ açıktır. İlk başarısız CI kaydı silinmedi; başarılı yeni iş onun çözüm kanıtıdır.
