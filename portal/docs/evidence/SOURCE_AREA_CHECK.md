---
status: Validating
updated: "2026-10-19"
review_summary: "Seçili NASA granülünde AREA bulunmadığının canlı metadata ve çevrim dışı tekrarla kontrolü."
change_summary: "Canlı metadata HTTP 200 ve eski hash ile eşleşme; AREA yok, sayısal alt küme istenmedi. Yeni uygunluk komutu eklendi."
---
# AREA kaynağı · Gerçek metadata kontrolü

**Ortam:** 2026-10-19, Windows, analysis sanal ortamı / Python 3.12.14. M1 devam talebi; fetch sonrası yeni main/M2 katkısı yok. M1 yerel `c0c79e2` korunarak kendi dalında çalışıldı. [Bilimsel yorum ve iki NASA belge kaydı](../research/SOURCE_AREA.md).

## Gerçek istek ve gözlem

Kayıtlı proje `.env` anahtarı yalnız NASA isteği için program içinde kullanıldı; değeri ekrana veya kanıt dosyasına yazılmadı, kayıt değiştirilmedi. Mevcut `earthdata.probe` ve `surface_source.metadata_spec` ile sabit ürün DMR'si bir kez okundu. HTTP 200; UTC **2026-10-19 09:10:18** / Türkiye **12:10:18**. Erişimden sonra token referansı temizlendi. Yeni sayısal veri/AREA sorgusu yapılmadı.

| Alan | Gözlenen |
|---|---|
| Ürün/granül | M2C0NXASM 5.12.4, MERRA2_101.const_2d_asm_Nx.00000000.nc4 |
| Kaynak | [Sabit NASA DMR URL'si](https://opendap.earthdata.nasa.gov/collections/C1276812819-GES_DISC/granules/M2C0NXASM.5.12.4%3AMERRA2_101.const_2d_asm_Nx.00000000.nc4.dmr.xml) |
| Boyut / SHA-256 | 17.065 bayt / `baa82cb258a18165c39ec5da17e4e5ec3582ae7facf75e733534ac75f1a3d35a` |
| Önceki kayıtla ilişki | examples altındaki A/B tam ürün DMR'siyle aynı hash |
| Sayısal değişkenler | lon, time, lat, FRLAND, PHIS, FRLANDICE, FROCEAN, SGH, FRLAKE |
| AREA | Sayısal bildirim yok; alan değeri veya karşılaştırma sonucu üretilmedi |
| Yerel ham kanıt | ignored `analysis/artifacts/area-source-20261019T091018Z/metadata.dmr.xml` ve `metadata-check.json`; credential değeri içermez |

Bu URL tam granül DMR'sidir; sadece dört fraksiyonu projekte eden bir sorgunun değişken listesi değildir. Sonuç, seçili granül ve bu erişim zamanı için geçerlidir. Şartname–kaynak farkının nedeni varsayılmadı.

## Tekrar üretim

`analysis` içinde, Windows CMD:

```cmd
.venv\Scripts\python.exe -X utf8 -m expedition73 check-source-area --metadata examples/a-surface-fractions/metadata.dmr.xml
```

Mac/Linux: `.venv/bin/python -X utf8 -m expedition73 check-source-area --metadata examples/a-surface-fractions/metadata.dmr.xml`. Yeni komut ağ/token istemez. `analysis/examples/source-area-capability.json` kayıtlı tam çıktıdır. Mevcut A kaydı ve yeni canlı DMR dosyasıyla CLI ayrı çalıştırıldı; ikisi aynı hash ve `not_available_in_selected_granule` verdi. Bu komut yeni canlı erişim veya gerçek Mac çalıştırması değildir.

## Doğrulama sınırı

Yedi yeni test; gerçek kayıt/özet eşitliği, gelecekte AREA bildiriminin yine veri doğrulaması sayılmaması, Attribute–sayısal dizi ayrımı, yinelenen/gruplu değişken reddi, yanlış ürün/grid/bozuk/büyük XML ve çevrim dışı CLI başarı/hata davranışı sınandı. **153 test / 33,269 saniye, başarılı.** İki nokta validate, A alan, B parçalı alan ve iki fraksiyon replay'i başarılı. Portal check/strict build ve git diff --check geçti; bunlar sayısal AREA doğrulaması değildir. Sayısal AREA dönüştürücüsü veya kaynak alanıyla fark hesabı yok; mevcut sıcaklık ve koşullu kapsam sonuçları değişmedi.

Yeni dilim M1 dalında yerel; GitHub/Pages/Ubuntu CI veya Mac yayını/çalıştırması yapılmadı. M2'nin bu yeni bulguyu incelediği varsayılmaz. `.env` ve özel artifacts korunur.
