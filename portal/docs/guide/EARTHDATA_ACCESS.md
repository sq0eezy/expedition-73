---
review_summary: "Earthdata kaydından sonra yerel terminalde gizli token girişiyle NASA metadata erişimini sınama."
change_summary: "GES DISC onayı sonrası gerçek A/B fraksiyon çıktıları alındı ve çevrim dışı doğrulandı; eski 403 adımları tarihsel."
---
# Earthdata · Kayıttan sonra erişimi kontrol et

**Güncel sonuç · 2026-10-18:** Kullanıcı GES DISC arşiv onayını tamamlayıp komutu çalıştırdığını bildirdi. Gerçek A/B fraksiyon dosyaları bulundu ve 56/55 hücre için çevrim dışı dönüşüm tekrarları geçti. [Kanıt](../evidence/SURFACE_SUBSET_CHECK.md). Aşağıdaki 403 notları çözüm öncesi denemeleri anlatır; yeni token girişi gerekmedi.


**Metadata kontrolü tamamlandıysa sıradaki komut:** [Küçük A/B fraksiyon alt kümesi](SURFACE_SUBSET.md). Yeni dönüştürücü hazırdır; aşağıdaki komut yalnız metadata kontrolü yapar.

**2026-10-17 gerçek sonuç:** Kullanıcının bu komutu çalıştırmasıyla metadata isteği HTTP 200 verdi; dört maske değişkeni bulundu ve XML bütünlüğü kontrol edildi. [Kanıt](../evidence/EARTHDATA_METADATA.md). Bu başarı maske değerlerinin alındığı anlamına gelmez.

Hesap açmak, tarayıcı oturumunu Python isteğine otomatik taşımaz. `analysis/scripts/check_earthdata_access.py` kullanıcı terminalinde token'ı gizli alıp yalnızca daha önce CMR'de bulunan MERRA-2 sabitleri metadata adresine tek istek yapar. Parola istemez; token değeri komut argümanına veya süreç ortamına yazılmaz. Kullanıcının 2026-10-18 talebiyle proje kökündeki Git dışında tutulan `.env` içinden `EARTHDATA_TOKEN` okuma ve `--save-token` ile açıkça kaydetme desteği eklendi.

## 2026-10-18 · Son deneme ve yerel kayıt

Kullanıcı yeni çalıştırmada önce 500 (yanlış değer yapıştırdığını bildirdi), sonra 403 gördüğünü iletti. Alt küme aşaması mesajı görünmedi; bu, yeni metadata isteğinin reddedildiğiyle tutarlıdır. Önceki HTTP 200 tarihsel gerçek sonuçtur; bugünkü erişimi garanti etmez. 403 nedeni yalnız durum koduyla belirlenmedi.

