---
status: Validating
updated: "2026-10-26"
review_summary: "Kayıtlı aylık T2M değerlerini bütün dönem boyunca inceleme ve seçilen ayı ayrıntılara bağlama."
change_summary: "288 aylık grafik/tablo, ortak pencere-yüzey seçimi ve klavyeli ay geçişi eklendi; istatistik/eğilim hesabı yok."
---
# Kayıtlı ayların uzun dönem görünümü

M1'in devam talebiyle [2001–2024 aday kayıtları](T2M_LONG_PERIOD.md) tek zaman eksenine bağlandı. Her pencere için 288 aylık **mevcut değer** çizilir; yeniden sıcaklık hesabı, yıllık ortalama, yumuşatma, anomali, eğilim veya iklim etkisi eklenmez. [Gerçek kontrol](../evidence/TIMELINE_PREVIEW_CHECK.md).

## Kullanım

Depo kökünde Windows CMD `scripts\start-preview.cmd`; Mac'te `sh scripts/start-preview.sh`. Yıl grafiğinin altında **Aylar boyunca birlikte bak** bölümü bulunur. Üstteki aday pencere ve yüzey seçimi iki grafiğe de uygulanır. Dönem ve her pencerenin geçerli ay sayısı gösterilir; boş seçimde eski grafik/tablo temizlenir.

Uzun dönem **Ay seç** kaydırıcısı bütün kayıtlı ayları sırayla dolaşır. Klavyede oklar bir ay, Home/End ilk/son aya gider; odak yıl değişiminde korunur. Seçilen ay mevcut yıl/ay alanını, hücreyi, kaynakları, hesap akışını ve pencere karşılaştırmasını birlikte günceller. Üstteki yıl/ay seçimi veya eski rapor açılması da uzun dönem işaretçisini aynı tarihe taşır. İki görünümün ayrı tarih seçimleri yoktur.

**Bütün kayıtlı ayları tablo olarak incele** her ayı ve her görünür pencereyi altı ondalık gösterir. Bu gösterim basamağı ölçüm doğruluğu değildir. Tablo açılınca dikey kaydırılabilir; grafik bütün ayları gösterir, ay atlamaz/seyreltmez. Eksik değer sıfırla doldurulmaz; çizgi o ayda kesilir ve tablodaki değer “Veri yok” olur. Tamamen eksik seriye yapay çizgi eklenmez. Dikey ölçek görünür seri/değerlere göre değişir.

## Yıllar arasında teknik uygunluk

Saf `recordedMonthlyHistory` mevcut comparison.mjs içindedir; aynı pencerenin yılları arasında şunları denetler:

- Tam/sıralı/takip eden yıllar, her yılın 12 ayı ve seçilen pencerenin her yılda bulunması.
- Gösterge/yükseklik/birim; takvim/zaman standardı; kaynak/ürün/API ve kaynak üyeleri.
- Pencere kimliği, aday sınır/sürüm, grid/alan yaklaşımı, hücre geometrisi/alanı ve kullanılan yüzey ağırlıkları.
- Yalnız tüketilen işlemlerin sürüm/çıktı sözleşmeleri. Kara seçeneklerinde sabit fraksiyon ürünü/sürümü/kayıt hash'leri ve yerleşim varsayımı.

Pencerelerin birbirleriyle aynı geometriye sahip olması istenmez; A kendi yıllarıyla, B kendi yıllarıyla eşleşir. Her yılın sıcaklık ham yanıt hash'i doğal olarak farklıdır; bu kimliklerin aynı olması istenmez. Fraksiyon kullanılmayan maskesiz görünüm, yalnız fraksiyon/başka kullanılmayan işlem değişti diye engellenmez. Kayıt sırası dışında JSON anahtar/hücre/kaynak üyesi sıralaması anlamsal fark değildir.

Uygunluk sağlanmazsa uzun dönem çizgisi/tablosu üretilmez ve açıklama gösterilir; geçerli tek yıl görünümü kullanılabilir. Bozuk genel katalog/annual sözleşmesi önceki yükleme denetiminde tüm kaydı reddedebilir. Bu teknik eşleşme, bilimsel dönem/maske/sınır seçimi veya model doğruluğu kanıtı değildir.

## Sözleşme ve yorum sınırı

Yeni NASA isteği, token, sunucu hesabı veya kalıcı cache yoktur. Mevcut kayıtlı data/results.json byte'ları değişmedi; web 0.4.0, yıllık snapshot 0.3.0, rapor 0.1.0, ZIP manifesti 0.3.0 ve altı genel dosya korunur. JSON indirme/karşılaştırma raporu **seçili yıllık kayda** aittir; bütün dönemin bilimsel raporuna dönüşmedi.

Kara/kara+buz seçenekleri aynı sabit fraksiyon örneğinin aday ağırlıklarını kullanır; tarihsel maske/ayrı kara sıcaklığı doğrulanmış sayılmaz. Kaynak AREA ve kesilmiş hücre alanı varsayımları aynı kalır. Mevsimsel dalgalanmaya bakarak ısınma/soğuma sonucu çıkarılmaz. Ortak bilimsel sınır/yüzey/dönem, yıllık özet ve istatistik yöntemi hâlâ açık; M2'nin yeni ekranı veya profili kabul ettiği varsayılmaz.
