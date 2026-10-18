# Kayıtlı küçük NASA fraksiyon alt kümeleri

`a-surface-fractions/` ve `b-surface-fractions/`, 2026-10-18'de kullanıcı tarafından NASA OPeNDAP üzerinden alınan küçük A/B alt kümelerinin açık veri/üretim kayıtlarıdır. A 56, B 55 kaynak hücresini kapsar; bütün dünya dosyası değildir. Kaynak: NASA GMAO / GES DISC **M2C0NXASM 5.12.4**, MERRA-2 const_2d_asm_Nx, DOI [10.5067/ME5QX6Q5IGGU](https://doi.org/10.5067/ME5QX6Q5IGGU). [NASA atıf rehberi](https://gmao.gsfc.nasa.gov/gmao-products/merra-2/citing-merra-2-data_merra-2/).

Her klasöre yalnız beş açık kaynak/hesap dosyası kopyalandı: `request.json`, `response.nc4`, `metadata.dmr.xml`, `fractions.json`, `conversion-report.json`. Özel `.env` veya başka yerel dosya kopyalanmadı. Rapordaki `credentials_persisted: true`, ilk kullanıcının yerel kaydı kullandığını belirtir; credential değeri içermez ve çevrim dışı tekrar için credential gerekmez. İlk özel artifacts klasörü korunur.

`a-surface-sensitivity.json` / `b-surface-sensitivity.json`, bu fraksiyonlar ile mevcut gerçek 2024 POWER T2M pencerelerinin **aday** yeniden ağırlıklandırma denemesidir. Kaynak SHA-256, birim/dönem, yöntem ve varsayımlar içerir. Kaynak hücre sıcaklığı kara parçasına özgü sıcaklığa dönüşmez; fraksiyon kırpılmış hücre parçasında sabit kabul edilir. Nihai maske/analiz bölgesi veya iklim eğilimi sonucu değildir.

Çevrim dışı doğrulama/yeniden hesaplama, `analysis` içinde Windows CMD:

```cmd
.venv\Scripts\python.exe scripts/fetch_surface_fractions.py --replay examples/a-surface-fractions
.venv\Scripts\python.exe scripts/fetch_surface_fractions.py --replay examples/b-surface-fractions
.venv\Scripts\python.exe -m expedition73 run-surface-workflow --window-run examples/b-window-2024 --fraction-run examples/b-surface-fractions --output-dir artifacts/b-surface-new-run
```

Mac/Linux'ta `.venv\Scripts\python.exe` yerine `.venv/bin/python` kullanılır. Yerel ortamda `requirements-mask.txt` kurulu olmalıdır. [Yöntem, komut ve doğrulama kanıtı](../../portal/docs/evidence/SURFACE_WORKFLOW.md).
