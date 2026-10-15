---
review_summary: "sq0eezy için Bölge B: ilk yapılacaklar, teslimler ve modül hazır olunca entegrasyon."
change_summary: "M1'in iş bölümü talebiyle Bölge B için sıralı görevler ve somut çıktı ölçütleri eklendi."
---
# Bölge B · sq0eezy'nin çalışma listesi

**Görev ataması:** M1, 2026-10-16 tarihinde Bölge B'yi sq0eezy'ye ayırdı. Bu atama kaydıdır; M2'nin çalışmaya başladığı veya sonuç ürettiği varsayılmaz. Görev durumları ve inceleyenler [iş panosunda](WORK_BOARD.md). İş bölümü: [ADR-005](../decisions/ADR-005-TEAM-OWNERSHIP.md).

**İlk gösterge:** 2 metre hava sıcaklığı. Modülleri M1 geliştiriyor; sen Bölge B'nin sınırını, veri uygunluğunu, bölgesel girdilerini ve sonuç kontrolünü hazırlıyorsun. Mevcut B adayı [Kuzey Alaska](../research/REGION_CANDIDATES.md); alan seçimi henüz kesinleşmedi. “B” bir iş kimliği; ülke/bölge kararının yerine geçmez.

## Hemen başlayacağın iki iş

1. **R-B01:** [Bölge B çalışma fişini](../research/regions/REGION_B_PROFILE.md) aç. Aday alanın neyi temsil ettiğini, önerilen sınırı ve kara/su durumunu kaynakla yaz. Ön arama dikdörtgenini kesin sınır sayma.
2. **R-B02:** Aynı fişte küçük bir NASA API denemesini belgele. İstenen değişken T2M; amaç önce gerçek sayısal değere erişmek. API dokümanı, sorgu parametreleri, tarih, birim, eksik değer ve dönen koordinat/zaman bilgisini kaydet. Sonuç alınamıyorsa gerçek hata ve denenen yolu yaz.

Bu ikisi için sıcaklık modülünün bitmesini beklemek gerekmiyor. API'ye sadece katalog kaydı sormak sayısal erişim denemesi sayılmaz. Birkaç aylık/noktalık deneme uzun dönem bölge eğilimi değildir.

## Baştan sona görevler

| Görev | Yapılacak | Beklenen çıktı ve bitiş ölçütü | Bağımlılık |
|---|---|---|---|
| R-B01 · Bölge tanımı | Adayı incele; analiz sorusu, gerekçeli sınır/poligon önerisi, kaynak ve sınır sürümünü yaz | Çalışma fişi dolu; haritada yeniden bulunabilir alan ve aday/kabul ayrımı açık | Başlayabilir |
| R-B02 · API erişimi ve kapsam | Küçük T2M yanıtı al; yükseklik tanımı, birim, tarihler, ızgara/alan kapsamı ve eksik değerleri incele | Tekrarlanabilir sorgu ve yanıt özeti; nokta/alan ayrımı ve gerçek hata/başarı kaydı | R-B01'in aday alanı yeterli |
| R-B03 · Ortak veri profili | A ile aynı sağlayıcı/ürün, gösterge, dönem, frekans ve varsa referans dönemini karşılaştır; B'nin kapsam sorunlarını bildir | [Ortak profil](REGION_WORKFLOW.md) için B uygunluk görüşü; farklı ürünler sessizce eşitlenmemiş | R-B02 + A'nın erişim özeti + M1'in profil taslağı; nihai sürüm henüz gerekmez |
| R-B04 · Küçük hesap ve entegrasyon | M1'in sürümlü modülüne B yapılandırmasını ver; bir tarih için bölge özetini bağımsız hesapla kontrol et | Kullanılan modül/sınır sürümü, örnek değerler/ağırlıklar ve karşılaştırma sonucu; uyumsuzluk varsa kayıt | R-B03 + MOD-02 + MOD-03 |
| R-B05 · Tam dönem kalite ve sonuç | Ortak dönem serisini aynı modülle üret; eksik/tekrarlı aylar, geçerli alan kapsamı, maske ve uyarıları incele | Kaynaklı seri/kalite/analiz çıktısı bağlantıları ve yöntem sürümü; veri yetersizliği açık | R-B04 + uygun uzunlukta gerçek seri |
| R-B06 · Bölgesel yorum ve web kontrolü | B'nin bulgusunu belirsizlik/kapsamla anlat; A ile karşılaştırmaya uygunluğunu ve web kartlarını kontrol et | Kısa bulgu notu, kaynaklar ve açık sorunlar; grafikte B/sınır/tarih/birim sonuçla aynı | R-B05; web kontrolü arayüz hazır olduğunda |

R-B04'te veri ürününde doğrudan kalite bayrağı yoksa varmış gibi üretme; sağlanan kapsam/eksiklik bilgilerini ve bilinmeyeni yaz. Ham hücreleri doğrudan eşit ağırlıkla ortalamak yerine modülün gerekçeli alan/kesişim yöntemini kontrol et. Bir nokta sorgusunu bölge ortalaması diye sunma.

## M1'e bırakacağın devir

[H-M1-002 için beklenen yanıt](../team/HANDOFFS.md) alanına veya kendi [M2 notuna](../team/members/M2.md) şu özeti ekle:

- Çalışılan görev kimliği ve [B fişi](../research/regions/REGION_B_PROFILE.md) bağlantısı.
- Aday/sınır önerisi ve gerçek erişim denemesinin sonucu.
- Kaynak/ürün, parametreler, birim, kapsama ve eksiklik.
- Modülün senden alacağı bölge girdileri; M1'den beklediğin sözleşme/sürüm/örnek çağrı.
- Engel, sonraki adım ve varsa incelenmesi gereken çıktı.

API erişim anahtarı/çerez/oturum bilgisi yayımlanan fişe yazılmaz. API ile yalnızca gerekli alt küme istenir; tekrarlanabilirlik için sorgu ve yanıtın kaynak/sürüm izi saklanır. Saklanacak sayısal örnek/sonuç dosyasının yeri henüz seçilmedi; kamuya uygun kanıt bağlantısını kaydet.

## Kendi AI aracına verebileceğin başlangıç metni

> Bu depoda Bölge B sorumlusu sq0eezy olarak çalışıyorum. Önce AGENTS.md, CURRENT_STATE, iki üye notu, planning/REGION_B.md, planning/REGION_WORKFLOW.md, iş panosu ve ilgili devirleri oku. İlk pilot T2M. Önce R-B01 ve R-B02 için gerçek kaynaklı bölge fişi ve küçük NASA API erişim denemesi hazırla. Bölgeler/ürün/dönem hâlâ aday; nokta yanıtını bölge ortalaması sayma. Modüller M1'in sorumluluğunda; B'nin girdilerini ve doğrulamasını hazırla. Sonucu kendi üye notuma ve görev kaydına işle; sıradaki bağımlılığı açıkla.
