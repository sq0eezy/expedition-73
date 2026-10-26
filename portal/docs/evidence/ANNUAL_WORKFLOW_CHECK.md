---
status: Validating
updated: "2026-10-26"
review_summary: "Gerçek aylık kaynakları yıllık hesap düğümüne bağlayan iki adımlı motor denemesi."
change_summary: "234 Windows testi, gerçek A/B yıllık akışları ve 43 JS geçti. Aynı yıllık raporlar ve yedi web dosyasının byte kimliği korundu; paylaşım SYNC'te ayrılır."
---
# Yıllık modül akışı · Gerçek kontrol

2026-10-26, Windows, analysis kendi venv Python. M1 devam istedi. Başlangıç temiz d95cce1, mevcut codex/m1-modules-region-a. İki üye/fikir/devir/pano/durum/harita okundu; fetch'te main a1a83d5/M2 6047c42 aynı, M1 dalında alınmamış commit yoktu. Copilot dalında son görülen commit f0bca80 boş plandır; bu dilimde ondan kod alınmadı. [Kullanım ve sözleşme](../guide/ANNUAL_WORKFLOW.md).

## Uygulama

annual_workflow.build önce sabit parent/annual kaynak byte'larını yakalar. ReplayRecordedHistory, history.assemble ile her ham yanıtı ve parent manifest/sonucu doğrular; CompareAnnualWeighting bu düğümün artifact'ini tüketir. Annual hesap için gereken ay serisi/alan/sağlayıcı yıllık değerleri küçük JSON girdilerine ayrılır; tam ham byte'lar workflow artifact'ine kopyalanmaz. Kaynak hash'leri hem context'te hem mevcut audit provenance içinde izlenir. Geri çağrılar kaynak dosyalarını açmaz ve token/ağ kullanmaz.

Eski annual_weighting.run ile yeni işlem aynı _summarize_verified ve summarize_year fonksiyonlarını kullanır. Değişen yalnız adapter/yürütme bağlantısıdır; iki formül, eksiklik kuralı, aynı kaynak API referansı ve aday bayrakları korunur. Yeni verified_annual_weighting_inputs 0.1.0 iç sözleşmesi ve iki kayıtlı işlem 0.1.0 vardır; workflow motoru/audit/kaynak şemaları değişmez. Yeni CLI, başarılı çalışmada gerçek workflow_trace.project projeksiyonunu ayrı trace.json olarak üretir. Webdeki beş düğümlü aylık grafiğe eklenmedi.

## Gerçek kontroller

İlk `analysis/.venv/Scripts/python.exe -X utf8 -m unittest tests.test_annual_workflow tests.test_annual_weighting` koşusu **26 test / 78,808 s**, OK. Sonraki küçük kaynak-yorumlama düzenlemesi ve ek kabul-bayrağı testi dahil son durum tam ortak kontrolde yeniden sınanır; ilk hedef sayı son suite'in toplamı değildir.

Testler gerçek A/B 24'er yıllık çıktıyı kayıtlı audit'lerle, ham parent sonuç byte hash'i ve gerçek girdi/ata kimlikleriyle karşılaştırır. History tekrarının bir kez çağrıldığı, execute sırasında kaynak dosyalarının yeniden okunmadığı, token/ağ yollarına gidilmediği denetlenir. Bozuk ham/parent manifest/parent sonuç/yıllık sonuç, sonradan değiştirilmiş dosyalar, context bölge/dönem/hash etiketi, yanlış birim sözleşmesi ve yöntem parametresi sınanır. Kaynak başarısızlığında yıllık düğüm blocked; çıktı kabul denetimi başarısızsa sahte artifact yoktur. Sentetik eksik Ocak'ta iki yıllık aday null, mevcut provider referansı ayrı kalır. CLI var olan hedefi korur; başarısız motor çalışmasında yalnız iki tanı dosyası kalır.

Son `analysis/.venv/Scripts/python.exe scripts/workspace.py check`, **234 test / 559,165 s**, OK, 0 atlanan/hata; gerçek nokta/A alan/B tiled, iki/tam dönem history, fraksiyon ve kayıtlı annual audit tekrarları geçti. İki eski beş düğümlü yüzey akışı ve yeni A/B 24'er yıllık **History/AnnualWeighting completed** sonucu üretildi. İki yeni çıktı geçici ve temizlenen hedeflerde kaldı. **43 JS / 827,9406 ms**, sözdizimi kontrolleri ve yedi dosyalı builder geçti; tam komut exit 0. Yerel ignored log: analysis/artifacts/annual-workflow-final-check.log; exit kaydı aynı önekte -exit.txt. NumPy deprecation ve kasıtlı duplicate ZIP uyarıları test hatası değildir.

Son derlemenin yedi dosyası önceki gerçek web/artifacts/expedition73-preview.zip içeriğiyle **byte aynı** doğrulandı. Aylık JSON SHA-256 `58cbad9e6951c648501a33a9f0bda71e589d09dd6bfb38f3de1727498ed75fdb`, yıllık JSON `c6b366f27a252432130691b47740615cb52d787e60ea7fdc69a7d8f1dc25ab1c`; önceki ZIP `59f8831c2adb97b8f840ef55fb36718c24389a2198784c7253d67c15aca1b13e`. Yeni ZIP üretildi veya yeni browser koşusu yapıldı sayılmaz. Kaynak analysis/examples değişmedi. Önceki web 0.4.0/annual snapshot 0.3.0/yıllık zarf 0.1.0/ZIP manifesti 0.4.0 korunur. Önceki 76 Chrome senaryosu bu dilimde tekrar koşulmadı; UI kodu değişmedi.

Portal kendi venv check ve strict build ilk turda 5,69 s, son belge değişiklikleri sonrası 3,56 s ile geçti. Yeni yerel HTTP/QA sunucusu açılmadı. Yeni dilim Windows'ta doğrulandı; önceki b7e0333 uzak native/Docker koşuları yeni kodun Mac/Linux/ARM64 kanıtı değildir.

## Sınırlar ve paylaşım

İşlem sırası/kaynak bağı teknik kanıttır; bilimsel profil, maske, kesin sınır/dönem, anomali/eğilim, M2 kabulü veya R-A05/R-B05 tamamlanması değildir. Yeni dilimin uzak CI'sı önceki b7e0333 platform koşusuyla karıştırılmaz; [önceki CI](CI_PLATFORM_CHECK.md), [güncel paylaşım](../team/SYNC.md). Yeni sunucu/hosting/Pages/main birleştirmesi yok.
