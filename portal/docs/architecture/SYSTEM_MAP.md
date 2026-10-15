# Sistem haritası

Tüm uygulama bileşenleri **öneridir**; oklar çalışan entegrasyon göstermez.

~~~mermaid
flowchart TB
    N[Seçilecek NASA sayısal ürünü] --> Q[Kalite ve birim kontrolü]
    Q --> R[Ortak dönem ve bölge serileri]
    R --> T[Trend ve belirsizlik analizi]
    T --> A[Sürümlü sonuç dosyaları]
    A --> W[Web arayüzü]
    W --> M[Harita ve zaman animasyonu]
    W --> C[İki bölge zaman serisi]
    W --> E[Kaynak ve yöntem kartı]
    G[İsteğe bağlı GIBS görüntüleri] -. Görsel bağlam .-> M
~~~

Portal bu veri akışının dışında proje belgelerini tutar. İlk sürümde sonuç dosyalarıyla çalışma veya API kullanma seçimi henüz yapılmadı.
