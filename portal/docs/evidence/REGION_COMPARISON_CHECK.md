---
status: Validating
updated: "2026-10-22"
review_summary: "Kayıtlı iki pencerenin aynı ay farkı; teknik eşleşme, eksik aylar ve bilimsel yorum sınırı."
change_summary: "Pencere çifti/yönü, üç ağırlık seçeneği, fark grafiği/tablosu ve eşleşme koşulları yerelde doğrulandı: 180 analiz, 22 JS ve 36 Chrome senaryosu."
---
# İki pencereyi karşılaştırma · Gerçek kontrol

## Kaynak ve kapsam

M1 devam istedi. Başlangıçta güncel durum/harita, iki üye, fikir/devir/pano ve paylaşım kayıtları okundu. Temiz M1 dalı `ca485eb`, uzak M1 `6047c42`; fetch sonrası main/M2 `a1a83d5` olarak aynı, yeni katkı yok. M2'nin son macOS/B kaydı esas alındı; yeni ekran/Docker veya bilimsel politika kabulü çıkarılmadı.

Yeni hesap saf `web/src/comparison.mjs` içinde `summarizeRegionDifferences(left, right, policy)` ile yapılır. Kaynak, aynı builder'ın doğruladığı gerçek A/B 2024 sonuçlarıdır. İki kayıt arasında **aynı aylık sıcaklık göstergesinin betimsel mekânsal farkı** çıkarılır; yeni NASA isteği, ikinci bilimsel gösterge veya bilimsel karşılaştırma profili eklenmedi. Analiz motoru/örnekleri, kaynak hash'leri, web sözleşmesi 0.3.0, teknik profil 0.1.0, altı genel dosya ve ZIP manifesti 0.2.0 korunur. JSON indirme mevcut seçili bölge girdilerini taşır; yeni fark özeti indirme zarfına eklenmedi.

## Teknik eşleşme kapısı

Farklı kimlik, aynı T2M/2 m/degC, tam aynı aylık takvim/dönem/zaman standardı, sıcaklık kaynağı/ürün/API sürümü/kaynak üyeleri, grid/alan yaklaşımı ve **kullanılan** işlemlerin sürüm/çıktı sözleşmesi kontrol edilir. Kara ağırlığı seçilirse fraksiyon ürünü/sürümü, kaydedilmiş tam DMR hash'i ve homojen fraksiyon yerleşim varsayımı da eşleşmelidir. Bu fraksiyon kontrolü mevcut sabit ürün snapshot'ı için temkinli bir teknik koşuldur; genel bilimsel uygunluk kuralı değildir. Maskesiz fark için fraksiyon kullanılmıyor olarak gösterilir. Aynı verinin tek istek veya iki tile ile alınması, farklı ham yanıt hash'i veya bölgeye özgü tanım parmak izi tek başına uyumsuzluk sayılmaz.

İşlem sürümü/sözleşmesi yalnız tüketilen akış için kontrol edilir: LandIce sürümü değişirse kara hesabı bundan dolayı engellenmez; Temperature her seçenekte ortaktır. Uyumsuzlukta fark grafiği/tablosu/kartları temizlenir ve teknik koşul tablosu açılır. Önceden var olan üstteki iki pencere fark kartı da aynı kapıdan geçer. Gösterge/dönem/sağlayıcı gibi temel bozukluklarda mevcut bütün ekranı reddetme kuralı ayrıca korunur. Teknik eşleşme bilimsel sınır/maske/dönem kabulü veya kaynak doğruluğu değildir.

## Betimsel hesap ve görünüm

Kullanıcı, görünür kayıtlar içinden farklı iki pencere seçer; yönü çevirince sol−sağ işareti tersine döner, maksimum |fark| ve ayları değişmez. Aynı yüzey seçeneği iki pencerede de kullanılır. Her ayda iki değer de varsa fark alınır; aksi halde null bırakılır ve çizgi kesilir. Gerçek sıfır korunur. Maksimum mutlak fark yalnız geçerli çiftlerde bulunur; tüm tam bağlar/ayları korunur. Hiç geçerli çift yoksa maksimum null/ay listesi boş kalır. Sonlu olmayan aritmetik reddedilir; gösterimde üç ondalık kullanılır, hesap önce yuvarlanmaz.

Seçili ay farkı, yıllık en büyük mutlak fark/ayları, ayrı geçerli çift sayısı, sıfır merkezli aylık çizim, erişilebilir tablo ve açılır teknik kontrol tablosu vardır. Bir veya sıfır pencere seçildiğinde eski grafik/tablo temizlenir. Yeni uygun kayıt eklendiğinde seçim mantığı aynı kalır; A/B adları kod içine bağlanmadı.

