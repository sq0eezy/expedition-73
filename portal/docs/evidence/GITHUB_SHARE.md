# GitHub main aktarımı

**Tarih:** 2026-10-15 · **Ortam:** Windows / PowerShell, Git, portalın Python 3.12.14 ortamı.

## Yetki ve kapsam

Kullanıcı portalı GitHub `main` dalına gönderip arkadaşının `pull` ile kurmasını açıkça istedi. Kaynaklar ve ekip belgeleri paylaşılır; yerel `.venv`, `site`, `.portal`, önizleme görüntüleri ve kişisel okuma kayıtları Git dışında tutulur.

## Gerçek işlemler

1. `git remote set-url origin https://github.com/sq0eezy/expedition-73.git`: eski yazımlı adres düzeltildi.
2. `git fetch origin`: uzak main `cab8fcc` alındı.
3. İncelenmiş dosyalar eklendi; `git diff --cached --check` başarılı.
4. `3725b30` commit'i portalı ve iki kişilik çalışma alanını korudu.
5. `git merge --no-edit origin/main`: `b75ef9b` oluşturuldu, çakışma çıkmadı. Uzak üç commit ve iki ek dosya korundu.

## Doğrulama ve uzak sonuç

Yeni kurulum belgeleriyle `.venv/Scripts/python.exe scripts/portal.py check` ve `build` çalıştırıldı; içerik kontrolü ve strict derleme başarılı. Motor değişmediği için önceki 29 Python / 12 JavaScript araç testi yeniden çalıştırılmadı.

`git push origin main` başarılı: uzak dal `cab8fcc` → `6f99b5f` ilerledi. GitHub Git Reference API'si ve yerel `git rev-parse HEAD` aynı tam kimliği döndürdü: `6f99b5fb3abea961b90997256e2341fb194912a4`. Gönderim sonrasında çalışma ağacı temizdi; `git merge-base --is-ancestor cab8fcc HEAD` başarılı, arkadaşın katkıları geçmişte korunuyor.

Bu doğrulama notu, ilk aktarımın ardından main'e eklenen takip kaydıdır. Tamamlanan iş, dosyaların GitHub main üzerinden paylaşılmasıdır; web barındırması kurulmadı.

## Sınırlar

Arkadaşın kendi bilgisayarında pull/kurulum sonucu henüz bildirilmedi. Yerel çalışma Windows'ta doğrulanır; macOS/Linux üzerinde gerçek kurulum yapılmış sayılmaz. NASA verisi veya analiz uygulaması bu aktarımda geliştirilmedi.
