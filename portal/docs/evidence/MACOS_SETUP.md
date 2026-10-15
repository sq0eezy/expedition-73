# Mac kurulum hazırlığı

**Tarih:** 2026-10-15 · **İstek:** Kullanıcı arkadaşının Mac kullandığını belirtti ve kurulumu buna göre düzenlemeyi istedi.

## Değişiklik

Mac için ayrı kurulum sayfası eklendi. README ve portal girişleri bu sayfaya bağlandı. macOS komutları `python3`, `portal/.venv/bin/python` ve Terminal kullanımına göre açıklandı; M2'nin çalışma ortamı kullanıcı beyanıyla macOS olarak kaydedildi.

## Kod incelemesi

`scripts/portal.py` içindeki `environment_python`, `darwin` için `.venv/bin/python` seçiyor. `setup` ortamı mevcut bilgisayarda `sys.executable -m venv` ile oluşturuyor; `serve` o yerel ortamı kullanıyor. Kod değişikliği gerekmedi.

## Kontroller

Windows / Python 3.12.14 ortamında, `portal/` klasöründen:

| Komut | Sonuç |
|---|---|
| `.venv/Scripts/python.exe -m unittest discover -s tests -p test_portal.py -v` | 19 mevcut CLI/içerik testi geçti; `darwin` ortam yolunu kontrol eden test dahil |
| `.venv/Scripts/python.exe scripts/portal.py check` | Başarılı |
| `.venv/Scripts/python.exe scripts/portal.py build` | Strict derleme başarılı |

Mac üzerinde gerçek çalıştırma henüz yapılmadı. Bu oturum motoru değiştirmedi; kurulum belgeleri güncellendi.

## Kaynak ve sınır

[Python macOS kılavuzu](https://docs.python.org/3/using/mac.html) ve [venv belgesi](https://docs.python.org/3/library/venv.html), 2026-10-15 tarihinde incelendi. Windows'taki testte `darwin` yolunun doğrulanması, Mac üzerinde kurulumu veya paket uyumluluğunu uçtan uca doğrulamaz. Sonraki kanıt M2'nin kendi Mac'inden gelmeli.
