# BIM 322 - Solar Guc Uretim Tahmini

**Ogrenciler:** Busra Demir & Nazenin Tatar

---

## Proje Konusu

Hindistan'daki iki gunes enerjisi santralinden alinan sensor verileri kullanilarak anlik guc uretiminin yuksek mi dusuk mu oldugu tahmin edilmistir. Hedef degisken AC_POWER, train setinin ortalamasina gore binary sinifa donusturulmustur.

---

## Kullanilan Final Model

XGBoost Classifier

---

## Test Sonuclari

| Metrik | Deger |
|---|---:|
| Accuracy | 0.9742 |
| Precision | 0.9623 |
| Recall | 0.9851 |
| F1 | 0.9736 |

---

## Ozellikler

4 farkli ozellik secim yontemiyle (Korelasyon, SelectKBest, RFE, Mutual Information) secilen 3 ozellik:

- IRRADIATION
- MODULE_TEMPERATURE
- AMBIENT_TEMPERATURE

---

## Calistirma

```bash
pip install -r requirements.txt
streamlit run app.py
```

Uygulama: http://localhost:8501

---

## Veri Seti

Projede kullanilan veri seti Kaggle uzerinden alinmistir:

https://www.kaggle.com/datasets/anikannal/solar-power-generation-data

---

### Canli Uygulama Linki

Streamlit ile gelistirilen canli uygulamaya asagidaki baglantidan erisilebilir:

https://bim322-solar-power-prediction.streamlit.app/

---

## Dosya Yapisi

```text
BIM322_SolarGucTahmini/
|-- data/
|   |-- Plant_1_Generation_Data.csv
|   |-- Plant_1_Weather_Sensor_Data.csv
|   |-- Plant_2_Generation_Data.csv
|   `-- Plant_2_Weather_Sensor_Data.csv
|-- modeller/
|   |-- xgboost_model.pkl
|   |-- scaler.pkl
|   `-- selected_features.pkl
|-- notebooks/
|   `-- solar_guc_tahmini.ipynb
|-- sunum/
|   `-- BusraDemir_NazeninTatar_BIM322_Sunum.pptx
|-- .gitignore
|-- README.md
|-- app.py
`-- requirements.txt
```
