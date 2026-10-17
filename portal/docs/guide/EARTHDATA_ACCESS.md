---
review_summary: "Earthdata kaydından sonra yerel terminalde gizli token girişiyle NASA metadata erişimini sınama."
change_summary: "Parola/token kaydetmeyen sabit NASA uç nokta kontrolü hazırlandı; gerçek kullanıcı erişimi henüz denenmedi."
---
# Earthdata · Kayıttan sonra erişimi kontrol et

**2026-10-17 gerçek sonuç:** Kullanıcının bu komutu çalıştırmasıyla metadata isteği HTTP 200 verdi; dört maske değişkeni bulundu ve XML bütünlüğü kontrol edildi. [Kanıt](../evidence/EARTHDATA_METADATA.md). Bu başarı maske değerlerinin alındığı anlamına gelmez.

Hesap açmak, tarayıcı oturumunu Python isteğine otomatik taşımaz. `analysis/scripts/check_earthdata_access.py` kullanıcı terminalinde token'ı gizli alıp yalnızca daha önce CMR'de bulunan MERRA-2 sabitleri metadata adresine tek istek yapar. Parola istemez; token için komut satırı argümanı, ortam değişkeni veya kalıcı dosya kullanmaz.

## Windows · M1 için

1. [Earthdata profilini](https://urs.earthdata.nasa.gov/profile) aç, **Generate Token** ile token oluştur. [NASA token rehberi](https://urs.earthdata.nasa.gov/documentation/for_users/user_token).
2. Depo kökünde kendi PowerShell terminalinde çalıştır:

```powershell
& .\analysis\.venv\Scripts\python.exe .\analysis\scripts\check_earthdata_access.py
```

3. `Earthdata token (hidden; not saved):` satırına token'ı yapıştırıp Enter'a bas. Yazı/karakter görünmemesi normaldir. Token sohbet mesajına yapıştırılmaz.

Başarılı olursa script `NASA metadata access succeeded` ve `analysis/artifacts/earthdata-access-...` klasörünü bildirir. Klasörde `metadata.dmr.xml` ve `access-report.json` bulunur; token bulunmaz. `artifacts/` Git tarafından yok sayılır. Bu çıktı üzerinden kaynak değişkenleri/boyutları incelenir; maske değerleri henüz alınmaz.

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