Gerçek A−B 2024 çıktıları, **12/12 geçerli çift**:

| Ağırlık | Ocak farkı °C | Yılın en büyük mutlak farkı °C | Ay |
|---|---:|---:|---|
| Maskesiz | 23,73591292791919 | 26,184637157262063 | Mart |
| Kara | 23,73549097404354 | 26,163601232011434 | Mart |
| Kara + kara buzu | 23,73605971304875 | 26,163316698608497 | Mart |

Bu farklılıklar aynı 2024 ayının iki aday coğrafyasını karşılaştırır. İklim değişikliği etkisinin, ısınma/soğuma eğiliminin, ilişki/nedenselliğin veya anlamlılığın farkı değildir. Kara fraksiyonu ağırlığı ayrı kara sıcaklığı çıkarmaz; küçük politikalar arası fark doğruluk/maske onayı değildir.

## Gerçek doğrulama · 2026-10-22

- Windows/Python 3.12.14, `analysis\.venv\Scripts\python.exe scripts/workspace.py check`: **180 test / 34,953 s**, atlama/hata yok. A/B nokta uyumu, A alan ve B tiled-window (iki tile/5 tekrar çıkarıldı/55 hücre), 56/55 fraksiyon dönüşümü ve iki gerçek beş düğümlü akış geçti. Mevcut NetCDF/NumPy deprecation ve bilerek bozuk ZIP duplicate-entry uyarıları mevcut; başarısız test yok.
- Aynı komutta **22 JS testi / 149,688 ms**, üç JS sözdizimi kontrolü ve builder başarılı. Dokuz yeni JS testi yön/bağlar/immutability, temel metadata uyumsuzlukları, tüketilen sürümler, maskeye bağlı kaynak/DMR/yerleşim, politika bazında eksik ay/sıfır, tüm çiftler eksik, geçersiz takvim/politika/overflow, kaynak sırası/üyeliği ve gerçek A/B'nin üç politikasının doğrudan çıkarma ile eşleşmesini kapsar.
- `web/serve.py` loopback 8873, `scripts/smoke_preview.py`: altı dosya 200, .mjs JavaScript MIME, özel/kaynak yolları 404. Codex panel açma isteği queued; kullanıcının sayfayı gördüğü varsayılmadı.
- Yerel kurulu Chrome headless/Playwright ile `node web/tests/browser.cjs`: **36 senaryo grubu**, JS hatası/dış runtime isteği 0. Yeni kontroller gerçek çift/yön/ay/politika/maksimumlar, tek/boş seçimin temizliği, eksik çiftler, tüm çiftler eksik, Land sürümü uyumsuzluğunda panel ve üst fark kartının engellenmesi, LandIce seçimine dönüşte toparlanma ve üçüncü kayıtla dinamik seçimdir. Üçüncü kayıt yalnız testte A'nın C isimli yapay UI kopyasıdır; yeni gerçek bölge/veri değildir. 1440×1100 ve 390×844 ekranlar görsel incelendi; yatay sayfa taşması yok.
- Yeni demo iki kez paketlendi: **333.744 byte**, SHA-256 `b00faba7e25062dd8a175dbd7265d3796681bd73a302476fd9b9c0a709ed6336`, baytları aynı ve altı dosya/manifest doğrulandı. Önceki 0.3.0 ZIP içindeki data/results.json ile yeni builder çıktısı byte düzeyinde aynı; yeni bilimsel veri eklenmedi. Paketler/görseller ignored web/artifacts içinde kalır.

Bu dilimde gerçek Mac, yeni Docker/Linux/ARM64 veya uzak CI çalıştırılmadı. Önceki Linux/ARM64 kanıtı bu yeni JS davranışının koşusu sayılmaz. Bilimsel maske/sınır/uzun dönem, nihai yığın ve hosting açık. U-02 Validating; [H-M1-016](../team/HANDOFFS.md) panel içi inceleme kaydıdır. Yeni dilim yerel M1 dalında; push/main/Pages/Sites veya dış mesaj yok. Portal kontrolleri bilimsel sonuç kabulü değildir.

QA sunucusu kapatıldı; 8873 TCP bağlantısı kapalı doğrulandı. Yeniden açma: Windows depo kökünde `scripts\start-preview.cmd`, Mac için `sh scripts/start-preview.sh`; sonra localhost 8873. Kaynak örneklerde Git farkı yok ve diff --check geçti.

2026-10-22 son kontrol: Portal içerik check ve strict build başarılı; bu belge kontrolü bilimsel kabul değildir.
