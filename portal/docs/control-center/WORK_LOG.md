# Çalışma günlüğü

## 2026-10-16 · İlk aday dikdörtgen alan hesabı

M1'in devam talebiyle A aday penceresinde bölgesel POWER erişimi sınandı. İlk 42 merkezli yanıtın kenar kesişimlerini eksik bıraktığı görüldü; yarım hücre payıyla gerçek 56 hücre/12 ay alındı. `analysis/` içinde nokta profilinden ayrı `monthly_window_series` şeması, bölgesel CLI, MERRA2 ızgara/kapsam kontrolü, orta noktadan hücre kenarı, küresel dikdörtgen kesişim alanı ve ağırlıklı ortalama eklendi. Eksik ayda ortalama null, eksik coğrafi hücrede hata; yıllık özet ayrı. Ham yanıt ve tüm hücre tanıları saklandı. [Kanıt](../evidence/T2M_WINDOW_PROBE.md), [Mac/Windows kılavuzu](../guide/T2M_WINDOW.md).

Windows'ta 41 testlik tam koşu geçti; dar sayısal tolerans değişimi sonrası dört ilgili test geçti, toplam 42 ayrı test doğrulandı. Ocak hesabı bağımsız satır/bant ağırlıklarıyla 12 ondalıkta eşleşti; eski nokta örneği ve yeni alan örneği çevrim dışı doğrulandı. Bu hesap kontrolüdür; kara maskesi, kesin bölge/yöntem veya uzun dönem iklim sonucu değildir. R-A04 Validating kaldı; ortak B profili ve nihai maske açık. Mevcut 6° B penceresi için parçalama gereği ve H-M1-004 panel içi ara teslim kaydedildi; B adına başlanmadı, dış mesaj gönderilmedi. Uzak main başlangıçta fetch ile denetlendi; yeni katkı yoktu. Portal check ve strict build geçti; geçici yerel HTTP sunucusunda yedi yol/içerik doğrulandı ve sunucu kapatıldı. Kaydedilmiş yanıtla CLI'nin yeni klasöre istek/yanıt/sonuç yazması ve yeniden hesabı da geçti. Uzak CI/yayın sonucu ayrıca kontrol edilecek.

## 2026-10-16 · İlk gerçek T2M API ve çalışan nokta adaptörü

**Son kontrol:** Kod main'de `092823f`; Ubuntu adaptör CI ve portal yayını başarılı. Kılavuz/kanıt/A fişi/durum canlı HTTP 200 ve yeni içerikle doğrulandı. Ayrıntılar [T2M kanıtının uzak doğrulama bölümünde](../evidence/T2M_POINT_PROBE.md). Aşağıdaki uzak sonuç henüz yok ifadesi kayıt hazırlanırkenki durumu anlatır.

M1 kendi modül/A görevlerine başlamamızı istedi. A adayının fişi ve sürümlü arama GeoJSON'u hazırlandı; 37,5°K/111°B noktasında 2024 T2M için gerçek POWER yanıtı alındı. `analysis/` içinde Python CLI, istek/sonuç JSON şemaları, kaynak/konum/dönem/birim doğrulaması, dolgu/eksik ayrımı ve yıllık özeti aylardan ayıran adaptör çalışıyor. Genel sözleşmenin yalnızca aylık T2M nokta profilini uygular; bölgesel hesap/istatistik/web ürünü değil. [ADR-006](../decisions/ADR-006-T2M-POINT-ADAPTER.md), [kanıt](../evidence/T2M_POINT_PROBE.md), [Mac/Windows çalıştırma](../guide/T2M_ADAPTER.md).

Windows/Python 3.12.14'te 26 çevrim dışı test ve gerçek örnek şema/anlamsal doğrulaması geçti. Örnek kendi kopyasıyla zaman uyumlu; çıkarım izni false. Uzak Ubuntu CI için ayrı workflow eklendi; bu kayıt yazılırken uzak sonuç henüz yok. R-A02 nokta erişimi doğrulandı, MOD-01/02/03 dar dilimde ilerliyor. B kaydı, ortak ürün/dönem/yöntem ve gerçek alan maskesi açık. M2'ye panel içi H-M1-003 ara teslimi eklendi; dış mesaj gönderilmedi. Portal check ve strict build geçti; geçici 127.0.0.1 statik sunucuda 9 yeni/ilgili yol HTTP 200 döndü ve katalog JSON doğrulandı. Geçici sunucu kapatıldı. git diff --check boşluk hatası vermedi. Bu portal kontrolleri bilimsel yöntem/alan hesabı doğrulaması değildir.


