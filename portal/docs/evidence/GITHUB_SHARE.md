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

Yeni kurulum belgeleri için içerik kontrolü/strict build ve main gönderimi bu kayıt tamamlanırken yapılacak. Push başarıyla sonuçlanmış sayılmadı.

## Sınırlar

Arkadaşın kendi bilgisayarında pull/kurulum sonucu henüz bildirilmedi. Yerel çalışma Windows'ta doğrulanır; macOS/Linux üzerinde gerçek kurulum yapılmış sayılmaz. NASA verisi veya analiz uygulaması bu aktarımda geliştirilmedi.
