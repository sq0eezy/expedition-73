# Expedition 73 · İlk sonuç ekranı

**2026-10-26 arayüz:** [Bütün 288 ay](../portal/docs/guide/T2M_TIMELINE.md) ayrı grafik/tablo ve ay seçiciyle incelenir. Seçilen ay yıl/ay/hücre/kaynak/rapor ayrıntılarına bağlıdır; pencere/yüzey seçimi ortaktır. Yalnız kayıtlı aylar taşınır, yeni istatistik/eğilim yok. Kaynak JSON byte'ları ve altı genel dosyalı sözleşme değişmedi. [Gerçek kontroller](../portal/docs/evidence/TIMELINE_PREVIEW_CHECK.md). Önceki tarihli bölümler ilgili dilimi anlatır.

**2026-10-24 güncel kayıt:** [2001–2024 aday dönemi](../portal/docs/guide/T2M_LONG_PERIOD.md), A/B 288'er ay ve yıl seçimi. Dönem satırı 24 yıl/288 kayıt gösterir; grafik yalnız seçilen yılın 12 ayıdır. Eski 2023/2024 rapor kimlikleri korundu; bilimsel eğilim ve maske kabulü yok. Çalıştırma aynı: Windows CMD `scripts\start-preview.cmd`, Mac `sh scripts/start-preview.sh`. Önceki bölümlerin sürüm/test sayıları ilgili tarihli dilime aittir.

Kayıtlı gerçek NASA POWER T2M ve MERRA-2 fraksiyon örneklerini inceleyen **yerel teknik prototip**. Mevcut yönetim portalından ayrıdır; nihai web ürünü/yığın veya bilimsel profil kabulü değildir. Bu dilimde framework ve ek tarayıcı paketleri gerektirmeyen HTML/CSS/JS kullanıldı. Yayın/hesap sunucusu kurulmadı.

## Kolay başlatma / Docker alternatifi

Windows: `scripts\start-preview.cmd`. Mac: `sh scripts/start-preview.sh`. Docker Desktop açıkken iki platformda aynı komut: `docker compose --env-file docker/compose.env up --build`. Başlatıcı her açılışta veriyi derler; Docker imajı değişince `--build` ile yenilenir. Docker önizlemesi için yalnız localhost portu açılır. [Kurulum, kontrol ve ZIP](../portal/docs/guide/DEV_PACKAGE.md), [gerçek doğrulama](../portal/docs/evidence/DEV_PACKAGE_CHECK.md).

## Windows CMD

Depo kökünde, mevcut analysis ortamıyla:

```cmd
analysis\.venv\Scripts\python.exe analysis\scripts\build_web_preview.py
analysis\.venv\Scripts\python.exe web\serve.py
```

Tarayıcı: **http://127.0.0.1:8873/**. Sunucuyu kapatmak: terminalde Ctrl+C. Sonraki açılışta veri/kod değişmediyse yalnız ikinci komut yeterli. Port doluysa `web\serve.py --port 8874` ile aç.

## macOS / Linux

Depo kökünde kurulu analysis ortamıyla:

```sh
analysis/.venv/bin/python analysis/scripts/build_web_preview.py
python3 web/serve.py
```

İlk kurulum gerekiyorsa `python3 -m venv analysis/.venv` ve `analysis/.venv/bin/python -m pip install -r analysis/requirements-mask.txt` kullanılır. Bu yeni ekranın gerçek Mac çalıştırması henüz bildirilmedi.

## Ekran

- A/B adaylarını birlikte veya ayrı göster; aynı yılın 12 aylık zaman serisini incele.
- Bütün pencere, FRLAND veya FRLAND+FRLANDICE ağırlığını açıkça seç. Son ikisi aday yöntemdir.
- Karşılaştırma bölümünde üç seçeneğin aynı ay değerlerini yan yana gör. Kara−maskesiz ve kara+buz−kara farkları, yılın en büyük mutlak farkı/ayı ve her çiftin geçerli ay sayısı gösterilir. Küçük fark yöntemin doğruluğunu kanıtlamaz; altı ondalık ölçüm doğruluğu değildir.
- Ay kaydırıcısı kartları ve grafik işaretlerini birlikte değiştirir; iki pencere seçiliyken o ayın A−B farkı gösterilir. Bu fark iklim eğilimi değildir.
- Hücre şemasında pencere seç; bir hücreye tıkla veya ok tuşlarıyla ilerle. Ayın gerçek grid T2M değeri, dört tam-hücre fraksiyonu ve seçili ağırlığın etkin alanı görünür. Renk politikayla değişmez; tüm ay/pencereler ortak ölçekte kalır. Şema alanı korumaz, kıyı çizgisi içermez.
- Koşullu alan kapsamı, kaynak AREA'nın bulunmaması ve hesaplanmamış eğilim açıkça görünür. Kaynak ayrıntısı ve erişilebilir değer tablosu açılabilir.
- JSON indirme seçili pencereleri/politikayı/ayı ve kaynak izlerini korur. Eksik değerler boş kalır, çizgide aralık atlanmaz; yükleme hatasında örnek değer üretilmez.

