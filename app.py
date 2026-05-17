import pickle
import numpy as np
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Solar Guc Tahmini",
    page_icon="☀️",
    layout="centered",
)

@st.cache_resource
def load_artifacts():
    with open("models/xgboost_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("models/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("models/selected_features.pkl", "rb") as f:
        features = pickle.load(f)
    return model, scaler, features

model, scaler, selected_features = load_artifacts()

# --- Baslik ---
st.title("☀️ Solar Güç Üretim Tahmini")
st.caption("BIM 322 – Makine Öğrenmesi | Büşra Demir & Nazenin Tatar")
st.divider()

st.subheader("Sensör Değerlerini Girin")

col1, col2, col3 = st.columns(3)

with col1:
    irradiation = st.number_input(
        "Irradiation (W/m²)",
        min_value=0.0, max_value=1.5,
        value=0.5, step=0.01,
    )

with col2:
    module_temp = st.number_input(
        "Modül Sıcaklığı (°C)",
        min_value=0.0, max_value=80.0,
        value=35.0, step=0.5,
    )

with col3:
    ambient_temp = st.number_input(
        "Ortam Sıcaklığı (°C)",
        min_value=0.0, max_value=50.0,
        value=28.0, step=0.5,
    )

st.divider()

if st.button("⚡ Tahmin Et", use_container_width=True, type="primary"):
    feature_order_full = [
        "DAILY_YIELD", "TOTAL_YIELD",
        "AMBIENT_TEMPERATURE", "MODULE_TEMPERATURE", "IRRADIATION"
    ]
    idx_map = {f: i for i, f in enumerate(feature_order_full)}
    dummy = np.zeros((1, 5))
    dummy[0, idx_map["IRRADIATION"]]         = irradiation
    dummy[0, idx_map["MODULE_TEMPERATURE"]]  = module_temp
    dummy[0, idx_map["AMBIENT_TEMPERATURE"]] = ambient_temp

    scaled_full = scaler.transform(dummy)
    sel_idx     = [idx_map[f] for f in selected_features]
    X_input     = scaled_full[:, sel_idx]

    pred       = model.predict(X_input)[0]
    pred_proba = model.predict_proba(X_input)[0]
    p_high     = pred_proba[1]
    p_low      = pred_proba[0]

    st.divider()

    if pred == 1:
        st.success(f"✅ YÜKSEK GÜÇ ÜRETİMİ  — Olasılık: {p_high*100:.1f}%")
    else:
        st.warning(f"⚠️ DÜŞÜK GÜÇ ÜRETİMİ  — Olasılık: {p_low*100:.1f}%")

    col_a, col_b = st.columns(2)
    col_a.metric("Yüksek Üretim Olasılığı", f"{p_high*100:.1f}%")
    col_b.metric("Düşük Üretim Olasılığı",  f"{p_low*100:.1f}%")

    with st.expander("Giriş Özeti"):
        df_show = pd.DataFrame({
            "Özellik": selected_features,
            "Ham Değer": [irradiation, module_temp, ambient_temp],
            "Ölçekli Değer": X_input[0].round(4),
        })
        st.dataframe(df_show, use_container_width=True, hide_index=True)

st.divider()
st.caption("Model: XGBoost | Accuracy: 97.42% | F1: 97.36% | Eşik: 544.71 W")
