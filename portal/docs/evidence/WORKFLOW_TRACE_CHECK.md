---
status: Validating
updated: "2026-10-21"
review_summary: "Gerçek motor çalıştırmasından genel bağımlılık izi, kararlı kimlikler ve sonuç ekranı."
change_summary: "180 Windows/Linux AMD64 testi, gerçek A/B tekrarları, 13 JS testi ve 30 Chrome senaryosu geçti; bilimsel seçim ve yeni yayın yok."
---
# Kayıtlı hesap akışı · Gerçek kontrol

## Kapsam ve kaynak

M1 devam istedi. Başlangıçta durum/harita, iki üye, ilgili fikir/devir/pano ve paylaşım kayıtları okundu. `codex/m1-modules-region-a` temiz, başlangıç `294fab6`; fetch sonrası main/M2 `a1a83d5`, uzak M1 `6047c42` olarak aynıydı. Bu dilim yerel M1 çalışmasıdır. M2'nin özel sohbeti görünmez; yeni web/Docker veya bilimsel politika kabulü çıkarılmaz.

A/B'nin mevcut gerçek `*-window-2024` ve `*-surface-fractions` kayıtları aynı `surface_workflow.run` ile yeniden işlenir. `workflow_trace.project` gerçek motor planını, sırasını, her düğümün tek bekleme/çalışma/tamamlama kaydını, tanım parmak izini ve gerçek artifact hash'lerini doğrular. Çalıştırma/context/işlem/sürüm/parametre/çıktı sözleşmesi ile girdi ve ata kimlikleri de eşleşir. Eski çalıştırmanın girdisini yeniden imzalanmış tüketici içine koymak reddedilir.

Ardından yalnız açık izin listesindeki kimlik/sürüm/sözleşme/girdi bağlantıları aktarılır. Özel context/parametre/payload, yerel yol, rastgele run UUID'si ve gerçek artifact kimlikleri tarayıcıya verilmez. Genel tanım kimliği kaynak dosya hash'lerini içeren context, düğüm tanımı ve bağımlılık parmak izlerine bağlıdır; sonuç hash'i, imza veya kaynakların bilimsel doğruluğunun kanıtı değildir. İşlem uygulaması değişirse sürümünün doğru güncellenmesi yine gereklidir.

## Çalışan görünüm

Her aday için beş düğüm, sekiz bağlantı: Temperature → Fractions; Temperature + Fractions → Land ve LandIce; Temperature + Land + LandIce → Sensitivity. Ortak üretici bir kez çalışır. İki hesap arasında uydurma Land → LandIce bağı yoktur. Adıma tıklama/Tab+Enter sürüm, çıktı tipi/şema/birim, girdiler ve iş tanımı kimliğini açar. Pencere seçimi bağımsızdır; ay/yüzey seçimi akış kimliğini değiştirmez. Seçim boşalınca eski akış/ayrıntı temizlenir. Telefon görünümü dikeydir. Yeni uygun bölge aynı kayıt sözleşmesiyle üretilir; genel modül editörü veya canlı iş sunucusu değildir.

Web aktarımı **0.3.0**; kaynak şemalar, bilimsel yöntem ve `t2m-technical-2024` 0.1.0 değişmedi. Altı genel dosya vardır: index.html, styles.css, app.js, comparison.mjs, trace.mjs, data/results.json. Yeni ZIP manifesti 0.2.0. Eski manifest 0.1.0/web 0.2.0 paketinin beş dosyalı doğrulaması da korunur. Yeni tarayıcı eski web verisini reddeder.

## Gerçek komutlar ve sonuçlar

