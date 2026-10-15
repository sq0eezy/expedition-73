---
review_summary: "GitHub üzerinden ortak çalışma önerisi ve bu yerel kopyanın henüz paylaşılmamış durumu."
change_summary: "Uzak ve yerel commit farkı gözlendi; ilk aktarımda korunacak çalışmalar kaydedildi."
---
# Paylaşım ve ilk eşitleme

## Neden GitHub öneriliyor?

İki kişinin aynı kod ve belge geçmişiyle çalışması için mevcut [ortak depo](https://github.com/sq0eezy/expedition-73) yeterli bir temel sunuyor. Bir kişi kendi üye notunu, fikir kartını veya görev değişikliğini hazırlar; pull request üzerinde diğeri yorumlayabilir. Sonuç ilgili esas belgeye işlenir. [GitHub'ın ortak depo ve pull request açıklaması](https://docs.github.com/en/pull-requests/reference/pull-requests).

Portal tarayıcıdan okunur; kaynaklar GitHub dosya düzenleyicisinde, yerel editörde veya kullandığınız yapay zekâ aracılığıyla değiştirilebilir. Pull request yorumu kendiliğinden proje kararı olmaz. Sonraki oturumda ilgili yorumlar okunup karar/görev özeti belgelere aktarılır.

## Bu oturumdaki gerçek durum · 2026-10-15

| Alan | Gözlem |
|---|---|
| GitHub'ın döndürdüğü güncel depo adresi | `sq0eezy/expedition-73` |
| Yerel origin adresi | Eski yazımlı `sq0eezy/expition-73`; bu oturumda değiştirilmedi |
| Yerel HEAD | `7c96f40` |
| API ile görülen uzak main | `cab8fcc`; yerel HEAD sonrasında üç commit var |
| Uzak son ağaçta görülen dosyalar | `README.md`, `ege.txt`, `.DS_Store` |
| Yerel portal ve ekip alanı | Henüz commit/push edilmedi |
| İşlem | Yalnızca okuma; pull, merge, reset, push veya uzak yorum yapılmadı |

**İlk paylaşım tamamlanmadı.** Yerel kayıtlar arkadaşının bilgisayarında henüz görünmez. İlk aktarımda yerel değişiklikler korunmalı, uzaktaki üç commit alınmalı, özellikle iki tarafta değişen README birlikte incelenmeli ve portal eklemesi ayrı branch üzerinden paylaşılmalı. Bu gözlem ileride güncelliğini yitirebilir; işlem öncesinde uzak uç yeniden kontrol edilir.

## Sonraki çalışmalar için önerilen sıra

1. Yerel değişiklik var mı kontrol et; korunmamış çalışmanın üzerine güncelleme alma.
2. Güncel ortak ana sürümü al, yapacağın işe özel branch aç. Örnek branch adları: `codex/m1-veri-kesfi`, `codex/m2-gorsel-akis`.
3. Kendi üye notunu ve ilgili görev/fikir kaydını güncelle; diğer kişinin notlarını onun ağzından yeniden yazma.
4. Portalda `check` ve `build` çalıştır; sonra incelenmiş dosyaları commit et.
5. Yetkili paylaşımda branch'i gönder ve kısa bir pull request aç: ne değişti, kimden hangi yanıt bekleniyor, nasıl kontrol edildi?
6. Birleşen sonucu diğer kişi kendi kopyasına alır. Benim de aynı güncel kayıtları okumam gerekir.

Bu sıra manuel bir çalışma düzenidir; otomatik Git işlemi veya bildirim kurulmadı. Güncellemenin henüz diğer kopyaya ulaşmamış olabileceği her oturumda açık tutulur.
