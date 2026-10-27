---
status: Validating
updated: "2026-10-27"
review_summary: "Yıllık gerçek motor çalıştırmasının webde kaynak ve işlem kimliğiyle incelenmesi."
change_summary: "238 Windows/48 JS/87 Chrome, gerçek A/B akışları ve paket doğrulaması geçti; aylık byte/audit sayıları aynı, yıllık zarf0.2/ZIP0.5."
---
# Yıllık web akışı · Gerçek kontrol

2026-10-27, Windows, analysis kendi venv Python; Node ve kurulu Chrome headless. Başlangıç temiz e6cb249, mevcut M1 dalı. Durum/harita/ekip/iki üye/fikir/devir/pano okundu. Fetch'te main a1a83d5, M2 6047c42 ve boş Copilot planı f0bca80 aynı; alınmamış M1 katkısı yoktu. Kullanıcı devam istedi. [Kullanım/sözleşme](../guide/ANNUAL_TRACE.md).

## Uygulama ve ilk kontroller

Builder, annual_workflow.run'ın tamamlanmış aynı iki adımlı çalıştırmasını ve workflow_trace.project kontrolünü kullanır. Audit aynı yıllık fonksiyondan gelir; mevcut değerler/kaynak kimlikleri korunur. Yeni 0.2.0 yıllık web zarfı yalnız izin verilen kaynak context JSON'u ve küçük projeksiyonu taşır. Tarayıcı context hash'i, bölge/dönem/parent/annual kaynak bağını ve iki düğümün bilinen işlem/bağ/sözleşme parmak izlerini denetler. Serbest özel context veya UUID kopyalanmaz.

Hedef `unittest tests.test_annual_web tests.test_workspace`: **19 test / 77,483 s**, OK. Gerçek A/B 24 yıllık audit eşleşmesi, exact eski katalog hash'i, aynı çalışma/context bağı, bozuk/yarım/yabancı artifact'in reddi, özel context'in dışarı çıkmaması ve eski paket uyumu sınandı. Python tam suite sonucu aşağıda ayrıca tutulur.

Node comparison/trace: **48 test / 742,9653 ms**, 0 hata/atlanan. Yeni akış testleri gerçek kayıtlı audit/source kimlikleriyle iki bilinen işlemi, bölge karışmasını, parent/period değişimini, özel alanı, yanlış parmak izi/işlem sürümü/birim/bağ ve tamamlanma iddiasını sınar. JS hash tekrarı yazar imzası veya NASA ham dönüşüm tekrarı değildir.

İlk `node web/tests/browser.cjs`: önceki **76** Chrome senaryosu geçti; ardından yeni akış davranışları eklenerek **87** senaryo, JS hatası 0/dış runtime isteği 0 ile geçti. Klavye odağı/Enter, seçili işlem ayrıntısı, yıl değişiminde açık bölüm/adım, maskeli kapsam kapanması ve bağımsız beş düğümlü aylık görünüm kontrol edildi. Yanlış bölge akışı, bozuk fingerprint/context/sürüm ve eski 0.1.0 zarfında yalnız akışın kapanması, yıllık değer/aylık ekranın kalması sınandı. Son okunabilirlik düzenlemesi sonrası **87** senaryo tekrar geçti; yenilenen masaüstü/telefon görselleri de incelendi. Bu tekrar aynı kod üzerindeki son yerleşimi doğrular, yeni Mac/telefon cihaz testi değildir.

Yerel HTTP smoke yedi dosya, yıllık/aylık bağ, ES MIME ve özel/kaynak yolları 404 ile geçti. Önizleme 8873 üzerinde kendi session'ında açıldı; open_in_codex queued döndü, görünür kullanıcı tabı teyidi değildir. Test görselleri web/artifacts/annual-workflow-desktop.png ve annual-workflow-mobile.png içindedir, ignored; 1440×1100 ve 390×844 viewport. Gerçek telefon/M2 Mac koşusu değildir. QA finalde kapatılır ve port kapanışı doğrulanır.

## Sürüm ve ortam sınırı

