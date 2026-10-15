# Portalı kullanma

Önce [mevcut duruma](../CURRENT_STATE.md), ardından [fikir karşılaştırmasına](../discovery/IDEA_COMPARISON.md) bak. Yeni konuşmalar [işleme akışıyla](AI_WORKFLOW.md) belgelere dönüştürülür.

## Yerel açma

**sq0eezy Mac kullanıyor:** [Mac için ilk kurulum ve açılış](MACOS_SETUP.md). Mac Terminal'de `python3` ve `.venv/bin/python` komutları kullanılır.

Çalışma alanının kökünden PowerShell:

~~~powershell
cd portal
.\.venv\Scripts\python.exe scripts\portal.py serve
~~~

Adres: http://127.0.0.1:8000 · Durdurma: terminalde Ctrl+C. Sunucu kapandığında aynı komutla yeniden açılır. Port doluysa `serve --port 8001` kullan; bu durumda adres 8001 olur ve tarayıcı okuma işaretleri ayrı origin altında tutulur.

Başka bilgisayarda Python 3.11+ gerekir. İlk kez `python scripts/portal.py setup` çalıştırılır; bu komut bağımlılıkları yerel `.venv` içine indirir. macOS/Linux'ta `python3` kullanılır. Sonrasında aynı temel Python komutuyla `scripts/portal.py check`, `build`, `serve` kullanılır; araç yerel ortamı kendisi seçer.

## İki kişi çalışırken

[Ekip alanında](../team/index.md) her üyenin kendi çalışma notu, fikir kartları ve yanıt bekleyen kayıtlar bulunur. Görev sahibi/inceleyen ortak iş panosunda tutulur. GitHub düzeni ve ilk kurulum [paylaşım kılavuzundadır](../team/SYNC.md).

Belgeleri Git üzerinden paylaşın; `.venv/`, `site/`, `.portal/`, ham konuşmalar ve kimlik bilgileri paylaşılmaz. Her kişi yerel kurulumunu yapar. Main aktarımının sonucu [kanıt kaydındadır](../evidence/GITHUB_SHARE.md); herkese açık web barındırması kurulmadı.

Görev durumları Markdown kaynaklarında güncellenir. Tarayıcıdaki [inceleme araçları](READER_TOOLS.md) kişiseldir; arkadaşının görev panosunu değiştirmez.
