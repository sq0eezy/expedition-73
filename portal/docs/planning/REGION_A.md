---
review_summary: "Emeç için Bölge A görevleri ve ortak modül geliştirmesiyle bağlantıları."
change_summary: "M1 modülleri ve Bölge A'yı üstlendi; alan işi ve modül teslimleri ayrıldı."
---
# Bölge A · Emeç'in çalışma listesi

M1, 2026-10-16 tarihinde **modülleri ve Bölge A'yı** üstlendi. Görev durumları/sorumlular [panoda](WORK_BOARD.md), ortak çalışma profili [iş bölümünde](REGION_WORKFLOW.md). Mevcut A adayı [Colorado Platosu çevresi](../research/REGION_CANDIDATES.md); kesin alan seçimi hâlâ açık.

## İlk ara teslim · 2026-10-16

[A fişi](../research/regions/REGION_A_PROFILE.md), gerçek 2024 T2M nokta yanıtı ve `analysis/` altında ilk CLI/şema/adaptör hazır. [Kılavuz](../guide/T2M_ADAPTER.md), [kontroller ve sınırlar](../evidence/T2M_POINT_PROBE.md). Nokta erişimi bölgesel analiz tamamlandı anlamına gelmez; görev durumları panoda.

## Bölge işleri

**İkinci ara teslim:** [Maskesiz aday dikdörtgen hesabı](../guide/T2M_WINDOW.md) gerçek 56 hücre/12 aylık yanıtta çalışıyor; Ocak bağımsız hesapla kontrol edildi. Bu R-A04'ün teknik denemesidir; R-A03 ortak profili veya nihai analiz maskesi yerine geçmez. [Kanıt](../evidence/T2M_WINDOW_PROBE.md).

| Görev | İş ve somut teslim | Bitiş ölçütü / bağımlılık |
|---|---|---|
| R-A01 | [A fişine](../research/regions/REGION_A_PROFILE.md) soru, kaynak, sınır/poligon önerisi ve kara/su bilgisini yaz | Alan yeniden bulunabilir; aday/kabul ayrımı açık |
| R-A02 | Küçük T2M API örneğini, parametreleri, birimi, zaman/ızgara kapsamını ve eksikliği belgele | Gerçek sayısal yanıt veya tekrarlanabilir hata; nokta/alan ayrımı açık |
| R-A03 | B erişim özetiyle ortak sağlayıcı/ürün, dönem, sıklık, maske/alan ve analiz profilini kaydet | Her iki alanın uygunluğu incelenmiş; [ortak profil](REGION_WORKFLOW.md) sürümlenmiş; R-A02/R-B02 gerekir |
| R-A04 | Aynı modüle A girdilerini ver; bir tarih için alan özetini bağımsız doğrula | Ara değer/ağırlıklar ve sonuç karşılaştırması kayıtlı; R-A03 + MOD-02/03 gerekir |
| R-A05 | Tam dönem seri, kalite ve analiz çıktısını üret; eksik ay/alan değişimini incele | Geçerli kapsam ve yöntemi izlenebilir çıktı; küçük örnek uzun trend yerine sunulmamış |
| R-A06 | A yorumunu yaz, B'nin karşılaştırılabilirliğini ve arayüzde A kartlarını incele | Kaynak/belirsizlik ve tarih/birim eşleşmesi; R-A05 ve arayüz gerektiği ölçüde hazır |

## Modül işleri

| Görev | M2'nin çalışmasını mümkün kılan teslim |
|---|---|
| MOD-01 | [Ortak sözleşmeyi](../architecture/DATA_AND_FLOWS.md) teknik şemaya dönüştür; örnek bölge girdisi, çıktı türleri, hata durumları ve çağrı biçimini kaydet. Girdi örneklerini A/B erişim denemelerinden doğrula. |
| MOD-02 | T2M kaynak erişimi/normalleştirme, bölgesel seri ve seçilecek istatistik yöntemini tek modülde uygula; küçük bağımsız örnekler ve yöntem varsayımlarını kontrol et. Bölge ayarları hesap kodundan ayrı olsun. |
| MOD-03 | Sonuç adaptörü ve uygunluk kontrolünü uygula; çalıştırılabilir örnek, bağımlılıklar, modül/sözleşme sürümü ve B'nin dolduracağı bölge girdilerini M2'ye bırak. Modüle özel tanılar korunsun. |

İlk ara teslim MOD-01'in örnek girdi/çıktısıdır; M2 bütün modülün bitmesini beklemeden B fişi/API denemesiyle ilerler. R-A03 ortak profilinden sonra MOD-02 bilimsel yöntemini sabitler; MOD-03 sürümüyle iki alan aynı hesap üzerinden çalışır. Web uygulamasının genel geliştirme sorumlusu ayrıca atanacak; modül sahipliği otomatik arayüz sahipliği sayılmaz.

[B görevleri](REGION_B.md) · [Pilot koşulları](PILOT.md)
