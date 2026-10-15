# Portalı kullanma

Önce [mevcut duruma](../CURRENT_STATE.md), ardından [fikir karşılaştırmasına](../discovery/IDEA_COMPARISON.md) bak. Yeni konuşmalar [işleme akışıyla](AI_WORKFLOW.md) belgelere dönüştürülür.

## Yerel açma

Çalışma alanının kökünden PowerShell:

~~~powershell
cd portal
.\.venv\Scripts\python.exe scripts\portal.py serve
~~~

Adres: http://127.0.0.1:8000 · Durdurma: terminalde Ctrl+C. Sunucu kapandığında aynı komutla yeniden açılır. Port doluysa `serve --port 8001` kullan; bu durumda adres 8001 olur ve tarayıcı okuma işaretleri ayrı origin altında tutulur.

Başka bilgisayarda Python 3.11+ gerekir. İlk kez `python scripts/portal.py setup` çalıştırılır; bu komut bağımlılıkları yerel `.venv` içine indirir. Sonrasında yerel Python ile `check`, `build`, `serve` kullanılır.

## İki kişi çalışırken

[Ekip alanında](../team/index.md) her üyenin kendi çalışma notu, fikir kartları ve yanıt bekleyen kayıtlar bulunur. Görev sahibi/inceleyen ortak iş panosunda tutulur. Önerilen GitHub düzeni ve henüz tamamlanmamış ilk aktarım [paylaşım kılavuzundadır](../team/SYNC.md).

Belgeleri Git üzerinden paylaşın; `.venv/`, `site/`, `.portal/`, ham konuşmalar ve kimlik bilgileri paylaşılmaz. Her kişi yerel kurulumunu yapar. Bu oturum uzak depoya push veya yayımlama yapmadı.

Görev durumları Markdown kaynaklarında güncellenir. Tarayıcıdaki [inceleme araçları](READER_TOOLS.md) kişiseldir; arkadaşının görev panosunu değiştirmez.
