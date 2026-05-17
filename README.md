# BIM 322 - Solar Güç Üretim Tahmini


**Öğrenciler:** Büşra Demir & Nazenin Tatar

---

## Proje Konusu

Hindistan'daki iki güneş enerjisi santralinden alınan sensör verileri kullanılarak anlık güç üretiminin yüksek mi düşük mü olduğu tahmin edilmiştir. Hedef değişken AC_POWER, train setinin ortalamasına göre binary sınıfa dönüştürülmüştür.

---

## Kullanılan Final Model

XGBoost Classifier

---

## Test Sonuçları

| Metrik | Değer |
|---|---|
| Accuracy | 0.9742 |
| Precision | 0.9623 |
| Recall | 0.9851 |
| F1 | 0.9736 |

---

## Özellikler

4 farklı özellik seçim yöntemiyle (Korelasyon, SelectKBest, RFE, Mutual Information) seçilen 3 özellik:

- IRRADIATION
- MODULE_TEMPERATURE
- AMBIENT_TEMPERATURE

---

## Çalıştırma

```bash
pip install -r requirements.txt
streamlit run app.py
```

Uygulama: http://localhost:8501

### Canlı Uygulama Linki
Streamlit ile geliştirilen canlı uygulamaya aşağıdaki bağlantıdan erişilebilir:
(https://bim322-solar-power-prediction.streamlit.app/)

---

## Dosya Yapısı

```
BIM322_SolarGucTahmini/
├── data/
│   ├── Plant_1_Generation_Data.csv
│   ├── Plant_1_Weather_Sensor_Data.csv
│   ├── Plant_2_Generation_Data.csv
│   └── Plant_2_Weather_Sensor_Data.csv
├── models/
│   ├── xgboost_model.pkl
│   ├── scaler.pkl
│   └── selected_features.pkl
├── solar_guc_tahmini.ipynb
├── BusraDemir_NazeninTatar_BIM322_Sunum.pptx
├── app.py
├── requirements.txt
└── README.md
```
