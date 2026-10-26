---
status: Validating
updated: "2026-10-26"
review_summary: "Kaynak tekrarı doğrulanmış maskesiz T2M için iki aday yıllık özet ve CLI kullanımı."
change_summary: "annual_weighting.py, 0.1.0 aday çıktı şeması ve iki 24 yıllık tekrar üretilebilir rapor eklendi."
---
# Aday yıllık ağırlık denetimi

Bu komut [yıllık özet için iki hedefi](../research/TEMPORAL_AGGREGATION.md) aynı kayıtlı maskesiz T2M üzerinde karşılaştırır. Her yıl için ayların gün sayıları/ağırlıkları, iki sonuç, farkı ve aynı kaynaktan gelen API yıllık hücre özeti bulunur. [Gerçek kanıt](../evidence/ANNUAL_WEIGHTING_CHECK.md). Bilimsel yöntem/maske/dönem seçimi, eğilim veya p-değeri değildir.

Windows CMD, **analysis içinde**:

```cmd
.venv\Scripts\python.exe -X utf8 -m expedition73 audit-annual-weighting --run examples/a-history-2001-2024
.venv\Scripts\python.exe -X utf8 -m expedition73 validate-annual-weighting --run examples/a-history-2001-2024 --input examples/a-annual-weighting-audit.json
.venv\Scripts\python.exe -X utf8 -m expedition73 validate-annual-weighting --run examples/b-history-2001-2024 --input examples/b-annual-weighting-audit.json
```

İlk komut JSON'u stdout'a verir; dosya yazmaz, NASA/token istemez. İstersen CMD'de önce `if not exist artifacts mkdir artifacts`, sonra ilk komutun sonuna `> artifacts/a-annual-audit.json` ekle; yeni dosya adı kullan. `-X utf8` yönlendirilen JSON'un UTF-8 olmasını sağlar. PowerShell Out-File'ın sürüme bağlı varsayılan kodlamasını bu CMD örneğiyle karıştırma.

Mac'te analysis içinde aynı argümanlarla `.venv/bin/python -X utf8 -m expedition73 ...`; klasör için `mkdir -p artifacts`. Depo kökünde `analysis/.venv/bin/python scripts/workspace.py check` eski/yeni kaynak tekrarlarıyla birlikte iki kayıtlı yıllık raporu da doğrular. Bu oturum Windows'ta çalıştı; yeni Mac sonucu iddia edilmez.

## Sözleşme ve kaynak bağı

Yeni çıktı `candidate_annual_weighting_audit` **0.1.0**, modül `air_temperature_2m_annual_weighting` 0.1.0; kaynak history 0.1.0 ve eski bilimsel alan yöntemi değişmedi. Bölgeler/birim/yüzey/dönem, açık iki yöntem tanımı, her ayın ağırlığı, yıl eksikliği, kaynak kimlikleri ve seçim yapılmadığı bilgisi taşınır. `selected_weighting=null`, `scientific_acceptance=not_performed`, `inference_performed=false` zorunludur.

Önce bütün yılların ham kaynakları history motoruyla yeniden hesaplanır. Sonra yıllık result/response/manifest byte'ları doğrulanan hash'lerle eşleşmeden kullanılmaz. Parent result.json da tekrar sonucuyla karşılaştırılır; `source_history_result_sha256` yeniden hesaplanan float'ların değil **kayıtlı dosya byte'larının** hash'idir. Böylece platformların olası son basamak aritmetik farkları kaynak kimliğine dönüşmez. Kimlik kontrolü bütün yıllık dosya hash'leriyle birlikte değerlendirilir; bir yazar imzası değildir.

`validate-annual-weighting` kaydedilen raporu şemayla ve yeniden hesaplanan bütün alanlarla karşılaştırır; kaynak/sayı/ağırlık/aday bayrakları değişirse reddeder. Mevcut sayısal tekrar toleransı korunur, yeni bilimsel doğruluk eşiği seçilmez. Eksik aylar/sağlayıcı yıllık hücreleri sıfırla veya kısmi ortalamayla doldurulmaz.

Bu ilk hesap analysis içindedir; genel web kataloğuna veya beş düğümlü yüzey motoruna eklenmedi. Mevcut web/rapor/ZIP sözleşmesi değişmedi. Yöntem adayının incelenmesi ve ortak bilimsel karar sonrasında genel sonuç adaptörüne bağlanması ayrı adımdır; M2'nin kabulü varsayılmaz.