## Veri ve genişletme

`regions.json` yalnız gösterim adı, iş kimliği ve analysis içindeki kayıtlı kaynak klasörlerini seçer. Yeni uygun bölge için bir kayıt ekle; dönemi/göstergesi aynı, sürümlü pencere ve fraksiyon girdileri mevcut modül tarafından doğrulanmalıdır. Bu prototip bir tam yıl ve 1–8 pencereyi destekler. Başka gösterge veya serbest poligon desteği eklenmiş sayılmaz.

Builder önce her kaydı gerçek kaynaklarından yeniden hesaplar ve metadata hash'ini eşleştirir. Başarısız/uyumsuz girdide yeni kısmi çıktı üretmez. Sadece `src/index.html`, `styles.css`, `app.js`, `comparison.mjs`, `trace.mjs` ve doğrulanmış seri/hücre `data/results.json` dosyasını `dist/` içine yazar. `.env`, ham özel artifacts, NetCDF, çalışma dizini veya token kopyalanmaz. Sunucu yalnız bu çıktı klasörünü loopback üzerinde sunar. Tarayıcı NASA'ya bağlanmaz; kaynak bağlantılarını açmak kullanıcının ayrı eylemidir.

Web aktarım sürümü 0.3.0; eski 0.1.0/0.2.0 web verisi yeni arayüzle reddedilir. Kod/veri birlikte builder ile yenilenir. Kaynak T2M/fraksiyon şemaları ve bilimsel yöntem sürümleri değişmedi.

`dist/` ve `artifacts/` Git dışında. Eski derleme varsa bir yeni derleme hatası onu güncellemez; hata sonrası eski çıktıyı yeni veri gibi sunma. Dosya değiştirince builder'ı tekrar çalıştır. Yönetim portalının mevcut Pages workflow'u bu klasörü yayımlamaz.

## Demo paketi

Depo kökünde analysis ortamı Python'u ile `scripts/workspace.py package`, sonra `scripts/workspace.py verify-package web/artifacts/expedition73-preview.zip`. ZIP yalnız altı genel dosya ve hash manifesti içerir; Git dışındadır. Kaynaklar yeniden doğrulanır, özel .env/ham yanıt kopyalanmaz. Hash kontrolü bilimsel kaynak doğrulaması veya imza değildir.

## Geliştirici kontrolü

Analysis testleri, **analysis içinde**: `.venv/bin/python -m unittest discover -s tests`. Windows karşılığı `.venv\Scripts\python.exe`.

Saf karşılaştırma hesabı için depo kökünde `node --test web/tests/comparison.test.mjs web/tests/trace.test.mjs` (Node yalnız geliştirici kontrolü için). `comparison.mjs` sunucuda JavaScript MIME türüyle sunulur; Windows kayıt defterindeki metin türü kullanılmaz.

İsteğe bağlı tarayıcı QA: Playwright paketinin bulunduğu Node ortamında, sunucu açıkken depo kökünden `node web/tests/browser.cjs`. Varsayılan yüklü Chrome; Edge için `EXPEDITION73_BROWSER=msedge`. Paket ayrı dizindeyse `EXPEDITION73_PLAYWRIGHT` mutlak paket dizini olabilir. Çalışan önizlemenin kendisi Node/Playwright gerektirmez. Test görüntüleri `web/artifacts/` altında tutulur.

[Ürün kapsamı](../portal/docs/product/RESULTS_PREVIEW.md) · [İlk ekran doğrulaması](../portal/docs/evidence/RESULTS_PREVIEW_CHECK.md) · [Hücre görünümü doğrulaması](../portal/docs/evidence/SPATIAL_PREVIEW_CHECK.md) · [Ağırlık karşılaştırması](../portal/docs/evidence/POLICY_COMPARISON_CHECK.md)

## Kayıtlı modül akışı

Her pencerenin aynı gerçek çalıştırmasından beş adım ve sekiz bağımlılık gösterilir. Adıma tıkla veya Tab/Enter ile işlem sürümünü, çıktı sözleşmesini ve aldığı girdileri incele. Ay/politika seçimi bu akışı yeniden hesaplamaz. Yeni uygun bölge kaydı aynı builder ile ayrı akış üretir; arayüze bölgeye özel bağlantı yazılmaz.

