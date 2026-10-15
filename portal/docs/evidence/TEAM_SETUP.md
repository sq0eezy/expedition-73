# Ekip alanı doğrulaması

**Tarih:** 2026-10-15 · **Ortam:** Windows, PowerShell, portalın yerel Python ortamı.

## Kapsam

Yalnızca belgeler, gezinme, yönergeler ve şablonlar değiştirildi. Portal motoruna veya NASA analizine kod eklenmedi. Üye kimlikleri, kullanıcı isteğiyle GitHub hesabı/depo/commit kayıtlarından eşleştirildi; e-posta veya ham API çıktıları belgelere kopyalanmadı.

## GitHub incelemesi

- Bağlı hesap: `emecyildiz`; profil adı Emeç Yıldız.
- Depo sahibi: `sq0eezy`; kullanıcı arkadaşının depo sahibi olduğunu belirtti.
- Depo API'si doğru güncel adı `sq0eezy/expedition-73` olarak döndürdü; son beş committe iki hesabın katkısı görüldü.
- Yerel `git log` ile HEAD `7c96f40`; uzak commit API'siyle main `cab8fcc` görüldü. Uzak ağaç okundu; farklar [eşitleme kaydında](../team/SYNC.md).
- Tam collaborator listesi alınmadı: connector contributors uç noktasını desteklemedi; ayrıntılı collaborator izin sorgusu entegrasyon izni nedeniyle 403 döndürdü. Buradaki eşleştirme tam erişim listesi iddiası değildir.
- Fetch/pull/commit/push/merge veya dış yorum yapılmadı.

## Portal kontrolleri

`portal/` içinden `.venv/Scripts/python.exe scripts/portal.py check` ve `.venv/Scripts/python.exe scripts/portal.py build` çalıştırıldı. İçerik kontrolü ve strict derleme başarılı. Python/JavaScript motoru değişmediği için önceki araç testleri tekrar çalıştırılmadı.

PowerShell `Invoke-WebRequest` ile `/team/`, iki üye sayfası, fikirler, devirler, çalışma akışı, eşitleme, iş panosu ve bu kanıt sayfasına dokuz istek yapıldı; tamamı HTTP 200 döndü. `Invoke-RestMethod` ile okuma kataloğunda 41 belge görüldü. `git diff --check` izlenen dosyalarda boşluk hatası bildirmedi.

Codex uygulama içi tarayıcıda `/team/` açıldı ve yeniden yüklendi. İki üye kartı, Türkçe içerik ve ekip gezinme bağlantıları görüldü. Görünüm Git dışında kalan `.portal/team-preview.png` dosyasına kaydedildi. Kişisel okuma işaretleri değiştirilmedi.

## Sınırlamalar

İki cihaz arasında eşitleme veya PR üzerinden gerçek paylaşım henüz yapılmadı. Üyelerin veri/arayüz rolleri atanmadı. Arkadaşın özel sohbetine erişim veya otomatik arka plan izleme yok. Ekip alanının yerelde açılması, diğer bilgisayarın bu kayıtlara eriştiğini doğrulamaz.
