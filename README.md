# Telco Customer Churn

Müşterilerin ayrılıp ayrılmayacağını tahmin etmek için hazırladığım makine öğrenmesi öğrenme projesi. Logistic Regression, Decision Tree ve Random Forest modellerini karşılaştırıyorum; GridSearchCV ile parametrelerini seçip en iyi modeli test verisinde değerlendiriyorum.

## Projede neler var?

- Eğitim/test ayrımında sınıf oranlarını koruyan `stratify` kullanımı.
- Sayısal eksikleri medyanla doldurma ve StandardScaler ile ölçekleme.
- Kategorik özellikler için OneHotEncoder.
- Ön işleme ve sınıflandırıcıyı birleştiren Pipeline.
- Beş katlı çapraz doğrulama ve ROC-AUC ile model seçimi.
- Test ROC-AUC, sınıflandırma raporu ve confusion matrix.

## Kurulum

Komutları bu README'nin bulunduğu **depo kökünde** çalıştır.
Kontrol edilen ortam Python **3.13**; paket sürümleri `requirements.txt` içinde sabitlenmiştir.

Windows / PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS / Linux:

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Veri

[IBM Telco Customer Churn CSV dosyasını](https://github.com/IBM/telco-customer-churn-on-icp4d/blob/master/data/Telco-Customer-Churn.csv) indirip `data/Telco-Customer-Churn.csv` olarak kaydet.
PowerShell indirme komutu ve veri açıklaması için [data/README.md](data/README.md) dosyasına bak.

CSV güncel sürümde Git tarafından izlenmez. İlk committe yer aldığı için eski sürümlerde erişilebilir; depoyu yeni indiren kişi veriyi kaynağından ayrıca edinebilir.

## Çalıştırma

Windows / PowerShell:

```powershell
.\.venv\Scripts\python.exe src/main.py
```

macOS / Linux:

```bash
.venv/bin/python src/main.py
```

Program sırasıyla veriyi yükler, eğitim/test setlerini ayırır, üç modelin başlangıç skorlarını hesaplar, parametre araması yapar ve seçilen modelin test raporunu terminale yazdırır.

Tam parametre araması 58 kombinasyon × 5 kat = **290 eğitim** içerir. Başlangıç değerlendirmeleri ve en iyi ayarlarla yeniden eğitim de ek süre alır. `n_jobs=-1` kullanılabildiği kadar işlemciyi kullanır; tamamlanma süresi bilgisayara bağlıdır. İşlemi durdurmak için `Ctrl+C` kullanılabilir.

Model ve rapor şu an dosyaya kaydedilmez; sonuçlar terminalde gösterilir.

## Dosya yapısı

```text
telco-customer-churn/
├── src/
│   ├── main.py            # Ana çalıştırma akışı
│   ├── data.py            # Veriyi yükleme ve bölme
│   ├── preprocessing.py   # Ön işleme adımları
│   └── train.py           # Modeller, çapraz doğrulama ve tuning
├── data/
│   ├── README.md          # Veri kaynağı ve indirme bilgisi
│   └── Telco-Customer-Churn.csv  # Yerel; Git tarafından hariç tutulur
├── EDA.ipynb              # Keşifsel analiz ve öğrenme notları
├── requirements.txt
├── requirements-notebooks.txt
└── README.md
```

Çalıştırılacak güncel kod **`src/main.py`** dosyasıdır. `EDA.ipynb` keşif notları içerir; ana eğitim akışı bu notebook'u kullanmaz.

Notebook'ları açmak için isteğe bağlı kurulum:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-notebooks.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

Notebook'u depo kökünden aç. CSV okuyan hücre `data/Telco-Customer-Churn.csv` yolunu kullanır. Notebook, eğitim pipeline'ından bağımsız keşif notları içerir.

## Sonuçları nasıl okuyorum?

Önceki tam çalıştırmada elde edilen örnek sonuçlar:

| Model | Başlangıç CV ROC-AUC | Tuning sonrası CV ROC-AUC |
|---|---:|---:|
| Logistic Regression | 0.8461 | 0.8463 |
| Decision Tree | 0.6559 | 0.8297 |
| Random Forest | 0.8177 | 0.8465 |

O çalıştırmada Random Forest seçildi. Test ROC-AUC **0.8428**, ayrılan müşteri sınıfı için precision **0.53**, recall **0.78** oldu. Test confusion matrix'i:

```text
                    Tahmin: Kalıyor   Tahmin: Ayrılıyor
Gerçek: Kalıyor            773               262
Gerçek: Ayrılıyor           82               292
```

374 ayrılan müşterinin 292'si yakalandı; 262 müşteriye yanlış alarm verildi. ROC-AUC bir doğruluk yüzdesi değildir. Müşterilerin çoğu kalıyor olduğu için yalnızca accuracy kullanmak yanıltıcı olabilir. Random Forest ile Logistic Regression arasındaki CV farkı çok küçük; belirgin bir üstünlük olarak yorumlanmamalıdır.

Parametre seçimi eğitim verisinde yapılır; test seti aramaya verilmez. ROC-AUC'ye göre seçilen modelin standart karar eşiğindeki precision'ı en yüksek olmak zorunda değildir. Eşik optimizasyonu henüz uygulanmamıştır. Sonraki adım, eğitim verisinde doğrulama tahminleriyle precision–recall dengesini incelemektir; test seti tekrar tekrar ayar seçmek için kullanılmamalıdır.

Bu bir öğrenme projesidir; üretim ortamında doğrulanmış bir müşteri kaybı sistemi değildir.
