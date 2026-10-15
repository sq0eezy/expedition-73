# Mimari önerisi

**Durum: Proposed.** Uygulama kodu yok; bileşenler ve araçlar seçilmedi.

İlk demo için değerlendirilecek yaklaşım: NASA sayısal verisini bir hazırlık adımında işleyip küçük, sürümlü sonuç dosyaları üretmek; web arayüzünde bunları harita ve grafikle göstermek. Böylece ürün seçimi ile etkileşim tasarımı ayrı ayrı sınanabilir. Canlı analiz API'sine ihtiyaç olup olmadığı veri boyutu ve deneyim üzerinden kararlaştırılacak.

- [Sistem haritası](SYSTEM_MAP.md): önerilen bileşenler.
- [Veri ve akışlar](DATA_AND_FLOWS.md): izlenebilirlik ve çıktı sözleşmesi.
- [Sınırlar](BOUNDARIES.md): portal, analiz ve uygulamanın sorumlulukları.

## Teknoloji kararı bekliyor

Python tabanlı veri hazırlığı, web tabanlı bir arayüz, harita ve grafik kütüphaneleri değerlendirilebilir. Framework, backend, veritabanı veya barındırma seçilmedi. Önce küçük sayısal veri örneğini ve çıktı boyutunu görmek gerekiyor.
