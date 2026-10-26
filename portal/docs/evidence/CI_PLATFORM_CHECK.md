---
status: Validating
updated: "2026-10-26"
review_summary: "Yıllık ekran kodunun uzak platform sonuçları ve ARM64 kurulum düzeltmesi."
change_summary: "07f87a3 dört işi geçti; ARM64 QEMU kurulumunda durdu. Platform değişkeni Compose adımlarına daraltıldı; yeni uzak sonuç ayrı izlenir."
---
# Uzak platform kontrolleri ve ARM64 kurulumu

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
