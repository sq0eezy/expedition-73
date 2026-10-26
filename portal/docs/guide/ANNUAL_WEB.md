---
status: Validating
updated: "2026-10-26"
review_summary: "Yıllık ağırlık adaylarını, kaynak yıllık hücre özetini ve 24 yılın farklarını webde inceleme."
change_summary: "Ayrı yıllık sonuç dosyası aylık kataloğa bağlandı; maske kapsamı, tablo/yıl odağı ve kaynak uyuşmazlığı davranışı eklendi."
---
# Yıllık adayları webde incele

[Python yıllık ağırlık hesabının](T2M_ANNUAL_WEIGHTING.md) iki adayı, uzun dönem aylık grafiğinin altındaki **Ayları nasıl birleştiriyoruz?** bölümünde görünür. [Yöntem hedefleri](../research/TEMPORAL_AGGREGATION.md), [gerçek ekran/derleme kanıtı](../evidence/ANNUAL_WEB_CHECK.md). Hiçbir ağırlık yöntemi seçilmiş bilimsel profil olarak sunulmaz.

## Kullanım

Windows CMD depo kökünde `scripts\start-preview.cmd`; Mac'te `sh scripts/start-preview.sh`. Üst yıl/pencere seçimi yıllık bölüme de uygulanır. Her görünür pencerede seçilen yılın eşit ay/gün sayısı adayları ve API yıllık hücrelerinin aynı alan ağırlıklarıyla özeti bulunur. API değeri bağımsız ölçüm veya hata payı değildir. Tam ay/gün kapsamı ve takvim ayrıca gösterilir.

Bu ilk yıllık modül **yalnız maskesiz** geçmişi kullanır. Kara/kara+buz seçince yıllık kartlar kapanır ve kapsam açıklanır; maskeli sonuç yerine maskesiz değeri göstermekten kaçınılır. Aylık grafik ve mevcut yüzey duyarlılığı çalışır. Tek/boş pencere seçimi yıllık bölüme de uygulanır.

Her kartta 24 yılın takvim günü−eşit ay farkı çizilir; bu bir ısınma/eğilim grafiği değildir. **Bütün yılları tablo olarak incele** 24 yılın sayısal değerlerini gösterir; yıl düğmesi aylık ayrıntıları aynı yıla taşır. Tablo/kaynak açıklaması açık kalır ve klavye odağı seçilen yıl düğmesinde korunur. Eksik ayda iki aday boş görünür; varsa API yıllık referansı ayrı kalır, doldurma yapılmaz.

## Veri bağı ve hata durumu

Builder bütün yıllık kayıtları `annual_weighting.run` ile ham kaynaklarından yeniden doğrular. Yıllık ve aylık derlemelerin her yıl için sıcaklık dosya hash'leri eşleşmezse yeni karışık çıktı üretilmez. Aylık **data/results.json aynı byte kaydı** olarak kalır; yeni **data/annual.json** yalnız bu kataloğun SHA-256 kimliğine bağlanır. İçinde 0.1.0 web zarfı ve mevcut 0.1.0 bilimsel aday raporları vardır.

Tarayıcı kaynak bağını, yöntem/aday bayraklarını, birim/takvim/yıl/ay kapsamını, ağırlıkları ve rapor içi farkların tutarlılığını denetler; yıllık sıcaklık ortalamalarını yeniden hesaplamaz. Matematiksel hesabın sahibi Python modülüdür. Hash bağı veri tutarlılığı içindir; yazar imzası veya bilimsel kabul değildir.

Yıllık dosya yoksa/bozuksa/başka kataloğa aitse veya Web Crypto yoksa yıllık bölüm kullanılamaz; geçerli aylık ekran çalışır. Eski tek yıllık kayıtta yıllık geçmiş bulunmadığı açıkça belirtilir. Genel yeniden yüklemede eski bir asenkron yıllık yanıt yeni kayda uygulanmaz. Tarayıcı NASA/token kullanmaz; iki genel JSON dosyasını yerel statik sunucudan okur.

## Sözleşmeler ve sınırlar

Aylık web 0.4.0, yıl snapshot'ı 0.3.0, karşılaştırma raporu 0.1.0 ve mevcut kaynak şemaları korunur. Yeni yıllık web zarfı `recorded_annual_weighting_web_preview` 0.1.0; **yedi genel dosya**, ZIP manifesti **0.4.0** vardır. Verifier önceki 0.1.0–0.3.0 manifestlerini kendi dosya listeleriyle açar. Aylık rapor indirme/açma kapsamı değişmedi; yıllık kartlar o rapora yeni istatistik eklemez.

Mevcut beş düğümlü akış ekranı aylık yüzey hesabını anlatır. Yıllık modül derlemede ayrı doğrulanır; bu akış grafiğinde yeni bir işlem gibi gösterilmedi. Bilimsel yüzey/sınır/dönem ve ağırlık kararı, M2 incelemesi, anomali/eğilim/aralık/p-değeri hâlâ açık. GitHub geliştirme dalına gönderim main/Pages yayını değildir; güncel paylaşım durumu [SYNC](../team/SYNC.md) içindedir.
