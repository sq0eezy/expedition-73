---
status: Validating
updated: "2026-10-18"
review_summary: "A/B için küçük MERRA-2 sabit fraksiyon alt kümesini alma ve çevrim dışı dönüşüm kontrolü."
change_summary: "Kullanıcının gerçek A/B alt kümeleri 56/55 hücreyle çevrim dışı yeniden doğrulandı; kara/buz politikası ve maskeli seri açık."
---
# Küçük kara/su fraksiyon alt kümesi

**2026-10-18: gerçek A/B fraksiyon yanıtıyla dönüşüm doğrulandı.** Kullanıcının yerel çıktısındaki 56/55 hücre iki ayrı çevrim dışı tekrar kontrolünden geçti; [gerçek kaynak/özet kanıtı](../evidence/SURFACE_SUBSET_CHECK.md). Kara/buz politikası veya maskeli sıcaklık serisi henüz seçilmedi/üretilmedi. Önceki [metadata erişimi](../evidence/EARTHDATA_METADATA.md) HTTP 200 verdi. Bu yeni adım A'nın 56 ve B'nin 55 kaynak hücresi için dört oranı ve koordinatları ister; tam dünya dosyası istenmez. [Yazılım kontrolü ve sınırları](../evidence/SURFACE_SUBSET_CHECK.md).

## Windows · M1

Bu çalışma alanında ek paketler yalnızca analiz sanal ortamına kuruldu. Depo kökündeki kendi PowerShell terminalinde:

```powershell
& .\analysis\.venv\Scripts\python.exe .\analysis\scripts\fetch_surface_fractions.py
```

Varsayılan olarak proje kökündeki `.env` içinden `EARTHDATA_TOKEN` okunur; yoksa kaydetmeden gizli sorulur. Kullanıcı 2026-10-18’de yerel kayıt istedi. Bir kez kaydetmek veya değiştirmek için aynı komuta `--save-token` eklenir. Değer gizli girilir, yalnız Git dışında tutulan `.env` anahtarı güncellenir; argümana, süreç ortamına veya sonuç dosyalarına kopyalanmaz. Önceki metadata denemesi kalıcı kayıt yapmamıştı. Yeni kaydı kullanıcı kendi terminalinde yapacak. Bir metadata ve iki sınırlı veri isteği yapılır; yönlendirme izlenmez. [403 kontrolü ve CMD ile kayıt](EARTHDATA_ACCESS.md).

Yeni ortamda önce `& .\analysis\.venv\Scripts\python.exe -m pip install -r analysis/requirements-mask.txt` gerekir. Var olan temel nokta/alan komutları için NetCDF paketi zorunlu değildir.

## macOS · M2

Bu kod kendi dalına incelenerek alınmış ve analiz ortamı kurulmuşsa, depo kökünden:

```sh
analysis/.venv/bin/python -m pip install -r analysis/requirements-mask.txt
analysis/.venv/bin/python analysis/scripts/fetch_surface_fractions.py
```

Temel ortam yoksa `python3 -m venv analysis/.venv` ile oluşturulur. Python 3.11+ gerekir. Sabitlenen netCDF4 1.7.2 için macOS sürümü/mimarisiyle uyumlu paket gerekebilir; bu komutlar bu oturumda gerçek Mac'te çalıştırılmadı. [Paketin dağıtımları](https://pypi.org/project/netCDF4/1.7.2/).

## Başarı ve çevrim dışı tekrar

İki yanıt da geçerliyse `NASA A/B surface subsets converted and replayed` mesajı ve `analysis/artifacts/surface-fractions-ZAMAN/` yolu çıkar. İçindeki `a/` ve `b/` klasörleri ayrı ayrı şunları içerir:

- `request.json`: aday sıcaklık penceresi yapılandırması.
- `metadata.dmr.xml`: kullanılan sabit ürünün metaverisi.
- `response.nc4`: yalnızca istenen küçük NetCDF alt kümesi.
- `fractions.json`: dört oranı ayrı koruyan ortak maske girdisi 0.1.0.
- `conversion-report.json`: dönüştürücü sürümü, metadata/yanıt SHA-256, bayt ve hücre sayısı; yerel credential kayıt durumu ve bilimsel profil kabulü false.

`artifacts/` yereldir ve Git tarafından yok sayılır. Gerçek çıktı klasörüyle çevrim dışı tekrar, Windows'ta:

```powershell
& .\analysis\.venv\Scripts\python.exe .\analysis\scripts\fetch_surface_fractions.py --replay analysis/artifacts/surface-fractions-ZAMAN/a
```

Mac'te aynı argümanlarla `analysis/.venv/bin/python analysis/scripts/fetch_surface_fractions.py --replay ...` kullanılır. `ZAMAN` yerine başarı mesajındaki klasör yazılır. Tekrar kontrolü token veya ağ istemez; kaydedilmiş ham verinin tekrar aynı sonuca dönüştüğünü gösterir, kaynağın bağımsız kimlik doğrulaması değildir.

## Hangi kontroller uygulanır?

Kaynak kimliği, global boyutlar, `/time,/lat,/lon` sırası, tür/birim ve kimlik ölçek/ofseti önce metadata'da denetlenir. NetCDF içindeki boyutlar, gerçek koordinat vektörleri ve kaynak dolgu metaverisi ayrıca karşılaştırılır. Tam beklenen hücre kapsamı, sonlu ve 0–1 arası oranlar, hücrede toplamın 1'e `1e-6` yakınlığı gerekir. Dolgu/eksik oran sıfıra çevrilmez; koordinat ters çevrilmez veya yeniden örneklenmez. Sunucu bu beklentilerden farklı yanıt verirse dönüştürücü durur; gerçek yanıtla yeni sürüm incelenir.

URL `.dap.nc4?dap4.ce=...` biçiminde, sıfır tabanlı dahil indekslerle oluşturulur. [NASA GES DISC açıklaması](https://forum.earthdata.nasa.gov/viewtopic.php?t=8140) sunucu tarafında alt küme için bu DAP4 biçimini tarif ediyor. NetCDF kütüphanesi sadece bellekteki yanıtı açar; token veya ağ adresi almaz. [Kütüphane belgesi](https://unidata.github.io/netcdf4-python/).

## Bu adım neyi sonuçlandırır?

Başarı, kaynak oranlarını sıcaklık hücrelerine koordinatla bağlayan küçük aktarımı doğrular. `FRLAND` / `FRLANDICE` seçimi, gerçek kıyı çizgisi, kesin analiz alanı ve bilimsel uygunluk ayrıca değerlendirilir. Bu komut sıcaklığı değiştirmez veya maskeli seri üretmez. Tam hücre oranını kırpılmış alana uygulamak yaklaşık yöntemdir; T2M kara parçasının özel sıcaklığına dönüşmez. [Maske araştırması](../research/SURFACE_MASK.md).
