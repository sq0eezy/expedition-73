---
review_summary: "Bölgeyi ve açılacak modülleri NASA verisine bağlayan, henüz kabul edilmemiş ürün/mimari taslağı."
change_summary: "Kullanıcının bölge→modül→karşılaştırma fikri; veri, ortak ölçüm ve nedensellik sınırlarıyla işlendi."
---
# Bölge + veriyle açılan modüller

**Güncel durum:** Modüle özel hesap + ortak çıktı yaklaşımı ve tek göstergeli T2M pilotu [ADR-004](../decisions/ADR-004-MODULES-AND-PILOT.md) ile kabul edildi. Bu sayfa ilk bölge/modül gerekçesini korur; kesin alanlar, ürünler ve dönem hâlâ öneridir. Güncel teknik kaynak [modül sistemi](MODULE_SYSTEM.md), uygulama sırası [pilot planıdır](../planning/PILOT.md). Türkiye yalnızca örnekti.

## Kullanıcının düşüncesi

Bir bölge seçmek, NASA verilerine göre o bölgeye modüller eklemek, ikinci bölgeyi aynı biçimde incelemek ve karşılaştırmak. Zaman kalırsa yeni modüllerle genişletmek. Bölgelerin ve modüllerin veri uygunluğuna dayanması kullanıcı için temel koşul.

## Önerilen düzenleme

1. **Araştırma sorusu:** Ne ölçüp neyi karşılaştıracağımızı yazalım.
2. **Veri uygunluğu:** Ürün/sürüm, kapsam, erişim, kalite ve ortak dönem küçük örnekle sınansın.
3. **Bölge profili:** Yeniden bulunabilir sınır, kara/ekosistem maskesi ve aday statüsü tutulsun.
4. **Modül kartı:** Ölçülen değişken, birim, yöntem, uygun zamanlar ve veri durumu kaydedilsin.
5. **Karşılaştırma:** Aynı değişken ve uyumlu dönemle ortak modüller kıyaslansın; bölgeye özgü göstergeler ayrıca anlatılsın.

“İklim değişikliği” ana tema olabilir; hesap yapan modüller sıcaklık, NDVI veya kar örtüsü gibi tanımlı göstergelere dayanmalı. Bir modül ancak uygun sayısal veriyle desteklendiğinde açılacak adaydır. Katalog eşleşmesi tek başına uygulamada “hazır” durumu üretmemeli.

~~~mermaid
flowchart TB
    Q[Araştırma sorusu] --> D[NASA ürün ve erişim incelemesi]
    D --> P[Küçük sayısal pilot ve kalite kontrolü]
    P --> R[Aday bölge profilleri]
    R --> C[İki bölgede ortak gösterge modülleri]
    R --> S[Veri uygunsa bölgeye özgü modüller]
    C --> V[Aynı ölçüm ve ortak dönemle karşılaştırma]
    S --> H[Ayrı göstergelerle bölgesel anlatım]
    V --> E[Kaynak, yöntem, belirsizlik ve sınırlar]
    H --> E
~~~

## Her modül için uygunluk kartı

| Alan | Karar öncesi gereken |
|---|---|
| Soru ve ölçülen büyüklük | İklim/bitki etkisi gibi geniş başlık yerine somut ölçüm |
| Ürün ve coğrafi yapı | NASA görevi/modeli, kısa ad, sürüm, çözünürlük, karo/ızgara |
| Erişim | Sayısal örnek gerçekten alınabildi mi; hangi yolla? |
| Bölge uygunluğu | Sınır, maske ve yeterli geçerli gözlem |
| Zaman | Veri sıklığı, ortak dönem, referans ve mevsim tanımı |
| Analiz | Eğim birimi, belirsizlik, anlamlılık ve varsayımlar |
| Karşılaştırma rolü | Ortak ölçüm / bölgeye özgü bağlam |
| Durum | Araştırılıyor / sayısal örnek incelendi / uygun / uygun değil |

Son iki satır tasarım önerisidir; portalın mevcut otomatik durum mekanizması veya uygulanmış veri şeması değildir.

## Başlangıç kapsamı önerisi

Önceki iki göstergeli sıcaklık/bitki örtüsü önerisi daraltıldı: ilk pilot **yalnızca 2 metre hava sıcaklığı**. NDVI ve kar daha sonraki adaylar. İki bölge, ürünler ve 2001–2024 dönemi henüz onaylanmadı. [Güncel pilot](../planning/PILOT.md).

**Yeni modül ekleme koşulu:** Yeni bir soruya katkı, NASA sayısal kaynağı, erişilebilir örnek ve yeterli kalite. Modül sayısı başarı ölçütü olarak seçilmedi.

## Yorum sınırı

Farklı eğilimler beklenebilir ama vaat edilmez. İki yerde de artış, belirsiz sonuç veya veri yetersizliği kabul edilir. Birlikte değişen iki seri tek başına neden göstermez; “iklim değişikliği sonucunda” açıklaması ayrıca bilimsel kanıt gerektirir. İlk sürüm gözlenen değişimi ve ilişkiyi kaynaklarıyla sunabilir.

[Tartışma ve iki üyenin görüşleri](../team/ideas/IDEA-M1-001.md). Güncel sistem haritası kabul edilen mimari yönü gösterir; bu sayfadaki bölge/veri adaylarını kabul edilmiş saymaz.
