---
review_summary: "Maskesiz aday dikdörtgen için alan ağırlıklı T2M denemesi ve Mac/Windows komutları."
change_summary: "Nokta profilinden ayrı bölgesel erişim, kenar hücreleri, eksik veri kuralı ve çevrim dışı yeniden hesaplama eklendi."
---
# T2M · İlk alan hesabı

`analysis/` artık **aday dikdörtgen için maskesiz aylık alan ortalaması** üretebiliyor. İlk [nokta adaptörü](T2M_ADAPTER.md) korunuyor. Bu deney kesin bölge seçimi, kara ortalaması veya iklim eğilimi değildir. [Gerçek sonuç ve kontroller](../evidence/T2M_WINDOW_PROBE.md).

## Mac üzerinde önce kaydedilmiş örneği doğrula

Depo güncelken, depo kökünden:

```sh
cd analysis
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m expedition73 validate-window examples/a-window-2024
.venv/bin/python -m unittest discover -s tests -v
```

Ortam zaten kuruluysa ilk iki kurulum komutunu atlayabilirsin. `validate-window` NASA'ya bağlanmaz; istek, ham yanıt ve sonuçtan geometriyi, ağırlıkları, aylık değerleri ve kaynak izini yeniden hesaplar. Son basamaklardaki platform farkı için sayı karşılaştırması `rel_tol=1e-12`, `abs_tol=1e-10`; ham yanıt SHA-256'sı ve metinler tam eşleşir. Gerçek macOS çalıştırma sonucu henüz bildirilmedi.

Yeni, küçük API denemesi:

```sh
.venv/bin/python -m expedition73 fetch-power-window --config examples/a-window-2024.config.json --output-dir artifacts/a-window-new-run
.venv/bin/python -m expedition73 validate-window artifacts/a-window-new-run
```

Var olan çıktı klasörü üzerine yazılmaz. API hatası sahte sonuç üretmez; yeniden deneme kullanıcı tarafından başlatılır. Büyük veri arşivi indirmek gerekmez; küçük API yanıtı tekrar hesaplanabilirlik için saklanır.

Windows PowerShell'de aynı işlemler `analysis` klasöründe `& .\.venv\Scripts\python.exe` ile çalışır. Örneğin:

```powershell
& .\.venv\Scripts\python.exe -m expedition73 validate-window examples/a-window-2024
```

## Hesap ne yapıyor?

1. İstek yapılandırmasındaki aday sınırı kullanır; hesap kodunda A'ya özel koordinat yoktur.
2. POWER aylık bölgesel T2M uç noktasından sınırın etrafına yarım hücre payı ekleyerek veri ister. Böylece merkezi dışarıda olup sınırla kesişen hücreler kaybolmaz.
3. Yanıtın MERRA2 kaynağını, 0,625° boylam × 0,5° enlem çıktı ızgarasına oturmasını, tekrarlanan/eksik hücreleri, birim ve tarihleri denetler. Farklı ızgarayı sessizce dönüştürmez.
4. Hücre kenarlarını komşu merkezlerin orta noktalarıyla yeniden kurar; aday dikdörtgenle kesiştirir. Bu, açık bir yöntem varsayımıdır; NASA'nın yanıtta verdiği hücre alanı veya poligon değildir.
5. Küre üzerinde kesişim alanını hesaplar: `A = R² × Δboylam(radyan) × [sin(kuzey) − sin(güney)]`; `R=6.371.008,8 m`. Aylık ortalama `Σ(A × T2M) / ΣA` olur. Hücre içindeki değer sabit kabul edilir; daha ince çözünürlük üretilmez.
6. **Bütün kesişen hücrelerde o ay veri varsa** ortalama yayımlar. Bir aylık değer dolguysa veya dönmediyse o ayın ortalaması `null` olur; geçerli hücre sayısı ve alan oranı ayrıca kalır. Kayıp alanı her ay farklı biçimde yeniden ağırlıklandırarak gizlemez. Tam bir coğrafi hücre dönmezse çalışmayı reddeder.

`202413` yıllık sağlayıcı özeti aylara katılmaz; hücre ayrıntılarında korunur. Her hücrenin kesişim sınırı, alanı ve aylık değer/dolgu durumu sonuçta tutulur.

## Ortak dil ve kapsam

Yeni çıktı türü `monthly_window_series`, şema sürümü `0.1.0`; eski `monthly_point_series` ile karıştırılmaz. Bölge, değişken, zaman, yöntem, kaynak izi, kalite ve seri alanları ortak yapıyı izler; hücre ayrıntıları `module_details` içinde kalır. Noktalar için olan `check-alignment` bölgesel sonuçları kabul etmez. Bölgesel A/B bilimsel uygunluk karşılaştırması henüz uygulanmadı.

İlk uygulama yalnızca **dikdörtgen, maskesiz, en çok iki yıllık** teknik denemeyi destekler. Yarım hücre payı dahil her eksende en çok 5° proje sınırı vardır; bu NASA'nın genel hizmet sınırı iddiası değildir. Kutup/tarih çizgisi aşan pay, keyfî poligon, arazi fraksiyonu, yükselti düzeltmesi ve istek parçalama desteklenmez. Mevcut 6° genişlikteki B arama penceresi bu sürümün tamamına tek istekte verilemez. M2 mevcut [nokta denemesini](T2M_ADAPTER.md) sürdürebilir; B sınırı/profili geldiğinde parçalama veya uygun veri yolu birlikte ele alınacak. B'yi sessizce küçültmeyin.

Kesin sınır, kara/su maskesi ve ortak A/B profili incelenmeden bu teknik hesap nihai bilimsel yöntem sayılmaz. Uzun seri, mevsimsellik/otokorelasyon, trend belirsizliği ve web görünümü sıradaki ayrı işlerdir.
