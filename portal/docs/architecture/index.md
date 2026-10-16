---
review_summary: "Kabul edilen modüler yön ve açık teknik seçimler."
change_summary: "Özel hesap + ortak adaptör, konu ağacı/veri bağımlılığı ve T2M pilotu mimarinin temeli oldu."
---
# Mimari

**Kabul edilen yön:** Modüle özel bilimsel hesap, ayrıntıları koruyan ortak sonuç sözleşmesi, türü tanımlı modül bağlantıları ve sonuçları inceleten web uygulaması. İlk pilot tek gösterge: **2 metre hava sıcaklığı**. [ADR-004](../decisions/ADR-004-MODULES-AND-PILOT.md).

Konu/alt modül ağacı ile veri bağımlılığı ayrı tutulur. Yeni bölge mevcut modülün bölge tanımı ve uygunluk kontrolüyle eklenir; yeni gösterge kendi hesabını/adaptörünü getirir. Ortak sözleşme farklı bilimsel büyüklükleri eşitlemez.

- [Modül sistemi](MODULE_SYSTEM.md): hiyerarşi, giriş/çıkış ve bağımlılıklar.
- [Sistem haritası](SYSTEM_MAP.md): NASA verisinden web uygulamasına akış.
- [Veri ve akışlar](DATA_AND_FLOWS.md): ortak zarf ve özel ayrıntılar.
- [Pilot planı](../planning/PILOT.md): ilk denemenin çıkış koşulları.
- [Sınırlar](BOUNDARIES.md): portal, modüller ve ürün arayüzü.
- [Önceki bölge taslağı](REGIONAL_MODULE_PROPOSAL.md): veriyle bölge/modül açma gerekçesi; alan adayları hâlâ açık.

## Açık teknik seçimler

İlk Python API/nokta adaptörü, JSON şemaları ve gerçek POWER örneği var; [çalıştırma](../guide/T2M_ADAPTER.md). Bölgesel hesap ve eğilim yok. Ürün, sınırlar, dönem ve yöntem pilotla doğrulanacak. Python/jsonschema nokta prototipi için seçildi: [ADR-006](../decisions/ADR-006-T2M-POINT-ADAPTER.md). Nihai web framework/backend/veritabanı ve barındırma seçilmedi. Sonuç dosyalarıyla başlangıç bir aday; canlı API ihtiyacı veri boyutu ve deneyim üzerinden belirlenecek. Mevcut Pages yayını proje yönetim portalına aittir.
