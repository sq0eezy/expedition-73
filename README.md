varlık

# Expedition 73 · NASA Space Apps

İki kişilik ekibin fikir, veri, mimari ve karar hafızası [portal/](portal/README.md) içindedir.

[Ekip alanı](portal/docs/team/index.md): Emeç Yıldız ve sq0eezy için ayrı çalışma notları, fikir alışverişi, görev sahipliği ve devir kayıtları. Ortak kayıtlar bu deponun `main` dalından paylaşılır; [paylaşım kılavuzu](portal/docs/team/SYNC.md).

**Mevcut aşama:** tek göstergeli **2 metre hava sıcaklığı** pilotunu hazırlama. Modüle özel hesap + ortak sonuç adaptörü kabul edildi; bölgeler/ürün/dönem/yöntem açık. [Pilot planı](portal/docs/planning/PILOT.md), [modül sistemi](portal/docs/architecture/MODULE_SYSTEM.md). Bilimsel uygulama henüz geliştirilmedi.

Başlangıç: [mevcut durum](portal/docs/CURRENT_STATE.md), [fikir karşılaştırması](portal/docs/discovery/IDEA_COMPARISON.md), [NASA kaynakları](portal/docs/research/DATA_SOURCES.md).

## Ortak web paneli

Yönetim portalı **[GitHub Pages üzerinde açık](https://sq0eezy.github.io/expedition-73/)**. Başarılı yayın ve HTTP erişimi doğrulandı: [yayın kaydı](portal/docs/evidence/PAGES_SETUP.md).

Ortak adres: **https://sq0eezy.github.io/expedition-73/**. Sonraki `main` güncellemeleri başarılı derlemeden sonra otomatik yayımlanır. Okumak için pull veya yerel kurulum gerekmez; sayfayı yenilemek yeterli. Kalem simgesiyle GitHub üzerinden belge düzenlenebilir. [Web kullanımı ve ilk açılış](portal/docs/guide/WEB_PORTAL.md).

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



