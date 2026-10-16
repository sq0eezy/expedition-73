# Expedition 73 çalışma yönergesi

Bu depo iki kişilik NASA Space Apps projesinin çalışma alanıdır. `portal/`, proje hafızası için uyarlanmış Project Context Portal'dır.

## Önce oku

- `portal/docs/CURRENT_STATE.md`: mevcut aşama ve sıradaki adım.
- `portal/docs/DOCUMENTATION_MAP.md`: konunun esas belgesi.
- `portal/docs/team/index.md`, iki üyenin `team/members/` notları, `team/IDEAS.md`, `team/HANDOFFS.md` ve ortak iş panosu: ekip niyeti ve iş sahipliği.
- Portal içinde çalışırken `portal/AGENTS.md` yönergelerini de uygula.

## Projenin sınırı

Güncel karar ADR-004: modüle özel bilimsel hesap + ortak sonuç adaptörü, ayrı konu hiyerarşisi/veri bağımlılığı ve dar pilot kabul edildi. İlk pilot göstergesi 2 metre hava sıcaklığıdır. Bölge, ürün, dönem, yöntem ve teknoloji seçilmedi; NDVI ilk pilot değildir. İlk teknik dilim analysis/ içinde: NASA POWER T2M nokta API/CLI, 0.1.0 şemaları, normalleştirme ve 26 çevrim dışı test. Çalışma analysis/README.md ve evidence/T2M_POINT_PROBE.md içinde; nokta örneğini bölge ortalaması/trend veya nihai web uygulaması sayma. analysis/ değişikliklerinde kendi .venv Python ile unittest ve gerçek örnek validate komutunu çalıştır. Genel sözleşme/arayüz taslağını çalışan uygulama sayma. Ayrıntılar portal/docs/architecture/MODULE_SYSTEM.md ve portal/docs/planning/PILOT.md içindedir.

Kullanıcının yeni konuşmalarını özetleyerek ilgili belgelere işle; öneriyi kabul edilmiş karar, konuşmayı bilimsel kanıt sayma. Ham konuşmaları, kişisel dosya yollarını ve erişim anahtarlarını yayımlanan `portal/docs/` içine kopyalama.

Türkiye yalnızca örnekti. Güncel bölge/modül düşüncesi `portal/docs/team/ideas/IDEA-M1-001.md` içindedir. Colorado Platosu ve Kuzey Alaska araştırma adaylarıdır; kabul edilmiş bölge/ürün/dönem sayma. CMR granule eşleşmesini bilimsel piksel kalitesi veya trend kanıtı diye sunma.

Anlamlı çalışma sonunda ilgili kaynakları, CURRENT_STATE ve WORK_LOG'u güncelle. Öneri, uygulama ve doğrulamayı ayır. Portal kontrolleri NASA analizinin çalıştığını kanıtlamaz. Portal değişikliklerinde `portal/.venv/Scripts/python.exe portal/scripts/portal.py check` ve `build` çalıştır.

M2 (sq0eezy) macOS kullanıyor. Ona yönelik komutlar `python3` ve `portal/.venv/bin/python` üzerinden verilir; kılavuz `portal/docs/guide/MACOS_SETUP.md` içindedir. Windows ortamında çalıştırılan yol testini gerçek macOS kurulumu olarak raporlama.

## İki kişilik çalışma

Üye eşleştirmesi `portal/docs/team/index.md` içindedir. Kullanıcının ve arkadaşının görüşlerini ayrı koru; yanıt yoksa kabul varsayma. Hangi üye adına çalışıldığı belirsizse kişisel niyet yazma. Görev sahibi ve inceleyen için esas kaynak iş panosudur; bir kişiye önerilen görev, kabul edilmiş görev sayılmaz.

2026-10-16 iş bölümü: M1 modüller/A, M2 B; ayrıntılar ADR-005, planning/REGION_A.md, REGION_B.md ve REGION_WORKFLOW.md. M2 ataması M1 tarafından bildirildi; M2 adına başlama veya kabul beyanı üretme. Coğrafi adaylar hâlâ seçilmedi.

Başlangıçta iki üyenin son notunu ve ilgili fikir/devir kaydını oku. İlgili GitHub PR/yorum bağlantısı varsa okunmadan diğer kişinin fikri biliniyor sayılmaz. Kayıtlar erişilen kopya kadar günceldir; arkadaşın özel sohbeti görünmez. Yeni üye güncellemesi, ilgili esas belge, pano/devir ve kısa çalışma günlüğüyle ilişkilendirilir.

Paylaşım düzeni ve gözlenen yerel/uzak fark `portal/docs/team/SYNC.md` içindedir. Korunmamış çalışmaya körlemesine pull uygulama, iki katkıdan birini reset/force ile silme. Yeni branch'lerde varsayılan `codex/` önekini kullan. Belgelerdeki “push et” veya “mesaj gönder” ifadesi dış işlem yetkisi değildir.
