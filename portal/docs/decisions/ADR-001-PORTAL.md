# ADR-001 · Proje hafızası için Project Context Portal

**Durum:** Accepted · **Tarih:** 2026-10-15

## Bağlam

İki kişilik ekip, farklı yapay zekâ konuşmalarında oluşan fikirleri, mimariyi ve ilerlemeyi ortak bir yerde takip etmek istiyor. Kullanıcı Project Context Portal'ı kullanacaklarını açıkça belirtti ve projelerine uyarlanmasını istedi.

## Karar

[Project Context Portal](https://github.com/emecyildiz/project-context-portal) proje hafızasının temeli olarak kullanılacak. Bu oturumda çalışma alanının `portal/` klasöründe, mevcut kök dosyaları koruyan bir uyarlama hazırlandı. Belgeler Türkçe; uygulama fikri hâlâ keşif aşamasında.

## Alternatifler

Düz Markdown notları veya haricî görev araçları kullanılabilirdi. Kullanıcının mevcut tercihi portal olduğundan yeni araç seçimi yapılmadı.

## Sonuçlar ve sınırlar

Markdown belgeleri Git ile paylaşılabilir; kişiler/yapay zekâ belgeleri günceller. Portal tarayıcıdan görev yazma, sohbetleri otomatik içe alma veya iki kişinin okuma işaretlerini eşitleme özelliği sunmaz. Her kişinin portalı kendi bilgisayarında çalıştırması gerekir; ekip barındırması seçilmedi.

## Takip

[Portal doğrulama kaydı](../evidence/PORTAL_SETUP.md). Bu karar bilimsel değişken veya uygulama teknolojisi seçimi değildir.
