# BIM 322 - Solar Güç Üretim Tahmini

**Öğrenciler:** Busra Demir & Nazenin Tatar  
**Veri Seti:** Solar Power Generation Dataset (Kaggle)  
**Teslim Tarihi:** 17 Mayıs 2026, saat 00:00  
**Sunum Tarihleri:** 18 ve 20 Mayıs 2026 (ders saatlerinde)  
**Hedef:** AC_POWER → Binary Sınıflandırma (HIGH_POWER: 0/1)

---

## Proje Özeti

Hindistan'daki iki güneş enerji santralinden alınan sensör verileriyle XGBoost modeli eğitildi. Girilen anlık ışınım, modül sıcaklığı ve ortam sıcaklığı değerlerine göre santralin o an yüksek mi yoksa düşük mü güç ürettiği tahmin ediliyor. Model Streamlit arayüzü üzerinden kullanılabiliyor.

---

## Dosya Yapısı

```
BIM322_SolarGucTahmini/
├── BusraDemir_NazeninTatar_BIM322_SolarGucTahmini.ipynb
├── BusraDemir_NazeninTatar_BIM322_Sunum.pptx
├── app.py
├── xgboost_model.pkl
├── scaler.pkl
├── selected_features.pkl
├── Plant_1_Generation_Data.csv
├── Plant_1_Weather_Sensor_Data.csv
├── Plant_2_Generation_Data.csv
└── Plant_2_Weather_Sensor_Data.csv
```

---

## Görev Durumları

**Görev 1 – Veri Ön İşleme (10 puan)** ✅  
- Gece satırları filtrelendi (AC_POWER > 0): 136.472 → 68.859 satır  
- IQR ile aykırı değer temizliği uygulandı  
- Train/Val/Test ayrımı: %64 / %16 / %20 (random_state=42)  
- Binary hedef: eşik = train setinin AC_POWER ortalaması = 544.71  
- Sınıf dağılımı: ~%51 Düşük / ~%49 Yüksek

**Görev 2 – Özellik Seçimi (25 puan)** ✅  
- MinMaxScaler yalnızca train verisine fit edildi  
- 4 yöntem kullanıldı: Korelasyon, SelectKBest, RFE, Mutual Information  
- Seçilen 3 özellik (4 yöntemin kesişimi): `IRRADIATION`, `MODULE_TEMPERATURE`, `AMBIENT_TEMPERATURE`

**Görev 3 – Modelleme (25 puan)** ✅  
5 model eğitildi, her biri için confusion matrix çizildi:

| Model | Val Accuracy |
|---|---|
| XGBoost | 0.9740 |
| Random Forest | 0.9734 |
| KNN | 0.9719 |
| Logistic Regression | 0.9499 |
| Naive Bayes | 0.9122 |

**Görev 4 – Model Değerlendirme (30 puan)** ✅  
En iyi model XGBoost — test seti sonuçları:

| Metrik | Train | Val | Test |
|---|---|---|---|
| Accuracy | 0.9758 | 0.9740 | 0.9742 |
| Precision | 0.9650 | 0.9639 | 0.9623 |
| Recall | 0.9862 | 0.9836 | 0.9851 |
| F1 | 0.9755 | 0.9737 | 0.9736 |

- ROC ve Precision-Recall eğrileri her model için Train vs Validation olarak çizildi  
- SHAP (TreeExplainer) ile kara kutu açıklanabilirlik eklendi  
- Streamlit deploy: `streamlit run app.py` → http://localhost:8501

**Görev 5 – Rapor ve Sunum (10 puan)** ⏳  
- PPT hazırlanacak  
- Sunum 18 veya 20 Mayıs'ta yapılacak

---

## Teknik Notlar

**Özellikler:**

| Özellik | Birim | Açıklama |
|---|---|---|
| IRRADIATION | W/m² | Güneş ışınımı yoğunluğu (en etkili) |
| MODULE_TEMPERATURE | °C | Panel yüzey sıcaklığı |
| AMBIENT_TEMPERATURE | °C | Ortam hava sıcaklığı |
| DAILY_YIELD | kWh | Günlük toplam üretim — elendi |
| TOTAL_YIELD | kWh | Kümülatif toplam üretim — elendi |

**Data Leakage önlemleri:**
- Scaler yalnızca train verisine fit edildi
- Binary eşik yalnızca train setinin ortalamasından hesaplandı
- DC_POWER özellik setine dahil edilmedi (target leakage riski)

**SHAP sonuçları (ortalama mutlak etki):**
- IRRADIATION: 6.19
- MODULE_TEMPERATURE: 1.06
- AMBIENT_TEMPERATURE: 0.55

---

## Teslim Öncesi Kontrol

- [x] Veri seti seçim gerekçesi yazıldı
- [x] Aykırı değer temizliği (IQR)
- [x] Normalizasyon (MinMaxScaler)
- [x] 4 özellik seçimi yöntemi
- [x] 5 ML algoritması
- [x] Train/Val/Test ayrımı
- [x] Confusion matrix
- [x] Accuracy/Precision/Recall/F1 tablosu
- [x] ROC analizi (Train + Validation)
- [x] Precision-Recall analizi (Train + Validation)
- [x] Streamlit deploy
- [x] SHAP açıklanabilirlik
- [x] pkl dosyaları kaydedildi
- [ ] PPT hazırlanacak
- [ ] Sunum (18 veya 20 Mayıs)
- [ ] Kampüs + OYS + GitHub'a yükleme
