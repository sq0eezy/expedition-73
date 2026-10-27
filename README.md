varlık

# Expedition 73 · NASA Space Apps

İki kişilik ekibin fikir, veri, mimari ve karar hafızası [portal/](portal/README.md) içindedir.

[Ekip alanı](portal/docs/team/index.md): Emeç Yıldız ve sq0eezy için ayrı çalışma notları, fikir alışverişi, görev sahipliği ve devir kayıtları. Ortak kayıtlar bu deponun `main` dalından paylaşılır; [paylaşım kılavuzu](portal/docs/team/SYNC.md).

**Mevcut aşama:** testli **2 metre hava sıcaklığı** temeli main'de; [adım adım toparlama](portal/docs/planning/CONSOLIDATION.md). [T2M adaptörleri](analysis/README.md), gerçek A/B 2001–2024 aday kayıtları, aylık/yıllık hesap ve [teknik sonuç ekranı](web/README.md) çalışıyor. Veri/hesap çekirdeği hazır; [bilimsel pilotun tamamı bitmedi](portal/docs/planning/PILOT.md). Kesin profil/maske/sınır, eğilim ve belirsizlik açık. [Sade karşılaştırma arayüzü taslağı](portal/docs/product/COMPARISON_WORKSPACE.md) sonraki ayrı teslimdir; yeni gösterge henüz seçilmedi.

Başlangıç: [mevcut durum](portal/docs/CURRENT_STATE.md), [fikir karşılaştırması](portal/docs/discovery/IDEA_COMPARISON.md), [NASA kaynakları](portal/docs/research/DATA_SOURCES.md).

## İsteğe bağlı geliştirme paketi

Docker Desktop açıkken depo kökünde `docker compose --env-file docker/compose.env up --build`; adres http://127.0.0.1:8873/. Durdurma: Ctrl+C ve aynı env-file ile `docker compose --env-file docker/compose.env down`. Docker olmadan Windows'ta `scripts\start-preview.cmd`, Mac'te `sh scripts/start-preview.sh`. [Kurulum, ortak kontrol ve demo ZIP kılavuzu](portal/docs/guide/DEV_PACKAGE.md), [ilk main teslimi ve gerçek platform kontrolleri](portal/docs/evidence/T2M_BASELINE_RELEASE.md). Kaynak artık main'dedir; Pages yalnız yönetim portalını yayımlar.

## İlk yerel sonuç ekranı

Main'deki teknik sonuç ekranı `web/` içinde. Windows CMD'de depo kökünden `analysis\.venv\Scripts\python.exe analysis\scripts\build_web_preview.py`, ardından `analysis\.venv\Scripts\python.exe web\serve.py`. Adres http://127.0.0.1:8873/, kapatma Ctrl+C. [Mac komutları ve ekran kapsamı](web/README.md). Kaynak main'den alınabilir; sonuç uygulamasının çevrim içi barındırılması henüz kurulmadı.

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



