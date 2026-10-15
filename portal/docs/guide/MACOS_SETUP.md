---
review_summary: "sq0eezy için macOS Terminal üzerinden ilk kurulum, açılış ve güncelleme."
change_summary: "Arkadaşın Mac kullandığı bilgisine göre macOS kılavuzu eklendi."
---
# Mac için kurulum

Bu kılavuz sq0eezy'nin Mac bilgisayarı içindir. Komutları **Terminal** içinde çalıştır.

## 1. Python sürümünü kontrol et

~~~sh
python3 --version
~~~

Python 3.11 veya üstü gerekir. Portalın mevcut paketleri için Python 3.12 yerelde doğrulanan sürümdür. `python3` bulunmuyorsa veya sürümü eskiyse [Python'ın resmî macOS kurulum kılavuzundan](https://docs.python.org/3/using/mac.html) uygun kurulumu yap. Zaten kurulu bir `python3.12` kullanacaksan aşağıdaki temel `python3` komutlarını `python3.12` olarak çalıştır.

## 2. Depoyu güncelle ve ilk kurulumu yap

Terminal'de kendi `expedition-73` depo klasörüne geç. Commit edilmemiş yerel değişikliklerini koruduktan sonra:

~~~sh
git switch main
git pull --ff-only origin main
cd portal
python3 scripts/portal.py setup
python3 scripts/portal.py check
python3 scripts/portal.py serve --open
~~~

`setup`, paketleri Mac üzerinde oluşturulan `portal/.venv` içine kurar. Bu ortam her bilgisayarda ayrı oluşturulur; [Python venv açıklaması](https://docs.python.org/3/library/venv.html). Kurulum komutu bir kez gerekir; bağımlılıklar değiştiğinde yeniden çalıştırılabilir.

Tarayıcıda [yerel portal](http://127.0.0.1:8000/) açılır. **Ekip → sq0eezy** bölümünden kendi çalışma notuna ulaşabilirsin. Sunucu Terminal açıkken çalışır; durdurmak için **Ctrl+C**.

## 3. Sonraki açılışlar

Depo klasöründen:

~~~sh
cd portal
.venv/bin/python scripts/portal.py serve --open
~~~

Mac'teki yerel Python yolu `.venv/bin/python` olur. Komutlar ortamı doğrudan kullandığından ayrıca aktivasyon adımı gerekmez.

## 4. Arkadaşının güncellemelerini al

Sunucuyu Ctrl+C ile durdur. Depo kökünde kendi değişikliklerini koruyup `git pull --ff-only origin main` çalıştır, sonra portalı yeniden aç. Başkasının `.venv` klasörü paylaşılmaz; Git yalnızca kaynakları getirir.

## Bir adım çalışmazsa

| Görülen durum | Sonraki adım |
|---|---|
| Python sürümü 3.11'den eski | Uygun Python kurulumunu veya kurulu uygun sürüm komutunu seç |
| `.venv/bin/python` bulunamıyor | `portal/` içinde `python3 scripts/portal.py setup` çalıştır; kurulumun bitmesini bekle |
| `scripts/portal.py` bulunamıyor | Terminal'in `portal/` klasöründe olduğunu kontrol et |
| Port 8000 kullanımda | `serve --open --port 8001` çalıştır; adres 8001 olur |
| Paket indirme / sertifika hatası | Hata metnini paylaş; python.org kurulumu kullanılıyorsa resmî kılavuzdaki `Install Certificates.command` adımını kontrol et |
| `pull --ff-only` ilerleyemiyor | Yerel/uzak commit farkını incele; iki kişinin çalışmasını koruyarak birleştir |

Mac kurulum sonucu henüz bildirilmedi. Açıldıktan sonra Python sürümü, macOS sürümü ve başarılı/başarısız adımı kendi üye notunda paylaşabilirsin. Mevcut kontroller ve sınırlar [Mac hazırlık kaydında](../evidence/MACOS_SETUP.md).
