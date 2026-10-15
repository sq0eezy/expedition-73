# Modül ve pilot tasarım kaydı

**Tarih:** 2026-10-15 · **Ortam:** Windows, mevcut Python 3.12/MkDocs portal ortamı.

## Kaynak ve kapsam

M1 modüle özel hesap + ortak sonuç dili yaklaşımını kabul etti; alt modüller, modül çıktısının girdi olması, dar deneme ve web uygulaması teslimi istedi. İlk gösterge sorusuna 2 metre hava sıcaklığı yanıtı verdi. [ADR-004](../decisions/ADR-004-MODULES-AND-PILOT.md). M2 görüşü, alan/ürün/dönem/yöntem seçimi varsayılmadı.

Konu hiyerarşisi ve veri bağımlılığı ayrı tanımlandı; özel hesap/adaptör/uygunluk akışı, sürümlü çıktı taslağı, pilot koşulları ve web ekranlarının kapsamı belgelendi. Uygulama kodu veya çalışır JSON Schema üretilmedi.

## Kontroller

- Depo kökünde `portal/.venv/Scripts/python.exe portal/scripts/portal.py check`: yerel bağlantı, durum, gezinme ve şablon kontrolleri geçti.
- `portal/.venv/Scripts/python.exe portal/scripts/portal.py build`: strict MkDocs derlemesi geçti.
- `git diff --check`: boşluk hatası yok.
- Statik çıktı geçici olarak `127.0.0.1` üzerinde `/expedition-73/` önekiyle sunuldu. Python HTMLParser ile 57 HTML sayfasındaki yerel bağlantılar/varlıklar toplandı; 67 benzersiz HTTP yolu 200 döndü. Önek dışına kaçan yol yok; okuma kataloğu geçerli JSON. Pilot sayfasında T2M ve aday dönem metni doğrulandı. Geçici sunucu kontrol sonunda kapatıldı.

Bu kontroller belge portalına aittir. Bilimsel veriye erişim, çalışan istatistik/adaptör, modüller arası entegrasyon ve ürün arayüzü henüz doğrulanmadı. Mermaid kodları derleme çıktısına alındı; bu kontrolde tarayıcıda görsel render sınanmadı.
