---
status: Validating
updated: "2026-10-22"
review_summary: "Gerçek 2023 alımı, 2024 byte korunumu, yıllık kaynak birleştirme ve yıl seçimi/rapor geçişi."
change_summary: "A/B 24/24 ay; Windows 197 test, gerçek kaynak tekrarları, 30 JS ve 49 Chrome senaryosu geçti. Docker motoru hazır olmadı; yeni Linux sonucu yok."
---
# İki yıllık T2M geçmişi · Gerçek kontrol

## Yetki ve kapsam

M1, önce 2023–2024 denemesi, zaman parçalama/kalite ve daha sonra aday uzun dönem önerisi üzerine devam istedi. Temiz başlangıç 3e4e5ee, M1 dalı. Ekip/durum/fikir/devir/pano okundu. Fetch sonrası M2 dalı a1a83d5'ten **6047c42**'ye ilerlemişti; commit aralığı okundu: bunlar zaten M1 dalında bulunan önceki paylaşım commit'leri. Yeni bağımsız M2 kodu veya kabul notu yok; main a1a83d5. Yeni bilimsel dönem/maske/bölge veya M2 başlama kabulü çıkarılmadı.

[Kaynak, sözleşmeler ve komutlar](../guide/T2M_HISTORY.md). NASA'nın [Monthly belgesi](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/) yeniden okundu; yıllık parça denemesi kodun erişim stratejisidir. Son yılların genel erişimi veya 2001–2024 eksiksizliği bu iki yıllık testten çıkarılmaz.

## Gerçek kaynaklar ve sorunların çözümü

A için 2023 tek regional isteği, B için iki regional tile isteği başarıyla alındı. API v2.10.0/MERRA2/LST önceki 2024 kaydıyla eşleşti. B'nin ilk iki isteğinden sonra parent şemanın tek istek request_bbox alanını beklemesi saptandı; yeni history sonucu bunu ortak **request_envelope_bbox** alanında taşır. Eski A/B şemaları/byte'ları değiştirilmedi. B isteği düzeltme sonrası iki tile ile açıkça tekrarlandı; ilk başarısız toplama tamamlanmış kayıt bırakmadı. Toplam beş küçük NASA isteği yapıldı; token kullanılmadı.

Windows TemporaryDirectory'nin özel erişim kuralları rename sonrası normal çalıştırmayı engelledi. Yeni staging UUID'li normal klasörle parent erişimini devralır; yalnız doğrulanan, kendisine ait klasörü temizler. Bu oturumda eski yöntemle oluşmuş iki yeni açık örnek klasörünün inheritance erişimi onarıldı; eski örnekler/özel dosyalar değişmedi. Bir Set-Acl denemesi işletim sistemi ayrıcalık hatası verdi; yalnız bu yeni hedeflerde icacls inheritance ile çözüldü. Sonra yükseltilmiş offline B collect çıktısı standart çalıştırmada validate edildi; yeni yöntem okuma engelini üretmedi.

Yeni açık kayıtlar analysis/examples/a-history-2023-2024 (9 dosya/246.429 byte) ve b-history-2023-2024 (13 dosya/248.774 byte). Her iki seri 2023-01…2024-12, **24/24 tam ay**, eksik ay listesi boş. A 56/B 55 hücre ve aynı kaynak grid/alan yöntemi; yıllık B 2 tile/5 tekrar çıkarılması korunur. Kopyalanan bütün 2024 kaynak dosyaları eski örneklerle byte aynı; orijinal T2M/fraksiyon örneklerinde Git farkı yok.

## Doğrulama · 2026-10-22

