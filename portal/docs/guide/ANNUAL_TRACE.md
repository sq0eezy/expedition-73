---
status: Validating
updated: "2026-10-27"
review_summary: "Yıllık adayın doğrulanmış geçmişten hangi adımlarla üretildiğini webde inceleme."
change_summary: "Bölgeye bağlı iki adımlı akış; kaynak/işlem kimlikleri doğrulanır, hata yalnız akış görünümünü kapatır."
---
# Webde yıllık hesap akışı

Yüzey ağırlığını **Bütün pencere · maskesiz** seçip yıllık aday kartındaki **Yıllık hesap akışı** bölümünü açın. Her görünür aday pencerenin kendi History → AnnualWeighting bağlantısı vardır. Adıma tıklayın veya Tab ile odaklanıp Enter/Boşluk kullanın; işlem sürümü, çıktı sözleşmesi, aldığı girdi ve iş tanımı kimliği görünür. [Gerçek kontroller](../evidence/ANNUAL_TRACE_CHECK.md).

Akış 2001–2024 kaydının tamamına aittir; üst yıl seçimi o kayıttaki yıllık sonucu gösterir, yeni iş başlatmaz. Yıl değişirken açık bölüm ve seçili adım korunur. Kara/buz yıllık hesabı eklenmediği için bu yüzeylerde yıllık kart/akış kapanır. Aylık beş düğümlü yüzey akışı ayrı bölümde aynı kalır. İki düğüm iki ayrı bilimsel gösterge değildir.

## Kaynak bağı

Builder yıllık adayları artık [run-annual-workflow](ANNUAL_WORKFLOW.md) üzerinden üretir. Tamamlanmış aynı çalıştırmanın artifact/context/girdi/ata kimlikleri workflow_trace.project ile doğrulanmadan akış dışarı verilmez. Mevcut yıllık hesap fonksiyonu ve candidate_annual_weighting_audit 0.1.0 sayıları değişmez.

Yalnız yıllık web zarfı **0.2.0** oldu: her bölgenin audit'ine workflow.trace ve workflow.context_json eklenir. Context JSON; sabit scope, aday bölge/sınır sürümü, dönem, üç parent dosya hash'i ve yıllık kaynak hash'lerinden oluşan açık izin listesidir. Fazladan alan veya parent dosya adı reddedilir. Yerel yollar, ham yanıtlar, özel parametreler, rastgele çalışma UUID'si ve gerçek artifact kimlikleri aktarılmaz.

Tarayıcı önce yıllık adayın mevcut exact aylık katalog bağını denetler. Sonra context JSON SHA-256'sını, audit'in parent sonuç/yıllık kaynak kimlikleriyle eşleşmesini, iki bilinen işlem/sürüm/çıktı sözleşmesini ve her düğümün tanım parmak izini doğrular. Python context JSON'unun sayıları yazma biçimi korunur; bağ kontrolü sayısal ortalamaları JS'de yeniden hesaplamaz. İş tanımı kimliği, dosya hash'i veya yazar imzasıyla aynı şey değildir; bunlar bağımsız NASA kaynağı doğrulaması değildir.

Yanlış bölgeye ait/değişmiş akışta yalnız o bölgenin akış bölümü kapanır; doğrulanmış yıllık adaylar ve aylık ekran kalır. Eski yıllık zarf 0.1.0 hâlâ açılır, akışın eski sürümde bulunmadığı açıklanır. Kaynak bağı/Web Crypto gerektiren mevcut yıllık doğrulama sınırı korunur.

## Dosya ve paket sürümleri

Yedi genel dosya aynı kalır; yeni endpoint/ek dosya/hesap sunucusu yok. data/results.json exact byte kimliği korunur; web kataloğu 0.4.0, annual snapshot 0.3.0 ve karşılaştırma raporu 0.1.0 değişmez. data/annual.json yeni 0.2.0 zarfıyla yeniden derlenir. Yeni ZIP manifesti **0.5.0**; verifier eski 0.1.0–0.4.0 paketlerini kendi sözleşmeleriyle korur. Yeni pakette akışın context/trace kimliği de kontrol edilir; tam anlamsal graph doğrulaması tarayıcıdadır.

Çalıştırma [Windows/Mac başlatıcıları](DEV_PACKAGE.md) ile aynıdır. Tarayıcı NASA/token kullanmaz. Kaynakları alıp yeniden derlemek gerekir; geliştirme dalına push canlı Pages panelini değiştirmez. Bu kayıtlı hesap görünümüdür; canlı görev monitörü, kalıcı cache, bilimsel yöntem/maske/sınır/dönem seçimi veya M2 kabulü değildir.
