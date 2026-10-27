---
status: Validating
updated: "2026-10-19"
review_summary: "Dosya şartnamesi ile gerçek seçili granül arasındaki AREA farkı; hangi alanın doğrulanabildiği."
change_summary: "Canlı DMR HTTP 200: AREA yok. Çevrim dışı kaynak yeterlilik kontrolü eklendi; doğrudan alan karşılaştırması yapılmadı."
---
# Kaynak alanı · AREA uygunluk incelemesi

**Sonuç:** Seçili `M2C0NXASM` 5.12.4 / `MERRA2_101.const_2d_asm_Nx.00000000.nc4` granülünün 2026-10-19'da yeniden okunan DMR metaverisinde sayısal `AREA` değişkeni yok. Doğrudan kaynak AREA–pilot alanı karşılaştırması bu granülden yapılamadı. Bu gözlem bütün NASA koleksiyonlarında AREA bulunmadığı anlamına gelmez. [Gerçek erişim, hash ve komut kanıtı](../evidence/SOURCE_AREA_CHECK.md).

## Belgeler ve gerçek kaynak

| Kaynak | Gözlem | Nasıl kullanıldı? |
|---|---|---|
| [2015 MERRA-2 şartnamesi §6 / PDF sayfa 21](https://ntrs.nasa.gov/api/citations/20150019760/downloads/20150019760.pdf#page=21) | Sabit koleksiyon tablosunda AREA satırı var | Araştırma ipucu; seçili dosyada bulunduğunun kanıtı sayılmaz |
| [NASA MERRA2.README §2 / PDF sayfa 7](https://gmao.gsfc.nasa.gov/gmaoftp/mikeb/Harvey/MERRA2.README.pdf#page=7) | Aynı koleksiyon tablosu dört fraksiyon, PHIS ve SGH listeliyor; AREA listelenmiyor | Belge içeriklerinin farklı olduğu kaydedildi; nedeni/sürüm tarihi uydurulmadı |
| Seçili granülün canlı ve kayıtlı DMR'si | Aynı SHA-256; dokuz sayısal değişken: lon/time/lat, dört fraksiyon, PHIS, SGH | Gerçek granül için erişilebilir değişken envanteri; AREA sayısal isteği yapılmadı |

Şartnamenin [§4.1 / PDF sayfa 15](https://ntrs.nasa.gov/api/citations/20150019760/downloads/20150019760.pdf#page=15), 576×361 çıktı gridinin 0,625°×0,5° boyutunu ve modelin küp-küre gridini ayırır. Bu bilgi koordinat eşleştirmesini destekler; pilotun hücre kenarları/alan varsayımına bağımsız fiziksel doğrulama sağlamaz. Kaynaklar 2026-10-19'da okundu.

## Yazılımın davranışı

`check-source-area --metadata DOSYA`, mevcut sıkı ürün/grid/fraksiyon metadata kontrolünü kullanır ve yalnız üst düzey sayısal değişkenleri sayar. AREA adlı açıklama metnini veri saymaz; yinelenen veya gruplu değişkenlerde örtük eşleme yapmaz. Çıktı `source_area_capability_check` 0.1.0 ve kaynak metadata hash'idir:

- Gerçek kaynakta `comparison_status=not_available_in_selected_granule`.
- İleride sayısal AREA bildirimi görülse bile `metadata_present_values_not_validated`; değer/birim/geometri karşılaştırması ayrıca gerekir.
- Her iki durumda `numeric_values_retrieved=false`, `comparison_performed=false`, `scientific_profile_accepted=false`. Otomatik ürün/alan yöntemi değişimi yok.

Komutun başarılı çıkışı kontrolün tamamlandığını anlatır; AREA'nın bulunduğunu anlatmaz. Sayısal karşılaştırma veya yeni alan dönüştürücüsü uygulanmış sayılmaz. [Koşullu yüzey kapsamı denetimi](SURFACE_SUPPORT.md) kendi açık varsayımlarıyla korunur; daha önceki “AREA alınabilir” beklentisi doğrulanmadı.

## Hesap ve sonraki adım

Pilotun küresel alanı tanımlı bir geometrik yaklaşımdır. Tüm hücre ağırlıklarını aynı pozitif sabitle çarpmak normalize sıcaklık ortalamasını değiştirmez: `Σ(cwT)/Σ(cw)=Σ(wT)/Σw`. Bu cebirsel özellik, yarıçap kaynaklı ortak ölçeğin sıcaklık ortalamasında sadeleşmesini açıklar; hücreden hücreye değişen geometri, fiziksel alan veya yüzey fraksiyonu hatasını çözmez. Mutlak km² değerleri ölçeğe bağlıdır. Bu bir NASA hata modeli veya yeni yöntem seçimi değildir.

**Sonraki öneri:** Mevcut 2024 kayıtlarını, kaynak/sınır/iki aday yüzey seçeneği ve bu yeterlilik durumuyla birlikte gösteren ilk sonuç ekranı taslağı hazırlanabilir. Uzun dönem/trend ve bilimsel A/B yorumu öncesinde hedef yüzey, kesin sınır ve ortak profil seçilmelidir. Başka bir AREA ürünü sessizce eklenmez; gerekirse ayrı ürün/sürüm/grid uygunluğu araştırılır. M2 adına seçim veya inceleme beyanı yok.
