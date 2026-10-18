---
status: Validating
updated: "2026-10-18"
review_summary: "Gerçek kayıtlı T2M ve MERRA-2 fraksiyonlarıyla çalışan bağımlılık akışı ve aday duyarlılık hesabı."
change_summary: "İki gerçek girdi motorla bağlandı; A/B 12 ay için iki aday politika hesaplandı, 13 yeni test ve toplam 134 test geçti. Bilimsel maske seçilmedi."
---
# Gerçek verili modül akışı · Aday fraksiyon duyarlılığı

M1 devam talebiyle `analysis/expedition73/surface_workflow.py` ve `run-surface-workflow` komutu eklendi. Önceki [yapay A/B/C motoru](WORKFLOW_ENGINE.md) artık mevcut gerçek NASA örneklerini çevrim dışı doğrulayan işlemlerle de çalıştırıldı. Yeni bilimsel değişken/modül, uzun dönem trend veya kabul edilmiş maske değildir.

## Çalışan bağımlılıklar

~~~mermaid
flowchart LR
    T[Sıcaklık ham yanıtını yeniden doğrula] --> F[Fraksiyon dönüşümü ve T ile grid uyumu]
    T --> L[FRLAND aday önizlemesi]
    F --> L
    T --> I[FRLAND + FRLANDICE aday önizlemesi]
    F --> I
    T --> S[Duyarlılık raporu]
    L --> S
    I --> S
~~~

Fraksiyon değerleri sıcaklıktan türetilmez. F'nin T'yi tüketmesi, hesaplanacak pencerenin kimliği/sınırı ve kaynak hücrelerine **uygunluk kontrolü** içindir. Her iki önizleme aynı doğrulanmış sıcaklık ve fraksiyon çıktı kimliklerini alır; ortak üreticiler bir kez çalışır. Nihai rapor ata izini ve kaynak dosya özetlerini korur. İki girdi hazır/doğrulanmış olmadan önizleme çalışmaz.

`build` bütün gerekli dosyaları sınırlandırılmış boyutta bir kez belleğe alır. Callback'ler dosyaları tekrar açmaz; çalışma sırasında dosyanın değişmesi bu snapshot'ı karıştırmaz. Yeniden kurulan istekte ham dosya SHA-256'ları değişmişse önceki sonuçlar güncel değil saptanır. Bu örnekte context bütün girdi özetlerini içerdiği için geçersizleştirme muhafazakârdır; bir kaynak değişimi bütün akışı etkileyebilir. Cache veya otomatik kaynak takibi değildir.

## Gerçek girdiler ve tekrarlanabilir kayıt

