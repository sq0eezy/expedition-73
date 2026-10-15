# ADR-003 · GitHub Pages ile ortak web paneli

**Durum:** Accepted · **Tarih:** 2026-10-15

## Bağlam

Kullanıcı, her belge değişikliğini okumak için iki kişinin de `pull` yapıp yerel portal açmasını zor buldu; GitHub'a gönderilen değişikliklerin ortak bir siteden görülebilmesini istedi. Talep, ortak okuma erişimidir. NASA uygulamasının teknoloji veya bölge seçimiyle ilgili değildir.

## Karar

Talebi uygulamak için mevcut MkDocs portalı GitHub Pages'e hazırlanır. Teknik seçim bu oturumda yapıldı: ayrı sunucu, veritabanı veya yeni bir hizmet hesabı gerektirmeden mevcut deponun statik çıktısı yayımlanabilir. `main` dalına her push, içerik kontrolü ve strict derlemeyi tetikler; başarılı çıktı GitHub Actions üzerinden yayımlanır. Hedef adres ve ilk etkinleştirme adımları [web kılavuzundadır](../guide/WEB_PORTAL.md).

## Sonuçlar ve sınırlar

Okumak için yerel kurulum ve pull gerekmez. GitHub kaynakların esas kaynağı olmaya devam eder. Düzenleme dosyalar/GitHub üzerinden yapılır; canlı ortak düzenleme veya ortak tarayıcı işareti eşitlemesi eklenmez. Yerel geliştirmede güncel kaynakları alma ihtiyacı sürer. Pages'i ilk açma, depo sahibinin yönetim/bakım yetkisini gerektirir; bu oturumdaki hesapta yoktur.

ADR-002'deki yerel paylaşımın üzerine web okuma yolu eklenir. M2'nin bir bilimsel öneriyi kabul ettiği veya Mac kurulumunu tamamladığı varsayılmaz. Uygulama ile gerçek yayın doğrulaması ayrı takip edilir: [kanıt kaydı](../evidence/PAGES_SETUP.md).
