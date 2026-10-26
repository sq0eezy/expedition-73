---
status: Validating
updated: "2026-10-24"
review_summary: "Aday 2001–2024 döneminin gerçek yıllık T2M kaynakları ve inceleme sınırları."
change_summary: "A/B için 288'er ay alındı; web yıl kataloğu 24 yıla genişletildi. Bilimsel dönem/maske ve eğilim hesabı açık."
---
# 2001–2024 · Gerçek kaynak ve yıl kataloğu

**2026-10-26 güncel arayüz:** [Kayıtlı 288 ay görünümü](T2M_TIMELINE.md) eklendi. Bu sayfadaki ilk tek yıl ekranı ve sonraki görünüm önerisi 2026-10-24 aşamasına aittir; kaynak erişimi ve bilimsel sınırlar korunur.

M1'in devam talebiyle [iki yıllık erişim altyapısı](T2M_HISTORY.md) daha uzun aday dönemde çalıştırıldı. Bu çalışma kesin bölge/sınır, bilimsel dönem, maske veya istatistik yöntemini seçmez. [Gerçek kontrol kaydı](../evidence/T2M_LONG_PERIOD_CHECK.md).

| Kayıt | A aday penceresi | B aday penceresi |
|---|---|---|
| Zaman | 2001-01…2024-12 | 2001-01…2024-12 |
| Eksiksiz aylık kayıt | 288/288 | 288/288 |
| Kesişen grid hücresi | 56 | 55 |
| Tekil hücre × ay | 16.128 | 15.840 |
| Coğrafi istek/yıl | 1 | 2; 5 ortak hücre tekilleştirilir |

2001–2022 için A'da 22, B'de 44 yeni küçük NASA POWER isteği yapıldı; otomatik retry kullanılmadı. Kayıtlı 2023/2024 kaynakları byte aynı kopyalandı. Tamamlanan yıllar, ayrı yıllık kayıtlar olarak ignored artifacts içinde tutulup açık seed'lerle birleştirildi. Bu bir kalıcı cache veya otomatik güncelleme hizmeti değildir. Küçük ham JSON alt kümeleri tekrar doğrulanabilmesi için examples içinde yer alır; tüm NASA arşivi indirilmez. Tarayıcıda NASA erişimi veya token yok.

## Kullanım ve doğrulama

Windows CMD depo kökünde `scripts\start-preview.cmd`; Mac'te `sh scripts/start-preview.sh`. **Kayıtlı yıl** 2001…2024 seçeneklerini sunar; varsayılan 2024'tür. Dönem satırı kayıtlı yıl/ay sayısını belirtir. Ana grafik ve pencere farkı yalnız seçili yılın 12 ayını gösterir. Tek çizgide 288 ay grafiği, yıllık ortalama/anomali, eğilim veya p-değeri eklenmedi.

Windows CMD, analysis içinde:

```cmd
.venv\Scripts\python.exe -m expedition73 validate-window-history examples/a-history-2001-2024
.venv\Scripts\python.exe -m expedition73 validate-window-history examples/b-history-2001-2024
```

Mac'te aynı argümanlarla `.venv/bin/python`; depo kökünde `analysis/.venv/bin/python scripts/workspace.py check`. Yeni Mac doğrulaması yapılmış sayılmaz. Ortak check eski iki yıllık ve yeni uzun kayıtları ayrı ayrı tekrarlar. B reusable erişim örneği M2'nin R-B05 görevine başladığı veya bilimsel politika kabulü değildir.

## Kayıt ve yorum sınırı

Her yıl orijinal ham yanıt/istek/sonuç ve varsa tile manifestini korur. Parent history.json bütün yıllık byte hash'lerini taşır; sonuç her ham kayıttan yeniden üretilir. Kaynak/API sürümü v2.10.0, MERRA2, LST, grid/geometri, gösterge/birim ve alan yöntemi eşleşti. Bütün aylarda bütün kesişen hücreler mevcut; eksik aylık alan yok. Bu kontroller sağlayıcının vermediği piksel QA'sını, gözlem doğruluğunu, model hatasını veya bilimsel temsil gücünü doğrulamaz.

Web kataloğu 0.4.0, yıllık snapshot 0.3.0, rapor 0.1.0 ve ZIP manifesti 0.3.0 korunur; altı genel dosya vardır. 2023/2024 yıllık snapshot kimlikleri değişmez; eski raporlar aynı yıllık kayda bağlanabilir. Katalog 8 MB işlem sınırı içinde tutulur. 24 yılın aynı ekranda bulunması tek başına yıllar arasında istatistik/karşılaştırma yöntemi tanımlamaz.

Kara/kara+buz seçenekleri bütün yıllarda aynı kayıtlı **sabit** M2C0NXASM fraksiyonlarını yalnız aday ağırlık duyarlılığı için kullanır. Tarihsel arazi değişimi, değişmeyen bilimsel maske veya ayrı kara sıcaklığı sonucu değildir. Kaynak AREA hâlâ yok; küresel alan/kesilmiş hücre varsayımları korunur. Kesin sınır/yüzey/dönem ve eksik veri/istatistik profili kararlaştırılmadan eğilim bilimsel sonuç diye sunulmaz. Sıradaki teknik öneri kayıtlı 288 ay için kesintisiz zaman görünümüdür; eğilim yöntemi ayrı karar olarak açık kalır.
