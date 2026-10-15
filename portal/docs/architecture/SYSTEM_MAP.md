---
review_summary: "Modüle özel hesaplamadan ortak çıktıya ve sunulacak web uygulamasına akış."
change_summary: "Kabul edilen adaptör yaklaşımı ve tek göstergeli pilot sistem haritasına işlendi."
---
# Sistem haritası

Mimari yön [ADR-004](../decisions/ADR-004-MODULES-AND-PILOT.md) ile kabul edildi. Şema uygulanacak tasarımdır; oklar çalışan entegrasyon göstermez.

~~~mermaid
flowchart TB
    B[Sürümlü bölge tanımı] --> M[Modüle özel hazırlık ve hesap]
    N[Seçilecek NASA sayısal ürünü] --> M
    I[Varsa başka modülün çıktısı] --> U[Girdi uygunluk kontrolü]
    U --> M
    M --> A[Sonuç adaptörü]
    A --> O[Ortak sonuç ve özel ayrıntılar]
    O --> V[Karşılaştırma uygunluk kontrolü]
    V --> C[A ve B karşılaştırması]
    O --> W[Sunulacak web uygulaması]
    C --> W
    H[Konu ve alt modül ağacı] -. gezinme .-> W
    W --> T[Harita - zaman serisi - istatistik - kaynak]
~~~

İlk pilot **2 metre hava sıcaklığı modülü**; başka bilimsel modülden girdi alma sonraki genişlemedir. İki alanın çıktıları karşılaştırma bileşenine verilir. Konu ağacı ve veri bağımlılığı [modül sistemindedir](MODULE_SYSTEM.md).

Portal bu akışın dışında proje hafızasını tutar. Sonuç dosyalarıyla başlangıç/API seçimi ve web teknolojisi açık. [Pilot planı](../planning/PILOT.md).
