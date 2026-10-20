# Expedition 73 · İlk sonuç ekranı

Kayıtlı gerçek NASA POWER T2M ve MERRA-2 fraksiyon örneklerini inceleyen **yerel teknik prototip**. Mevcut yönetim portalından ayrıdır; nihai web ürünü/yığın veya bilimsel profil kabulü değildir. Bu dilimde framework ve ek tarayıcı paketleri gerektirmeyen HTML/CSS/JS kullanıldı. Yayın/hesap sunucusu kurulmadı.

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
- Ay kaydırıcısı kartları ve grafik işaretlerini birlikte değiştirir; iki pencere seçiliyken o ayın A−B farkı gösterilir. Bu fark iklim eğilimi değildir.
- Hücre şemasında pencere seç; bir hücreye tıkla veya ok tuşlarıyla ilerle. Ayın gerçek grid T2M değeri, dört tam-hücre fraksiyonu ve seçili ağırlığın etkin alanı görünür. Renk politikayla değişmez; tüm ay/pencereler ortak ölçekte kalır. Şema alanı korumaz, kıyı çizgisi içermez.
- Koşullu alan kapsamı, kaynak AREA'nın bulunmaması ve hesaplanmamış eğilim açıkça görünür. Kaynak ayrıntısı ve erişilebilir değer tablosu açılabilir.
- JSON indirme seçili pencereleri/politikayı/ayı ve kaynak izlerini korur. Eksik değerler boş kalır, çizgide aralık atlanmaz; yükleme hatasında örnek değer üretilmez.

## Veri ve genişletme

`regions.json` yalnız gösterim adı, iş kimliği ve analysis içindeki kayıtlı kaynak klasörlerini seçer. Yeni uygun bölge için bir kayıt ekle; dönemi/göstergesi aynı, sürümlü pencere ve fraksiyon girdileri mevcut modül tarafından doğrulanmalıdır. Bu prototip bir tam yıl ve 1–8 pencereyi destekler. Başka gösterge veya serbest poligon desteği eklenmiş sayılmaz.

Builder önce her kaydı gerçek kaynaklarından yeniden hesaplar ve metadata hash'ini eşleştirir. Başarısız/uyumsuz girdide yeni kısmi çıktı üretmez. Sadece `src/index.html`, `styles.css`, `app.js` ve doğrulanmış seri/hücre `data/results.json` dosyasını `dist/` içine yazar. `.env`, ham özel artifacts, NetCDF, çalışma dizini veya token kopyalanmaz. Sunucu yalnız bu çıktı klasörünü loopback üzerinde sunar. Tarayıcı NASA'ya bağlanmaz; kaynak bağlantılarını açmak kullanıcının ayrı eylemidir.

Web aktarım sürümü 0.2.0; eski 0.1.0 web verisi yeni arayüzle reddedilir. Kod/veri birlikte builder ile yenilenir. Kaynak T2M/fraksiyon şemaları ve bilimsel yöntem sürümleri değişmedi.

`dist/` ve `artifacts/` Git dışında. Eski derleme varsa bir yeni derleme hatası onu güncellemez; hata sonrası eski çıktıyı yeni veri gibi sunma. Dosya değiştirince builder'ı tekrar çalıştır. Yönetim portalının mevcut Pages workflow'u bu klasörü yayımlamaz.

## Geliştirici kontrolü

Analysis testleri, **analysis içinde**: `.venv/bin/python -m unittest discover -s tests`. Windows karşılığı `.venv\Scripts\python.exe`.

İsteğe bağlı tarayıcı QA: Playwright paketinin bulunduğu Node ortamında, sunucu açıkken depo kökünden `node web/tests/browser.cjs`. Varsayılan yüklü Chrome; Edge için `EXPEDITION73_BROWSER=msedge`. Paket ayrı dizindeyse `EXPEDITION73_PLAYWRIGHT` mutlak paket dizini olabilir. Çalışan önizlemenin kendisi Node/Playwright gerektirmez. Test görüntüleri `web/artifacts/` altında tutulur.

[Ürün kapsamı](../portal/docs/product/RESULTS_PREVIEW.md) · [İlk ekran doğrulaması](../portal/docs/evidence/RESULTS_PREVIEW_CHECK.md) · [Hücre görünümü doğrulaması](../portal/docs/evidence/SPATIAL_PREVIEW_CHECK.md)
