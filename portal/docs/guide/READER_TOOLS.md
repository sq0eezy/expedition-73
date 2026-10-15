# Okuma araçları

[İnceleme merkezi](../review/index.md) kişisel okuma listesi ve sayfa sürümü karşılaştırması sunar.

1. İlk kullanımda başlangıç karşılaştırmasını kendin kaydet; önceki ziyaretler bilinmiyor.
2. Sayfaları incelenecek, okundu, anlaşılmadı veya yapay zekâya sor olarak işaretle.
3. Sonraki ziyarette eklenen/değişen/silinen belgeleri karşılaştır.
4. Değişiklikleri kabul etmek tüm sayfaları okunmuş işaretlemez. Okunmuş sayfa değiştiğinde yeniden incelemek gerekir.

İşaretler tarayıcı `localStorage` alanında, proje kimliği ve origin altında tutulur. Proje kimliğini gelişigüzel değiştirmeyin. Başka cihazda veya başka portta aynı okuma geçmişi görünmeyebilir. Yerel JSON dışa aktarımı vardır; içe aktarım ve hesap eşitlemesi yoktur.

Depolama engellenirse geçici durum bildirilir; bozuk veya desteklenmeyen kayıtlar kendiliğinden temizlenmez. Tarayıcı verilerini silmek işaretleri kaybettirebilir. Bunlar görev ilerlemesi değildir ve Git'e yazılmaz.

`review_summary` sayfa girişidir; `change_summary` yazarın son kısa değişiklik notudur. Otomatik anlamsal fark özeti değildir. Oluşturulan katalog sadece yayımlanan belgeleri kapsar; uygulama kodunu ve özel sohbetleri izlemez.
