# Mimari önerisi

**Durum: Proposed.** Uygulama kodu yok; bileşenler ve araçlar seçilmedi.

## Yeni tartışma önerisi

Kullanıcının **bölge → veriye göre modüller → karşılaştırma** fikri [ayrı bir taslakta](REGIONAL_MODULE_PROPOSAL.md) işlendi. Kaynaklı [iki bölge adayı](../research/REGION_CANDIDATES.md) ve [ekip tartışması](../team/ideas/IDEA-M1-001.md) bağlantılıdır. Bu öneri kabul edilmiş mimari kararı değildir; aşağıdaki önceki temel yaklaşım ve sistem haritası uygulanmış sayılmaz.

İlk demo için değerlendirilecek yaklaşım: NASA sayısal verisini bir hazırlık adımında işleyip küçük, sürümlü sonuç dosyaları üretmek; web arayüzünde bunları harita ve grafikle göstermek. Böylece ürün seçimi ile etkileşim tasarımı ayrı ayrı sınanabilir. Canlı analiz API'sine ihtiyaç olup olmadığı veri boyutu ve deneyim üzerinden kararlaştırılacak.

- [Sistem haritası](SYSTEM_MAP.md): önerilen bileşenler.
- [Veri ve akışlar](DATA_AND_FLOWS.md): izlenebilirlik ve çıktı sözleşmesi.
- [Sınırlar](BOUNDARIES.md): portal, analiz ve uygulamanın sorumlulukları.

## Teknoloji kararı bekliyor

Python tabanlı veri hazırlığı, web tabanlı bir arayüz, harita ve grafik kütüphaneleri değerlendirilebilir. Framework, backend, veritabanı veya barındırma seçilmedi. Önce küçük sayısal veri örneğini ve çıktı boyutunu görmek gerekiyor.
