---
review_summary: "Sunulacak web uygulaması ve tek göstergeli pilot ekranları."
change_summary: "Web uygulaması teslimi ve T2M pilotu kabul edildi; ilk ekranların kapsamı taslaklaştırıldı."
---
# Ürün deneyimi ve kapsam

**Kabul edilen:** Sunulacak çıktı bir web uygulaması; başlangıç tek göstergeli deneme: 2 metre hava sıcaklığı. [ADR-004](../decisions/ADR-004-MODULES-AND-PILOT.md). Ekran düzeni/görsel tasarım/teknoloji taslak; çalışan ürün henüz yok.

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
