---
review_summary: "M1: modüller ve A; M2: B. Paralel başlanacak işler, ortak profil ve karşılıklı teslimler."
change_summary: "2024 pilotu ile NASA zaman kapsamı ayrıldı; iki yıl/12 ay kod sınırları ve önerilen çok yıllı geçiş sırası açıklandı. Dönem seçimi/veri alımı yok."
---
# İki bölge için iş bölümü

**2026-10-16:** Kullanıcı kendisinin modülleri ve A'yı, arkadaşının B'yi yapacağını belirtti: [ADR-005](../decisions/ADR-005-TEAM-OWNERSHIP.md). M2 adına bağımsız kabul/başlama beyanı yazılmadı. Atama, görüş ve gerçek ilerleme ayrı kaydedilir. Görev durumlarının esas kaynağı [iş panosudur](WORK_BOARD.md).

| Kişi | Sorumluluk | İlk açacağı sayfa |
|---|---|---|
| Emeç · M1 | Ortak modüller, sözleşme/adaptör ve Bölge A | [A ve modül görevleri](REGION_A.md) |
| sq0eezy · M2 | Bölge B girdileri, veri uygunluğu, hesap/sonuç kontrolü | [B görevleri](REGION_B.md) |

İlk pilot tek gösterge: 2 metre hava sıcaklığı. A/B iş kimlikleridir; mevcut Colorado Platosu/Kuzey Alaska adaylarının kesin seçildiği anlamına gelmez. Ürün, dönem ve analiz yöntemi de açık.

## Çalışma sırası

1. **Paralel:** İki kişi kendi bölge fişini ve küçük API erişim denemesini hazırlar (R-A01/02, R-B01/02). M1 ayrıca MOD-01 sözleşme taslağını hazırlar.
2. **Birlikte eşleştir:** A/B özetleriyle M1 önce ortak profil taslağını paylaşır (R-A03); M2 B'nin uygunluğunu inceler (R-B03); sonra profilin kullanılacak sürümü kaydedilir. M2'nin incelemeye başlaması için R-A03'ün bütünüyle bitmesi gerekmez. Eksik alan veya erişim sorunu varsa gerekçesiyle karar güncellenir.
3. **Ortak modülü teslim et:** M1 MOD-02/03'ü doğrulanabilir örnek ve sürümle hazırlar; M2 B'nin yapılandırmasını bu arayüze bağlar.
4. **Küçük hesabı çapraz kontrol et:** R-A04/B04'te tek tarih/az sayıda hücreyle ara hesap incelenir; hatayı tam dönem sonuç üretmeden yakala.
5. **Aynı sürümle iki alan:** R-A05/B05 tam seri, kapsam ve analiz üretir. R-A06/B06 yorum ve web kontrolünü tamamlar. A–B farkı için ayrıca uygun analiz gerekir.

## Ortak teknik deneme profili · 0.1.0, aday

**Kimlik:** `t2m-technical-2024`, sürüm `0.1.0`, durum **Candidate / teknik deneme profili uzlaştırıldı, bilimsel profil seçimi açık**. Bu tablo eldeki teknik denemelerin ortak özelliklerini kaydeder; nihai ürün/alan/dönem/maske veya istatistik kabulü değildir. Kodun bu profil belgesini çalışma zamanında otomatik tükettiği varsayılmadı. R-A03 taslağı hazırlandı. M2, `791e07c` ve 2026-10-19 güncellemesiyle teknik B uygunluğunu onayladı ve `t2m-technical-2024` (`0.1.0`) teknik deneme kimliği ile `monthly_window_series` (`0.2.0`) şema sürümü ayrımına katıldı: [inceleme](../team/SYNC.md). Nihai bilimsel profil, kesin sınır ve maske politikası seçildiğinde yeni sürüm/gerekçe yazılacak.