`workflow_trace.project` gerçek artifact hash'lerini, çalıştırma/context/girdi/ata kimliklerini ve her adımın tek çalışmasını kontrol eder. Tarayıcıya yalnız küçük bir izin listesi aktarılır. Ekrandaki SHA-256 **iş tanımı kimliğidir**, gerçek çıktı artifact kimliği değildir; rastgele çalıştırma UUID'si ve özel parametreler dışarı verilmez. Böylece aynı kaynaklar ve tanımlarla ZIP tekrarlanabilir kalır. Bilimsel doğruluk, canlı görev monitörü veya kalıcı cache kanıtı değildir. [Gerçek kontrol](../portal/docs/evidence/WORKFLOW_TRACE_CHECK.md).

Yeni ZIP manifesti 0.2.0, web verisi 0.3.0 kullanır. `verify-package` önceki manifest 0.1.0/web 0.2.0 beş dosyalı ZIP'i de doğrular; eski web verisini yeni arayüzle karıştırmaz.

## İki pencerenin aynı ay farkı

“İki pencere arasında” bölümünde görünür kayıtlardan farklı bir çift seç, sol−sağ yönünü değiştir. Üstteki ay/yüzey seçimleri bu bölüme de uygulanır. Aylık fark, geçerli çift sayısı ve en büyük mutlak fark/ayları grafikte ve tabloda incelenir. Eksik aylar doldurulmaz. Teknik koşul tablosu gösterge/zaman/kaynak/grid ve tüketilen işlem sürümlerini kontrol eder; kara seçeneklerinde fraksiyon snapshot'ı da eşleşmelidir. Uyumsuz çift için fark gösterilmez. Bu betimsel mekânsal farktır; eğilim, iklim değişikliği etkisi veya bilimsel yöntem kabulü değildir. [Esas doğrulama](../portal/docs/evidence/REGION_COMPARISON_CHECK.md).

Yeni hesap mevcut comparison.mjs içindedir; web 0.3.0, altı genel dosya ve manifest 0.2.0 korunur. JSON indirme kaynak kayıtlarını taşır, bu yeni çift özetini eklemez. Son kontrol: Windows 180 analiz testi/gerçek A/B, 22 JS ve 36 Chrome senaryosu; bu sürüm için yeni Mac/Docker koşusu yok.

## Karşılaştırmayı raporla tekrar açma

Uyumlu çift/yön/ay/yüzeyi seçip **Karşılaştırma raporunu indir**. Aynı veri kaydı açıkken **Raporu aç ve doğrula** alanından seç: kaynak hash'i ve yeniden hesaplanan bütün alanlar eşleşirse seçimler açılır. Hatalı/farklı kaynakta seçimler korunur. Dosya sunucuya yüklenmez; 128 KiB sınırı ve Web Crypto yoksa raporları kapatma yolu var. [Kullanım/sözleşme](../portal/docs/guide/COMPARISON_REVIEW.md), [gerçek kontrol](../portal/docs/evidence/COMPARISON_REVIEW_CHECK.md).

Ayrı rapor 0.1.0; web 0.3.0/altı dosya/manifest 0.2.0 ve önceki genel JSON indirme korundu. JS farkı tekrar hesaplanır, NASA ham dönüşümü tarayıcıda tekrarlanmaz. SHA-256 imza/bilimsel/yazar kabulü değildir. Windows 180 analiz/gerçek A-B, 30 JS ve 42 Chrome senaryosu geçti; yeni Mac/Docker/uzak CI yok.

## Yıl seçimi · 2023 ve 2024

Kayıtlı yıl alanından 2023/2024 seçilir; grafik o yılın 12 ayını gösterir. Ay/yüzey/çift korunur. Yeni history-regions.json kayıtları yıllık kaynakları seçer; builder tüm geçmişi ve her yıllık T2M/fraksiyon akışını tekrar doğrular. 2023'te aynı sabit fraksiyon yalnız aday duyarlılıktır. [Kullanım/CLI](../portal/docs/guide/T2M_HISTORY.md), [gerçek kontrol](../portal/docs/evidence/T2M_HISTORY_CHECK.md).

Dış web zarfı 0.4.0 yıllık katalogdur. Her snapshot aynı 0.3.0 annual verisini exact UTF-8 JSON metni ve hash ile korur; eski standalone 0.3.0 da açılır. Eski 2024 raporları çalışır; başka yılın raporu doğru yıl snapshot'ında doğrulanıp yılı değiştirir. Kaynak kimliği artık seçili annual snapshot byte'larıdır; katalog zarfının tamamı değildir. Altı genel dosya, rapor 0.1.0; yeni manifest 0.3.0 ve eski 0.1.0/0.2.0 ZIP doğrulaması korunur. 197 Windows analiz, gerçek replay, 30 JS ve 49 Chrome senaryosu geçti; bu dilimde yeni Mac/Docker/Linux başarısı yok. Çok yıllı tek çizgi/trend ve gerçek 2001–2024 serisi henüz yok.
