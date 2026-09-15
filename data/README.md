# Veri seti

Eğitim, IBM Telco Customer Churn örnek veri setini kullanır.

- [IBM kaynak dosyası](https://github.com/IBM/telco-customer-churn-on-icp4d/blob/master/data/Telco-Customer-Churn.csv)
- Beklenen dosya adı: `Telco-Customer-Churn.csv`
- Boyut: 7.043 satır, hedef dahil 21 sütun.
- Hedef: `Churn` (`No` / `Yes`). `customerID` eğitim özelliği olarak kullanılmaz.

CSV dosyasını bu klasöre koy. Proje kökünden PowerShell ile indirmek için:

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv" -OutFile "data/Telco-Customer-Churn.csv"
```

CSV, `.gitignore` ile depodan hariç tutulur; veri kaynağı ve kullanım koşulları IBM deposundadır. Veriyi yeniden dağıtmadan kaynaktan edinebilirsin.

`TotalCharges` içindeki sayıya çevrilemeyen değerler yüklenirken `NaN` olur. Medyanla doldurma ve ölçekleme, her eğitim katında pipeline tarafından öğrenilir.
