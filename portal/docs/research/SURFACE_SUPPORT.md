---
status: Validating
updated: "2026-10-19"
review_summary: "Kırpılan hücrelerde tam hücre fraksiyonunun nerede bulunduğunu bilmeden ne kadar alan söylenebileceği."
change_summary: "Koşullu kapsam korunuyor; canlı granül metadata'sında AREA yok, önceki doğrudan alan karşılaştırması beklentisi güncellendi."
---
# Maske kapsamı · Sınır hücreleri ve karar ölçütleri

**Araştırma ve çalışan teknik denetim; bilimsel profil kabulü değil.** [İlk aday akış](../evidence/SURFACE_WORKFLOW.md) FRLAND ve FRLAND+FRLANDICE ile T2M'yi yeniden ağırlıklandırıyor. İki sıcaklık serisinin yakınlığı, pencerenin kara kapsamının doğru belirlendiğini tek başına göstermez. Tam hücre oranı içindeki karanın pencerenin hangi tarafında kaldığı bilinmiyor.

## NASA'nın tanımladığı ve bizim varsaydığımız

[NASA POWER yöntemi](https://power.larc.nasa.gov/docs/methodology/meteorology/) T2M'nin 0,625°×0,5° çıktı gridini ve hücreyi temsil eden değer olduğunu açıklar. Yeniden ağırlıklandırma, bu değerden hücre içindeki ayrı kara sıcaklığını çıkarmaz.

[MERRA-2 dosya şartnamesi, §6 / PDF sayfa 21](https://ntrs.nasa.gov/api/citations/20150019760/downloads/20150019760.pdf#page=21) sabit koleksiyonda FRLAND, FRLANDICE, FRLAKE, FROCEAN ve ayrıca AREA değişkenini listeler. Aynı belgenin giriş bölümü, dağıtılan gridin model hesap gridinden farklı olduğunu belirtir. Eşleşen koordinatlar tek başına bütün bilimsel alan tanımlarını doğrulamaz. Kaynaklar 2026-10-19'da yeniden okundu; yeni sayısal NASA isteği yapılmadı.

**2026-10-19 sonraki kontrol:** Şartname AREA'yı listelese de seçili granülün kayıtlı ve yeniden alınan tam DMR'sinde AREA yok. Başka bir NASA README tablosu da AREA'yı listelemiyor. [Kaynak uygunluk incelemesi](SOURCE_AREA.md), [HTTP 200/hash kanıtı](../evidence/SOURCE_AREA_CHECK.md). Bu granülden küçük AREA alt kümesi alınabileceği varsayımı geçerli değil.

Mevcut pilot hücre kenarlarını orta noktalardan kuruyor ve ilan edilmiş küre üzerinde alan hesaplıyor. Gerçek alt kümede dört fraksiyon var; **kaynak AREA ile küresel alan karşılaştırması yapılamadı.** Bu denetim, kaynak fraksiyonunu aynı küresel alan ölçüsünde kesin pay kabul eden bir koşullu deneydir. Kaynak fraksiyonunun fiziksel alan/yeniden gridleme hatasını kapsamaz.

## Koşullu hesap

Bir kaynak hücresinin alanı `A`, pencere içinde kalan alanı `a`, seçilen bileşenlerin toplam oranı `f` olsun. Aynı alan ölçüsünde `f` kesin kabul edilirse hücrede seçili yüzey alanı `fA` olur. Bunun pencere parçasında bulunabilecek alanı:

```text
alt sınır = max(0, fA − (A − a))
üst sınır = min(a, fA)
mevcut homojen dağılım tahmini = fa
```

Alt sınır seçili alanın olabildiğince pencere dışında, üst sınır olabildiğince içinde bulunmasına karşılık gelir. Ayrık hücrelerin sınırları toplanır. Tam hücrede veya f=0/1 ise yerleşim belirsizliği kalmaz. Bu formül projenin alan korunumu türetimidir; NASA'nın sağladığı bir belirsizlik ürünü değildir.

Çıktı `candidate_surface_support_audit` 0.1.0: iki politikanın koşullu alt/homojen/üst alanı, kesilmiş hücreler, hücre bazında hesap ve kaynak hash'leri. **Güven aralığı, olasılık, sıcaklık hata payı, bağımsız kıyı doğrulaması veya trend sınırı üretmez.** İki politika seçilmez; eski sonuçlar değişmez. [Gerçek sonuç/komut/test](../evidence/SURFACE_SUPPORT_CHECK.md).

## Karar için sıradaki kontroller

| Soru | Eldeki durum | Seçimden önce gereken |
|---|---|---|
| Hangi yüzeyin T2M'sini karşılaştırıyoruz? | T2M grid değeri; iki yeniden ağırlık adayı | Kara, kara+buz veya bütün pencere hedefini ortak araştırma sorusuyla tanımlamak |
| Fraksiyon ve alan ölçüsü uyumlu mu? | Koordinat/birim uyumu doğrulandı; seçili granülde AREA bildirimi yok | [Kaynak kısıtı](SOURCE_AREA.md) görünür kalır; mevcut küresel alan varsayımı açıkça gösterilir. Farklı alan kaynağı gerekirse ayrıca uygunluk incelemesi gerekir |
| Kırpılan parçada yüzey nerede? | Yalnız koşullu yerleşim sınırları var | Kesin sınırı gerekçelendirmek; daha ince maske gerekiyorsa ayrı ürün/sürüm ve yeniden gridleme yöntemi incelemek |
| Buz dahil edilmeli mi? | FRLANDICE ayrı bileşen; iki aday sürüyor | A/B için aynı gösterge tanımını, kara buzu/deniz buzu ayrımını açıkça yazmak |
| Bu kontroller trend için yeterli mi? | Yalnız 2024 teknik örnek | Ortak uzun dönem, zaman ağırlıkları, kalite/eksiklik ve istatistik varsayımlarını ayrıca seçmek |

M1 bu denetimi MOD-05 ve R-A04 kapsamında hazırladı. M2'nin B değerlendirmesi beklenir; burada onun adına seçim yapılmadı. Yeni ana gösterge veya bilimsel yöntem kararı verilmedi.
