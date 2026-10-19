---
review_summary: "T2M için MERRA-2 kara/su oranı adayı, gerçek 401 erişim sonucu ve deneysel ağırlık kontrolü."
change_summary: "Gerçek M2C0NXASM fraksiyon alt kümeleri A 56/B 55 hücreyle alındı ve yeniden doğrulandı; bilimsel maske seçimi açık."
---
# Kara/su maskesi · Araştırma ve teknik deneme

**Durum: araştırma adayı ve deneysel altyapı.** Kesin maske veya analiz yöntemi seçilmedi. T2M örnekleri maskesiz olarak korunuyor. Gerçek NASA fraksiyonları artık iki açık aday ağırlık önizlemesinde uygulandı; bu kabul edilmiş bilimsel maske profili değildir. [Gerçek akış ve duyarlılık](../evidence/SURFACE_WORKFLOW.md).

## Kaynak adayı ve gerçek erişim

**Güncel sonuç · 2026-10-18:** Kullanıcının GES DISC onayı sonrası çalıştırdığı komut gerçek A/B alt kümelerini üretti. Yerel dosyalar ve iki `--replay` kontrolü başarılı; A 56/B 55 hücre, dört fraksiyon, koordinatlar ve kaynak dolgu kuralları doğrulandı. [Ayrıntılı kanıt](../evidence/SURFACE_SUBSET_CHECK.md). B’de 5 hücrede pozitif okyanus, 45 hücrede göl, 6 hücrede kara buzu oranı var; bunlar tüm kaynak hücresine ait oranlardır, aday alan toplam yüzdesi değildir. Önceki 401/403 ve “gerçek oran yok” ifadeleri ilk denemelerin tarihsel kaydıdır. Sonraki akışta FRLAND ile FRLAND+FRLANDICE için ayrı aday sıcaklık önizlemeleri üretildi; maske bileşen seçimi kabul edilmedi.


**2026-10-18 teknik adım:** Küçük A/B `.dap.nc4` alt kümesi için dönüştürücü ve yerel gizli-token komutu hazırlandı. Kaynak metadata'sı gerçek kayıtla denetlendi; 13 dönüşüm testi yapay NetCDF ile geçti. [Kılavuz](../guide/SURFACE_SUBSET.md), [doğrulama sınırı](../evidence/SURFACE_SUBSET_CHECK.md). Gerçek fraksiyon veri isteği henüz bekleniyor; aşağıdaki ilk hazırlık ifadeleri tarihseldir.

**Son durum · 2026-10-17:** İlk oturumsuz 401 denemesinden sonra kullanıcı yerel token kontrolünü çalıştırdı. [Gerçek metadata isteği HTTP 200](../evidence/EARTHDATA_METADATA.md); dört fraksiyon değişkeni ve 1×361×576 boyut sırası doğrulandı. Aşağıdaki 401 ifadeleri ilk denemeyi anlatır. Sayısal fraksiyonlar ve koordinat vektörleri henüz alınmadı.