İlk kontrol: [Earthdata profilinde](https://urs.earthdata.nasa.gov/profile) Applications → Authorized Apps → Approve More Applications → **Hyrax in the cloud** → Authorize. Zaten onaylıysa Authorized Apps listesinde kontrol edilir; [NASA rehberi](https://urs.earthdata.nasa.gov/documentation/for_users/how_to_preauth_app) onaylı uygulamanın aramada görünmeyebileceğini belirtir. Aynı hesabın güncel token değeri kullanılmalı; uygulama yetkisi ve token geçerliliği birlikte kontrol edilir. Bu adımların 403’ü çözdüğü henüz gözlenmedi.

CMD terminalinde token’ı yerel `.env` içine bir kez gizli kaydetmek ve metadata’yı yeniden sınamak için:

```cmd
.\analysis\.venv\Scripts\python.exe .\analysis\scripts\check_earthdata_access.py --save-token
```

`--save-token` her kullanıldığında gizli yeni giriş ister ve yalnız `EARTHDATA_TOKEN` anahtarını ekler/değiştirir. Diğer ayarlar korunur. Token NASA isteğinden önce kaydedilir; 401/403 durumunda da yerel dosyada kalır. Sonraki çalıştırmada bayrak olmadan `.env` otomatik okunur; token yeniden sorulmaz. Eksik/boş anahtarda kaydetmeden gizli giriş yapılır; bozuk/tekrarlı anahtarda içerik basılmadan durulur. `.env.example` boş örnektir; token içermez. `.env` düz metin yerel dosyadır, Git ve yayımlanan portal dışında tutulur; kullanıcı gerçek token’ı bu sohbete göndermez. Bu oturumda gerçek token okunmadı veya dosyaya yazılmadı; kayıt kullanıcı komutuyla yapılacak.

## 2026-10-18 · Hyrax onaylı, GES DISC erişimi ayrı incelendi

Kullanıcının ekranında **Hyrax in the cloud** Approved Applications listesinde görünüyor. Kaydedilmiş token, değeri ekrana/rapora çıkarılmadan doğrudan isteklerde kullanıldı. Aynı token ile `https://opendap.earthdata.nasa.gov/hyrax/data/nc/fnoc1.nc.dmr.xml` HTTP 200 / DMR Dataset verdi; token olmadan bu örnek giriş yönlendirmesi istedi. M2C0NXASM metadata isteği ise HTTP 403 / `application/vnd.opendap.dap4.error.xml` verdi. Hata gövdesi yayımlanmadı; sınıflandırmada `data.gesdisc.earthdata.nasa.gov`, GES DISC/S3 ve Forbidden işaretleri görüldü. Böylece token dosyasının okunması ve Hyrax örneğine authenticated erişim doğrulandı; ürün erişimi doğrulanmadı.

Ekrandaki onaylı listede **NASA GESDISC DATA ARCHIVE** görünmüyor. [NASA Earthdata erişim rehberi](https://urs.earthdata.nasa.gov/documentation/for_users/data_access/curl_and_wget) veri alınan uygulamaya ayrıca ön yetki verilmesini ve GES DISC erişiminde ilgili GESDISC uygulamasının kontrolünü önerir. [GES DISC destek yanıtı](https://forum.earthdata.nasa.gov/viewtopic.php?t=6850) bu arşiv uygulamasını ele alır. Bu nedenle sıradaki hedefli kontrol: **Approve More Applications → GESDISC → NASA GESDISC DATA ARCHIVE → gerekli şartları incele → Authorize**. Bu izin tamamlanmış veya 403 çözülmüş sayılmaz; ürün tarafındaki başka bir erişim sorunu da henüz dışlanmadı.

Onay sonrası kayıtlı token ile CMD üzerinden `analysis\.venv\Scripts\python.exe analysis\scripts\fetch_surface_fractions.py` çalıştırılır; `--save-token` gerekmez. Yeni token üretmek veya Hyrax onayını kaldırıp eklemek bu bulgularla gerekli görünmüyor. Token değeri/özel JWT bilgileri bu kayda alınmadı, `.env` Git dışında kalır.

## Windows · M1 için

1. [Earthdata profilini](https://urs.earthdata.nasa.gov/profile) aç, **Generate Token** ile token oluştur. [NASA token rehberi](https://urs.earthdata.nasa.gov/documentation/for_users/user_token).
2. Depo kökünde kendi PowerShell terminalinde çalıştır:

```powershell
& .\analysis\.venv\Scripts\python.exe .\analysis\scripts\check_earthdata_access.py
```

3. `Earthdata token (hidden; not saved):` satırına token'ı yapıştırıp Enter'a bas. Yazı/karakter görünmemesi normaldir. Token sohbet mesajına yapıştırılmaz.

Aşağıdaki bayraksız komut mevcut `.env` değerini kullanır, yoksa kaydetmeden gizli sorar. Başarılı olursa script `NASA metadata access succeeded` ve `analysis/artifacts/earthdata-access-...` klasörünü bildirir. Sonuç klasöründe `metadata.dmr.xml` ve `access-report.json` bulunur; token bu çıktılara kopyalanmaz. Rapordaki `credentials_persisted` yerel `.env` kullanımını doğru yansıtır. `artifacts/` Git tarafından yok sayılır. Bu çıktı üzerinden kaynak değişkenleri/boyutları incelenir; maske değerleri henüz alınmaz.

## macOS · M2 için

Geliştirme dalındaki bu sürüm alınmış ve analiz ortamı kurulmuşsa, depo kökünden:

```sh
analysis/.venv/bin/python analysis/scripts/check_earthdata_access.py
```

M2'nin bu sürümü aldığı veya Mac'te çalıştırdığı varsayılmadı.

## 401/403 veya yönlendirme olursa

Token süresi/geçerliliğini ve veri uygulamasına yetkiyi kontrol et. [NASA uygulama yetkisi rehberi](https://urs.earthdata.nasa.gov/documentation/for_users/how_to_preauth_app): Applications → Authorized Apps → Approve More Applications. Bu servis için [OPeNDAP'ın resmî açıklaması](https://opendap.github.io/documentation/tutorials/ClientAuthentication.html) **Hyrax in the cloud** uygulamasını tanımlar; gereken uygulamayı yetkilendir. Kaydı oluşturmak, uygulama yetkisinin tamamlandığını kanıtlamaz.

Script yönlendirmeleri izlemez ve token'ı başka adrese taşımaz. [OPeNDAP token erişim belgesi](https://opendap.github.io/documentation/tutorials/ClientAuthenticationWithEDLTokens.html) Hyrax'ta doğrudan Bearer başlığıyla erişimi açıklar. Hata gövdesi/header/cookie ekrana basılmaz; HTML giriş ekranı geçerli veri sayılmaz. Gizli giriş desteklenmeyen terminalde görünür girişe dönmek yerine durur. Token yoksa veya erişim reddedilirse başarılı sonuç klasörü oluşturulmaz.

## Doğrulama sınırı

Yapay token ve XML ile otomatik testler, başlığın doğru kurulmasını, yönlendirme reddini, token yansıması/HTML/bozuk XML/boyut sınırını, gizli girişi ve hata metinlerinin kimlik bilgisi içermemesini denetler; otomatik testler canlı token kullanmaz. Ayrıca kullanıcının yerel gerçek isteği HTTP 200 ile doğrulandı: [kanıt](../evidence/EARTHDATA_METADATA.md). Bu DMR yanıtı metadata erişimini kanıtlar; fraksiyon değerleri/koordinat vektörleri, NetCDF dönüşümü ve bilimsel maske kararı sonraki adımlardır.
