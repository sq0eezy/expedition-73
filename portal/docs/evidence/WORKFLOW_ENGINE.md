---
status: Validating
updated: "2026-10-18"
review_summary: "A→B, A+B→C için çalışan yerel teknik deneme; bilimsel modül entegrasyonu değildir."
change_summary: "İlk bağımlılık motoru, yapay CLI örneği ve 20 yeni test hazır; toplam 121 test ve eski gerçek veri tekrarları geçti."
---
# Modül yürütme denemesi · 0.1.0

**Sonraki adım tamamlandı:** Aşağıdaki kayıt ilk yapay denemeyi anlatır. Gerçek T2M/fraksiyon adaptörleri daha sonra bağlandı; [ayrı gerçek veri kanıtı](SURFACE_WORKFLOW.md). İlk 121 test sonucu tarihsel, sonraki toplam 134.


M1 devam talebi sonrasında `analysis/expedition73/workflow.py`, `workflow_demo.py`, `schemas/workflow-request.schema.json`, `demo-workflow` komutu ve `tests/test_workflow.py` eklendi. Mimari yön [modül sistemindedir](../architecture/MODULE_SYSTEM.md). Bu, MOD-06'nın **yerel ve yapay verili** uygulama kanıtıdır; yeni bir bilimsel modül, NASA hesabı veya son web uygulaması değildir.

## Gerçekte çalıştırılan örnek

`analysis/examples/workflow-demo.json` bu komutla üretilen, açıkça `synthetic_fixture` işaretli bir örnek kayıttır:

| Çalıştırma | A | B = 2 × A | C = A + B | Gerçek çağrı sırası |
|---|---:|---:|---:|---|
| İlk yapay istek | 4 | 8 | 12 | A, B, C; her biri bir kez |
| A parametresi değişince yeni istek | 7 | 14 | 21 | A, B, C; yeni çalışma kimliği |

İlk kaydın yeni isteğe göre karşılaştırılması A/B/C için `stale` verdi; eski kayıt değiştirilmedi. B'nin A girdisi ile C'nin A girdisinin aynı çıktı kimliği olduğu doğrulandı. Eski A ile yeni B karışımı aynı context altında olsa bile ortak ata kimliği uyuşmadığından reddedildi. Buradaki A/B/C coğrafi bölgeler değil, yapay işlem kimlikleridir.

## Kontroller ve çalışma sınırı

- İstek JSON şeması: benzersiz düğüm kimliği, en çok 64 düğüm, düğüm başına en çok 32 girdi; her düğümün tek `result` portu var.
- Başlamadan eksik üretici, döngü, istenen çıktı portu, tip/şema sürümü/birim etiketleri ve kayıtlı işlemin tam sürümü kontrol edilir. JSON içinden Python, dosya yolu veya shell komutu çalıştırılmaz; yürütülecek fonksiyonlar uygulamanın kayıt listesinde açıkça verilir.
- Hedefin zorunlu ataları tek topolojik sırayla çalışır. Kullanılmayan düğümler hesaplanmaz; geçersiz döngüler bütün tanımda reddedilir. Bu sürüm sıralıdır, paralel çalıştırma motoru değildir.
- Girdiler, parametreler ve context tüketiciye ayrı kopyalarla verilir; bir tüketici başka tüketicinin kaynak kaydını değiştiremez. Çıktıda çalışma kimliği, işlem sürümü, girdi kimlikleri, ata izi, context/parametre kaydı, değer ve SHA-256 bulunur. Kimlik denetimi yerel bütünlük kontrolüdür; bağımsız kaynak doğrulaması değildir.
- Teknik hesap bitse bile kayıtlı çıktı doğrulayıcısından geçmeyen değer `OUTPUT_INVALID` olur. Hata veren düğüm `failed`, zorunlu tüketicisi `blocked` olur; bağımsız kardeş devam edebilir. Hata metni çıktıya kopyalanmaz; ayrıntılı hata tanısı henüz ayrı geliştirme işidir.
- `compare_snapshot` açıkça çağrıldığında tanımlı context/parametre/sürüm/bağlantı değişimini ve aşağıdaki işleri güncel değil olarak saptar. Canlı izleme, kalıcı sonuç deposu veya çalıştırmalar arası cache **yoktur**. Aynı istek yeniden çalıştırılırsa yeniden hesaplanır; tek çalıştırma içindeki ortak A ise bir kez hesaplanır.
- Dış kaynak değişimi kendiliğinden keşfedilmez; kaynak revizyonu/hash'i isteğe işlenmelidir. Context şu an uygulamanın verdiği JSON'dur: motor gerçek bölge poligonu, takvim, NASA kalite kuralı veya göstergenin fiziksel anlamını yorumlamaz. Tip/sürüm/birim etiketlerinin eşitliği bilimsel uygunluk kanıtı değildir; gerçek modülün ek uygunluk/doğrulama kuralları gerekecek.

Çalıştırma durumu waiting/running/completed/failed/blocked olayları olarak raporlanır; webde canlı gösterim uygulanmadı. Genel bilimsel ortak sonuç şeması değişmedi. Bu ilk deneme anında gerçek T2M/fraksiyon adaptörleri bağlı değildi; sonraki entegrasyon üstteki ayrı kanıtta. Önceki CLI'lar çalışmaya devam eder.

## Çalıştırma

Depo kökünden **Windows CMD**, kurulu analiz ortamıyla:

```cmd
cd analysis
.venv\Scripts\python.exe -m expedition73 demo-workflow
```

Mac/Linux:

```sh
cd analysis
.venv/bin/python -m expedition73 demo-workflow
```

Komut yalnız yapay verili raporu konsola basar; ağ, Earthdata token'ı veya ek paket istemez. UUID ve bunlara bağlı çıktı kimlikleri yeni çalıştırmada değişir; sayı ve bağların tutarlılığı sınanır. Mac komutu burada gerçek Mac'te çalıştırılmadı.

## Doğrulama · 2026-10-18

Windows / Python 3.12.14 / analysis sanal ortamı: `-m unittest discover -s tests` **121 test / 14,722 saniye**, başarılı. Bunların 20'si yeni workflow testidir. Sıra ve ortak A'nın tek çalışması, kayıtlı örneğin izleri, döngü/kayıp tanım/sürüm/port/birim hataları, başarısız üst iş/bağımsız kardeş, çıktı denetimi, kopya izolasyonu, kaynak/bölge/dönem/parametre değişimi ve eski/yeni ata karışımı sınandı.

Önceki gerçek A/B nokta `validate`, A `validate-window`, B `validate-tiled-window` ve yerel gerçek A/B fraksiyon `--replay` komutları tekrar geçti. NASA'ya yeni istek yapılmadı; bu kontroller eski gerçek örneklerin korunduğunu gösterir, workflow içinde bilimsel entegrasyon kanıtı değildir. Mevcut yapay NetCDF testlerinde NumPy deprecation uyarısı sürdü; hata yoktu. Portal check/build ile ilgili sonuç çalışma günlüğündedir.

İş yerel M1 dalında; M2 incelemesi, uzak CI, main birleşmesi ve Pages yayını yapılmış sayılmaz.