[NASA GMAO veri erişim tablosu](https://gmao.gsfc.nasa.gov/gmao-products/merra-2/wmo-data-access_merra-2/) MERRA-2 için kara maskesini sabit veri olarak listeliyor. [NASA ürün kaydı](https://data.nasa.gov/dataset/merra-2-const-2d-asm-nx-2d-constants-0-625-x-0-5-degree-v5-12-4-m2c0nxasm-at-ges-disc-f6cfc) `M2C0NXASM` 5.12.4'ü hücre içindeki kara/göl/okyanus oranları içeren sabit model koleksiyonu olarak tanımlıyor. [Dosya şartnamesi §6, PDF sayfa 21](https://ntrs.nasa.gov/api/citations/20150019760/downloads/20150019760.pdf#page=21) dört değişkeni ayırıyor: `FRLAND` kara, `FRLANDICE` kara buzu, `FRLAKE` göl, `FROCEAN` okyanus; birimleri `1`.

2026-10-17'de [NASA CMR granule sorgusu](https://cmr.earthdata.nasa.gov/search/granules.json?short_name=M2C0NXASM&version=5.12.4&page_size=2) çalıştı; `G1277560809-GES_DISC`, koleksiyon `C1276812819-GES_DISC` ve güncel OPeNDAP bağlantısı bulundu. CMR sorgusunun UTC zamanı 09:08:22. Bu metadata bulgusudur; hücre kalitesi veya veri alımı kanıtı değildir.

CMR'deki OPeNDAP bağlantısına `.dmr.xml` eklenerek yapılan **kimlik doğrulamasız metadata isteği HTTP 401 Unauthorized döndürdü**. Gerçek fraksiyon, canlı değişken boyut sırası veya dolgu değeri alınamadı. [Makine okunur erişim kaydı](https://github.com/sq0eezy/expedition-73/blob/codex/m1-modules-region-a/analysis/resources/merra2-mask-access.json) yalnızca genel kaynak URL'lerini ve sonucu içerir; kimlik bilgisi içermez. POWER'ın oturumsuz çalışması bu ayrı koleksiyonun da oturumsuz erişileceği anlamına gelmez.

Eski `goldsmr4` adresini kodun içine varsayılan servis diye yazmadık. [NASA GES DISC'in 2026 servis açıklaması](https://forum.earthdata.nasa.gov/viewtopic.php?t=8140), bulut OPeNDAP adresini ve DAP4 alt küme sözdizimini açıklıyor. Gerçek authenticated metadata incelenmeden çalışır bir alt küme URL'si veya NetCDF dönüştürücü varmış gibi sunulmadı.

## Hazırlanan hücre planları

`plan-surface-mask` NASA'ya bağlanmadan mevcut aday dikdörtgenle kesişen sıcaklık hücrelerini ve kaynak dizinlerini listeler. Plan, yayımlanmış 0,625°×0,5° ızgara, başlangıç 180°B/90°G, 361 enlem/576 boylam varsayımını kullanır. Canlı servis boyut adları/sırası ve bu dört oran gerçek erişimde ayrıca doğrulanacak.

| Aday pencere | Hücre | Boylam indeksleri | Enlem indeksleri |
|---|---:|---|---|
| A | 56 | 107–114 | 252–258 |
| B | 55 | 38–48 | 316–320 |

İndeksler sıfırdan başlar, iki uç dahil; sabit veride zaman indeksi adayı 0. Dosyalar `analysis/examples/a-surface-mask-plan.json`, `b-surface-mask-plan.json`. Bunlar **istek planıdır, maske ölçümü değildir**. Planın `access_verified=false` ve `NO_MASK_VALUES_FETCHED` kayıtları korunur.

## Neden doğrudan “kara ortalaması” demiyoruz?

Kara ve kara buzu için hangi bileşenlerin dahil olacağı açıkça seçilmelidir. `FRLAND` ile `FRLAND + FRLANDICE` aynı tanım değildir; sessiz bir eşik veya varsayılan eklenmedi. Dört oranlı hücrenin yalnızca merkezine bakıp tamamını kara/su saymak da ayrıca bir yöntem seçimi olur.

Deneysel ağırlık `w = hücre∩aday_pencere_alanı × seçilen_tam_hücre_oranı`. Ortalama `Σ(w×T2M)/Σw`. Tam hücre oranının, hücrenin sınır içinde kalan parçasında da aynı olduğu **yaklaşımı** kullanılır; gerçek kıyı/poligon kesişimi elde edilmez. Daha ince çözünürlük üretilmez. Ayrıca kara oranıyla yeniden ağırlıklandırmak, hücre T2M'sini ayrı bir kara yüzey bileşenine ait sıcaklığa dönüştürmez.

`preview-surface-mask` bu nedenle ayrı `candidate_surface_weight_preview` türü üretir. `monthly_window_series` yerine geçirilmez; nihai bölgesel karşılaştırmaya veya trend çıkarımına otomatik onay vermez. Kaynak etiketini denetlemek uzak sunucu kaynak doğrulaması değildir; gerçek alt küme ve dönüştürme zinciri ayrıca sınanmalıdır.

## Çalıştırma

Mac'te `analysis` klasöründe kurulu ortamla:

```sh
.venv/bin/python -m expedition73 plan-surface-mask --config examples/a-window-2024.config.json
.venv/bin/python -m expedition73 plan-surface-mask --config examples/b-window-2024.config.json
```

Gelecekte gerçek kaynak alt kümesinden doğrulanmış biçimde dönüştürülen maske dosyasıyla önizleme çağrısı:

```sh
.venv/bin/python -m expedition73 preview-surface-mask --run examples/b-window-2024 --mask artifacts/b-surface-fractions.json --components FRLAND
```

`artifacts/b-surface-fractions.json` **henüz mevcut bir NASA örneği değildir**. Kaynak sözleşmesi `analysis/schemas/surface-fractions.schema.json`: bütün kesişen hücrelerin dört oranı, kaynak/ürün/sürüm/zaman/SHA-256 ve ızgara kimliği gerekir. Kaybolan hücreyi su kabul etmez. Toplam oran için `1e-6` tolerans vardır; eksik/dolgu/negatif değer reddedilir, gizli ölçek dönüşümü veya yeniden normalize etme yoktur.

Sıcaklık run'ı önce eski ham yanıtlardan yeniden hesaplanır. Pozitif ağırlıklı hücrede eksik aylık T2M varsa sonuç null; sıfır ağırlıklı su hücresinin eksikliği kara destekli adayı bozmaz. Etkin alan sıfırsa sıcaklık verilmez. Sentetik maske varsayılan olarak reddedilir; `--allow-synthetic` yalnızca test için açıkça gerekir ve çıktı sentetik etiketini taşır. Yapay sayılar NASA fraksiyonu diye depolanmadı.

Windows'ta aynı komutlarda Python yolu `& .\.venv\Scripts\python.exe`. Bu sürümün gerçek Mac çalıştırması doğrulanmadı.

## Gerçek veri için sonraki adım

**Kayıt adımı güncellemesi · 2026-10-17:** Earthdata kaydının tamamlandığı bildirildi. Canlı programatik erişim ve uygulama yetkisi henüz doğrulanmadı. Parola/token kaydetmeyen [yerel erişim kontrolü](../guide/EARTHDATA_ACCESS.md) hazır; önce bu metadata isteğinin gerçek sonucu incelenecek.

Kimlik doğrulamalı erişim henüz kurulmadı. [Earthdata Login](https://urs.earthdata.nasa.gov/) üzerinden Register ile hesap açıp etkinleştirmek, sonra koleksiyonun veri erişim akışında gereken uygulama yetkisini tamamlamak gerekir. [NASA kayıt rehberi](https://urs.earthdata.nasa.gov/documentation/for_users/how_to_register), [uygulama yetkisi açıklaması](https://urs.earthdata.nasa.gov/documentation/for_users/how_to_preauth_app). Kimlik bilgileri sohbet veya yayımlanan proje belgelerinde tutulmaz.

Ardından authenticated metadata, küçük A/B alt kümeleri, canlı boyut/ızgara/dolgu ve dört oranın anlamı kontrol edilecek; gerçek dönüşüm/yeniden üretim testi yapılacak. Maske tanımı ve sınır/parça yaklaşımı iki üyenin incelemesine sunulacak. Sabit fraksiyonlar yıllara göre değişen kıyı/bitki örtüsü modülü yerine geçmez.
