---
review_summary: "Modül sonuçlarının ortak dili, özel ayrıntıları ve bağlantı uygunluğu."
change_summary: "Modüle özel hesap ve adaptör için sürümlü sonuç sözleşmesi taslağı tanımlandı."
---
# Veri ve akışlar

Ortak sözleşme yaklaşımı [ADR-004](../decisions/ADR-004-MODULES-AND-PILOT.md) ile kabul edildi. Genel alanlar sözleşme taslağıdır. İlk **aylık T2M nokta-serisi profili v0.1.0** için JSON Schema ve anlamsal doğrulama `analysis/` içinde çalışıyor: [kılavuz](../guide/T2M_ADAPTER.md), [kanıt](../evidence/T2M_POINT_PROBE.md). Bu ilk profil harita, bölgesel ortalama veya istatistik özeti desteği değildir.

## Ortak zarf ve özel içerik

| Bölüm | Bilgi |
|---|---|
| Kimlik | Sözleşme sürümü, modül/sürüm, çıktı kimliği/türü ve üretim çalışması |
| Bölge | Kimlik, sınır sürümü, maske ve uzaysal destek |
| Gösterge | Kesin büyüklük, birim, gerekiyorsa yükseklik/derinlik |
| Zaman | Frekans, tarihler, analiz/referans dönemi ve mevsim tanımı |
| Kaynak | NASA ürün/sürüm, değişken, erişim yolu/tarihi, girdi özeti ve üst modül çıktı izleri |
| Kalite | Geçerli alan/zaman kapsamı, eksiklik, filtreler ve uyarılar |
| Yöntem | Analiz profili/sürümü, parametreler, varsayımlar ve belirsizlik kapsamı |
| Ortak içerik | Türüne göre seri, harita referansı, özet istatistik veya kalite raporu |
| Özel içerik | Modülün ayrıntılı tanıları, ek göstergeleri ve haritaları |

Her çıktıda eğim/p-değeri zorunlu değildir. Seri ve analiz özeti farklı çıktı türleridir; p-değeri varsa test ve sıfır hipotezi belirtilir. Eksik/girdi yetersiz değeri sıfıra çevrilmez. Ortak zarf bütün sonuçların bilimsel olarak karşılaştırılabilir olduğunu göstermez.

## Bağlantı ve karşılaştırma kontrolü

Alıcı modül istediği çıktı türünü/göstergeyi; kabul ettiği birimleri, zaman/alan desteğini, kalite koşullarını ve sözleşme sürümünü bildirir. Sonuç **uygun**, **açık dönüşüm/yeniden hesaplama gerekli** veya **uyumsuz** olur; gerekçe saklanır. Farklı yöntemlerin p-değerleri etki büyüklüğü gibi karşılaştırılmaz.

Kaynak çıktı değişince bağımlı sonuç güncel değil sayılır. Zorunlu girdi eksikse alıcı çalışmaz; kısmi hesap destekleniyorsa koşulu yöntem kartında açıklanır. [Modül bağlantıları](MODULE_SYSTEM.md).

## Pilot akışı

1. Gerçek T2M örneğinde birim, ölçek, kalite ve zamanı incele.
2. Seçilecek sınır/alan ağırlığıyla seri üret; gözlenen alanın zamanla değişimini raporla.
3. Modüle uygun yöntemle eğilim/belirsizlik ve alanların farkı için ayrı analiz yap.
4. Adaptörde ortak zarfı, özel ayrıntıları ve kaynak izlerini üret.
5. Uygun çıktıları aynı bölge/tarih seçimleriyle webde göster.
6. Ara hesabı ve sonuç aktarımını bağımsız örnekle doğrula.

Kimlik bilgileri sonuç dosyasına veya tarayıcı paketine eklenmez. Saklama biçimi/API ihtiyacı gerçek örnekten sonra seçilir. [Pilot koşulları](../planning/PILOT.md).
