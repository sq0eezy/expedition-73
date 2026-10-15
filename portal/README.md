# Expedition 73 · Proje Hafızası

NASA Space Apps için fikir, veri, mimari, karar ve ekip takibi. [Project Context Portal](https://github.com/emecyildiz/project-context-portal) temel alınarak Türkçe uyarlandı; kaynak ve lisans ayrıntıları [UPSTREAM.md](UPSTREAM.md) içinde.

**Aşama:** fikir karşılaştırması. Değişken veya bölgeler henüz seçilmedi. Bu portal geliştirme hafızasıdır; NASA verilerini analiz eden uygulama henüz geliştirilmedi.

## Başlangıç

- [Mevcut durum](docs/CURRENT_STATE.md)
- [Fikir karşılaştırması](docs/discovery/IDEA_COMPARISON.md)
- [NASA veri kaynakları](docs/research/DATA_SOURCES.md)
- [İş panosu](docs/planning/WORK_BOARD.md)
- [İki kişilik ekip alanı](docs/team/index.md)
- [GitHub paylaşımı ve ilk eşitleme](docs/team/SYNC.md)
- [Yeni konuşma işleme](docs/guide/AI_WORKFLOW.md)

## Yerel çalıştırma

Python 3.11+ gerekir. İlk kurulumda bu klasörden:

~~~powershell
python scripts/portal.py setup
~~~

Kurulum sistem geneline değil `.venv` içine yapılır. Ardından:

~~~powershell
.\.venv\Scripts\python.exe scripts\portal.py check
.\.venv\Scripts\python.exe scripts\portal.py build
.\.venv\Scripts\python.exe scripts\portal.py serve
~~~

Adres: http://127.0.0.1:8000 · Durdurma: terminalde Ctrl+C. Yeniden açmak için aynı serve komutunu çalıştır. Port doluysa `serve --port 8001` kullan.

`docs/` değişiklikleri açık geliştirme sunucusunda yenilenir. Arkadaşın depoyu kendi bilgisayarına aldığında yerel kurulumu yapmalı; `.venv/`, `site/` ve `.portal/` Git'e girmez. Okuma işaretleri tarayıcıya özeldir. Bu uyarlama uzak depoya gönderilmedi veya yayımlanmadı.

## Doğrulama

~~~powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
node tests/test_reader_core.cjs
~~~

Gerçek sonuçlar [portal kanıt kaydında](docs/evidence/PORTAL_SETUP.md). Eski `verification/` ve `RELEASE.md`, kaynak aracın geçmişidir; bu projenin uygulama kanıtı değildir. Portal kontrolü NASA analizini doğrulamaz.

Ortak çalışma yönergesi `AGENTS.md` ve [AI_SETUP.md](AI_SETUP.md) içinde. Özel sohbetleri, anahtarları ve kişisel dosya yollarını `docs/` içine koymayın. MIT lisansı ve üçüncü taraf bildirimleri korunmuştur.
