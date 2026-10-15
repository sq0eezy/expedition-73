# GitHub Pages yayın hazırlığı

**Tarih:** 2026-10-15 · **Ortam:** Windows, Python 3.12, mevcut yerel portal ortamı.

## Erişim gözlemi

Git'in mevcut GitHub kimlik bilgisi yalnızca GitHub REST API isteği için bellekte kullanıldı; anahtar dosyaya veya çıktıya yazılmadı. `GET /repos/sq0eezy/expedition-73` yanıtında `push=true`, `admin=false`, `maintain=false` görüldü. `GET /repos/sq0eezy/expedition-73/pages` HTTP 404 döndü. Bu hesap ilk Pages ayarını yönetemiyor; yayın açık diye raporlanmadı.

## Hazırlanan yayın

`.github/workflows/portal-pages.yml`, `main` push ve elle çalıştırma için hazırlandı. Ubuntu üzerinde Python 3.12 ile yerel portal ortamını kurar, içerik kontrolü + strict derleme yapar, yalnızca `portal/site` çıktısını yükler. Yayın işi yalnızca `main` için çalışır; `pages:write` ve `id-token:write` yetkileri bu işle sınırlıdır. Kaynak yazma yetkisi veya kişisel erişim anahtarı eklenmedi. GitHub'ın resmî action sürümleri 2026-10-15 tarihinde API üzerinden doğrulanıp commit SHA'larına sabitlendi.

MkDocs'a `/expedition-73/` yayın adresi, depo bağlantısı ve GitHub dosya düzenleyicisine giden kalem eklendi. Proje okuma kimliği korundu.

## Kontrol sonucu

- Depo kökünde `portal/.venv/Scripts/python.exe portal/scripts/portal.py check`: geçti.
- `portal/.venv/Scripts/python.exe portal/scripts/portal.py build`: içerik kontrolü ve strict MkDocs derlemesi geçti.
- Oluşturulan site geçici olarak yalnızca `127.0.0.1` üzerinde `/expedition-73/` öneki altında sunuldu. Python `HTMLParser` ile 53 HTML sayfasındaki yerel bağlantılar, CSS/JS ve okuma kataloğu adresleri toplandı; 63 benzersiz HTTP yolu 200 döndü. Önek dışına kaçan yol veya erişim hatası yoktu. Sunucu kontrol sonunda kapatıldı.
- Okuma kataloğu geçerli JSON olarak okundu. M2 sayfasının kalem bağlantısının `edit/main/portal/docs/team/members/M2.md` adresine gittiği HTML çıktısından doğrulandı. Tarayıcıdaki kişisel işaretler değiştirilmedi.
- `git diff --check`: boşluk hatası yok.

Bu kontroller Windows'ta oluşturulan statik çıktıyı doğrular; GitHub'ın Ubuntu derlemesi veya canlı yayının kanıtı değildir. Uzak workflow çalışması ve canlı site şu anda doğrulanmış değildir. Depo sahibinin bir kerelik [Pages etkinleştirmesi](../guide/WEB_PORTAL.md) gerekiyor.
