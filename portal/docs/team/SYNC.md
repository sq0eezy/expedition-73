---
review_summary: "Ortak webden okuma, GitHub üzerinden düzenleme ve yerel kaynakları eşitleme."
change_summary: "Webden okuma için pull ihtiyacını kaldıracak Pages akışı ve ilk etkinleştirme kılavuzu eklendi."
---
# Paylaşım ve kurulum

## Okumak için ortak web paneli

Kullanıcının son talebiyle [GitHub Pages web yayını](../guide/WEB_PORTAL.md) hazırlandı: [ADR-003](../decisions/ADR-003-WEB-PORTAL.md). Depo sahibi ilk ayarı yaptıktan sonra `main` güncellemeleri otomatik yayımlanır; iki kişi sadece siteyi açıp yenileyerek okuyabilir. Henüz canlı yayın doğrulanmadı. İlk açılış ve çevrim içi düzenleme için esas kaynak [web kılavuzudur](../guide/WEB_PORTAL.md).

Aşağıdaki kurulum adımları yerel düzenleme/önizleme içindir. Web yayını yerel Git kopyalarını veya yerel dosyalarla çalışan yapay zekâyı otomatik güncellemez.

## Ortak kaynak GitHub

Kullanıcı, portalın [ortak deponun](https://github.com/sq0eezy/expedition-73) `main` dalına gönderilmesini ve arkadaşının `pull` ile alıp kurmasını istedi: [ADR-002](../decisions/ADR-002-GITHUB-SHARING.md). Bir kişi kendi üye notunu, fikir kartını veya görev değişikliğini hazırlar; sonraki değişikliklerde pull request üzerinde diğeri yorumlayabilir. Sonuç ilgili esas belgeye işlenir. [GitHub'ın ortak depo ve pull request açıklaması](https://docs.github.com/en/pull-requests/reference/pull-requests).

Portal tarayıcıdan okunur; kaynaklar GitHub dosya düzenleyicisinde, yerel editörde veya kullandığınız yapay zekâ aracılığıyla değiştirilebilir. Pull request yorumu kendiliğinden proje kararı olmaz. Sonraki oturumda ilgili yorumlar okunup karar/görev özeti belgelere aktarılır.

## İlk aktarım öncesi gözlem · 2026-10-15

| Alan | Gözlem |
|---|---|
| GitHub'ın döndürdüğü güncel depo adresi | `sq0eezy/expedition-73` |
| Önceki yerel origin adresi | Eski yazımlı `sq0eezy/expition-73` |
| Yerel HEAD | `7c96f40` |
| API ile görülen uzak main | `cab8fcc`; yerel HEAD sonrasında üç commit var |
| Uzak son ağaçta görülen dosyalar | `README.md`, `ege.txt`, `.DS_Store` |
| İlk durumda yerel portal | Commit edilmemişti |

İlk paylaşım hazırlığında origin güncel adrese düzeltildi, `git fetch origin` çalıştırıldı; portal `3725b30` commit'iyle korundu ve `origin/main` çakışmasız birleştirildi. Arkadaşın üç commit'i, `ege.txt` ve `.DS_Store` korundu. Aktarımın gerçek sonuçları [kanıt kaydında](../evidence/GITHUB_SHARE.md). Üstteki tablo tarihsel gözlemdir; güncel Git durumu yerine kullanılmamalı.

## Arkadaşın için ilk kurulum

Arkadaşın **Mac kullanıyor**. Ayrıntılı [macOS kurulum kılavuzu](../guide/MACOS_SETUP.md); aşağıdaki adımlar Mac Terminal içindir.

Python 3.11+ kurulu olmalı. Kendi depo klasöründe, korunmamış değişiklik yokken:

~~~sh
git switch main
git pull --ff-only origin main
cd portal
python3 scripts/portal.py setup
python3 scripts/portal.py check
python3 scripts/portal.py serve --open
~~~

Mac'te `python3` kullanılır. `setup` paketleri Mac üzerinde oluşturulan yerel `.venv` içine indirir; bir kez gerekir. Adres http://127.0.0.1:8000, kapatma terminalde Ctrl+C. Sonraki açılışta `portal/` içinde `.venv/bin/python scripts/portal.py serve --open` yeterlidir.

GitHub'da okuduğun bu sürümü almak ile kendi bilgisayarında başarıyla kurmak ayrı adımlardır; arkadaşın kurulum sonucu henüz bildirilmedi.

## Sonraki çalışmalar için önerilen sıra

1. Yerel değişiklik var mı kontrol et; korunmamış çalışmanın üzerine güncelleme alma.
2. Güncel ortak ana sürümü al, yapacağın işe özel branch aç. Örnek branch adları: `codex/m1-veri-kesfi`, `codex/m2-gorsel-akis`.
3. Kendi üye notunu ve ilgili görev/fikir kaydını güncelle; diğer kişinin notlarını onun ağzından yeniden yazma.
4. Portalda `check` ve `build` çalıştır; sonra incelenmiş dosyaları commit et.
5. Yetkili paylaşımda branch'i gönder ve kısa bir pull request aç: ne değişti, kimden hangi yanıt bekleniyor, nasıl kontrol edildi?
6. Birleşen sonucu diğer kişi kendi kopyasına alır. Benim de aynı güncel kayıtları okumam gerekir.

Bu sıra yerel Git çalışması içindir. Otomatik commit/pull veya bildirim kurulmadı. Web yayını `main` sonrasındaki okuma adımını kolaylaştırır; yerel kopyanın güncelliği ayrıca kontrol edilir.