| Alan | Güncel kayıt |
|---|---|
| Profil kimliği/sürümü | `t2m-technical-2024` / `0.1.0`; kabul edilmemiş teknik deneme taslağı |
| Gösterge | 2 metre hava sıcaklığı; pilot seçildi |
| Sağlayıcı/ürün/sürüm ve API yolu | İki küçük örnekte NASA POWER Monthly and Annual API v2.10.0, kaynak `MERRA2`, monthly/point ve regional; nihai ürün seçilmedi. Doğrudan MERRA-2 dosya sürümüyle eşit sayılmaz. [Parçalı deneme kanıtı](../evidence/T2M_TILING.md) |
| A ve B sınır kimliği/sürümü | İki proje arama dikdörtgeni; `search-window-0.1.0`. A `[-113,36,-109,39]`, B `[-156,68,-150,70]`; kabul edilmiş analiz sınırı değil. [A fişi](../research/regions/REGION_A_PROFILE.md), [B fişi](../research/regions/REGION_B_PROFILE.md) |
| Ortak dönem/sıklık | Gerçek teknik örnekler 2024-01…2024-12, aylık, Gregoryen, LST. Uzun dönem seçilmedi; 2001–2024 aday |
| Birim/ölçek/eksik değer kuralı | T2M, degC, 2 metre; sağlayıcı C tanımı kontrol ediliyor. -999 dolgu ve dönmeyen ay ayrı null statüleri. Yıllık 13. kayıt aylara karışmıyor. Alan hesabında her pozitif destek hücresi gerekli |
| Kara/su maskesi ve alan/kesişim ağırlığı | Mevcut gerçek T2M örnekleri maskesiz; orta nokta hücre kenarı ve küresel dikdörtgen kesişim alanı yöntemi 0.1.0. A 56/B 55 hücre. M2C0NXASM 5.12.4 fraksiyon alt kümeleri (A: 56, B: 55 hücre) alınıp Windows, Ubuntu ve macOS'ta yeniden doğrulandı; `FRLAND` ve `FRLAND+FRLANDICE` aday duyarlılıkları hesaplandı, nihai kara/buz seçimi ve bilimsel uygunluk açık. [Maske araştırması](../research/SURFACE_MASK.md), [aday akış](../evidence/SURFACE_WORKFLOW.md) |
| Referans dönem/mevsim tanımı | Gerekliyse açıkça seçilecek |
| Analiz profili/sürümü ve varsayımlar | Seçilmedi |
| Modül/sözleşme sürümü ve örnek çağrı | Nokta ve tek istek 0.1.0, parçalı pencere 0.2.0, aday yüzey duyarlılığı 0.1.0. Bilimsel alan yöntemi aynı 0.1.0; farklı şemaları aynı sürümmüş gibi etiketlemeyin. [Çalıştırma](../guide/T2M_TILED_WINDOW.md) |
| Gözlenen uyumluluk/engeller | Nokta A/B aktarım/zaman kontrolünde 12 ay eşleşiyor; `inference_allowed=false`. A tek istek/B parçalı alan örnekleri ve 5 düğümlü aday yüzey akışı ayrı yeniden hesaplamalardan geçiyor; bölgesel bilimsel uygunluk onayı yok. Metadata ve sayısal fraksiyon alımı/dönüşümü doğrulandı; bilimsel maske tanımı açık |

## Bilimsel profil için karar bekleyenler

Kesin alan/poligon, kara/buz dahil etme kuralı, maskenin tam hücre oranını sınır parçasında kullanma yaklaşımı, gerçek maske alt kümesi, ortak uzun dönem, istatistik yöntemi ve belirsizlik incelemesi henüz seçilmedi. `preview-surface-mask` ayrı aday türdür; gerçek bölgesel seri veya nihai profil yerine geçirilmez. İki üyenin nihai bilimsel uygunluk kararı olmadan bu teknik tablo bilimsel kabul kaydı sayılmaz.

API kullanımı bütün arşivi elle indirmek zorunda olmak değildir. Öncelik gerekli küçük alt kümeye programla erişmek; sorgu, yanıt ve üretim izini korumaktır. [NASA POWER aylık API](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/) bir seçenektir; nokta yanıtı bölge ortalaması sayılmaz. POWER yanıtı doğrudan MERRA-2 dosyasıyla aynı ürün/sürüm diye etiketlenmez. Sağlayıcı değişikliği önce uygunluk kontrolünden geçer.

