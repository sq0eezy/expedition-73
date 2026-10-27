---
review_summary: "Ortak webden okuma, GitHub üzerinden düzenleme ve yerel kaynakları eşitleme."
change_summary: "Yıllık modül bağlantısı 5dd0630 ile M1 dalına gönderildi; uzak SHA eşleşti, yeni CI sırada. 234 Windows/43 JS yerel kanıt; main/M2/Pages aynı."
---

# Paylaşım ve kurulum

## 2026-10-27 · Native ARM64 düzeltmesi ve yıllık ekran hazırlığı

6f5db6de9dc2c1eb4a6f2f9bd2db5aa31e75713a yalnız workflow/belge olarak normal M1 push ile gönderildi. [40459504376](https://github.com/sq0eezy/expedition-73/actions/runs/40459504376) tamamlandı: beş iş success; [ARM64 günlük kanıtı](../evidence/CI_PLATFORM_CHECK.md) 234 Python/43 JS/HTTP kontrolünü doğrular. Main a1a83d5/M2 6047c42 değişmedi. Bu kod henüz yeni yıllık akış web ekranını içermez; 238 yerel testli yeni dilimin uzak kanıtı diye sunulmaz.

[Yıllık akış ekranı](../guide/ANNUAL_TRACE.md), aynı M1 dalında yerelde hazırlanıp [kendi kontrolleriyle](../evidence/ANNUAL_TRACE_CHECK.md) doğrulanır. Gönderildiğinde yeni kaynak SHA/CI ayrıca kaydedilir; M2 adına kabul veya main/Pages/Sites yayını yok.

## 2026-10-26 · Yıllık modül akışı GitHub'da

M1 devam talebiyle temiz d95cce1 üzerinde [History → AnnualWeighting](../guide/ANNUAL_WORKFLOW.md) eklendi. [234 Windows/43 JS ve gerçek A/B](../evidence/ANNUAL_WORKFLOW_CHECK.md) geçti; bütün yedi genel web dosyası önceki ZIP ile byte aynı. Kaynaklar/hesap yöntemi/web sözleşmeleri değişmedi. Kaynak **5dd0630d6d04cd11404c037a7a97b575716ed0d1** mevcut codex/m1-modules-region-a dalına normal push ile gönderildi, ls-remote eşleşti. [Yeni kod CI'sı 40372881297](https://github.com/sq0eezy/expedition-73/actions/runs/40372881297) aynı SHA'da ilk gözlem pending; başarı değildir. Bu sonraki paylaşım belge commit'i aynı dala gider, yeni uygulama testi değildir.

Önceki b7e0333 CI'sının üç native ve Docker AMD64 işleri success; ARM64 kontrolü bu gözlemde sürüyordu. Bu işler yeni yıllık motor bağlantısının uzak testi değildir. Workflow'un mevcut cancel-in-progress ayarı yeni kaynak koşusu başladığında önceki koşuyu iptal edebilir; iptal veya yarım ARM64 sonucu tam başarı sayılmaz. Main a1a83d5/M2 6047c42 aynı doğrulandı; M2 kabulü veya main/Pages/Sites yayını yok. H-M1-023 dalda alınabilir; M2'nin gördüğü/kabul ettiği varsayılmaz.

## 2026-10-26 · Tamamlanan CI sonucu ve ARM64 düzeltmesi

Önceki paylaşımın kod SHA'sı 07f87a3, paylaşım belge başlığı 2de8bf8 uzak M1 ile eşleşti. [40335437683](https://github.com/sq0eezy/expedition-73/actions/runs/40335437683) tamamlandı: Windows/macOS ARM64/Ubuntu ve Docker AMD64 success, Docker ARM64 QEMU kurulumunda failure. [Tam kanıt ve kapsam](../evidence/CI_PLATFORM_CHECK.md). İlk in_progress gözlemi tarihsel olarak korunur; bütün matrix başarılı sayılmaz.

Devam talebiyle hedef mimari ayarı yalnız Compose adımlarına daraltıldı. Testler/uygulama/bilimsel kaynaklar aynı. Düzeltme normal commit/push ile **b7e03335d6d6cfbbdfd484fa2826532cd95352ff** olarak mevcut M1 dalına gönderildi; ls-remote eşleşti. [Yeni CI 40369026391](https://github.com/sq0eezy/expedition-73/actions/runs/40369026391) aynı SHA'da başladı. ARM64 QEMU adımı success, konteyner kontrolleri in_progress; ilk engel aşıldı, bütün testlerin başarısı henüz doğrulanmadı. Bu sonraki belge kaydı aynı dala gönderilir; yeni uygulama testi değildir. Fetch'te Copilot dalı/PR #1 görülüp metin ve yorumları okundu; incelenen f0bca80 boş plan commit'i. PR/main değiştirilmedi, M2'ye yeni niyet atfedilmedi. Main a1a83d5, M2 6047c42 korunur; Pages/Sites/main merge yok.

## 2026-10-26 · Yıllık web ve önceki M1 dilimleri GitHub'da

Kullanıcı devam edilmesini ve GitHub'a gönderilmesini açıkça istedi. [Kaynak kod 07f87a3](https://github.com/sq0eezy/expedition-73/commit/07f87a3beb921ce44343739b49e1c8058202bfc9), önceki dokuz yerel commit ile birlikte normal push ile [codex/m1-modules-region-a](https://github.com/sq0eezy/expedition-73/tree/codex/m1-modules-region-a) dalına gönderildi. ls-remote başlık **07f87a3beb921ce44343739b49e1c8058202bfc9** olarak yerelle eşleşti. Main a1a83d5 ve M2 dalı 6047c42 aynen kaldı; reset/force/main merge/Pages/Sites yayını yok.

Gönderim; geliştirme paketi, gerçek akış/aylık fark/rapor, iki yıllık ve 24 yıllık kaynaklar, 288 aylık görünüm, aday yıllık Python hesabı ve [yıllık aday ekranını](../guide/ANNUAL_WEB.md) kapsar. [222 Windows/43 JS/76 Chrome ve paket kanıtı](../evidence/ANNUAL_WEB_CHECK.md) yereldir. [GitHub Actions 40335437683](https://github.com/sq0eezy/expedition-73/actions/runs/40335437683) tam bu kod SHA'sında başladı; ilk gözlem **in_progress**, sonucu henüz doğrulanmadı. Bu yazılı paylaşım kaydı koddan sonraki belge commit'i olarak aynı dala gönderilir; kod CI'sı bu belge commit'inin test koşusu diye sunulmaz.

H-M1-014…022 artık geliştirme dalından alınabilir; M2'nin gördüğü/kabul ettiği anlamına gelmez. Korunmamış değişiklikler varken körlemesine pull/checkout yapılmaz. M2 kendi işini koruyup önce `git fetch origin` ile dalı inceleyebilir; uygun temiz çalışma dalında normal birleştirme sonrası Mac'te `sh scripts/start-preview.sh` kullanılır. Yıllık data/annual.json dahil yedi dosya birlikte derlenir. Ana Pages URL'si main'den üretildiği için bu paylaşım onu güncellemez.

## 2026-10-26 · Aday yıllık hesap yerelde

Başlangıç temiz 4a1d3dc; fetch sonrası main a1a83d5, uzak M1/M2 6047c42; yeni katkı yok. [Yıllık ağırlık adayları](../guide/T2M_ANNUAL_WEIGHTING.md), ayrı CLI/şema ve iki gerçek aday rapor yerel M1 dalındadır. Önceki sekiz yerel commit korunur; push/main merge/Pages/Sites/dış mesaj yok. H-M1-021/M2 incelemesi bekler. Yeni modül genel webde görünmez; mevcut uzak dal önceki yerel geliştirmeleri de içermez. M2 notu veya bilimsel kabulü değiştirilmedi.

## 2026-10-26 · Uzun dönem görünümü yerelde

Başlangıç temiz c9e7d9c, fetch sonrası main a1a83d5 ve uzak M1/M2 6047c42; yeni katkı yok. [288 aylık görünüm](../guide/T2M_TIMELINE.md) aynı kaynak byte'larıyla yerel M1 dalında eklendi; önceki yedi yerel commit korunur. Push/main merge/Pages/Sites/dış mesaj yok. H-M1-020/M2 incelemesi bekler; mevcut uzak dal yeni kodu/verileri içermez. M2'nin özel sohbeti veya yeni kabulü biliniyor sayılmaz.

## 2026-10-24 · Uzun aday dönem yerelde

Başlangıç temiz cfaf9d2. Fetch sonrası main a1a83d5, uzak M1/M2 6047c42; yeni katkı yok. [2001–2024 kayıt/yıl kataloğu](../guide/T2M_LONG_PERIOD.md) yerel M1 dalında; önceki altı yerel commit korunur. Push/main merge/Pages/Sites/dış mesaj yapılmadı. H-M1-019/M2 incelemesi bekler; mevcut uzak dal bu veri/ekranı içermez. M2 notu ve iş sahipliği değiştirilmedi.

## 2026-10-22 · İki yıllık kaynak/yıl ekranı yerelde

Başlangıç 3e4e5ee. Fetch'te M2 uzak dalı a1a83d5'ten 6047c42'ye ilerledi; commit aralığı okundu ve tamamının mevcut M1 dalında olduğu görüldü. Yeni M2 kabulü/bağımsız kodu yok; main a1a83d5, uzak M1 6047c42. [2023–2024 teknik dilimi](../guide/T2M_HISTORY.md) ve önceki yerel işler hâlâ M1 dalında, push/main merge/Pages/Sites/dış mesaj yok. H-M1-018/M2 incelemesi bekler; eski uzak kopya yeni veriyi/ekranı içermez.

## 2026-10-22 · Karşılaştırma raporu yerelde

Temiz fdaf166; fetch sonrası uzak M1 6047c42, main/M2 a1a83d5, yeni katkı yok. [Rapor indirme/açma](../guide/COMPARISON_REVIEW.md) ve önceki üç dilim yerel M1 dalında; yeni push/main merge/Pages/Sites/dış mesaj yok. H-M1-017 henüz gönderilmiş/kabul edilmiş sayılmaz. İki kişi kullanabilmek için güncel kaynak/veri önce paylaşılmalıdır; eski uzak dalda özellik yok.

## 2026-10-22 · Pencere farkı ekranı yerelde

Temiz başlangıç `ca485eb`; fetch sonrası main/M2 `a1a83d5`, uzak M1 `6047c42`, yeni katkı yok. [Betimsel pencere farkı ve teknik eşleşme](../evidence/REGION_COMPARISON_CHECK.md) M1 dalında yerel geliştirildi; önceki geliştirme paketi ve akış ekranı da henüz yereldir. Push/main merge/Pages/Sites yayını veya dış mesaj yok. H-M1-016, M2'ye gönderilmiş veya kabul edilmiş sayılmaz.

## 2026-10-21 · Akış görünümü yerelde devam

Başlangıç temiz M1 `294fab6`; fetch sonrası uzak M1 `6047c42`, main/M2 `a1a83d5`, yeni katkı yok. [Akış ekranı ve paket uyumu](../evidence/WORKFLOW_TRACE_CHECK.md) yerel M1 dalında eklendi; önceki geliştirme paketi de henüz yereldir. Yeni push/main merge/Pages/Sites yayını veya dış mesaj yok. H-M1-015 ve güncel ekran henüz M2 tarafından incelenmiş/kabul edilmiş sayılmaz. Eski paylaşımdan bu yeni kodu göreceği varsayılmaz.

## 2026-10-21 · Yeni geliştirme paketi yerelde

Başlangıçta fetch yapıldı; M1 uzak dalı `6047c42`, main/M2 `a1a83d5` olarak aynı, yeni katkı yoktu. [İsteğe bağlı Docker/native paket](../guide/DEV_PACKAGE.md) mevcut M1 dalında geliştirildi. Önceki Docker önerisi artık alternatif teknik çalıştırma yoluyla uygulandı; nihai yığın veya M2 tercihi kabulü yok. Yeni kod bu oturumda push/main merge/Pages/Sites yayınına gönderilmedi; hazırlanan CI matrisi henüz uzakta çalıştırılmadı. [Yerel gerçek kontroller](../evidence/DEV_PACKAGE_CHECK.md), [H-M1-014](HANDOFFS.md).

## 2026-10-20 · M1 geliştirme dalı GitHub’da paylaşıldı

Kullanıcı yapılan çalışmaları GitHub’a göndermeyi açıkça istedi. Temiz çalışma alanında fetch yapıldı; main ve M2 `a1a83d5` olarak aynıydı, M1 uzak dalında alınmamış katkı yoktu. M1’in sekiz yerel commit’i normal push ile `codex/m1-modules-region-a` dalına gönderildi. `git ls-remote` sonucu uzak başlık **`6b4ab124ca35b7b89e26b654ca5bbf4179736c83`**, yerel kaynakla aynı. [Paylaşılan dal](https://github.com/sq0eezy/expedition-73/tree/codex/m1-modules-region-a), [son kod commit’i](https://github.com/sq0eezy/expedition-73/commit/6b4ab124ca35b7b89e26b654ca5bbf4179736c83). Main/M2 aynı SHA’da korundu; force veya main birleştirmesi yapılmadı.

Paylaşım; koşullu alan denetimi, kaynak AREA kontrolü, ilk web ekranı, hücre görünümü ve aday ağırlık kıyaslamasını kapsar. Önceki [164 analiz + 8 JS hesap testi ve 22 Chrome senaryosu](../evidence/POLICY_COMPARISON_CHECK.md) kodu değişmeden gönderildi; bu oturumda yeni analiz/Chrome koşusu veya Ubuntu/Mac CI başarısı iddia edilmez. Token/.env, sanal ortam ve özel/generated artifacts Git dışında; gönderilen kaynaklar arasında bu yolların izlenmediği kontrol edildi. Docker yalnız öneri olarak konuşuldu; Docker uygulaması veya kabul kararı yok.

H-M1-009..013 artık dal üzerinden alınabilir; M2’nin gördüğü veya kabul ettiği anlamına gelmez. Canlı Pages main’den üretildiği için bu push ortak URL’yi güncellemez. Arkadaşın kendi çalışmalarını koruyarak önce `git fetch origin` yapıp M1 dalını inceleyebilir; [Mac web komutları](../product/RESULTS_PREVIEW.md) builder ve ardından `python3 web/serve.py` adımlarını içerir. Yerel korunmamış dosyalar varsa körlemesine dal değiştirme/pull yapılmaz.

## 2026-10-20 · M2 güncellemesi yerel M1 dalına alındı

Fetch sonrası `origin/main` ve `origin/codex/m2-region-b` aynı `a1a83d5e78e7eccf74739f1b449f6be269c5b6f5` commit'inde görüldü. [M2'nin commit'i](https://github.com/sq0eezy/expedition-73/commit/a1a83d5e78e7eccf74739f1b449f6be269c5b6f5), üye/devir/pano ve B notları okundu: 134 macOS testi, B fraksiyon/akış doğrulaması ve teknik profil kimliği uzlaşması. Sekiz belge değişimi var; yeni kaynak verisi/analiz kodu yok. Mac sonucu M2'nin beyanıdır; bu Windows oturumu Mac doğrulaması yapmadı.

M1'in üç yerel commit'i korunarak normal merge yapıldı (`b3718b4`). CURRENT_STATE ve WORK_LOG çakışmaları iki tarafın kayıtları korunarak çözüldü; portal check/build geçti. Yeni hücre görünümü kendi dalımızda yerel devam etti; uzak M1/M2 veya main'e push yapılmadı. [Yeni kanıt](../evidence/SPATIAL_PREVIEW_CHECK.md). H-M1-009/010/011/012 ve yeni ekran M2 tarafından kabul edilmiş sayılmaz.

## 2026-10-19 · M2 dal senkronizasyonu ve macOS doğrulaması

M2 (`sq0eezy`), `origin/main` (`6da0103`) sürümünü `codex/m2-region-b` dalına birleştirdi ve Emeç'in inceleme notlarını koruyarak çakışmaları çözdü. macOS/Python 3.14 (`netCDF4 1.7.2`, `numpy 2.5.4`) ortamında 134 birim testin tamamı (0 atlanan), A/B nokta ve pencere doğrulamaları, 55 hücreli `b-surface-fractions` NetCDF dönüşüm tekrarı ve 5 düğümlü `run-surface-workflow` Bölge B aday duyarlılık akışı doğrulandı. Teknik deneme profili için `t2m-technical-2024` (`0.1.0`) kimliği ve şema (`0.2.0`) / bilimsel alan yöntemi (`0.1.0`) ayrımı uzlaştırıldı; nihai bilimsel maske/sınır/dönem seçimi açık bırakıldı.

## 2026-10-18 · Mevcut M1 dilimini canlıya paylaşma talebi

M1 mevcut doğrulanmış çalışmanın canlı panele gönderilmesini açıkça istedi. Kaynak `7e50536`, ardından byte koruma düzeltmesi `75afeeb`, `codex/m1-modules-region-a` dalında kaydedilip paylaşıldı. PR API yetkisi 403 olduğu için yerel inceleme/test sonrası normal Git merge/push kullanıldı. Main `96815c5` için 134 Ubuntu testi, gerçek A/B aday akışları ve Pages başarılı; yeni canlı belgeler/katalog HTTP 200. Bu talep yalnız mevcut dilimin yayını içindir; sonraki geliştirme yine ayrı M1 dalında sürer. M2 dalı `791e07c` olarak korundu, bu yayına birleştirilmedi; teknik inceleme notu korunuyor. [Yayın kanıtı](../evidence/SURFACE_RELEASE.md) ilk CI hatası, düzeltme ve başarılı iş bağlantılarını tutar. Webden okumak için pull gerekmez; yerel kaynak kullanan AI için kendi değişikliklerini koruyarak main'i çalışma dalına almak gerekir.


## 2026-10-18 · M2 dalı okundu, birleştirme yapılmadı

Fetch ile `origin/codex/m2-region-b`, `791e07cba899e11065f9bb9846dfe44204eca84c` görüldü. Commit ve altı belgenin farkı okundu: [M2 katkısı](https://github.com/sq0eezy/expedition-73/commit/791e07cba899e11065f9bb9846dfe44204eca84c). M2, B örneğini Mac/Python 3.14 üzerinde tekrar çalıştırıp 58 testi geçtiğini, H-M1-005 teslimini doğruladığını ve R-B03 teknik uygunluğunu onayladığını kaydetmiş. Pano/devir bu gerçek beyana göre güncellendi. Bu oturum Mac'te çalışmadı; uzak dal merge edilmedi, uzak M2 dalına yazılmadı.

**M1 incelemesi:** `common-profile-t2m-0.2.0` önerisi M1 dalındaki `t2m-technical-2024` 0.1.0 taslağıyla uzlaştırılmalı. Parçalı gerçek çıktı türü `monthly_window_series`, şema/modül 0.2.0; bilimsel alan yöntemi 0.1.0. M2'nin -8,73 °C B ve +12,19 °C A özetleri, mevcut 12 aylık pencere değerlerinin eşit aylık ağırlıklı aritmetik ortalamalarıyla uyuşuyor; kabul edilmiş yıllık zaman ağırlıklandırması henüz yok. +20,92 °C mekânsal sıcaklık farkı tek başına iklim değişikliği/eğilim/etki farkı değildir. Maske dışında kesin sınır, uzun dönem, kalite ve istatistik de açıktır; “kalan tek engel maske” ifadesi nihai kapsamı karşılamıyor. M2'nin teknik onayı korunur; ortak bilimsel profil kendiliğinden kabul edilmiş sayılmaz.

## Güncel geliştirme düzeni · 2026-10-17

M1'in talimatıyla yeni çalışma doğrudan main yerine **`codex/m1-modules-region-a`** dalında devam eder: [ADR-007](../decisions/ADR-007-FEATURE-BRANCHES.md). M2 için ayrı bir kişisel/iş dalı önerilir; M2 adına dal açıldığı veya tercihi kabul ettiği varsayılmadı. Main ortak bütünleşmiş sürüm, geliştirme dalı devam eden iş içindir. Dal değişiklikleri pull request üzerinden incelenip birleştirilir; bu düzen otomatik merge kurmaz.

Bu geçişte çalışma alanı temizdi. `fetch` sonrası main'in bir commit geride olduğu görüldü. M2'nin [4ad9448 katkısı](https://github.com/sq0eezy/expedition-73/commit/4ad9448e171672a3746adb02b30646343f48432b) incelendi; B geometri/config/gerçek nokta yanıtı, test, fiş ve üye/devir notları `git pull --ff-only origin main` ile çakışmasız alındı. Main'in eski `origin/master` izleme ayarı `origin/main` olarak düzeltildi; M1 dalı bu güncel sürümden açıldı. İnceleme anında açık GitHub pull request yoktu.

**Geliştirme dalına push canlı paneli değiştirmez.** Mevcut Pages workflow'u main'den yayımlar. Dalın belgelerini GitHub'da o dalı seçerek veya yerel portal ile inceleyin. Ortak URL ancak değişiklikler main'e birleştirilip yayın başarılı olduğunda güncellenir.

M1'in sonraki oturumlarında, önce `git status` ile korunmamış çalışma kontrol edilir. Temiz ve commit edilmiş çalışma üzerinde:

```sh
git switch codex/m1-modules-region-a
git fetch origin
git log --oneline HEAD..origin/main
git merge origin/main
```

Main katkılarını incelemeden birleştirmeyin. Çakışma olursa iki kişinin değişikliği anlaşılır biçimde korunur; körlemesine reset/force kullanılmaz. Paylaşımda yalnızca çalışılan dal hedeflenir: `git push -u origin codex/m1-modules-region-a`. Yeni dış işlem için güncel kullanıcı yetkisi esas alınır.

## Okumak için ortak web paneli

Kullanıcının son talebiyle [GitHub Pages web yayını](../guide/WEB_PORTAL.md) hazırlandı: [ADR-003](../decisions/ADR-003-WEB-PORTAL.md). İlk ayar tamamlandı; başarılı yayın ve HTTP erişimi doğrulandı. `main` güncellemeleri başarılı derlemeden sonra otomatik yayımlanır; iki kişi siteyi açıp yenileyerek okuyabilir. İlk açılış ve çevrim içi düzenleme için esas kaynak [web kılavuzudur](../guide/WEB_PORTAL.md).

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
