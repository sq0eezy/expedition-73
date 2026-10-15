---
review_summary: "Bölgeyi ve açılacak modülleri NASA verisine bağlayan, henüz kabul edilmemiş ürün/mimari taslağı."
change_summary: "Kullanıcının bölge→modül→karşılaştırma fikri; veri, ortak ölçüm ve nedensellik sınırlarıyla işlendi."
---
# Bölge + veriyle açılan modüller

**Durum: Proposed / Tartışılıyor.** Kaynak: Kullanıcının 2026-10-15 tarihli fikri ve bölge araştırması talebi. Uygulama kodu veya kabul edilmiş mimari kararı değildir. Türkiye yalnızca örnekti; hiçbir bölge veya modül seçilmedi.

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

[İki aday alanda](../research/REGION_CANDIDATES.md) sıcaklık ve bitki örtüsünü önce inceleyelim. Kar örtüsü kapsam/kalite kontrolüne bağlı ek aday olsun. İki bölge, ürünler ve 2001–2024 dönemi henüz onaylanmadı. Önceki tek değişkenli ilk demo önerisi daha küçük alternatif olarak korunuyor.

**Yeni modül ekleme koşulu:** Yeni bir soruya katkı, NASA sayısal kaynağı, erişilebilir örnek ve yeterli kalite. Modül sayısı başarı ölçütü olarak seçilmedi.

## Yorum sınırı

Farklı eğilimler beklenebilir ama vaat edilmez. İki yerde de artış, belirsiz sonuç veya veri yetersizliği kabul edilir. Birlikte değişen iki seri tek başına neden göstermez; “iklim değişikliği sonucunda” açıklaması ayrıca bilimsel kanıt gerektirir. İlk sürüm gözlenen değişimi ve ilişkiyi kaynaklarıyla sunabilir.

[Tartışma ve iki üyenin görüşleri](../team/ideas/IDEA-M1-001.md). Kapsam kabul edilmeden mevcut sistem haritası uygulama planı olarak değiştirilmedi; bu sayfa ayrı bir öneridir.
