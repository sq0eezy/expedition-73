# Veri ve akışlar

**Durum: Proposed.** Dosya veya şema henüz uygulanmadı.

## Önerilen hazırlık akışı

1. Ürün kimliği/sürümü ve erişim yolunu [kaynak kaydından](../research/DATA_SOURCES.md) seç.
2. Küçük örnekte birim, ölçek, dolgu ve kalite alanlarını incele.
3. Bölge sınırları ve ortak dönemi kaydet; zaman eşleştirmesini açıkça tanımla.
4. Kararlaştırılan ön işleme ve yöntemle serileri/analizleri üret.
5. Sonuçları kaynak ve yöntem metaverisiyle arayüze ver.
6. Harita/grafik tarih uyumunu ve örnek bir sonucu bağımsız hesapla doğrula.

## Taslak çıktı sözleşmesi

| Bilgi | Neden gerekli? |
|---|---|
| Ürün kimliği, sürümü, kaynak URL'si, erişim tarihi | Tekrar bulunabilirlik |
| Bölge kimliği ve coğrafi sınırları | Bölge/piksel karışıklığını önlemek |
| Değişken, birim, ölçek ve kalite politikası | Değerleri doğru yorumlamak |
| Zaman damgası, frekans, ortak dönem, varsa referans dönem | Harita ve seriyi eşlemek |
| Değerler, geçerli örnek sayısı, eksik veri göstergesi | Kapsama ve eksikliği göstermek |
| Yöntem, eğim birimi, belirsizlik, varsa p-değeri | Sonucun sınırlarını anlatmak |
| Üretim komutu, sürüm ve girdi dosyası özeti | Hesabı tekrarlamak |

Eksik değer sıfıra çevrilmemeli; geçersiz/hesaplanamadı durumu ayrıca taşınmalı. Tarih değiştiğinde harita ve grafik aynı seçim durumunu kullanmalı. Bunlar uygulama tasarımı için önerilen kurallardır; test edilmiş davranış değildir.
