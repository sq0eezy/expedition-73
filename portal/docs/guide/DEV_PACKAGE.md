---
status: Validating
updated: "2026-10-21"
review_summary: "İki kişilik çalışmada isteğe bağlı Docker, yerel başlatıcı, ortak offline kontrol ve demo paketi."
change_summary: "Windows/Mac komutları, sabit bağımlılıklar, altı dosyalı akış ekranı demo arşivi ve CI akışı hazırlandı; bilimsel seçim değildir."
---
# Taşınabilir geliştirme paketi

M1, daha büyük bir geliştirme paketiyle devam istedi. Önceki Docker önerisi bu teknik dilimde **isteğe bağlı çalışma yolu** olarak uygulandı; nihai ürün yığını, hosting veya M2'nin ortam tercihi kabulü değildir. Yönetim portalı mevcut Pages düzeninde kalır. [Gerçek doğrulama ve ortam sınırları](../evidence/DEV_PACKAGE_CHECK.md).

## Docker ile tek komut

Kurulu Docker Desktop açık ve Linux konteyner motoru hazırken depo kökünde Windows CMD veya Mac Terminal:

```sh
docker compose --env-file docker/compose.env up --build
```

Adres `http://127.0.0.1:8873/`. Terminalde Ctrl+C; ardından aynı kökte:

```sh
docker compose --env-file docker/compose.env down
```

`--env-file docker/compose.env` özellikle bırakılır: bu açık boş dosya kullanılır, özel Earthdata `.env` dosyası Compose girdisi yapılmaz. Önizleme kayıtlı örnekleri imaj derlemesinde doğrular; çalışma anında NASA/token istemez. İlk derleme imaj ve pip paketlerini internetten alır; kaynak API çağrısı yapmaz. Değişiklik sonrası aynı `up --build` komutuyla imaj yenilenir. Canlı yenileme/bind mount yok; eski imaj yeni kod sanılmaz.

Yalnız `127.0.0.1:8873` hosta açılır. Konteyner içindeki `0.0.0.0` dinlemesi bu port yönlendirmesi içindir; normal yerel sunucu varsayılanı hâlâ loopback'tir. Port doluysa mevcut başka süreci kapatmadan önce inceleyin; Docker olmadan aşağıdaki başlatıcıda `--port 8874` kullanılabilir.

Tam offline kontrol için:

```sh
docker compose --env-file docker/compose.env run --rm --build checks
```

Kontrol konteyneri root olmayan kullanıcıyla, salt okunur dosya sistemi ve `network_mode: none` ile çalışır; geçici çıktı için yalnız `/tmp` ve belirli artifacts/dist alanları yazılabilir. Test/önizleme hizmetleri ayrı imaj hedefleridir; son önizleme imajında analiz kaynakları, Node ve NetCDF bulunmaz. `.dockerignore` varsayılan olarak her şeyi dışlar; yalnız gereken açık kaynak klasörleri içeri alınır. `.git`, portal, sanal ortam, özel artifacts, `.env` ve önceki dist imaja kopyalanmaz.

İmajlar resmi Python/Node çok mimarili index digest'lerine sabitlenir; pip geçişli sürümleri `docker/requirements.lock` içindedir. Host mimarisi varsayılan olarak seçilir. AMD64 ve ARM64 derleme/test sonuçlarını gerçek Mac donanımıyla eşitlemeyin. [Docker çok mimarili imaj açıklaması](https://docs.docker.com/build/building/multi-platform/), [Compose hizmetleri](https://docs.docker.com/reference/compose-file/services/).

## Docker olmadan

Mevcut çalışan analysis ortamı korunur. Windows CMD, depo kökünde:

```cmd
scripts\start-preview.cmd
```

Mac Terminal:

```sh
sh scripts/start-preview.sh
```

Başlatıcı önce eksik ortamı kurar, sonra kayıtlı veriyi yeniden derleyip önizlemeyi açar; terminal açık kalır, Ctrl+C ile kapanır. Mac başlatıcısı `python3`, sonra `analysis/.venv/bin/python` kullanır. Windows ilk ortam için `py -3` kullanır. Docker isteğe bağlıdır; Python kurulumu yoksa iki başlatıcı da bunu kendiliğinden işletim sistemine kurmaz.

Kurulumu ayrı çalıştırmak veya mevcut ortamın bağımlılıklarını kilitli sürümlere getirmek:

```sh
python3 scripts/workspace.py setup
analysis/.venv/bin/python scripts/workspace.py doctor
analysis/.venv/bin/python scripts/workspace.py check
```

Windows karşılığı ilk satırda `py -3`, sonraki satırlarda `analysis\.venv\Scripts\python.exe` kullanır. Kurulum analysis sanal ortamına pip paketleri yükler; global Python veya mevcut .env değişmez. Python 3.12 ve tam kontroller için Node 24 önerilen teknik ortamdır. Önizleme Node gerektirmez. `doctor` paket sürümlerini/bulunurluğunu bildirir; NASA isteği veya token okuma yapmaz, Docker motorunun hazır olduğunu garanti etmez.

