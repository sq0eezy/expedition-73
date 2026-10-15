---
review_summary: "Modüle özel hesap, ortak sonuç sözleşmesi, modül bağlantıları ve tek göstergeli pilot kararı."
change_summary: "M1 modüler yaklaşımı ve dar pilotu kabul etti; ilk gösterge olarak 2 metre hava sıcaklığını seçti."
---
# ADR-004 · Modül bağlantıları ve dar sıcaklık pilotu

**Durum:** Accepted · **Tarih:** 2026-10-15 · **Kararın kaynağı:** M1'in bu sohbetteki açık yönlendirmesi. M2'nin ayrıca görüş bildirdiği varsayılmadı.

## Bağlam ve karar

Kullanıcı her modülün kendi bilimsel hesabını yapmasını, ayrıntıları korunarak ortak bir veri biçiminde sonuç vermesini istedi ve bu yaklaşımı kabul etti. Geniş konuların alt modülleri olabileceğini, bir modülün çıktısının başka bir modüle girdi olabileceğini belirtti. Başlangıcın dar bir deneme, sunulacak ürünün bir web uygulaması olmasını istedi. İlk gösterge sorusuna **2 metre hava sıcaklığı** yanıtını verdi.

- İlk pilot tek bilimsel göstergeyle başlar: 2 metre hava sıcaklığının zaman serisi ve eğilimi. Veri kaynağı, kesin alanlar, dönem ve istatistik yöntemi ayrıca doğrulanacak.
- Her analiz modülü kendi hazırlığını ve bilimsel yöntemini yönetir. Sonuç adaptörü ortak sözleşmeyi üretir; özel ayrıntılar korunur.
- Konu/alt modül ilişkisi (`contains`) ile hesaplama bağımlılığı (`consumes`) ayrı tutulur. Hiyerarşi otomatik veri bağımlılığı doğurmaz.
- Türü tanımlı çıktılar başka modüllere girdi olabilir. Birim, zaman, alan, gösterge, yöntem ve sürüm uyumluluğu kontrol edilir.
- Sunulacak ürün kaynak/yöntem/kalite bilgisiyle sonuçları inceleten web uygulamasıdır. Mevcut portal geliştirme hafızasıdır.

## Sonuçlar ve açık seçimler

Önce tek modülün uçtan uca akışı sınanır; bütün modüller, genel bir hesap motoru veya “küresel ısınma skoru” başlangıç işi değildir. Konu grupları ve bağlantılar tasarlanır.

Colorado Platosu ve Kuzey Alaska, ürünler ve 2001–2024 dönemi aday olmaya devam eder. A/B bölge sahipliği düşünülen iş bölümüdür; kişi/bölge ataması yok. Framework, uygulama barındırması ve canlı analiz API'si seçilmedi. Karar çalışan uygulama veya NASA analiz sonucu değildir.

[Modül sistemi](../architecture/MODULE_SYSTEM.md) · [Veri sözleşmesi](../architecture/DATA_AND_FLOWS.md) · [Pilot](../planning/PILOT.md) · [Web deneyimi](../product/index.md)

**2026-10-16 takip kararı:** İş sorumluluğu sonradan [ADR-005](ADR-005-TEAM-OWNERSHIP.md) ile M1: modüller/A, M2: B olarak kaydedildi. Üstteki kişi/bölge ataması yok ifadesi bu kararın ilk tarihindeki durumu anlatır.
