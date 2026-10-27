---
status: Validating
updated: "2026-10-22"
review_summary: "Yıllık NASA T2M kaynaklarını doğrulayıp zaman boyunca birleştirme ve yıl seçerek inceleme."
change_summary: "İlk iki yıllık kayıt ve yıllık CLI sözleşmeleri; 2026-10-24 gerçek 2001–2024 uzantısına bağlantı eklendi."
---
# Çok yıllı T2M erişimi · İlk iki yıllık dilim

**2026-10-24 güncel erişim:** [2001–2024 gerçek kaynak/yıl kataloğu](T2M_LONG_PERIOD.md) iki pencerede 288'er ayla hazır. Bu sayfa ilk iki yıllık kaydı ve değişmeyen yıllık CLI/sözleşmeleri anlatır; aşağıdaki henüz alınmadı ifadeleri 2026-10-22 aşamasına aittir.

M1, önce iki yıllık deneme ve sonra uzun dönem altyapısı önerisi üzerine devam istedi. Bu teknik çalışma, kesin bölge/maske/2001–2024 bilimsel dönem veya eğilim yöntemi kabulü değildir. [Gerçek kanıt](../evidence/T2M_HISTORY_CHECK.md).

A/B için 2023-01…2024-12, **24/24 ay** kayıt var. Yeni 2023 NASA POWER yanıtları alındı, önceki 2024 kaynak byte'ları aynen yeniden kullanıldı. A 56, B 55 hücre; B yılda iki coğrafi tile/5 tekrar çıkarılmasıyla birleşir. Yeni history.py zaman parçalarını birleştirir; coğrafi tile ortalamalarını tekrar ortalamaz.

## Çalıştırma

Windows CMD, depo kökünde `scripts\start-preview.cmd`; Mac'te `sh scripts/start-preview.sh`. Ekrandaki **Kayıtlı yıl** alanından 2023/2024 seçilir. Ay/yüzey/çift seçimi yıl değişince korunur. Grafik seçilen yılın 12 ayını gösterir; yılları tek çizgide birleştiren uzun dönem grafiği ve trend hesabı henüz yok.

Çevrim dışı kontrol, Windows CMD **analysis içinde**:

```cmd
.venv\Scripts\python.exe -m expedition73 validate-window-history examples/a-history-2023-2024
.venv\Scripts\python.exe -m expedition73 validate-window-history examples/b-history-2023-2024
```

Mac'te analysis içinde aynı komutların Python yolu `.venv/bin/python`; depo kökünden `analysis/.venv/bin/python scripts/workspace.py check` bütün kontrolleri çalıştırır. Yeni bağımlılık eklenmedi.

Yeni ağ denemesi, analysis içinde; komut var olan hedefi ezmez:

```cmd
.venv\Scripts\python.exe -m expedition73 fetch-power-history --config examples/a-history-2023-2024/request.json --run examples/a-window-2024 --output-dir artifacts/a-history-new
```

Bu örnekte kayıtlı 2024 açık seed olarak doğrulanır, yalnız eksik 2023 API'den alınır. B config/seed ile aynı komut B'nin coğrafi tile'larını kullanır. `assemble-window-history` aynı arayüzde yalnız bütün yılların `--run` kayıtları sağlanınca çevrim dışı çalışır. Birden fazla --run verilebilir, kaynak sırası önemsizdir; yinelenen/fazla/başka bölge yıl kaydı reddedilir.

## Kayıt ve sınırlar

Parent request pencere şeması 0.1.0'dır; her alt istek tek yıla indirgenir. İstek başına önceki iki yıl sınırı kaldırılmadı. Collector en çok 50 yıl ve yıllık plan başına en çok 16 tile ile sınırlı; gelecek yıl/bozuk geometri bütün plan için ağdan önce reddedilir. Bu sayılar pilot işlem sınırıdır, NASA genel veri kapsamı iddiası değildir.

Her `year-YYYY` klasörü ham yanıt/istek/normalize sonucu ve gerekiyorsa tile manifestini korur. Parent `history.json` yıllık dosya byte hash'lerini; yeni `recorded_window_history` 0.1.0 sonucu kesintisiz aylık seriyi, kaliteyi ve kaynakları taşır. Bütün alt kayıtlar yeniden hesaplanır. Aynı bölge/sınır, gösterge/birim, kaynak/API sürümü, takvim/zaman standardı, bilimsel alan yöntemi, grid ve alan desteği eşleşmelidir. Eksik yıllar reddedilir, eksik ay null kalır; sıfırla doldurulmaz.

Tamamlanmamış toplama yeni tamamlanmış çıktı diye yayımlanmaz. Hata geçici çalışma klasörünü temizler, önceki kayıtlar korunur. Otomatik retry/kalıcı cache yok; uzun sorgular için açık yıllık seed'ler kullanılabilir. Kaynak kontrolü bilimsel kalite veya bağımsız NASA kimlik doğrulaması değildir.

## Yıl kataloğu ve rapor uyumu

web/history-regions.json iki geçmişi seçer. Builder önce her geçmişi, sonra her yılın mevcut beş düğümlü T2M/fraksiyon akışını doğrular. Varsayılan 2024, seçenekler 2023/2024. **Web zarfı 0.4.0** (`recorded_temperature_year_catalog`), snapshot'lar aynı **0.3.0** sözleşmesinde exact UTF-8 JSON metni ve hash taşır. Böylece 2024 snapshot'ı eski çıktı ile byte aynı kalır; eski 2024 raporları çalışır. Rapor açılınca ayın ait olduğu yıl katalogda varsa önce o kayıtta doğrulanır, sonra yıl/seçimler uygulanır. Eski bağımsız 0.3.0 web verisi de açılır.

Altı genel dosya korunur; yeni ZIP manifesti **0.3.0**, verifier eski 0.1.0/0.2.0 manifestleri de kendi veri sürümüyle doğrular. Rapor 0.1.0 ve bilimsel alan yöntemi/teknik 2024 profili 0.1.0 değişmedi. Tüm katalog 8 MB sınırı içindedir.

2023'te de aynı kayıtlı sabit M2C0NXASM fraksiyon örneği yalnız aday duyarlılık için kullanılır; 2023 arazi örtüsünün veya uzun dönem değişmeyen maskenin bilimsel doğrulanması değildir. 2001–2024 için **24 yıllık parça/288 beklenen ay** planı test edildi, o yılların tamamı alınmadı. Sonraki adım, erişim/kalite dilimini daha uzun aday döneme büyütmek; bilimsel sınır/yüzey/dönem ve istatistiği ayrıca kararlaştırmaktır.
