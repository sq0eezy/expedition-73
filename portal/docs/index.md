---
review_summary: "İki kişilik ekibin NASA Space Apps çalışması için ortak başlangıç noktası."
change_summary: "Gerçek bölgesel T2M yanıtıyla maskesiz aday dikdörtgenin ilk alan hesabı ve bağımsız kontrolü eklendi."
---
# {{ project_name }}

<div class="portal-hero" markdown>

## Tek göstergeyle başlayalım. Hesabı görünür kılalım.

{{ project_description }}

<span class="portal-badge">{{ current_status }}</span>
<span class="portal-badge">Güncelleme: {{ current_updated }}</span>

**Şu an:** {{ current_phase }}

İlk pilot: **2 metre hava sıcaklığı**. Modüle özel hesaplar ortak sonuç diliyle bağlanacak. İlk NASA POWER nokta API/adaptör dilimi çalışıyor. Bölgesel ürün/sınır/dönem/yöntem ve sunulacak web uygulaması henüz açık.

</div>

## Nereden başlayalım?

<div class="portal-grid">
<a class="portal-card portal-card-featured" href="evidence/T2M_POINT_PROBE/"><strong>İlk gerçek veri · T2M API</strong><span>12 aylık nokta yanıtı, çalışan ilk adaptör ve doğrulama sınırları.</span></a>
<a class="portal-card portal-card-featured" href="evidence/T2M_WINDOW_PROBE/"><strong>Yeni · T2M alan hesabı</strong><span>56 hücre, 12 aylık aday dikdörtgen ortalaması ve bağımsız hesap kontrolü. Maske ve kesin bölge açık.</span></a>
<a class="portal-card portal-card-featured" href="planning/REGION_B/"><strong>sq0eezy · Bölge B'de ne yapacağım?</strong><span>İlk iki iş, API denemesi, modül entegrasyonu ve beklenen çıktılar.</span></a>
<a class="portal-card portal-card-featured" href="planning/REGION_A/"><strong>Emeç · Modüller ve Bölge A</strong><span>Ortak modül teslimleri, A görevleri ve arkadaşına bırakılacak girdiler.</span></a>
<a class="portal-card portal-card-featured" href="planning/PILOT/"><strong>İlk pilot · Hava sıcaklığı</strong><span>Tek göstergede veri, hesap, adaptör ve web deneyiminin küçük denemesi.</span></a>
<a class="portal-card portal-card-featured" href="architecture/MODULE_SYSTEM/"><strong>Modüller nasıl bağlanacak?</strong><span>Üst/alt başlıklar, özel hesaplar, ortak çıktı ve veri bağlantıları.</span></a>
<a class="portal-card portal-card-featured" href="research/REGION_CANDIDATES/"><strong>İki bölge adayı · Tartışılıyor</strong><span>Colorado Platosu ve Kuzey Alaska neden aday? NASA'nın bölgelemesi, veri sorguları ve açık sorular.</span></a>
<a class="portal-card portal-card-featured" href="team/"><strong>Ekipte kim ne düşünüyor?</strong><span>Emeç ve sq0eezy'nin çalışma notları, fikirleri ve birbirinden bekledikleri.</span></a>
<a class="portal-card portal-card-featured" href="discovery/IDEA_COMPARISON/"><strong>Hangi fikir?</strong><span>NDVI, su depoları, sıcaklık ve diğer adayları aynı sorularla karşılaştır.</span></a>
<a class="portal-card" href="research/DATA_SOURCES/"><strong>NASA verilerini keşfet</strong><span>Görsel katman ile sayısal analiz verisini ayır; erişimde neyin sınanacağını gör.</span></a>
<a class="portal-card" href="control-center/"><strong>Şu an neredeyiz?</strong><span>Kesinleşenler, açık kararlar, kanıtlar ve sıradaki küçük adım.</span></a>
<a class="portal-card" href="architecture/"><strong>Nasıl çalışabilir?</strong><span>Veriden trend analizine ve animasyona uzanan öneri mimarisi.</span></a>
<a class="portal-card" href="planning/WORK_BOARD/"><strong>İki kişi nasıl ilerleriz?</strong><span>Görevler, bekleyen seçimler ve tamamlanma ölçütleri.</span></a>
<a class="portal-card" href="decisions/"><strong>Neye karar verdik?</strong><span>Kabul edilmiş tercihler ve değerlendirmedeki seçenekler.</span></a>
</div>

## Yeni konuşmalar kaybolmasın

[Ortak web paneli](guide/WEB_PORTAL.md) ilk yayın ayarını ve sayfalardaki kalemle GitHub üzerinden not düzenlemeyi açıklar. Web yayını açık; kayıtları okumak için yerel kurulum veya pull gerekmez.

[Konuşma işleme kılavuzu](guide/AI_WORKFLOW.md), gelen fikirlerin kayda nasıl geçeceğini açıklar. [İnceleme listem](review/index.md) ise okuduğun sayfaları ve sorularını bu tarayıcıda tutar.

!!! note "Durum etiketleri"
    **Proposed:** öneri · **Validating:** sınanıyor · **Implemented:** uygulandı · **Verified:** kanıtla doğrulandı · **Deferred:** ertelendi · **Rejected:** reddedildi. Mimari çizimi, çalışan uygulama kanıtı değildir.
