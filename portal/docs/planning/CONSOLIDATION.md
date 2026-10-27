---
status: In progress
updated: "2026-10-27"
review_summary: "Çalışan sıcaklık temelini main'e alma, arayüzü sadeleştirme ve yeni modülü ayrı adımlarla sınama."
change_summary: "M1 toparlamayı ve main teslimlerine başlamayı istedi; ilk paket mevcut testli T2M temeli, yeni arayüz/modül sonraki işler."
---
# Toparlama · Adım adım teslim

M1, 2026-10-27'de yapılanları main'e almaya başlanmasını, sıcaklık modülünün bitiş durumunun açıklanmasını, daha sonra yeni bir modül denenmesini ve arayüzün sadeleştirilmesini istedi. İşler ayrı teslimlere bölünür. Bu ilk teslim için main birleştirme yetkisi vardır; sonraki her dal push'u kendiliğinden main yetkisi değildir. M2'nin bilimsel yöntem veya yeni ekran kabulü varsayılmaz.

| Adım | Somut çıktı | Durum |
|---|---|---|
| 1 · Çalışan T2M temeli | Mevcut API/kayıt/replay, 2001–2024 seri, aday yıllık hesap, bağımlılık motoru, teknik sonuç ekranı ve çalışma paketini incelenmiş sürüm olarak main'e al | Tamamlandı: 6db86b2 main'de; beş iş/Pages/HTTP başarılı; [teslim kanıtı](../evidence/T2M_BASELINE_RELEASE.md) |
| 2 · Karşılaştırma çalışma alanı | Uzun tek sayfayı görev odaklı bölümlere ayır; ortak seçimler ve ana kıyas aynı çalışma alanında olsun | [Taslak](../product/COMPARISON_WORKSPACE.md); yeni arayüz henüz uygulanmadı |
| 3 · Yeni gösterge için küçük veri sınaması | NASA ürün/parametre, tanım/birim, zaman, grid ve eksiklik uygunluğunu küçük gerçek örnekle doğrula | Gösterge/ürün seçilmedi; yeni modül başlamadı |
| 4 · İkinci modülün bağlantı denemesi | Özel bilimsel hesabı + ortak adaptör + T2M ile açık uygunluk/girdi sözleşmesi + bağımsız küçük doğrulama | 3'ün sonucu ve yöntem tasarımı gerekir |

Bu sıra ilk paketten sonra izlenecek önerilen iş sırasıdır; ekran taslağının tamamı veya ikinci gösterge seçilmiş sayılmaz. Bir teslimde hem arayüzü hem bilimsel hesabı değiştirmeyerek sonuç değişiminin kaynağı izlenir. Yeni geliştirme M1 dalında sürer; main ortak ve testli temel olarak korunur.

## Sıcaklık modülü bitti mi?

**Teknik ilk sürüm hazır; bilimsel pilotun tamamı bitmedi.** [Pilot bitiş durumu](PILOT.md#2026-10-27-bitis-durumu) esas kayıttır. Veri alma/normalleştirme, kayıtlı ham kaynaktan tekrar hesaplama, aylık/yıllık aday sonuçlar, taşıma/uygunluk sözleşmeleri ve webde inceleme çalışır. Eğilim, belirsizlik ve nihai bilimsel profil tamamlandı diye işaretlenmez.

İkinci modülü küçük bir veri/uygunluk denemesi olarak sınamak mümkündür. Bu, sıcaklık pilotunun bütün açık bilimsel işleri bitti demek değildir. Yeni modül, sırf sıcaklıkla fiziksel ilişkisi olduğu için sıcaklıktan hesaplanmış sayılmaz; NASA'dan doğrudan gelen bağımsız gösterge ile iki göstergeyi tüketen ilişki hesabı ayrı tasarlanır.

## İlk teslimin sınırı

Mevcut testli teknik paket bir bütün olarak alınır; birbirine bağlı history/builder/JS/veri sürümleri rastgele commit seçilerek ayrılmaz. Yeni arayüz tasarımı veya ikinci modül kodu bu pakete eklenmez. Main'e kaynakların gelmesi, yönetim portalının Pages yayınına girmesini sağlar; sonuç uygulamasının barındırılması ayrı konudur. Mevcut Pages workflow yalnız portal/site yayımlar.
