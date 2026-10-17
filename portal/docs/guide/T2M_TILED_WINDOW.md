---
review_summary: "M2 için 6° B aday penceresini küçültmeden çalıştıran parçalı T2M erişimi ve Mac komutları."
change_summary: "İki gerçek NASA isteğini birleştiren destek, v0.2.0 çıktı ve çevrim dışı tekrar hesaplama eklendi."
---
# T2M · Geniş alanı parçalı isteklerle hesapla

**B'nin 6° genişliğindeki aday penceresi artık küçültülmeden işlenebiliyor.** Yeni `fetch-power-tiled-window` komutu alanı küçük isteklere böler, hücreleri koordinatlarına göre birleştirir ve orijinal pencere üzerinde alan ağırlıklı hesabı bir kez yapar. [Gerçek API ve test kaydı](../evidence/T2M_TILING.md). Bu, M1'in ortak modül teslimidir; M2 adına nihai alan veya bilimsel yorum seçimi değildir.

## Arkadaşın için Mac adımları

Önce kendi değişikliklerini commit edip koru; temiz main üzerinde güncelle ve kendi çalışma dalına geç. B dalın varsa aşağıdaki örnek yerine onun adını kullan. `codex/m2-region-b` yalnızca yeni dal için önerilen addır; varsa `git switch codex/m2-region-b` kullanılır.

```sh
git switch main
git pull --ff-only origin main
git switch -c codex/m2-region-b
cd analysis
```

Analiz ortamı zaten kuruluysa doğrudan doğrulamaya geç. İlk kurulum gerekiyorsa:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Kaydedilmiş gerçek B örneğini **NASA'ya bağlanmadan** doğrula:

```sh
.venv/bin/python -m expedition73 validate-tiled-window examples/b-window-2024
```

Yeni bir gerçek API denemesi istendiğinde:

```sh
.venv/bin/python -m expedition73 fetch-power-tiled-window --config examples/b-window-2024.config.json --output-dir artifacts/b-window-new-run
.venv/bin/python -m expedition73 validate-tiled-window artifacts/b-window-new-run
```

Var olan çıktı klasörü üzerine yazılmaz. `artifacts/` Git tarafından yok sayılır; incelenmemiş çıktıları topluca depoya eklemeyin. Windows PowerShell'de `analysis` içinde `.venv/bin/python` yerine `& .\.venv\Scripts\python.exe` kullanılır. Bu geliştirme Windows ve Ubuntu kontrolleriyle doğrulanır; bu sürümün gerçek Mac çalıştırması ayrıca M2 tarafından bildirilmelidir.

## Aynı modül, bölgeden ayrı ayarlar

`examples/b-window-2024.config.json`, M2'nin mevcut B arama penceresi `[-156,68,-150,70]` ve `search-window-0.1.0` üzerinden teknik modül denemesi için hazırlanmıştır. Başka alanda bölge kimliği/açıklaması, aday bbox/sürümü ve yıl aralığını yapılandırmada değiştir; kodda B'ye özel koordinat yoktur. `mask: none` gerçek kara maskesi değildir. A'nın dar penceresi de bu komutta tek parçayla çalışır.

Her parça gövdesi en fazla 4°×4° olur; çevresine MERRA2 ızgarasının yarım hücresi eklenir. B için iki gövde `[-156,68,-153,70]` ve `[-153,68,-150,70]`; istekler kenar hücreleri için üst üste biner. Gövdelerin araya boşluk bırakmaması ve tüm gerçek pencerenin bir kez hesaplanması test edilir. Enlem ve boylam boyunca iki yönde parçalama desteklenir.

## Ortak hücre ve hata kuralları

- Her yanıt önce mevcut [tek istekli alan adaptörünün](T2M_WINDOW.md) ızgara, hücre kapsamı, tarih, birim ve dolgu kontrollerinden geçer.
- Kaynak, API sürümü, zaman standardı, dolgu değeri ve tarih metaverisi parçalar arasında aynı olmalıdır.
- Aynı koordinattaki hücreler bir kez tutulur. Değer, aylık kayıt veya yükselti dahil hücre içeriği farklıysa işlem hata verir; sessiz ortalama veya birini seçme yapılmaz.
- Parça ortalamaları birbirleriyle ortalanmaz. Birleştirilmiş hücrelerin **asıl pencereyle kesişimleri** yeniden hesaplanır. Böylece örtüşen kenarlar iki kez ağırlık almaz.
- Bir coğrafi hücre eksikse çalışma reddedilir. Bir hücrenin aylık değeri eksik/dolguysa o ayın tüm pencere ortalaması `null` kalır; geçerli alan oranı saklanır.
- İstekler sırayla yapılır; otomatik tekrar yoktur. Bir istek başarısızsa tamamlanmış gibi bir sonuç klasörü üretilmez.

## Sürüm, kayıt ve yeniden hesaplama

Parçalı sonuç `monthly_window_series` türünde **şema/modül sürümü 0.2.0** kullanır. Bilimsel alan yöntemi aynı kalır: `spherical_midpoint_cell_intersection` 0.1.0. Eski nokta ve tek-istek 0.1.0 örnekleri/komutları çalışmaya devam eder. Nokta `check-alignment` komutu bu çıktının bölgesel uygunluğunu onaylamaz.

Çıktı klasörü: `request.json`, `manifest.json`, `tile-001.json`, `tile-002.json`… ve `result.json`. Her ham parçanın istek URL'si, UTC erişim zamanı ve SHA-256'sı kaydedilir. `validate-tiled-window` planı yeniden kurar; tüm ham parçaları doğrular, hücre birleşimi ve alan hesabını tekrar yapıp sonuçla karşılaştırır. Manifest dosya yolunu serbestçe belirleyemez; beklenen dosya adları yeniden oluşturulur. Sonuçtaki `request_envelope_bbox` tüm isteklerin dış zarfıdır; tek bir büyük API isteği değildir.

## Kalan sınırlar

Pilot en çok **16 istek ve iki yıl** destekler. Her isteğin pay dahil 5° proje sınırı korunur; bu NASA'nın genel hizmet sınırı iddiası değildir. Tarih çizgisini/kutbu aşan pay, keyfî poligon, kara/su fraksiyonu, yükselti düzeltmesi, uzun dönem trend ve istatistiksel çıkarım yoktur. Parçalama daha ince mekânsal çözünürlük üretmez. Kesin A/B sınırı, maske ve ortak bilimsel profil hâlâ incelenecek.