## 2026-10-16 · Bölge görevleri ve iş bölümü

M1 modülleri/A'yı yapacağını ve arkadaşının B'yi yapacağını bildirdi; arkadaşının panelden takip edebilmesi için yapılacaklar istedi. [ADR-005](../decisions/ADR-005-TEAM-OWNERSHIP.md), [A/modül listesi](../planning/REGION_A.md), [B listesi](../planning/REGION_B.md) ve [ortak profil](../planning/REGION_WORKFLOW.md) eklendi. Panoda MOD-01/03 ve R-A01/06, R-B01/06 görevleri sorumlu, bağımlılık, çıktı ve inceleme planıyla ayrıldı. Boş bölge çalışma fişleri oluşturuldu; sayısal veri/hesap/ilerleme uydurulmadı. M2 ataması M1'den geldi; M2'nin kendi başlama/kabul kaydı yok. Alan/ürün/dönem seçimi bu atamayla kesinleşmedi.

İlk bağımsız işler: bölge tanımı ve küçük T2M API erişimi. Ortak modül teslimi sonrası küçük bağımsız hesap, tam dönem kalite/analiz ve web kontrolü planlandı. Genel web arayüzü geliştirme sorumlusu açık kaldı. Windows/Python 3.12 ortamında depo kökünden `portal/.venv/Scripts/python.exe portal/scripts/portal.py check` ve `build` geçti; strict MkDocs derlemesi başarılı. `git diff --check` boşluk hatası vermedi. Geçici 127.0.0.1 statik sunucuda yeni görev/fiş/karar sayfaları, ana sayfa, pano, iki üye notu ve katalog dahil 11 yol HTTP 200 döndü; katalog JSON ve B görev kimlikleri/bağımlılık bağlantıları doğrulandı. Sunucu kapatıldı. Bu kontroller görev belgelerini doğrular; NASA API erişimi, bilimsel hesap, M2 başlangıcı veya gerçek Mac kurulumu kanıtı değildir.

## 2026-10-15 · Modül bağlantıları ve dar T2M pilotu

M1 özel hesap + ortak sonuç adaptörü yaklaşımını kabul etti; üst/alt modüller, bir modül çıktısının girdi olması ve web uygulaması teslimini istedi. İlk gösterge olarak **2 metre hava sıcaklığı** seçildi: [ADR-004](../decisions/ADR-004-MODULES-AND-PILOT.md). Konu hiyerarşisi ile veri bağımlılığı ayrı modellendi; sistem haritası, çıktı sözleşmesi, pilot koşulları ve ürün ekranları güncellendi. Bölge/ürün/dönem/yöntem ve kişi/bölge ataması açık; M2 görüşü varsayılmadı. Gerçek bilimsel veri ve uygulama kodu henüz yok. [Tasarım ve doğrulama kaydı](../evidence/MODULE_DESIGN.md).

Kullanıcının Pages ayarı sonrasında başarılı GitHub çalışması ve başlangıç/katalog HTTP 200 doğrulandı; portalın yayın durumu güncellendi. [Yayın kanıtı](../evidence/PAGES_SETUP.md). Önceki girişlerdeki başarısız yayın/aday kapsam ifadeleri tarihsel kayıtlardır.

## 2026-10-15 · Pull gerektirmeyen ortak web paneli

Kullanıcı, her değişikliği okumak için iki bilgisayarda pull/kurulum gerektirmeyen web yayını istedi. Mevcut statik portal için GitHub Pages seçildi: [ADR-003](../decisions/ADR-003-WEB-PORTAL.md). `main` push sonrası kontrol/strict derleme ve yalnızca site çıktısını yayımlayan iş akışı eklendi. Sayfalara GitHub düzenleme bağlantısı ve [web kılavuzu](../guide/WEB_PORTAL.md) eklendi. Bağlı hesapta push yetkisi var, yönetim/bakım yetkisi yok; depo sahibinin bir kerelik etkinleştirmesi gerekiyor. [Kontrol sonuçları ve yayın sınırı](../evidence/PAGES_SETUP.md). Bilimsel adaylar tartışma durumunda kaldı.

Yerel içerik/strict derleme ve `/expedition-73/` altında 63 HTTP yolu geçti. Hazırlık `f0ae5d9` ile main'e gönderildi. GitHub'ın ilk Ubuntu derlemesi ve artifact yüklemesi başarılı; yayın Pages henüz açık olmadığından `Not Found` ile durdu. İlk ayar ve yeniden çalıştırma depo sahibinden bekleniyor; site yayında sayılmadı.

