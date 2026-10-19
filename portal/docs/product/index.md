---
review_summary: "Sunulacak web uygulaması ve tek göstergeli pilot ekranları."
change_summary: "Kayıtlı gerçek T2M için ilk yerel sonuç ekranı çalışıyor; nihai yığın ve bilimsel profil açık."
---
# Ürün deneyimi ve kapsam

**Kabul edilen:** Sunulacak çıktı bir web uygulaması; başlangıç tek göstergeli deneme: 2 metre hava sıcaklığı. [ADR-004](../decisions/ADR-004-MODULES-AND-PILOT.md). [İlk yerel sonuç ekranı](RESULTS_PREVIEW.md) mevcut kayıtlarla çalışıyor; görsel düzen ve kullanılan HTML/CSS/JS bu teknik prototipe ait. Nihai teknoloji, genel web sorumlusu ve bilimsel profil seçilmedi.

## İlk deneyim taslağı

1. **Keşif:** Haritada hazır alanları ve veri uygunluğunu gör; konu ağacından sıcaklık modülüne gir. Seçilmemiş alanlar aday etiketi taşır.
2. **Modül ayrıntısı:** Zaman serisi, kalite/kapsama, eğilim ve belirsizlik; ürün, gösterge tanımı, birim ve yöntem aynı seçim bağlamında görünür.
3. **A/B karşılaştırması:** Uyumlu gösterge/dönemle iki alanı incele; eğilim farkını ve belirsizliğini gör. Bölge içi anlamlılık ve eğilimler arası farkın testi ayrı anlatılır.

Ortak zaman seçicisi, duraklatılabilen oynatma ve hareketi azaltma desteği görsel taslakta yer alır. Animasyon gerçek zaman dilimlerini göstermeli; veri olmayan tarih için ara değer üretilirse bu görsel yöntem açıklanmalı. Gerçek çıktı gelmeden grafik/harita sunum sonucu sayılmaz.

## Arayüz ilkeleri

- Konu ağacı gezinmeyi kolaylaştırır; hesaplamanın hangi girdiden beslendiği ayrıca incelenebilir.
- Ortak kartlar karşılaştırmayı, özel ayrıntı alanı bilimsel derinliği korur.
- Veri yetersiz, uyumsuz karşılaştırma, hesaplanmadı ve güncel değil durumları görünürdür.
- Eğim, güven aralığı, geçerli gözlem ve kaynak birlikte gösterilir; yalnızca p-değeri etiketi kullanılmaz.
- Yeni bölge/modül veri ve hesap hazır olmadan etkin sonuç gibi açılmaz.

## Pilot sınırı

Tek gösterge, seçilecek tek ürün/sürüm ve ortak dönem, uygunluğu sınanacak iki alan. Önce veri erişimi ve bağımsız küçük hesap, sonra web: [pilot planı](../planning/PILOT.md). Serbest poligon, dünya genelinde anlık hesap, hesap sistemi ve genel modül editörü pilot sonrası değerlendirilecek önerilerdir.

Mevcut portal fikirleri, kararları ve işi tutar. Ürün barındırma kararı portalın Pages kararından ayrıdır.