## Bir iş tamamlandığında

Kendi fişine gerçek sonuç ve kaynak ekle; panoda ilgili görev satırını güncelle. Diğer kişiden istenen girdiyi [devir listesine](../team/HANDOFFS.md), kısa niyet/özeti kendi üye notuna yaz. İnceleyen adı incelemenin yapıldığı anlamına gelmez. Dış bildirim gönderilmez; ortak sitede görünmesi için değişiklik GitHub main'e ulaşmalı.

## 2026-10-22 · Diğer yıllara geçiş açıklığı

M1, ekranın neden 2024 ile sınırlı olduğunu ve 2001–2024 verilerinin ne zaman geleceğini sordu; yeni kesin dönem/maske/sınır kabulü bildirmedi. 2024 gerçek teknik pilotudur, NASA veri kapsamının tamamı değildir. [NASA POWER Monthly belgesi](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/) 2026-10-22'de kontrol edildi: aylık meteorolojik parametreler MERRA-2 tabanlı olarak 1981-01-01'den önceki yıla kadar tarif ediliyor. Aynı sayfadaki 2001 başlangıcı CERES güneş verisi bölümündedir. Son mevcut yıl ve her konum/ayın doluluğu bu oturumda gerçek API sorgusuyla denenmedi; belgede kapsam olması eksiksiz piksel/ay kanıtı değildir. 2001–2024 proje aday dönemidir, API'nin evrensel alt/üst sınırı değildir.

Mevcut kod: power.py başlangıç/bitiş yılını işler; regional.validate_config istek başına en fazla iki takvim yılına izin verir. Bu projemizin pilot erişim sınırıdır; NASA belgesinden alınmış iki yıl iddiası değildir. web_preview.payload ve ön uç takvim/karşılaştırma/ay seçicileri bir tam yılın 12 ayına göre yazıldı. Yalnız istek URL'sini değiştirmek bütün ekranı çok yıllı yapmaz. Veriler kendiliğinden gelmez; istemci şu anda kayıtlı 2024 snapshot'ını okur.

**Önerilen sıradaki teknik paket:** Önce 2023–2024 gibi küçük bir aday iki yıllık kayıtla zaman parçalama/birleştirme ve ay-sürekliliği sınanır; ardından aday 2001–2024 için yıl parçaları, aynı grid/konum/birim/zaman sürümü, eksik/tekrarlı aylar ve kaynak kimlikleri denetlenir. 24 yıl × 12 ay = pencere başına 288 beklenen aylık kayıt; bu, 288 ayın gerçekten alındığı anlamına gelmez. Çok yıllı grafik/seçici/karşılaştırma ve rapor sözleşmeleri bundan sonra uyarlanır. Bir yıllık eski kayıtlar bozulmadan korunur.

Teknik erişim ve kalite denemesi için bilimsel maske kabulünü beklemek zorunlu değildir; aday/maskesiz olarak işaretlenir. Uzun dönem bilimsel sonuçta kesin sınır/yüzey hedefi/ortak dönem ve eğilim yöntemi ayrıca kararlaştırılır. Seriyi almak, eğilim veya anlamlılık hesabını tamamlamaz. R-A05/R-B05 Proposed kalır; bu açıklama bir uygulama, yeni veri alımı, M2 başlama/onayı veya süre taahhüdü değildir.

## 2026-10-22 · İlk iki yıllık uygulama

M1 önceki aşamalı öneri üzerine devam istedi. [Gerçek teknik history ve yıl ekranı](../guide/T2M_HISTORY.md) A/B 2023–2024 24/24 ay ile doğrulandı. 2024 kaynakları değişmedi; 2023 NASA API alımı eklendi. Bu ilk teknik aşamadır; kesin 2001–2024 dönem/maske/bölge veya eğilim yöntemi kabulü değildir. T-01 teknik deneme Validating, R-A05/R-B05 tam dönem/analiz görevleri açık; M2 adına başlama/onay yok. Sonraki erişim adımı daha uzun aday dönem, bilimsel profil uzlaşması ayrıdır.
