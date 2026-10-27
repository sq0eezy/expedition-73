---
status: Validating
updated: "2026-10-27"
review_summary: "Yıllık ekran kodunun uzak platform sonuçları ve ARM64 kurulum düzeltmesi."
change_summary: "6f5db6d native-host düzeltmesi beş uzak işi geçti; ARM64 Linux 234 Python/43 JS/HTTP başarılı. Yeni yıllık web ekranının testi ayrı tutulur."
---
# Uzak platform kontrolleri ve ARM64 kurulumu

**2026-10-27 sonuç:** Native-host düzeltmesi **6f5db6de9dc2c1eb4a6f2f9bd2db5aa31e75713a** olarak normal M1 push ile paylaşıldı. [40459504376](https://github.com/sq0eezy/expedition-73/actions/runs/40459504376) beş işte completed/success: Windows, macOS, Ubuntu, Docker AMD64 ve native Docker ARM64. [ARM64 günlüğünde](https://github.com/sq0eezy/expedition-73/actions/runs/40459504376/job/122040513908) aarch64 host guard'ı, 234 test / 186,308 s, 43 JS, bütün offline replay/build ve yedi dosyalı HTTP smoke geçti. Tamamlanan matrix durumu GitHub iş listesinden okundu. Bu kod henüz yeni yıllık akış web görünümünü içermez; bu yeni yerel dilimin uzak testi diye sunulmaz. M2'nin kendi Mac kabulü veya bilimsel profil onayı değildir.

## 2026-10-27 · Yıllık modül kodu ve emülasyon süresi

[40372881297](https://github.com/sq0eezy/expedition-73/actions/runs/40372881297), 5dd0630 kodu için tamamlandı. İş durumları ve tam günlükler okundu: Windows 234 test / 273,373 s, Ubuntu 234 / 279,782 s, macOS ARM64 234 / 186,387 s ve Docker AMD64 234 / 181,844 s; dördünde 43 JS ve bütün offline replay/build geçti. Üç native iş package doğrulamasını, Docker AMD64 HTTP smoke'u da geçti. Bu sonuç önceki 07f87a3'ün 222 testinden ve yeni yerel web geliştirmesinden ayrıdır; M2'nin kendi cihaz kabulü değildir.

[ARM64 işi 121748364530](https://github.com/sq0eezy/expedition-73/actions/runs/40372881297/job/121748364530) QEMU ve imaj derlemesini geçti; build 513,4 s sürdü. İş 17:54 civarında başladı, `18:24:45Z` tarihinde 30 dakika sınırında `The operation was canceled` ile durdu. Testlerin tamamlandığı veya HTTP smoke geçtiği gösterilmedi; genel sonuç tam başarı değildir. Bu gözlem uygulama hesabının yanlış olduğunu göstermez, emülasyon altındaki süre sınırını gösterir.

Yeni workflow matrisi iki mimariyi de koruyarak AMD64 için ubuntu-24.04, ARM64 için ubuntu-24.04-arm seçer. [GitHub'ın resmi runner tablosunda](https://docs.github.com/en/actions/reference/runners/github-hosted-runners) ARM64 Linux hostu desteklenir. QEMU adımı kaldırılır, `uname -m` kontrolü beklenen x86_64/aarch64 hostunu doğrular. Compose platform ayarı yalnız Compose adımlarında kalır; 30 dakika sınırı, tam testler, read_only/ağsız çalışma ve always cleanup korunur. Yerel YAML kontrolü bu eşleştirmeleri doğruladı. Hazırlık anında uzak sonuç yoktu; tamamlanan 6f5db6d koşusu yukarıda ayrı kaydedildi. Yeni yerel Docker veya ARM64 koşusu yapılmadı.

2026-10-26, M1 devam talebiyle temiz 2de8bf8 dalında ekip kayıtları okundu ve fetch yapıldı. Main a1a83d5, M2 6047c42 değişmedi. [40335437683 çalışması](https://github.com/sq0eezy/expedition-73/actions/runs/40335437683), kod **07f87a3beb921ce44343739b49e1c8058202bfc9** için tamamlandı; genel sonuç failure. Önceki in_progress kaydı ilk gözlemdir; bu sayfa tamamlanan sonucu ayırır.

## Gerçek uzak sonuçlar

GitHub iş durumları ve tam günlükler okunarak şu sonuçlar doğrulandı:

| İş / günlük bağlantısı | Sonuç ve kapsam |
|---|---|
| [Windows](https://github.com/sq0eezy/expedition-73/actions/runs/40335437683/job/121615627848) | 222 Python testi / 217,614 s, 43 JS; gerçek A/B/yıllık tekrarları, builder ve yedi dosyalı paket doğrulaması geçti |
| [macOS ARM64](https://github.com/sq0eezy/expedition-73/actions/runs/40335437683/job/121615628270) | Hosted runner Python 3.12.10 arm64; 222 / 196,190 s, 43 JS, tekrar/build/paket geçti. M2'nin kendi bilgisayarındaki kullanım veya kabul değildir |
| [Ubuntu](https://github.com/sq0eezy/expedition-73/actions/runs/40335437683/job/121615628307) | 222 / 252,979 s, 43 JS, tekrar/build/paket geçti |
| [Docker Linux AMD64](https://github.com/sq0eezy/expedition-73/actions/runs/40335437683/job/121615627960) | 222 / 128,702 s, 43 JS, ağsız gerçek tekrar/build ve yedi dosya/annual-monthly bağı/MIME/özel yollar HTTP smoke geçti |
| [Docker Linux ARM64](https://github.com/sq0eezy/expedition-73/actions/runs/40335437683/job/121615628028) | QEMU yardımcı konteyneri başlatılırken `exec /usr/bin/binfmt: exec format error`; uygulama testleri başlamadı |

Bu yeni uzak kanıt önceki yerel Windows/Chrome sonucundan ayrıdır; CI tarayıcı senaryolarını çalıştırmaz. Paket hash'leri her platformda kendi içerikleriyle doğrulandı; platformlar arası bütün paket byte eşitliği iddiası yok.

## Kök neden ve dar düzeltme

Job düzeyindeki `DOCKER_DEFAULT_PLATFORM: ${{ matrix.platform }}`, Ubuntu AMD64 host üzerinde emülatör kurulmadan önce binfmt yardımcı imajının da ARM64 seçilmesine neden oldu. Günlükte yardımcı `docker run` komutu ve hemen sonraki exec hatası var; bu uygulamanın ARM64 bilimsel hesap hatası değildir. [Docker'ın QEMU kullanım sırası](https://github.com/docker/setup-qemu-action) önce emülatör kurulumunu, sonra hedef mimarinin konteynerini çalıştırmayı gösterir.

`.github/workflows/analysis-checks.yml` içinde değişken yalnız üç Compose adımına taşındı: checks, preview ve always cleanup. QEMU ve host HTTP smoke bu hedef değişkenini almaz. Matrix, sabit action SHA'ları, test/derleme komutları, 30 dakika sınırı, ağsız/read_only koşulları ve cleanup korunur. Test azaltma veya atlama yok.

Yerel PyYAML kontrolü yeni/eski workflow ağaçlarını UTF-8 ile okuyarak yalnız bu kapsam taşımasının değiştiğini, iki mimarinin/üç Compose adımının kaldığını ve QEMU/smoke'a hedef değişkeni verilmediğini doğruladı. İlk yardımcı karşılaştırma Windows varsayılan metin kodlamasıyla assertion verdi; açık UTF-8 ile yeniden kontrol geçti. `git diff --check` geçti. Yerel Docker motoru hazır değildi; yeni yerel konteyner başarı iddiası yok. Uygulama/analysis/web kaynakları değişmediği için bu dilimde Python/Chrome paketleri yerelde yeniden çalıştırılmadı.

## Eşzamanlı katkı ve paylaşım

[Copilot PR #1](https://github.com/sq0eezy/expedition-73/pull/1) metni ve yorumları okundu. İncelenen başlık f0bca80 yalnız boş “Initial plan” commit'i, sıfır değişen dosya ve yorumsuz taslaktı; açıklaması aynı neden ve kapsam önerisini içeriyor. Bu PR'dan uygulanmış kod veya M2 onayı alınmış sayılmaz. PR/main değiştirilmeden mevcut M1 dalında dar düzeltme hazırlanır; sonraki uzak koşunun başlık SHA'sı ve sonucu [SYNC](../team/SYNC.md) içinde ayrı tutulur. Bilimsel kaynaklar/yöntemler, maske/sınır/dönem ve M2 kabulü değişmez; main/Pages/Sites yayını yok.

## Düzeltme sonrası ilk gerçek gözlem

Normal push sonrası ls-remote **b7e03335d6d6cfbbdfd484fa2826532cd95352ff** ile eşleşti. [40369026391](https://github.com/sq0eezy/expedition-73/actions/runs/40369026391) tam bu kod SHA'sında başladı. [ARM64 işi 121734439215](https://github.com/sq0eezy/expedition-73/actions/runs/40369026391/job/121734439215) içinde QEMU kurulum adımı **completed/success**, sonraki Container checks adımı **in_progress** olarak gözlendi. Önceki kurulum engeli aşıldı; bu gözlem tek başına bütün ARM64 testleri/build/HTTP veya genel matrix başarısı değildir. Beş işin tamamı bu gözlemde sürüyordu. Portal check/strict build (8,64 s) geçti; bunlar workflow runtime testi değildir. Yeni yerel önizleme sunucusu başlatılmadı.
