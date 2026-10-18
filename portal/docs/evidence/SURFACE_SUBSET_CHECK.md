# Fraksiyon alt kümesi · Gerçek A/B veri ve yazılım kontrolü

**2026-10-18, Windows / Python 3.12.14, analysis sanal ortamı.** `surface_source.py` ve `scripts/fetch_surface_fractions.py` hazırlandı. İlk hazırlıkta yalnız yapay dönüşüm testleri vardı; kullanıcı GES DISC onayından sonra komutu çalıştırdı ve aşağıdaki gerçek A/B sonuçları yerelden doğrulandı. [Çalıştırma](../guide/SURFACE_SUBSET.md).

## Gerçek A/B fraksiyon yanıtı · 2026-10-18

Kullanıcı arşiv onayını ve komutu çalıştırdığını bildirdi. `analysis/artifacts/surface-fractions-20261018T084254Z/` altında iki bölgenin request, NetCDF yanıtı, metadata, fractions ve dönüşüm raporu bulundu. Bu oturumda yeni ağ isteği yapılmadan iki bölge ayrı `--replay` ile doğrulandı. Yerel Windows/Python 3.12.14; netCDF4 1.7.2. CMD ekranına bu oturumdan doğrudan erişilemedi; sonuç, oluşmuş dosyalar ve yeniden hesap üzerinden kontrol edildi.

| Denetim | A | B |
|---|---|---|
| Kaynak | M2C0NXASM 5.12.4 | M2C0NXASM 5.12.4 |
| Yanıt zamanı (UTC) | 2026-10-18 08:42:57 | 2026-10-18 08:42:59 |
| Hücre / yanıt boyutu | 56 / 55.588 bayt | 55 / 55.588 bayt |
| SHA-256 (ham NetCDF) | `62cccbedac8849e2a5e8de79c44dc37bed3757eb701ec74ce126def1ca5f4584` | `e0355f23cf902bbe91aab964888863fc74648fe4885ef3714c2f4b8238948bc3` |
| Yeniden dönüşüm | Passed | Passed |
| Hücre toplamında en büyük mutlak sapma | 6,019 × 10⁻⁸ | 8,661 × 10⁻⁸ |

Her iki metadata SHA-256 özeti `baa82cb258a18165c39ec5da17e4e5ec3582ae7facf75e733534ac75f1a3d35a`; önceki gerçek metadata ile aynı. Ham yanıt özetleri rapor/normalize kaynak kaydıyla eşleşti. Dört oran, gerçek koordinat vektörleri, beklenen boyut/sıra/tür/birim, kimlik ölçek/ofseti ve dolgu kurallarıyla yeniden okundu; hiçbir hücre doldurulmadı veya yeniden örneklenmedi. 0–1 aralığı, tam hücre kapsamı ve toplam toleransı `1e-6` geçti. Raporlar yerel credential kaydını true gösteriyor; token bu veri dosyalarına kopyalanmadı.

Pozitif bileşen taşıyan kaynak hücre sayıları:

| Bileşen | A | B |
|---|---:|---:|
| FRLAND | 56 | 55 |
| FRLANDICE | 0 | 6 |
| FRLAKE | 4 | 45 |
| FROCEAN | 0 | 5 |

B’de okyanus oranı hücre başına 0–0,0489867; göl oranı 0–0,0794320, kara buzu oranı 0–0,00910387. Bunlar **bütün kaynak hücresinin fraksiyonlarıdır**; aday dikdörtgenin toplam deniz/göl yüzdesi veya yeni sıcaklık sonucu değildir. Pozitif sayımlar birbiriyle örtüşebilir. A’daki FRLAND aralığı 0,9843141–1; B’de 0,8989273–1.

Gerçek tekrar komutları, analysis klasöründe Windows:

```powershell
& .\.venv\Scripts\python.exe scripts/fetch_surface_fractions.py --replay artifacts/surface-fractions-20261018T084254Z/a
& .\.venv\Scripts\python.exe scripts/fetch_surface_fractions.py --replay artifacts/surface-fractions-20261018T084254Z/b
```

İki komut sırasıyla 56/55 hücre için `Surface conversion replay passed` verdi. Özel artifacts klasörü Git dışında tutuldu. Bu çalışma ham veri aktarımı/dönüşümü doğrular; bilimsel kara/buz politikası veya maskeli seri kabulü değildir.

## Önceki gerçek metadata denetimi

Önceden kullanıcı tarafından alınmış [HTTP 200 DMR yanıtı](EARTHDATA_METADATA.md), yeni `metadata_spec` ile tekrar okundu. Kaynak kimliği, 1×361×576 global boyut, dört Float32 oran, Float64 koordinat değişkenleri, zaman/birim ve dolgu/kimlik ölçek metaverisi beklenen yapıyla eşleşti. Bu sadece gerçek metadata'nın dönüştürücü giriş denetiminden geçtiğini gösterir; fraksiyon değerleri veya NetCDF veri yanıtı değildir.

## Yapay veri ile denetlenen

`test_surface_source.py` geçici klasörlerde **tamamen yapay NetCDF/DMR** üretir; NASA ölçümü veya gerçek maske örneği diye saklanmaz. 13 test; A/B boyutları ve bilinen oranlar, DAP4 alt küme indeksleri, metadata değişimi, koordinat kayması/ters sıra/tekrar, dolgu/NaN/sonsuz/aralık/toplam hatası, geçerli sıfır kara, birim/packing/boyut/eksik değişken, HTML/bozuk/aşırı büyük yanıt, tarih, sabit uç nokta, hash/çıktı tekrar kontrolü ve yerel yardımcı komutun başarı/hata davranışını denetledi. Sahte token ile iki bölgenin kaydı ve tekrar hesabı geçti; token dosyalara veya konsol çıktısına taşınmadı.

İlk tam koşu 91 testle geçti; ardından rapor tutarlılığı ve iki bölgeyi birlikte kaydetme kontrolü tamamlanıp 13 dönüşüm testi yeniden geçti. Önceki gerçek A/B nokta `validate`, A `validate-window`, B `validate-tiled-window` komutları başarılı. Son tam koşu 92 test / 9,289 saniye ile başarılı; portal check ve strict build, git diff --check geçti. [Çalışma günlüğü](../control-center/WORK_LOG.md). NetCDF 1.7.2 / NumPy 2.5.4 ile yapay veri yazımında NumPy deprecation uyarısı görüldü; test hatası yoktu. Bu paragraf ilk yazılım kontrolünü anlatır; gerçek fraksiyon yanıtlarının sonraki doğrulaması üsttedir. Mac üzerinde yeni fraksiyon komutu çalıştırılmadı.

## Sonuç sınırı

Yazılımın yerel dönüşüm/tekrar denetimi hazırdır. Gerçek küçük alt küme ve hücre oranlarının dönüşümü artık doğrulandı. Kaynak gridinin POWER ile bilimsel uygunluğu, kabul edilmiş kara/buz politikası ve maskeli seri hâlâ açıktır. A/B yıllık farkı veya iklim değişikliği bulgusu bu çalışmadan üretilmedi. İş MOD-05 kapsamında, M1 dalında; main veya canlı Pages'e yayımlanmış sayılmaz.
