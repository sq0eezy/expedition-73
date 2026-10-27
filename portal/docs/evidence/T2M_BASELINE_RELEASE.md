---
status: Validating
updated: "2026-10-27"
review_summary: "Mevcut testli T2M temelinin ilk toparlama paketi olarak main'e alınması."
change_summary: "Kullanıcı main teslimlerine başlamayı istedi. c682441 kodu beş uzak işi geçti; birleştirme ve Pages sonucu ayrı kaydedilir."
---
# T2M temeli · Main teslimi

2026-10-27, M1 yapılanları main'e almaya başlanmasını ve adım adım toparlamayı istedi. Başlangıç temiz 43a3e03; M1 geliştirme dalı. Ekip/durum/harita/fikir/devir/pano ve pilot bitiş ölçütleri okundu. Fetch'te origin/main a1a83d5, origin/M2 6047c42 aynı; M1'e alınmamış katkı yoktu. Yerel main 6da0103 idi, origin/main'in gerisinde ve yerelde fazladan commit yoktu. [Kapsam/sıra](../planning/CONSOLIDATION.md), [sıcaklık bitiş durumu](../planning/PILOT.md#2026-10-27-bitis-durumu).

## İncelenen kaynak ve doğrulama

Uygulama kaynağı **c68244169258af16ea3cde2e6d8cf5d2e5d57411**; 43a3e03 ile fark yalnız dört portal belgesiydi. [40461143919](https://github.com/sq0eezy/expedition-73/actions/runs/40461143919) iş durumları ve beş tam günlük okundu; tamamı success:

| İş | Python / JS | Ek sonuç |
|---|---|---|
| Windows | 238 / 139,596 s; 48 JS | Gerçek replay/build ve yedi dosyalı paket doğrulandı |
| Ubuntu | 238 / 277,129 s; 48 JS | Gerçek replay/build ve paket doğrulandı |
| macOS ARM64 | 238 / 151,641 s; 48 JS | Gerçek replay/build ve paket doğrulandı; M2'nin kendi cihaz kabulü değildir |
| Docker AMD64 | 238 / 258,446 s; 48 JS | Ağsız replay/build ve HTTP smoke geçti |
| Docker ARM64 | 238 / 193,596 s; 48 JS | Native hostta ağsız replay/build ve HTTP smoke geçti |

Önceki [87 yerel Chrome ve gerçek paket/byte kontrolü](ANNUAL_TRACE_CHECK.md) aynı kaynak içindir; bu oturumda yeni Chrome koşusu yapılmadı. Mevcut kod değişmediği için aynı Python suite'i sırf belge/toparlama için tekrar yerelde çalıştırılmadı. Main sonrası CI aynı kaynağın bütünleştirilmiş ortamını ayrıca kontrol eder.

Main'den fark 320 kaynak dosyası; büyük kısmı kayıtlı açık NASA örnekleri. Kod/sözleşme/örnekler ve web builder birbirine bağlı tek teknik temel olarak incelendi. Core hesap, çağrı/adaptörler, derleme/ZIP/CI ve yayın iş akışları karşılaştırıldı; yeni arayüz/ikinci modül kodu eklenmez. git diff --check geçti; outgoing yollarda .env/venv/generated dist/artifacts yok. Ham örnek byte koruma ayarı korunur. Paketlerin her platformda kendi hash'leri doğrulandı; bütün ZIP'lerin platformlar arasında byte eşitliği iddiası yok.

## Birleştirme ve yayın kaydı

Açık Copilot PR #1 metni/yorumları okundu: f0bca80 boş plan, sıfır değişen dosya, yorum yok. Bu PR'dan kod veya M2 görüşü alındığı varsayılmaz; değiştirilmez. Bu teslim için mevcut M1 dalından PR yolu denenir; gerçek PR/merge veya yetki hatası sonrası normal Git yolu burada kaydedilir. Reset/force kullanılmaz, M2 dalı korunur.

Main birleştirme SHA'sı, uzak eşleşme, yeni CI/Pages ve HTTP sonucu işlem sonrası eklenir. Portal Pages workflow yalnız portal/site yayımlar; yeni sonuç uygulaması hosting'i kurulmaz. Bilimsel profil/eğilim tamamlandı veya M2 kabul etti sayılmaz. Toparlama ve arayüz taslakları belge değişikliğidir; portal check/build sonucu analiz testi yerine kullanılmaz.
