---
status: Verified
updated: "2026-10-27"
review_summary: "Mevcut testli T2M temelinin ilk toparlama paketi olarak main'e alınması."
change_summary: "6db86b2 main'de; main CI beş işte 238 Python/48 JS ile, Pages/HTTP ile geçti. Teknik temel teslim edildi; yeni arayüz/modül ve bilimsel pilot ayrı."
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

Hazırlık belgeleri öncesinde main'den fark 320 kaynak dosyasıydı; ilk merge ağacında 324. Büyük kısmı kayıtlı açık NASA örnekleri. Kod/sözleşme/örnekler ve web builder birbirine bağlı tek teknik temel olarak incelendi. Core hesap, çağrı/adaptörler, derleme/ZIP/CI ve yayın iş akışları karşılaştırıldı; yeni arayüz/ikinci modül kodu eklenmedi. git diff --check geçti; outgoing yollarda .env/venv/generated dist/artifacts yok. Ham örnek byte koruma ayarı korunur. Paketlerin her platformda kendi hash'leri doğrulandı; bütün ZIP'lerin platformlar arasında byte eşitliği iddiası yok.

## Birleştirme ve yayın kaydı

Açık Copilot PR #1 metni/yorumları okundu: f0bca80 boş plan, sıfır değişen dosya, yorum yok. Bu PR'dan kod veya M2 görüşü alındığı varsayılmaz; değiştirilmedi. Yeni teslim PR oluşturma çağrısı **403 Resource not accessible by integration** verdi; PR oluşmadı. Bu, Codex otomatik onay reddi değil GitHub entegrasyon yetkisidir. Kullanıcının açık main talebiyle incelenmiş dal normal Git merge/push yoluyla aktarıldı; reset/force kullanılmadı.

M1 hazırlık belgesi commit'i **6b7b290** normal push ile paylaşıldı. Temiz çalışma alanında origin/main'in M1'in atası olduğu doğrulandı; yerel main origin/main'e ff-only ile getirildi, M1 --no-ff ile birleştirildi. **6db86b27626f024527f16b41e585bd96413ef034** main'e normal push ile gönderildi; ls-remote eşleşti. Birleşen ağaç M1 6b7b290 ile git diff --quiet sonucunda aynıydı; c682441'den fark yalnız AGENTS/portal belgeleridir. M2 uzak dalı 6047c42 olarak korundu. M1 dalına dönülüp yeni main ff-only alındı; sonraki geliştirme yine ayrı daldadır.

Main ağacında portal check/strict build **3,89 s** ile geçti. [Main analiz CI 40464061367](https://github.com/sq0eezy/expedition-73/actions/runs/40464061367) aynı merge SHA'sında ilk gözlem in_progress, son gözlem **beş iş success**. Beş tam günlük okundu: her iş **238 Python/48 JS**, bütün offline kaynak/akış tekrarları ve builder başarılı. Python süreleri Windows 274,734 s; Ubuntu 150,042 s; macOS 144,219 s; Docker AMD64 263,663 s; native Docker ARM64 193,602 s. Üç native iş paket doğrulamasını, iki Docker işi yedi dosya/bağ/MIME/özel yollar HTTP smoke'unu geçti. Bu, önceki kaynak CI'sından ayrı gerçek main doğrulamasıdır. Bilimsel profil veya M2'nin kendi cihaz kabulü değildir.

[Pages 40464061377](https://github.com/sq0eezy/expedition-73/actions/runs/40464061377) aynı SHA için build ve deploy success. Canlı planning/CONSOLIDATION/, product/COMPARISON_WORKSPACE/ ve planning/PILOT/ sayfaları HTTP200, beklenen yeni içerikle doğrulandı. Portal Pages workflow yalnız portal/site yayımlar; yeni sonuç uygulaması hosting'i kurulmadı. Bilimsel profil/eğilim tamamlandı veya M2 kabul etti sayılmaz. Bu kayıt sonraki belge commit'iyle de main'de paylaşılır; uygulama kodunu değiştirmez, yeni bilimsel/Chrome test sayılmaz.