## 2026-10-15 · Veriyle bölge ve modül adayları

Kullanıcı Türkiye'nin örnek olduğunu açıkladı; iki bölgenin veriyle gerekçelendirilmesini ve fikrin aday olarak panele eklenmesini istedi. Resmî coğrafi veri düzeni araştırıldı; üç üründe iki alan/üç dönem için 18 CMR granule sorgusu başarıyla çalıştı. Bilimsel dosya indirilmedi. [İki adayın araştırması](../research/REGION_CANDIDATES.md), [öneri taslağı](../architecture/REGIONAL_MODULE_PROPOSAL.md) ve [IDEA-M1-001](../team/ideas/IDEA-M1-001.md) hazırlandı. Adayların kabulü veya yeni ADR yok; M2'nin görüşü [H-M1-001](../team/HANDOFFS.md) kaydında bekliyor. [Gerçek kontroller](../evidence/REGION_RESEARCH.md).

## 2026-10-15 · Mac kurulum kılavuzu

Kullanıcı arkadaşının Mac kullandığını belirtti. README, paylaşım ve kullanım sayfaları ayrı macOS kılavuzuna yönlendirildi; M2'nin çalışma ortamı kaydedildi. Mevcut kod `darwin` için `.venv/bin/python` seçtiğinden motor değiştirilmedi. 19 mevcut CLI/içerik testi, içerik kontrolü ve strict derleme Windows'ta geçti. [Kılavuz](../guide/MACOS_SETUP.md), [kontroller ve sınırlar](../evidence/MACOS_SETUP.md). Mac'te gerçek kurulum sonucu henüz yok.

## 2026-10-15 · Main aktarımı

Kullanıcı doğrudan main'e gönderimi istedi. Origin güncel depo adresine düzeltildi ve uzak değişiklikler alındı. Portal `3725b30` ile korundu; arkadaşın üç commit'i `b75ef9b` birleştirme commit'iyle çakışmasız alındı. `ege.txt` ve `.DS_Store` korundu. İlk kurulum için Windows ve macOS/Linux komutları eklendi. İçerik kontrolü/strict derleme geçti. Push başarılı; ilk paylaşım `6f99b5f` GitHub main'de aynı kimlikle doğrulandı. Arkadaşın kendi kurulumu bekliyor. [Karar](../decisions/ADR-002-GITHUB-SHARING.md), [aktarım kaydı](../evidence/GITHUB_SHARE.md).

## 2026-10-15 · İki kişilik ekip düzeni

Kullanıcı görev paylaşımı, fikir alışverişi ve yapay zekâların iki kişinin niyetinden haberdar olmasını istedi. GitHub hesabı, depo ve commit kayıtları okundu; [ekip kimlikleri](../team/index.md) eşleştirildi. Üye notları, fikir kartı/devir şablonları, sorumlu/üstlenme/inceleyen alanları ve PR şablonu eklendi. İki üyenin kayıtlarını okuma kuralı çalışma yönergelerine işlendi.

GitHub üzerinden paylaşım önerildi; henüz ortak kabul varsayılmadı. Yerelde olmayan üç uzak commit görüldü. Pull/push/merge veya yorum gönderilmedi. İçerik kontrolü ve strict derleme geçti; dokuz yerel yol HTTP 200 döndü ve iki üye kartı tarayıcıda görüldü. [Paylaşım durumu](../team/SYNC.md), [doğrulama](../evidence/TEAM_SETUP.md).

## 2026-10-15 · İlk uyarlama

- Kullanıcının ilk konuşması özetlendi; henüz değişken seçilmediği doğrudan kullanıcı yanıtıyla doğrulandı.
- [Proje bağlamı](../PROJECT_CONTEXT.md), [fikir karşılaştırması](../discovery/IDEA_COMPARISON.md) ve [NASA kaynakları](../research/DATA_SOURCES.md) hazırlandı.
- Mimari, ürün kapsamı ve iki kişilik plan öneri olarak kaydedildi.
- Portal Türkçe gezinme ve projeye özgü okuma kimliğiyle uyarlandı; kaynak lisansı korundu.
- İçerik kontrolü, strict derleme, 29 Python ve 12 JavaScript testi geçti; 12 yerel HTTP isteği 200 döndü. Tarayıcıda başlangıç ve diyagram görüldü. Ayrıntılar [portal kanıt kaydında](../evidence/PORTAL_SETUP.md).

Uygulama geliştirmesine veya bilimsel analize geçilmedi. Sonraki adım: iki adayın küçük sayısal veri örnekleriyle değerlendirilmesi.
