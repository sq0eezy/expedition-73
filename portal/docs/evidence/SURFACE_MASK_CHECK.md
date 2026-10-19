---
review_summary: "Maske kaynağı araştırması, gerçek 401 sonucu ve sentetik hesap testlerinin kapsamı."
change_summary: "72 test geçti; 14 yeni test yalnızca maske hesabını denetler. Gerçek NASA maskesi alınamadı."
---
# Maske hazırlığı · Doğrulama kaydı

**2026-10-17, Windows/Python 3.12.14, `analysis/.venv`.** M1'in devam talebiyle [maske araştırması ve aday teknik profil](../research/SURFACE_MASK.md) hazırlandı. M2'nin yeni katkısı yoktu: fetch sonrası M1 dalı ve origin/main eşleşiyordu. M2'nin kendi üye notu, fikir ve H-M1-005 kaydı okundu; yeni kabul/çalıştırma beyanı üretilmedi.

## Gerçek erişim

CMR `M2C0NXASM` 5.12.4 granule sorgusu HTTP başarıyla metadata döndürdü. Kaynak granule/servis bağlantısı [erişim JSON'unda](https://github.com/sq0eezy/expedition-73/blob/codex/m1-modules-region-a/analysis/resources/merra2-mask-access.json). Aynı kayıttaki güncel OPeNDAP `.dmr.xml` isteği, giriş kullanılmadan **401 Unauthorized** verdi. Değer veya servis boyut metaverisi alınmadı. Giriş formu, cookie, kullanıcı adı, parola veya anahtar saklanmadı. Gerçek maskeli A/B sıcaklığı üretilmedi.

## Uygulama ve sentetik kontroller

`masking.py` ve iki CLI komutu: native hücre/indeks planı ve ayrı aday ağırlık önizlemesi. Maske girdi şeması; hücrelerin tam eşleşmesi, dört fraksiyonun aralığı/toplamı, kaynak/sürüm/birim, açık kara/buz seçimi, pozitif alan ve aylık kapsam denetlenir. Tam hücre oranının kırpılmış parçada kullanımı yaklaşık yöntem olarak çıktı uyarılarında kalır. Mevcut T2M çıktıları değişmedi.

**Son koşuda 72 test 14,248 saniyede geçti.** Bunun 58'i mevcut nokta/alan/parçalama kontrolleri, 14'ü yeni sentetik maske kontrolüdür. Yeni testler: iki eşit alanlı hücrede 10 ve 20 °C için 0,75/0,25 kara payıyla 12,5 °C; tamamı kara örneğinin eski seriyi geri vermesi; kara buzu seçiminin alanı değiştirmesi; eksik pozitif/sıfır ağırlıklı değer ayrımı; gerçek sıfır sıcaklık; tümü eksik ay; kayıp/fazla/tekrar/kaymış koordinat; dolgu/negatif/bozuk toplam; birim/ızgara/kimlik/zaman hatası; sentetik veriye açık katılım gereği ve maske dosya hash'i. Bunlar NASA fraksiyonlarının doğruluğunu kanıtlamaz.

Depo `analysis` klasöründe:

```powershell
& .\.venv\Scripts\python.exe -m unittest discover -s tests -v
& .\.venv\Scripts\python.exe -m expedition73 validate examples/a-point-2024/result.json
& .\.venv\Scripts\python.exe -m expedition73 validate examples/b-point-2024/result.json
& .\.venv\Scripts\python.exe -m expedition73 validate-window examples/a-window-2024
& .\.venv\Scripts\python.exe -m expedition73 validate-tiled-window examples/b-window-2024
```

Tümü geçti; eski gerçek yanıtlar yeniden hesaplandı. Yeni maske önizlemesi sentetik verilerle test edildi. Hazırlanan A/B planlarında 56/55 hücre ve sırasıyla boylam 107–114 / 38–48, enlem 252–258 / 316–320 indeksleri, kayıtlı sıcaklık hücreleriyle eşleşiyor. Plan canlı servis sözdizimi/erişim doğrulaması değildir.

## Durum

M1 geliştirme dalında aday çalışma; nihai maske/istatistik veya bölge kabulü yok. Gerçek alt küme, kimlik doğrulama ve kaynak dönüştürme doğrulaması açık. Ortak teknik profil yalnızca gözlenen 2024 denemelerini kaydeder; çalışma dönemi seçimi değildir. Portal check ve strict build geçti; geçici yerel sunucuda araştırma/kanıt/profil/devir/durum için beş HTTP yol/içerik kontrolü geçti ve sunucu kapatıldı. git diff --check hata vermedi. Bu belge kontrolleri NASA maskesi kanıtı sayılmaz. Bu maske sürümü için uzak Ubuntu CI veya gerçek Mac doğrulaması yapılmış sayılmaz.
