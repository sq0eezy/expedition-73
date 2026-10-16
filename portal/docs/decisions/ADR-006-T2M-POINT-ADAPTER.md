# ADR-006 · İlk teknik dilim: POWER T2M nokta adaptörü

**Durum:** Accepted · **Tarih:** 2026-10-16 · **Kaynak:** M1'in kendi modül/A görevlerine başlama talebi kapsamında bu oturumdaki teknik uygulama seçimi.

Küçük gerçek veriye erişim ve sözleşme denemesi için NASA POWER aylık `point` API'si kullanılır. İlk örnek, A aday penceresi içindeki 37,5°K / 111°B noktasında 2024 yılıdır. Bu, kesin bölge/ürün/dönem seçimi veya bölgesel trend analizi değildir.

Kaynak erişimi ve normalleştirme prototipi `analysis/` içinde Python 3.11+ ile başlatılır. İlk `0.1.0` JSON sözleşmesi yalnızca **aylık T2M nokta-serisi profilini** uygular. Modüle özgü kaynak metaverisi korunur. Şema/anlamsal doğrulama ve zaman/kaynak uyumu kontrol edilir; `inference_allowed` daima false kalır.

Python/jsonschema bu küçük analiz aracının teknik seçimidir; nihai web uygulamasının framework/backend kararı değildir. POWER, MERRA-2 tabanlı servis olarak açıkça etiketlenir; doğrudan MERRA-2 `M2TMNXSLV` dosyasıyla aynı ürün/sürüm diye sunulmaz. Küçük API yanıtı kaynak iziyle örnek olarak saklanır; büyük arşiv indirmesi yapılmaz.

Sonraki adımda M2'nin B erişim örneği ve iki alanın gerçek poligon/maske/ızgara uygunluğu görülmeden bölgesel hesap ve yöntem kesinleştirilmez. [Gerçek kanıt](../evidence/T2M_POINT_PROBE.md), [çalıştırma](../guide/T2M_ADAPTER.md).