- Windows/Python 3.12.14: `analysis\.venv\Scripts\python.exe scripts/workspace.py check`: **197 test / 49,798 s**, atlama/hata yok. Önceki nokta/uyum, A alan/B tiled, yeni A/B history replay, 56/55 fraksiyon ve iki gerçek yüzey akışı geçti. **30 JS / 187,491 ms**, syntax ve builder geçti. Son kontrolde eşdeğer tek istek/parçalı annual sözleşme uyumu da denendi; mevcut public snapshot byte'ları değişmedi. Mevcut NumPy/bozuk ZIP uyarıları dışında başarısız kontrol yok.
- 13 yeni history testi: gerçek 24 ay ve annual sonuçlarının aynılığı, 2024 byte korunumu, 24 yıllık/288 ay yalnız plan, geçersiz yıl/range, eksik/ters/tekrarlı kaynak, fazla dosya, bozuk raw, tek başına geçerli API sürüm değişiminin karıştırılmaması, eksik ayın null/23 tam ay kalması, eksik seed, network öncesi seed reddi, hata sonrası kısmi çıktı bırakmama ve okunabilir/offline/ezilmeyen çıktı; ayrıca eşdeğer tek istek/parçalı annual sözleşmelerin ortak alan zarfıyla birleşmesi. Dört yeni katalog testi: iki yıl ve eski exact 2024 snapshot'ı, registry/default reddi, farklı yıl aralığını sessiz kırpmama ve annual maskesiz seriyle birebir eşleşme.
- Yerel kurulu Chrome headless/Playwright: `node web/tests/browser.cjs` **49 senaryo grubu**, JS hatası/dış runtime isteği 0. Önceki 42 kontrol + yıl seçenekleri/gerçek 2023 değerleri, 2023 raporunun 2024'ten doğru yılı açması, eski 2024 raporunun geri açılması ve bozuk digest/takvim/tekrar/default kataloğunun reddi. 1440×1100/390×844 görüntüler incelendi; 2023 grafik/rapor ve telefon yıl seçici çalıştı. Katalog SHA kullanılamayınca önceki grafik/rapor kapatma yolu da korundu.
- HTTP smoke: altı dosya 200, .mjs JavaScript MIME, özel/kaynak yolları 404. Codex panel açma çağrısı queued; kullanıcının gördüğü varsayılmadı.
- Yeni katalog 554.378 byte. 2023 annual snapshot SHA `f4c23871f99661d75e99102208ac9cb15b17f33e373c1ee18bc75a14d941fa5b`; 2024 **d4ce2e87783af79ccee855a6a8040845cfd19776a405b52dc829c88c766e7169**, eski ZIP içindeki snapshot ile byte aynı.
- Demo iki kez üretildi: **644.736 byte**, SHA `a536c057fdc8f9e8f8c87480645f234d40b12547852583251e8be2e5dc6dc86c`; aynı byte/hash ve manifest doğrulandı. Yeni manifest 0.3.0; gerçek önceki 0.2.0 paket de yeni verifier'dan geçti.
- Docker motoru başlangıçta pipe yok hatası verdi; Docker Desktop start ve build yanıt vermeden kaldı, yalnız bu iki CLI oturumu durduruldu. Son altı saniye sınırlı docker info başarısızdı. **Bu sürüm için Linux/Docker/ARM64 veya gerçek Mac sonucu yok.** Eski 180/171 testli platform kanıtları yeni kodun kanıtı sayılmadı. Yeni bağımlılık eklenmedi; mevcut CI matrisi uzakta çalıştırılmadı.

## Sınırlar

Yeni history sonucu 0.1.0, annual source şemaları 0.1.0/0.2.0, bilimsel yöntem ve t2m-technical-2024 0.1.0 korunur. Yıl kataloğu 0.4.0 içinde annual web sözleşmesi 0.3.0 byte metinleri taşınır; rapor 0.1.0 değişmez. Grafik bir yılın 12 ayını gösterir; birleşik çok yıllı trend/önemlilik/güven aralığı hesaplanmadı. 2023'e uygulanan eski sabit fraksiyon aday duyarlılıktır, tarihsel kara örtüsü doğrulaması değildir.

2001–2024'ün gerçek 288 aylık kaynakları henüz alınmadı; yalnız yıllık plan kapsamı test edildi. Kesin dönem/sınır/yüzey/istatistik ve M2 kabulü açık. T-01/U-02/D-02 Validating; R-A05/R-B05 tam dönem görevleri tamamlandı sayılmaz. [H-M1-018](../team/HANDOFFS.md) panel içi inceleme kaydıdır. Yeni kod/veri yerel M1 dalında, push/main/Pages/Sites veya dış mesaj yok.

Son kontrol: portal içerik check ve strict build geçti; mevcut altı dosya doğrulanmış demo byte kaydıyla eşleşti. QA sunucusu kapatıldı, 8873 TCP bağlantısı kapalı doğrulandı. Eski 2024/fraksiyon örneklerinde Git farkı yok; yeni örneklerin hash byte koruması .gitattributes ile sürer. Portal kontrolü bilimsel sonuç onayı değildir.

Git notu: yeni A 2023 isteği/normalize kaydı Windows CLI kaynaklı CRLF byte kaydını korur. Örnek dosyalar yeniden biçimlendirilmedi; .gitattributes içindeki whitespace=cr-at-eol yalnız Git whitespace denetiminin bu korunmuş satır sonunu tanımasını sağlar. Varsayılan staged diff --check geçti; 22 yeni dosyanın staged/çalışma byte kaydı birebir eşleşti.
