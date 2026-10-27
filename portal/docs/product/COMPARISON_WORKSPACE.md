---
status: Proposed
updated: "2026-10-27"
review_summary: "Kaydırmayı azaltan, sade ve veri karşılaştırmasını merkeze alan arayüz yenileme taslağı."
change_summary: "M1 gösteriş yerine anlamı ve okunabilir kıyası istedi; ilk taslak ortak seçimler, ana karşılaştırma ve isteğe bağlı ayrıntılar."
---
# Karşılaştırma çalışma alanı · Yenileme taslağı

## Kullanıcının belirttiği gereksinimler

M1 mevcut uzun sayfada bilgi ararken sürekli aşağı kaydırmanın zorlaştırdığını belirtti. Gösterişli öğeler/renkler yerine içeriğin ne anlattığı, farkların anlaşılması ve karşılaştırma önceliklidir. Yenileme adım adım yapılır; bu belge yeni arayüzün uygulanmış veya bütün ayrıntılarının kabul edilmiş olduğu anlamına gelmez. [Toparlama sırası](../planning/CONSOLIDATION.md).

## İlk düzen önerisi

| Çalışma alanı | Kullanıcının işi | İlk görünüm |
|---|---|---|
| Karşılaştırma | Aynı gösterge/dönemde iki alanın değerlerini ve farkını incele | Ortak seçimler, ortak eksenli ana seri ve A−B farkı; temel kapsam bilgisi |
| Bölge ayrıntısı | Seçili alanın hücre/ay/alan desteğine bak | Hücre görünümü ve o seçime ait ayrıntı |
| Kaynak ve hesap | Sonucun nereden ve hangi adımlardan geldiğini denetle | Kaynak/yöntem/eksiklik ve hesap akışı; ana kıyası bölmeden açılır |

Modül, A/B alanı, dönem/yıl ve yüzey seçimi çalışma alanları arasında korunur. Ayrıntıya gidip dönünce kıyasın bağlamı kaybolmaz. Ana grafik, yıllık özet, hücreler, bütün tablolar ve her motor grafiği art arda aynı sayfaya yığılmaz. Önce yalnız bu bilgi mimarisi uygulanır; aynı teslimde bilimsel hesap/renk dili/ikinci modül eklenmez.

## Kıyas nasıl anlaşılır olur?

- İki alanın mutlak sıcaklıkları aynı zaman ve aynı y ekseninde gösterilir; alan başına otomatik farklı ölçek yanıltıcı bir benzerlik üretmez. Birim, ay/dönem ve aday yüzey tanımı görünür olur.
- A−B farkı yönü açık ayrı küçük görünümde incelenir; sıfır referansı ve ortak geçerli ay sayısı görünürdür. Tek bölgedeki eksik veri çifti de eksik bırakır; sıfır üretilmez.
- Mutlak sıcaklık düzeyi ile zaman içindeki değişim farklı sorulardır. Bugünkü fark grafiği eğilim/ısınma veya nedensellik göstermez. Gelecekte anomali/eğilim görünümü eklenirse önce referans dönem/yöntem belirlenir; mevcut farkla aynı etiket kullanılmaz.
- Sayısal ayrıntı, grafik seçimine bağlı açılır; bütün 288 ayın veya bütün hücrelerin tablosu ilk ekrana yüklenmez. Aynı ay seçimi her iki alanın değerini ve farkını birlikte gösterir.
- Renk az ve işlevsel olur: alan kimlikleri değişmez, eksik/uyumsuz durumlar renk dışında metin ve işaretle de anlaşılır. Dekoratif kart/rozet ve büyük pazarlama başlıkları bilgi hiyerarşisinin yerini almaz.

## İlk arayüz tesliminin ölçütleri

Ana karşılaştırmaya uzun sayfayı taramadan erişilebilmeli; temel seçim ile ana grafik aynı çalışma alanında olmalı. Telefon ekranında sıkışık yan yana paneller yerine görevler arasında açık geçiş olmalı; her şeyi tek ekrana sığdırma iddiası yoktur. Klavye, görünür odak, anlaşılır başlıklar ve yeterli grafik metni korunur. Eski 2024/yıllık rapor açma, aynı seçim bağlamı, null/sıfır ve teknik uyumsuzluk davranışları bozulmamalı.

Bu teslimde değişmemesi gerekenler: hesap formülleri, kaynak/veri byte kimlikleri ve sonuç sözleşmeleri. Yeni yerleşim gerçek kayıtlarla masaüstü/telefon ve hedef kullanıcı görevi üzerinden sınanır. M2'nin mevcut veya yeni ekranı kabul ettiği varsayılmaz; görev alanlarının adları/sırası bu taslakta öneridir.