`check`, ilk başarısız adımda durur: Python testleri, A/B nokta/alan/fraksiyon tekrarları, iki gerçek beş düğümlü yüzey akışı, JS hesap/sözdizimi ve web derlemesi. NetCDF veya Node eksikse tam başarı raporlanmaz. Kontrol geçici iş klasörü temizlenir, mevcut özel artifacts üzerine yazılmaz.

## Doğrulanabilir demo ZIP'i

Mac/Linux, depo kökünde:

```sh
analysis/.venv/bin/python scripts/workspace.py package
analysis/.venv/bin/python scripts/workspace.py verify-package web/artifacts/expedition73-preview.zip
```

Windows'ta Python yolu `analysis\.venv\Scripts\python.exe`. Varsayılan ZIP `web/artifacts/expedition73-preview.zip`; Git dışında kalır. Paketleme önce gerçek kaynakları yeniden derler, sonra **yalnız altı genel dosyayı ve manifest.json** ekler. Sabit dosya sırası/tarih/izinlerle aynı bayt girdisinden tekrar aynı ZIP üretilir. Manifest her dosyanın byte sayısı/SHA-256'sını ve aday/kayıttan çalışma durumunu taşır; yerel mutlak yol veya zaman damgası içermez.

`verify-package` arşivi çıkarmadan dosya listesini, boyut sınırını, hash'leri ve sonuç sözleşmesini kontrol eder. Değişmiş içerik, ek/yinelenen veya üst dizine giden girdiler reddedilir. Bu bir bütünlük kontrolüdür; dijital imza veya bağımsız NASA kaynak doğrulaması değildir. Hatalı yeni derleme eski başarılı ZIP'i bozmaz; eski paket yeni sonuç diye sunulmaz. `--output` yalnız `web/artifacts` altında başka bir `.zip` seçebilir.

ZIP'i ayrı, boş bir klasöre çıkarıp o klasörde aşağıdaki komutla açabilirsiniz (Windows'ta `python3` yerine `py -3`). `.mjs` MIME türü özellikle ayarlanır; Windows'un varsayılan `python -m http.server` davranışı bu dosyayı metin diye sunabilir.

```sh
python3 -c "from http.server import SimpleHTTPRequestHandler as H, ThreadingHTTPServer as S; H.extensions_map['.mjs']='text/javascript'; S(('127.0.0.1',8873),H).serve_forever()"
```

Arşiv çevrim dışı inceleme içindir; dosyaya çift tıklamak yerine HTTP gerekir. Yalnız çıkarılmış genel dosyaların bulunduğu boş klasörde çalıştırın, depo kökünü sunmayın. Yeni veri/hesap veya ekip senkronizasyonu yapmaz; bilimsel aday sınırlamaları korunur.

## Otomatik kontroller ve paylaşım sınırı

Güncellenen `analysis-checks.yml`, ilgili main/codex push'larında, PR ve manuel çalıştırmada tetiklenir. Windows/macOS/Ubuntu native işleri aynı `setup/check/package/verify-package` komutlarını kullanır; yalnız demo ZIP'i yedi günlük workflow artifact'i olarak yükler. Docker işleri AMD64 ve QEMU ARM64 için ağsız kontrol, sağlıklı önizleme ve HTTP smoke çalıştırır; kendi konteynerlerini son adımda kapatır. Kaynak kod/paket artifaktı erişimi GitHub depo izinlerine bağlıdır.

Workflow dosyasının hazırlanması uzakta başarıyla koştuğu anlamına gelmez. Bu yeni dilimin gerçek koşuları kanıt sayfasındadır. Registry push, main merge, Pages/Sites yayını veya otomatik dış NASA işi eklenmedi. GitHub dalına push, Docker imajını veya demo dosyasını arkadaşın bilgisayarına otomatik taşımaz; güncel kaynak alınarak komut yeniden çalıştırılır. [Ekip senkronizasyonu](../team/SYNC.md).

## Akış ekranıyla paket sürümü

2026-10-21 devam diliminde `trace.mjs` altıncı genel dosya oldu. Yeni ZIP manifesti 0.2.0 / web verisi 0.3.0; kaynak bilimsel şemalar ve teknik profil değişmedi. `verify-package` eski manifest 0.1.0 / web 0.2.0 beş dosyalı paketi kendi izin listesiyle hâlâ doğrular. Yeni arayüz eski web verisini reddeder; builder ile birlikte yenilenir. Hash denetimi bilimsel onay veya imza değildir. [Güncel akış kanıtı](../evidence/WORKFLOW_TRACE_CHECK.md); önceki Docker/Mac ortam sınırları ayrı tutulur.

## 2023–2024 yıl kataloğu

[Çok yıllı teknik dilim](T2M_HISTORY.md) yeni web zarfı 0.4.0/manifest 0.3.0 kullanır; altı dosya ve eski paket doğrulaması korunur. Yeni Windows 197 test/30 JS/49 Chrome kanıtı ayrı [history kaydındadır](../evidence/T2M_HISTORY_CHECK.md). Bu dilimde Docker motoru hazır olmadığı için yeni Linux/ARM64/Mac sonucu yok; önceki platform testleri bu yeni kodun testi sayılmaz.
