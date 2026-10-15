---
review_summary: "Pull ve yerel kurulum olmadan ortak paneli okuma; GitHub üzerinden güncelleme."
change_summary: "GitHub Pages otomatik yayın akışı ve depo sahibinin bir kerelik açılış adımı eklendi."
---
# Ortak web paneli

**Ortak adres:** [Expedition 73 paneli](https://sq0eezy.github.io/expedition-73/). Yayın açıldı; başarılı GitHub çalışması ve HTTP 200 ile doğrulandı. [Yayın kanıtı](../evidence/PAGES_SETUP.md). Okumak için aşağıdaki ilk ayarları yeniden yapmak gerekmez.

## Tamamlanan ilk kurulumun başvuru adımları

sq0eezy hesabıyla:

1. [Deponun Pages ayarını](https://github.com/sq0eezy/expedition-73/settings/pages) aç.
2. **Build and deployment → Source → GitHub Actions** seç. Önerilen başka bir şablonu eklemek gerekmiyor; yayın dosyası depoda hazır.
3. [Portal · GitHub Pages iş akışını](https://github.com/sq0eezy/expedition-73/actions/workflows/portal-pages.yml) aç; **Run workflow → main → Run workflow** ile ilk yayını başlat. Önceki başarısız çalışmayı yeniden çalıştırmak da mümkün.
4. Derleme ve yayın işleri yeşil olduğunda hedef adresi aç.

İlk ayar için yönetim/bakım yetkisi gerekir. Bu oturumdaki bağlı hesap `main` dalına yazabiliyor fakat bu yetkilere sahip değil. Kişisel erişim anahtarı veya ek sunucu gerekmez. [GitHub'ın resmî kurulum açıklaması](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## İkiniz nasıl kullanırsınız?

| Amaç | Yol |
|---|---|
| Arkadaşının son notunu, fikrini veya görevini okumak | Ortak siteyi aç; başarılı yeni yayından sonra sayfayı yenile |
| Küçük bir not veya görev değişikliği yapmak | Sayfanın kalem simgesinden GitHub dosya düzenleyicisini aç; değişikliği kaydet |
| Yerel editör/yapay zekâ ile kapsamlı değişiklik yapmak | Güncel kayıtları al, dosyaları düzenle, kontrol et ve GitHub'a gönder |
| Ayrı branch veya pull request ile çalışmak | `main` ile birleştir; yayın ancak bundan sonra değişir |

Akış: **dosyayı düzenle → commit/push veya PR birleştirme → main → otomatik kontrol/derleme → web yayını → sayfayı yenile.** Yayın tamamlanması biraz zaman alır; anlık ortak yazma özelliği yoktur. Hata varsa Actions'ta görünür; başarısız yeni derleme önceki başarılı yayının yerini almaz. GitHub çevrim içi düzenlemede yetkilere göre doğrudan commit veya branch/PR sunabilir.

Mac, Windows ve telefondan okumak için Python kurulumu, yerel sunucu veya `pull` gerekmez. Yerelde dosya düzenleyen kişi ve yerel dosyalarla çalışan yapay zekâ ise çalışmaya başlamadan güncel kaynakları almalıdır. Web sitesi açılması yerel Git kopyasını otomatik güncellemez. [Birlikte çalışma düzeni](../team/SYNC.md).

## Neler ortak, neler kişisel?

Üye notları, fikirler, görevler ve kararlar GitHub dosyalarından ortak yayımlanır. Okudum işaretleri ve inceleme listesi tarayıcıya özeldir; diğer kişiye veya başka cihaza eşitlenmez. Yerel adres ile web adresi ayrı origin olduğundan yereldeki işaretler webde kendiliğinden görünmez; eski işaretler silinmez. [Okuma araçları](READER_TOOLS.md).

İş akışı yalnızca `portal/site` derleme çıktısını yayımlar; `.venv`, `.portal`, ham konuşmalar ve yerel çalışma dosyaları bu çıktının parçası değildir. `portal/docs` içeriği herkese açık web sayfasına dönüşür; gizli notlar bu klasöre eklenmez.

## Yayın sorunu olursa

Önce [Actions sonucuna](https://github.com/sq0eezy/expedition-73/actions/workflows/portal-pages.yml) bak. İlk çalışmada `Pages ayarını oku` adımında “Not Found / Ensure Pages has been enabled” görülürse depo sahibi ilk ayarı tamamlayıp yayını yeniden başlatmalı. Sonraki derleme hatalarında belge/bağlantı hatasını düzeltip `main` dalına gönder. Sırf eski sayfa göründüğü için tekrar kurulum yapma; başarılı çalışmayı ve sayfa yenilemeyi kontrol et.

Kaynak: [GitHub Pages özel iş akışları](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages). Yerel geliştirme için [Mac kılavuzu](MACOS_SETUP.md) ve [genel kullanım](index.md) geçerlidir.
