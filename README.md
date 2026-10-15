varlık

# Expedition 73 · NASA Space Apps

İki kişilik ekibin fikir, veri, mimari ve karar hafızası [portal/](portal/README.md) içindedir.

[Ekip alanı](portal/docs/team/index.md): Emeç Yıldız ve sq0eezy için ayrı çalışma notları, fikir alışverişi, görev sahipliği ve devir kayıtları. Ortak kayıtlar bu deponun `main` dalından paylaşılır; [paylaşım kılavuzu](portal/docs/team/SYNC.md).

**Mevcut aşama:** fikir karşılaştırması. Değişken ve bölgeler henüz seçilmedi; NASA analiz uygulaması geliştirilmedi.

Başlangıç: [mevcut durum](portal/docs/CURRENT_STATE.md), [fikir karşılaştırması](portal/docs/discovery/IDEA_COMPARISON.md), [NASA kaynakları](portal/docs/research/DATA_SOURCES.md).

## Arkadaşın için Mac kurulumu

Mac Terminal içinde `python3 --version` ile Python 3.11+ olduğunu kontrol et. Depo kökünden, korunmamış yerel değişiklik yokken:

~~~sh
git switch main
git pull --ff-only origin main
cd portal
python3 scripts/portal.py setup
python3 scripts/portal.py serve --open
~~~

Kurulum Mac üzerinde `portal/.venv` içine yapılır. Sonraki açılışta `portal/` içinde `.venv/bin/python scripts/portal.py serve --open` yeterlidir. [Mac kurulum kılavuzu](portal/docs/guide/MACOS_SETUP.md).

Kurulumu yapılmış Windows ortamında PowerShell ile portalı açma:

~~~powershell
cd portal
.\.venv\Scripts\python.exe scripts\portal.py serve
~~~

Yerel adres: http://127.0.0.1:8000 · Durdurma: terminalde Ctrl+C.
İlk kurulum veya başka bilgisayar için [portal kılavuzuna](portal/README.md) bak.



