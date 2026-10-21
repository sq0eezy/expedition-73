# Expedition 73 · İlk sonuç ekranı

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
