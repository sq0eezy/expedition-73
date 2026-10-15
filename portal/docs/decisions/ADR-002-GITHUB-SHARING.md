# ADR-002 · GitHub üzerinden paylaşım ve ilk main aktarımı

**Durum:** Accepted · **Tarih:** 2026-10-15

## Bağlam ve karar

Kullanıcı portalın GitHub `main` dalına gönderilmesini, arkadaşının `pull` ile alıp kurmasını açıkça istedi. Ortak proje kayıtları mevcut `sq0eezy/expedition-73` deposunda paylaşılacak. İlk aktarım doğrudan `main` üzerine yapılır; arkadaşın uzak commitleri korunur.

## Çalışma biçimi

Her üye kendi bilgisayarında yerel portalı kurar. Çalışma başında güncel ortak kayıtlar alınır; üye notu, görev, fikir ve devir kayıtları güncellenir. Sonraki işler için ayrı branch ve kısa pull request kullanımı önerilir; bu ilk main aktarımına ek bir onay şartı değildir.

## Sonuçlar ve sınırlar

GitHub kod ve proje hafızasının ortak kaynağıdır. Yerel Python ortamı ve kişisel tarayıcı işaretleri paylaşılmaz. Tarayıcıdan canlı ortak düzenleme, sohbetleri otomatik içe alma veya web barındırması bu kararın kapsamına alınmadı.

## Takip

[Paylaşım ve kurulum](../team/SYNC.md), [ilk aktarım kaydı](../evidence/GITHUB_SHARE.md). Arkadaşın kendi kurulum sonucu henüz bildirilmedi.