- Sıcaklık: `analysis/examples/a-window-2024/` (0.1.0, tek istek, 56 hücre), `b-window-2024/` (0.2.0, iki parça, 55 tekil hücre). Kaynak NASA POWER Monthly and Annual API v2.10.0, T2M; eski ham yanıt/sonuçlar değiştirilmedi.
- Fraksiyon: [2026-10-18 gerçek M2C0NXASM alt kümeleri](SURFACE_SUBSET_CHECK.md), 5.12.4, FRLAND/FRLANDICE/FRLAKE/FROCEAN. Her bölgenin yalnız beş açık veri/üretim dosyası `analysis/examples/a-surface-fractions/` / `b-surface-fractions/` içine kopyalandı ve tekrar doğrulandı. Özel `.env` kopyalanmadı. [NASA MERRA-2 atıf rehberi](https://gmao.gsfc.nasa.gov/gmao-products/merra-2/citing-merra-2-data_merra-2/); sabit koleksiyon DOI: [10.5067/ME5QX6Q5IGGU](https://doi.org/10.5067/ME5QX6Q5IGGU).
- Aday çıktı: `analysis/examples/a-surface-sensitivity.json`, `b-surface-sensitivity.json`. Bunlar bir politika seçmez; maskesiz seri, FRLAND ve FRLAND+FRLANDICE sonuçlarını aynı 12 ay için yan yana tutar. Kaynak/zaman/hash, alan desteği, yöntem ve uyarılar kayıtta bulunur.

Farklı bölge/sınır kimliği, eksik/bozuk ham yanıt, kaynak özeti/dolgu/koordinat uyumsuzluğu reddedilir. A ve B'nin sonuçları birbirinin girdisi yapılmaz; aynı akış her bölge için ayrı çalışır. Genel bilimsel sözleşme veya gelecekteki çapraz bölge kıyaslama yöntemi bu çalışmayla kesinleşmez.

## Gözlenen aday sonuçlar · 2024, 12/12 eşleşen ay

| Tanı | A | B |
|---|---:|---:|
| En büyük aylık mutlak fark: FRLAND − maskesiz | 0,00061586 °C | 0,03510533 °C |
| En büyük aylık mutlak fark: FRLAND+FRLANDICE − FRLAND | 0 °C | 0,00057698 °C |
| Yaklaşık etkili destek / pencere alanı, FRLAND | 0,99962266 | 0,98146476 |
| Yaklaşık etkili destek / pencere alanı, FRLAND+FRLANDICE | 0,99962266 | 0,98163911 |

Ocak kontrolü: A maskesiz −0,3911184860 °C, iki aday −0,3915333442 °C. B maskesiz −24,1270314140 °C; FRLAND −24,1270243183 °C; FRLAND+FRLANDICE −24,1275930573 °C. A'da bu örnekte kara buzu oranı sıfır olduğu için iki aday aynı çıkar. Bu sayılar aynı ham hücre sıcaklıklarının yaklaşık ağırlıklandırmaya duyarlılığıdır. Çok küçük farklara fiziksel anlamlılık/anlamlı basamak iddiası eklenmez; sağlayıcı hassasiyeti ve model belirsizliği ayrıca değerlendirilmelidir.

**Bilimsel sınır:** Tam kaynak hücresi oranı kırpılmış parçada eşit kabul edilir; ince kıyı çizgisi çıkarılmaz. T2M kaynak hücre sıcaklığıdır, kara/buz alt parçasının bağımsız sıcaklığı değildir. Sayısal grid eşleşmesi ve ham yanıt tekrar hesabı bilimsel profil kabulü değildir. FRLAND seçimi mi kara buzunu da içeren seçim mi kullanılacağı, gerçek analiz sınırı, dönem ve istatistik hâlâ açık. Trend/p-değeri/nedensellik veya iki bölge arasında iklim değişikliği sonucu üretilmedi.

## Komutlar

Depo kökünden **Windows CMD**, kurulu analysis ortamıyla:

```cmd
cd analysis
.venv\Scripts\python.exe -m expedition73 run-surface-workflow --window-run examples/a-window-2024 --fraction-run examples/a-surface-fractions --output-dir artifacts/a-surface-new-run
.venv\Scripts\python.exe -m expedition73 run-surface-workflow --window-run examples/b-window-2024 --fraction-run examples/b-surface-fractions --output-dir artifacts/b-surface-new-run
```

Mac/Linux'ta aynı argümanlarla `.venv/bin/python -m expedition73 ...` kullanılır. Ortam ilk kez hazırlanıyorsa `python3 -m venv .venv` ve `.venv/bin/python -m pip install -r requirements-mask.txt`. Bu oturumda gerçek Mac çalıştırması yapılmadı.

Başarılı klasörde `request.workflow.json`, `workflow.json`, `sensitivity.json` bulunur. Girdi başarısızsa çıkış kodu 2, `workflow.json` içinde failed/blocked durumları olur; `sensitivity.json` yazılmaz. Var olan klasörün üzerine yazılmaz. Okuma/istek hazırlığı hatası hesap başlamadan çıkış 1 verebilir. Komut ağ/token istemez; yeni API isteği yapmaz. `workflow.json` çalışma kimlikleri ve tam girdiler nedeniyle daha büyüktür; `sensitivity.json` kaynak izli aday özetidir.

## Doğrulama

2026-10-18, Windows/Python 3.12.14, analysis sanal ortamı: **134 test / 42,985 saniye**, başarılı; bunların 13'ü yeni entegrasyon testidir. İki bölgenin gerçek girdileri bir kez tekrarlandı; ortak kimlikler korundu. Ocak ağırlıklı ortalaması bağımsız NumPy weighted average hesabıyla 11 ondalık basamakta uyuştu. Kayıtlı aday JSON'lar yeniden hesapla eşleşti. Yanlış bölge, bozuk fraksiyon/sıcaklık yanıtı, kaynak dosyasının snapshot sonrasında değişimi, politika etiketinin değiştirilmesi, eksik ay, çıktı üzerine yazmama ve başarısız işte sahte sonuç yazmama sınandı. Hata testindeki değiştirilmiş kayıtlar yapay hata örnekleridir, NASA bulgusu değildir.

Eski gerçek A/B nokta validate, A tek pencere ve B parçalı pencere replay ile iki fraksiyon replay komutu da başarılı. Son CLI çalıştırmaları `artifacts/a-surface-workflow-20261018-verified/` ve B eşinde tamamlandı; beş düğüm completed. Mevcut yapay NetCDF testinde NumPy deprecation uyarısı sürdü; hata yoktu. CI tanımı çevrim dışı fraksiyon/akış kontrolleriyle genişletildi, uzak CI bu oturumda çalıştırılmadı.

MOD-05/06 Validating; M2 bilimsel/kullanım incelemesi açık. Kayıtlar yerel M1 dalında, main/Pages yayını yapılmadı. Portal kontrolleri çalışma günlüğünde; bilimsel doğrulama yerine geçmez.
