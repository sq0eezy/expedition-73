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

Bu yerel kontroller Windows'ta oluşturulan statik çıktıyı doğrular. Canlı yayın sonucu aşağıda ayrı tutulur.

## GitHub üzerindeki gerçek çalışma

Yayın hazırlığı `f0ae5d90325b6405081cddab2cf13258b68d5dc6` commit'iyle `main` dalına gönderildi; `git rev-parse HEAD` ile `git ls-remote origin refs/heads/main` aynı kimliği döndürdü. Arkadaşın mevcut commit'leri korundu.

[İlk otomatik çalışma](https://github.com/sq0eezy/expedition-73/actions/runs/38796594420) GitHub API üzerinden izlendi:

| İş | Gerçek sonuç |
|---|---|
| Portalı kontrol et ve derle · iş 116634487354 | **success**; Ubuntu 24.04 üzerinde ortam kurulumu, içerik kontrolü, strict derleme ve site artifact yüklemesi geçti |
| Ortak paneli yayımla · iş 116634684254 | **failure**; `Pages ayarını oku` adımı “Get Pages site failed… Pages enabled and configured to build using GitHub Actions… Not Found” döndürdü |
| GitHub Pages'e yayımla adımı | Önceki ayar adımı başarısız olduğundan **skipped** |

İş durumları ve yayın işi günlüğü okundu. Kod/derleme hatası gözlenmedi; ilk Pages etkinleştirmesi eksik. Canlı site henüz yayımlanmadı. Depo sahibinin [bir kerelik ayarı](../guide/WEB_PORTAL.md) tamamlayıp iş akışını yeniden çalıştırması gerekiyor. Bu kayıt hazırlanırken yönetim yetkisi alınmadı veya kişisel anahtar eklenmedi.

## Güncelleme · Canlı yayın doğrulandı

2026-10-15 tarihinde kullanıcı Pages kaynağını GitHub Actions yaptıklarını bildirdi. [Başarılı yayın çalışması](https://github.com/sq0eezy/expedition-73/actions/runs/38798369000) GitHub API üzerinden `completed/success` olarak görüldü; kaynak commit `6fbb3b908cf6d0d53eeb3ea7d0aa8bbe20dc5e63`. Python urllib ile başlangıç adresi `https://sq0eezy.github.io/expedition-73/` ve `assets/reader/catalog.json` HTTP 200 döndü. İlk ayarın tamamlandığı ve portalın açık olduğu doğrulandı; üstteki başarısızlıklar tarihsel ilk denemelerdir. Bu kontrol bilimsel web uygulamasının veya NASA analizinin doğrulaması değildir.
