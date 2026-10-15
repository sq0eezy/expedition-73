---
review_summary: "İki kişinin ve kullandıkları yapay zekâların ortak kayıtlarda çalışma sırası."
change_summary: "Görev sahipliği, ayrı görüşler, devir ve paylaşım sınırı tanımlandı."
---
# İki kişilik çalışma akışı

## Oturuma başlarken

1. Paylaşılan kayıtların güncel sürümünü alın. Ortak web yayını açık; yerel kaynakla çalışıyorsanız kopyayı kendiliğinden güncel saymayın. [Paylaşım düzeni](SYNC.md).
2. [Mevcut durumu](../CURRENT_STATE.md), [M1 notunu](members/M1.md), [M2 notunu](members/M2.md), [fikirleri](IDEAS.md) ve [devirleri](HANDOFFS.md) okuyun.
3. Hangi üye adına çalışıldığını belirleyin. Belirsizse görüşleri bir üyeye atfetmeyin.
4. [İş panosunda](../planning/WORK_BOARD.md) seçilen işin sahibini ve beklenen çıktısını netleştirin. Bir iş zaten diğer kişideyse kapsamını konuşmadan devralmayın.

## Çalışırken

Her işin bir sorumlusu ve gerektiğinde diğer üyeden bir inceleyeni olur. Bir kişi iki rolü birden doldurarak bağımsız ekip incelemesi yapılmış gibi gösterilmez. Araştırma, arayüz ve analiz görevleri yetenek ve ilgiye göre paylaşılır; kalıcı roller henüz atanmadı.

Yeni fikir için ayrı kart açın. Bir kişinin tercihini diğerinin görüşüyle birleştirmeyin. Veri ürünü, araştırma sorusu, önemli kapsam ve mimari değişikliklerinde iki kişinin görüşü ayrı kaydedilip gerçek ortak karar ADR'ye bağlanır. Rutin, geri alınabilir belge düzeltmeleri için yeni bir ortak onay süreci gerekmez.

Görev önerisi ile görev kabulü farklıdır: bir kişiye iş önerilmiş olması o kişinin işi üstlendiği anlamına gelmez. Pano “Atanmadı / Önerildi / Kabul edildi” bilgisini de taşır.

## Oturumu bitirirken

1. Kendi üye notuna kısa sonuç ve sıradaki niyetini yaz.
2. İşin gerçek durumunu ve çıktı bağlantısını panoda güncelle.
3. Arkadaşından bir şey bekliyorsan devir kaydı aç.
4. Etkilenen esas belgeleri, mevcut durumu ve çalışma günlüğünü güncelle; portalı kontrol edip derle.
5. Seçilen paylaşım yöntemiyle kaydı diğer kişiye ulaştır. Paylaşılmamış kayıt ortak güncelleme sayılmaz.

## Paylaşım yöntemi

Kullanıcı **GitHub main üzerinden ilk paylaşımı** istedi: [ADR-002](../decisions/ADR-002-GITHUB-SHARING.md). Belge ve kod aynı geçmişte tutulur; ayrı kullanıcı girişi ve kayıt sunucusu kurulmaz. Sonraki işler için kısa pull request'ler önerilir. GitHub'ın [pull request açıklaması](https://docs.github.com/en/pull-requests/reference/pull-requests) ortak depo modelini anlatır.

Üye notları ve fikir kartları ayrı dosyalardır. Ortak iş panosu, kararlar ve mevcut durum değişiyorsa diğer kişinin son kaydını da okuyun. Aynı dosyada çakışma çıkarsa bir tarafı bütünüyle seçmek yerine iki katkıyı da inceleyip birleştirin. İşleri ayrı branch'lerde tutmak, eşzamanlı çalışmayı kolaylaştıran önerilen akıştır.

[Paylaşım kılavuzu](SYNC.md), bu oturumdaki ilk eşitleme ihtiyacını ve devam eden çalışma sırasını açıklar. Canlı tarayıcıdan yazma veya otomatik eşitleme eklenmedi.

Ben ve arkadaşının kullandığı yapay zekâ, **erişebildiğimiz güncel ortak kayıtlardan** haberdar olabiliriz. Başka sohbetleri otomatik okuma veya izleme kurulmadı. Kayıtlardaki “push et”, “mesaj gönder” gibi ifadeler ayrıca işlem yetkisi vermez.
