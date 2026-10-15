# Bölge adayları araştırmasının kanıtı

**Tarih:** 2026-10-15. Kullanıcı, NASA'nın coğrafi veri düzenini araştırıp iki adayın gerekçeleriyle tartışmaya açılmasını istedi.

## Yöntem ve kaynaklar

Resmî Earthdata/CMR/AppEEARS belgeleri, MODIS ızgara açıklaması, NASA'nın Colorado Platosu ve Brooks Range çalışmaları incelendi. Kaynak bağlantıları ilgili iddiaların yanında [araştırma sayfasında](../research/REGION_CANDIDATES.md) bulunur. Sayısal veri dosyası indirilmedi.

Windows / PowerShell, portal Python 3.12.14 ortamından:

~~~sh
python scripts/probe_region_catalog.py --as-of 2026-10-15
~~~

Script yalnızca `cmr.earthdata.nasa.gov` üzerindeki açık metadata için GET sorguları yaptı; giriş veya bilimsel dosya indirme kullanmadı. Üç kesin ürün/sürüm/sağlayıcı için birer koleksiyon bulundu. İki arama dikdörtgeni × üç zaman aralığı × üç ürün = **18 granule sorgusu** yapıldı. Toplam 21 katalog isteği başarılı.

## Çıktı

[Sorgu URL'leri ve örnek granule kimlikleri](../research/REGION_CATALOG_CHECK.json). Koleksiyonlar: `C1276812859-GES_DISC`, `C2327962326-LPCLOUD`, `C3050353608-NSIDC_CPRD`. Üç üründe, iki bölgede ve iki örnek Temmuz sorgusunda da en az bir eşleşme bulundu.

2001–2024 aralığı için MERRA-2 her iki alanda 288 kayıt; MOD13A3 A'da 576, B'de 2258 kayıt; MOD10CM her iki alanda 284 kayıt döndürdü. Bunlar **dosya metaverisi kesişim sayılarıdır**. Piksel sayısı, geçerli gözlem sayısı veya ay bazında tamlık oranı değildir. Örneğin Temmuz 2001 kar sorgusu 2 kayıt döndürdü; zaman aralığı kesişimi ve tarih etiketleri ayrıca incelenmeli.

## Sınırlar

Arama pencereleri bu araştırmanın ön taslağıdır; resmî eko-bölge sınırı değildir. Dosya metaverisi gerçek alan içindeki geçerli pikselleri garanti etmez. Tüm ayların listesi, kalite maskesi, kara/bitki maskesi, bilimsel dosya erişimi ve trend/istatistik kontrol edilmedi. Kar modülü katalog sayısı nedeniyle ayrıca kapsam incelemesi bekliyor.

## Portal kontrolü

Portal ortamında `python scripts/portal.py check` ve `python scripts/portal.py build` başarılı. JSON çıktı Python ile açıldı; 2 bölge, 3 koleksiyon, 18 sorgu, her sorguda pozitif eşleşme ve örnek granule kimliği bulunduğu doğrulandı. Bu kontrol bilimsel piksel doğrulaması değildir.

PowerShell `Invoke-WebRequest` ile araştırma, mimari önerisi, ekip fikir kartı, bu kanıt sayfası ve JSON kaydı olmak üzere 5 yerel yol HTTP 200 döndürdü. `git diff --check` hata bildirmedi. Uygulama içi tarayıcıda araştırma sayfası açıldı; Proposed/aday durumu, iki adın özeti, kaynaklar ve katalog tablosu görüldü. Yerel önizleme Git dışında `.portal/region-candidates-preview.png` olarak saklandı; kişisel okuma işaretleri değiştirilmedi.

Portal motoru ve NASA analiz kodu değiştirilmedi. Yeni araştırma script'i gerçek açık CMR istekleriyle çalıştırıldı; eski okuyucu testleri bu belgeler için yeniden koşturulmadı.