- Windows/Python 3.12.14: depo kökünden `analysis\.venv\Scripts\python.exe scripts/workspace.py check`: **180 test / 64,732 s**, hiç atlama yok; A/B nokta, uyum, A alan/B tiled-window, 56/55 hücre fraksiyon dönüşümü ve iki gerçek yüzey akışı geçti. B iki tile/5 tekrar/55 hücre olarak kaldı. Ardından **13 JS testi / 195,573 ms**, üç JS sözdizimi kontrolü ve altı dosya builder geçti.
- Docker Desktop Linux AMD64/Python 3.12.15: `docker compose --env-file docker/compose.env --profile checks build checks`, ardından `docker compose --env-file docker/compose.env --profile checks run --rm --no-deps --name expedition73-trace-qa checks`: **180 test / 46,529 s**, aynı gerçek tekrarlar, **13 JS testi / 183,074 ms** ve builder geçti. Compose runtime network none/read_only/UID10001 düzeni korundu. Özel root .env verilmedi. İmaj metadata çözümleme yapıldı; bilimsel kaynaklar kayıtlıydı, NASA isteği yok.
- `web/serve.py` loopback 8873 üzerinde gerçek HTTP; `scripts/smoke_preview.py`: altı dosya 200, iki .mjs JavaScript MIME, kayıtlı çalışma, özel/kaynak yolları 404 geçti. Codex panel açma çağrısı queued döndü; kullanıcının sayfayı gördüğü iddia edilmez.
- Yerel kurulu Chrome headless + Playwright ile `node web/tests/browser.cjs`: **30 senaryo grubu**, JS hatası 0, dış runtime isteği 0. Mevcut seri/hücre/kıyaslama kontrollerine gerçek 5/8 bağ, tıklama/klavye girdileri, B seçimi, ay/politika kimlik kararlılığı, boş seçim, 390×844 mobil ve bozuk/eksik/ters sıralı akışın reddi eklendi. 1440×1100 ve 390×844 ekran görüntüleri görsel incelendi. Görüntüler yalnız ignored web/artifacts içindedir.
- Yedi yeni analiz izi testi ve iki paket uyumluluk testi: gerçek A/B 5/8 bağlantı, tek ortak sıcaklık, yeniden koşuda kararlı genel kimlik, özel alanların dışlanması, bozuk payload, eski girdi, yanlış ata/run/sözleşme/parametre, tekrar event/sıra/context hatası; yeni manifest eski web verisini kabul etmez. Beş yeni JS testi bağımlılık/kimlik/sıra/döngü/port/tekrar/hedef kapanışını kontrol eder.
- Gerçek önceki ZIP yeni verifier ile beş dosya olarak doğrulandı. Yeni `workspace.py package` iki kez çalıştırıldı: **318.518 byte**, SHA-256 `3ca7c8d1fb59b1b1e5d2a6063637ba114e69a6b98acffb02af50e37a99692067`; baytları aynı, altı dosya + manifest doğrulandı. ZIP ignored kalır.

Mevcut gerçek seri, fark/maksimum, kaynak hash'leri ve hücre ağırlıkları değişmedi; önceki testlerle yeniden eşleşti. NumPy'nin mevcut NetCDF testlerinde deprecation, bilerek bozuk ZIP testinde duplicate-entry uyarısı çıktı; başarısız test yok.

## Sınırlar

Tamamlanan derleme izi gösterilir; canlı durum geçişleri, iş kuyruğu, kalıcı cache, otomatik dış kaynak revizyon izleme veya sunucuda hesap hizmeti eklenmedi. Bilimsel profil/maske/sınır/uzun dönem ve nihai teknoloji/hosting açık. Fraksiyon ağırlığı ayrı kara sıcaklığı oluşturmaz; AREA karşılaştırması/trend/güven aralığı yapılmadı. Bu dilim gerçek Mac, yeni ARM64 veya uzaktaki CI/Pages koşusu değildir; önceki paketin ARM64 kanıtı bu sürüme taşınmaz.

U-02/MOD-06/D-02 Validating; [H-M1-015](../team/HANDOFFS.md) yalnız panel içi inceleme kaydı. Push/main merge/Pages/Sites yayını veya dış mesaj yapılmadı. QA sunucusu kapatıldı, 8873 TCP bağlantısının kapalı olduğu doğrulandı; yeniden açma [web kılavuzunda](../guide/DEV_PACKAGE.md). Portal check/build belge tutarlılığını doğrular; bilimsel analiz kabulü değildir.

Portal check ve strict build geçti; kaynak/örnek fark kontrolünde kayıtlı examples değişmedi. Git diff --check geçti.
