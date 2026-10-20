---
status: Validating
updated: "2026-10-20"
review_summary: "Üç yüzey ağırlığını aynı ayda karşılaştıran teknik ekranın sayısal ve tarayıcı kontrolleri."
change_summary: "164 analiz testi, 8 JavaScript hesap testi ve 22 Chrome senaryosu geçti; maske seçimi yapılmadı."
---
# Aday ağırlık karşılaştırması · Yerel doğrulama

2026-10-20, Windows/Python 3.12.14, yerel M1 dalı. Kullanıcının devam talebiyle U-02 ekranına, M2'nin beklediği yüzey hedefi tartışmasını destekleyen bir karşılaştırma eklendi. [Ürün ve çalıştırma](../product/RESULTS_PREVIEW.md). Maske/sınır/dönem veya yeni bilimsel yöntem seçimi değildir.

## Hesap ve görünen sonuç

Her seçili pencere için aynı ayın maskesiz, FRLAND ve FRLAND+FRLANDICE sıcaklıkları yan yana gösterilir. Grafikte seçili politika işaretlenir. İki açık karşıtlık vardır: **kara − maskesiz** ve **kara+kara buzu − kara**. Farklar aynı pencerenin aynı ayına aittir. A−B mekânsal farkıyla karıştırılmaz.

`web/src/comparison.mjs`, mevcut kayıtlı aylık serilerin ikili çıkarımlarını ve yılın en büyük mutlak farkını hesaplar. Sadece ilgili iki değeri geçerli olan ay kullanılır; her çiftin sayısı ayrıdır. Hiç geçerli çift yoksa maksimum null kalır. Tam eşit maksimumların bütün ayları korunur. Gösterim altı ondalıktır; maksimum hesaplanmadan önce yuvarlama yapılmaz. Sıcaklık hesabı, fraksiyonlar ve web veri sözleşmesi 0.2.0 değişmedi; yeni alan/servis veya NASA isteği yok.

Kayıtlı iki gerçek workflow'un fark ve maksimumları JavaScript hesabıyla birebir eşleşti:

| Aday pencere | En büyük mutlak kara−maskesiz farkı | En büyük mutlak kara+buz−kara farkı |
|---|---|---|
| A · Colorado çevresi | 0,000616 °C · Ağustos 2024 | 0,000000 °C · 12 ay eşit |
| B · Kuzey Alaska | 0,035105 °C · Kasım 2024 | 0,000577 °C · Ekim 2024 |

Bu farklar yalnız mevcut 2024 kayıtlarının ve homojen hücre fraksiyonu yaklaşımının aritmetik duyarlılığıdır. Ölçüm doğruluğu, toplam belirsizlik, güven aralığı, maske geçerliliği veya iklim etkisi değildir. Sıfır/küçük fark yüzey hedefinin aynı olduğu anlamına gelmez. [Bilimsel sınırlar](../research/SURFACE_SUPPORT.md) korunur.

## Gerçek doğrulama

- `analysis` içinde kendi sanal ortamıyla `python -m unittest discover -s tests`: **164 test / 27,386 saniye / OK**. Yeni Python hesap testi yok; mevcut builder paketi listesine yeni saf modül eklendi. Önceden var olan NumPy deprecation uyarısı hata üretmedi.
- İki nokta `validate`, A `validate-window`, B `validate-tiled-window` ve iki gerçek fraksiyon `--replay` komutu başarılı: A 56, B 55 hücre. Kaynak örnek dosyaları değiştirilmedi; token okunmadı.
- `node --test web/tests/comparison.test.mjs`: **8/8 test**, 113,003 ms. Negatif/pozitif/sıfır fark, ayrı çift eksikleri, tümü eksik, eşit maksimumlar, küçük farkın korunması, yanlış dönem/sayı/taşma ve gerçek A/B raporuyla eşleşme sınandı.
- `node --check web/src/app.js` ve `node --check web/src/comparison.mjs` geçti.
- `node web/tests/browser.cjs`, yüklü Chrome headless: **22 senaryo grubu başarılı**, ana sayfa JS hatası 0, dış origin runtime isteği 0. Yeni kontroller gerçek üçlü sıcaklıkları ve maksimum/aylarını, ay/politika eşleşmesini, boş seçim temizliğini, ikili eksik sayılarının 11/12 ile 12/12 ayrılmasını ve tümü eksikte null maksimumu doğrular. Önceki hücre/grafik/indirme/hata kontrolleri de geçti.
- İlk tarayıcı denemesi görünür sonuç beklerken zaman aşımına uğradı: Windows `.mjs` dosyasını `text/plain` sundu. `web/serve.py` yalnız bu uzantının MIME türünü açıkça `text/javascript` yapacak şekilde düzeltildi. Sunucu yeniden başlatıldı; modül HTTP 200 + JavaScript MIME kontrolü ve bütün tarayıcı testleri geçti. Hesap hatası değildi; ilk başarısız deneme saklanır.

Masaüstü 1440×1100 ve mobil 390×844 görüntüleri incelendi; yatay taşma yok. Karşılaştırma görselleri yerel ignored `web/artifacts/comparison-desktop.png` ve `comparison-mobile.png` altında. Sunucu HTTP 200 verdi; Codex panelinde açma isteği queued döndü, gerçek tarayıcı QA ayrı Chrome'da tamamlandı. Gerçek telefon/Mac/Ubuntu veya kullanıcı kabul testi değildir.

Git fetch'te main/M2 `a1a83d5` olarak aynıydı; yeni ekip katkısı yok. M2 adına bilimsel tercih/onay yazılmadı; yeni kod main/Pages'e yayımlanmadı. Yalnız `web/dist` sunulur; depo kökü/.env sunulmaz.

QA sunucusu final öncesi kapatıldı; loopback adresinin artık yanıt vermediği doğrulandı. Portal check/strict build ve git diff --check başarılı; uygulama hesap testlerinden ayrı belge kontrolleridir.
