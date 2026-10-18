---
review_summary: "Kullanıcının yerel Earthdata kontrolünde gerçek HTTP 200 ve MERRA-2 maske metadata doğrulaması."
change_summary: "Dört fraksiyon değişkeni, boyut sırası ve dolgu metaverisi okundu; fraksiyon değerleri henüz alınmadı."
---
# Earthdata metadata erişimi · Gerçek doğrulama

**2026-10-17 · Kullanıcının Windows/PowerShell terminalinde**, proje analiz Python ortamıyla `analysis/scripts/check_earthdata_access.py` çalıştırıldı. Kullanıcı sonucu kontrol etmemizi istedi. Terminal başarı mesajı, yerel erişim raporu ve kayıtlı DMR XML birlikte denetlendi. Token okunmadı; script token'ı kaydetmiyor.

| Alan | Gerçek sonuç |
|---|---|
| HTTP | **200**, `metadata_received` |
| UTC / Türkiye saati | 2026-10-17 09:29:33 / 12:29:33 |
| Kaynak dosya | `MERRA2_101.const_2d_asm_Nx.00000000.nc4` |
| Koleksiyon | `M2C0NXASM` 5.12.4, `C1276812819-GES_DISC` |
| İstek | [NASA OPeNDAP DMR metadata](https://opendap.earthdata.nasa.gov/collections/C1276812819-GES_DISC/granules/M2C0NXASM.5.12.4%3AMERRA2_101.const_2d_asm_Nx.00000000.nc4.dmr.xml) |
| Yanıt boyutu | 17.065 bayt |
| SHA-256 | `baa82cb258a18165c39ec5da17e4e5ec3582ae7facf75e733534ac75f1a3d35a` |
| Bütünlük kontrolü | Kayıtlı XML yeniden hash'lendi, erişim raporuyla eşleşti |
| Yerel kayıt | Yok sayılan `analysis/artifacts/earthdata-access-20261017T092924Z/` klasöründe XML ve rapor; kimlik bilgisi yok |

## Canlı metadata ile doğrulananlar

`FRLAND`, `FRLANDICE`, `FRLAKE`, `FROCEAN` değişkenlerinin dördü de Float32; birim `1`. Her birinin boyut sırası `/time`, `/lat`, `/lon`; boyutlar sırasıyla **1 × 361 × 576**. `_FillValue` ve `missing_value` metadata metni `9.99999987e+14`. Bu, POWER T2M yanıtındaki -999 dolgusundan farklıdır; gerçek maske dönüştürücüsü kaynak dolgusunu ayrıca uygulamalıdır.

## Sınır ve sonraki adım

Bu gerçek erişim başarısıdır; maske fraksiyonlarının sayısal değerleri, koordinat vektörleri veya gerçek maskeli T2M sonucu henüz alınmadı. `mask_values_retrieved=false` kaydı korunur. Erişim başarısı bütün diğer ürünlere yetki, kaydedilmiş token veya nihai bilimsel profil onayı anlamına gelmez.

Sırada küçük A/B fraksiyon/koordinat alt kümesi ve kaynak dönüşümünü doğrulama var. Kara/buz dahil etme kuralı ve tam hücre oranını sınır parçasında kullanma yaklaşımı aday olarak kalır. Önceki oturumsuz 401 sonucu tarihsel olarak doğrudur; yeni kayıt yerel token ile çalışan isteği doğrular.