Son `analysis/.venv/Scripts/python.exe scripts/workspace.py check`: **238 test / 643,771 s**, OK, 0 atlanan/hata; gerçek nokta/alan/B tiled, iki/tam dönem history, annual audit, fraksiyon ve A/B yüzey/yıllık motor akışları geçti. **48 JS / 1891,0754 ms**, syntax ve yedi dosyalı builder geçti; tam komut exit 0. Ignored kayıtlar analysis/artifacts/annual-trace-final-check.log ve -exit.txt. NumPy deprecation ve kasıtlı duplicate ZIP uyarıları test hatası değildir. Son UI yerleşimi ayrı son 87 Chrome koşusuyla doğrulandı.

`workspace.py package` ve verify-package exit 0: **6.994.000 byte**, ZIP SHA-256 `5d830f5cf45dd390015587b14440b45f5053139348fc09b5d48d48c030969efa`; yedi dosya son build ile byte aynı. data/annual.json **215.421 byte**, SHA-256 `9f31d573909ab9b3f56e8135988b604951b4377eb7bbb534858b2810af7622a7`. Önceki gerçek ZIP0.4 de yeni verifier ile geçti. İki ZIP'in data/results.json byte'ları eşit; hash `58cbad9e6951c648501a33a9f0bda71e589d09dd6bfb38f3de1727498ed75fdb`. İki bölgenin audit nesneleri eski/yeni pakette aynı değer ve kaynak kimlikleriyle eşit; audit anahtar sırası bilimsel değişim değildir. analysis/examples değişmedi. Yeni ZIP ve görseller Git dışındadır.

Son HTTP smoke tekrar geçti. Kendi QA session'ı kapatıldı, TCP8873 listener olmadığı doğrulandı. Portal check/strict build ilk yeni belge turunda 7,16 s, tamamlanmış test/paket kayıtlarından sonra 4,38 s ile geçti; paylaşım kaydı da kontrol edilir. Kodun son yerel doğrulaması Windows'tur; ayrı 6f5db6d uzak matrix başarısı bu yeni web kodunun Mac/Linux/ARM64 koşusu değildir.

Yeni yıllık zarf 0.2.0, yeni ZIP manifesti 0.5.0; yedi dosya ve aylık katalog/snapshot/rapor kimlikleri aynı. Yeni formül/istatistik, maske/sınır/dönem veya M2 kabulü yok; T-06/H-M1-024 inceleme bekler. Eski ZIP'in kopyası web/artifacts/expedition73-preview-before-annual-trace.zip içinde korunur.

[Önceki 5dd0630 uzak koşusu](CI_PLATFORM_CHECK.md) üç native ve Docker AMD64 için 234 Python/43 JS ile geçti, ARM64 QEMU 30 dakika sınırında iptal oldu. CI host düzeltmesi ayrı 6f5db6d commit'i olarak gönderildi; [40459504376](https://github.com/sq0eezy/expedition-73/actions/runs/40459504376) ilk gözlem in_progress, son gözlemde **beş iş success**. Native ARM64 234 Python/43 JS/HTTP ile doğrulandı. Bu kod yalnız workflow/belge içerir; yeni yıllık web değişikliklerini içermez. Yeni kaynak için yerel Mac/Linux/ARM64/Docker sonucu iddia edilmez. Main/Pages/Sites yayını yok; son dal/CI [SYNC](../team/SYNC.md) içinde ayrılır.

Yeni ekran kaynağı **c68244169258af16ea3cde2e6d8cf5d2e5d57411** normal M1 push ve uzak SHA eşleşmesiyle doğrulandı. [40461143919](https://github.com/sq0eezy/expedition-73/actions/runs/40461143919) bu kod SHA'sında ilk gözlem queued; henüz yeni ekran için uzak başarı iddiası yok. Sonraki belge commit'i bu paylaşımı aynı dalda kaydeder. Main a1a83d5/M2 6047c42 korunur; generated dist/ZIP, .env ve venv gönderilen kaynaklar arasında değildir.
