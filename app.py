import pickle
import numpy as np
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Solar Guc Tahmini",
    page_icon="☀️",
    layout="centered",
)

# --- CSS (sadece stil, Turkce karakter yok) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
* { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(160deg, #0a0f1e 0%, #0d1b2a 50%, #1a1a2e 100%);
}

div.stButton > button {
    background: linear-gradient(135deg, #f59e0b, #10b981);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    font-size: 1rem;
    padding: 14px;
    width: 100%;
    letter-spacing: 1px;
    transition: all 0.3s;
    box-shadow: 0 6px 24px rgba(245,158,11,0.3);
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 32px rgba(245,158,11,0.5);
}

.metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    margin: 8px 0;
}
.metric-val { font-size: 1.6rem; font-weight: 900; color: #f59e0b; white-space: nowrap; }
.metric-lbl { font-size: 0.75rem; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }

.result-high {
    background: rgba(16,185,129,0.12);
    border: 1.5px solid rgba(16,185,129,0.5);
    border-radius: 16px;
    padding: 28px;
    text-align: center;
}
.result-low {
    background: rgba(245,158,11,0.12);
    border: 1.5px solid rgba(245,158,11,0.5);
    border-radius: 16px;
    padding: 28px;
    text-align: center;
}
.result-title-high { color: #34d399; font-size: 1.6rem; font-weight: 900; margin: 0; }
.result-title-low  { color: #fbbf24; font-size: 1.6rem; font-weight: 900; margin: 0; }
.result-sub { color: rgba(255,255,255,0.55); font-size: 0.9rem; margin-top: 8px; }

[data-testid="stMetricValue"] { color: #f59e0b !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] { color: rgba(255,255,255,0.6) !important; }

.section-title {
    font-size: 0.78rem;
    font-weight: 700;
    color: rgba(255,255,255,0.4);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 16px;
}

input[type=number] {
    background: #111827 !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}
[data-testid="stNumberInput"] input {
    background: #111827 !important;
    color: #ffffff !important;
}
label { color: rgba(255,255,255,0.85) !important; font-weight: 600 !important; }
[data-testid="stWidgetLabel"] p { color: rgba(255,255,255,0.85) !important; }

/* Expander arkaplan ve yazi rengi */
[data-testid="stExpander"] { background-color: #ffffff !important; border-radius: 10px !important; }
.streamlit-expanderHeader { background-color: #ffffff !important; color: #000000 !important; border-radius: 10px !important; }
.streamlit-expanderHeader p { color: #000000 !important; font-weight: 700 !important; }
[data-testid="stExpander"] * { color: #000000 !important; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_artifacts():
    with open("modeller/xgboost_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("modeller/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("modeller/selected_features.pkl", "rb") as f:
        features = pickle.load(f)
    return model, scaler, features

model, scaler, selected_features = load_artifacts()

# --- Baslik ---
st.markdown('<h1 style="color:#e2e8f0; font-weight:900;">☀️ Solar Güç Üretim Tahmini</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#ffffff; font-size:1.1rem;"><b>BIM 322 – Makine Öğrenmesi</b> &nbsp;|&nbsp; Büşra Demir & Nazenin Tatar</p>', unsafe_allow_html=True)
st.divider()

# --- Model bilgi kartlari ---
col1, col2, col3, col4 = st.columns(4)
col1.markdown('<div class="metric-card"><div class="metric-val">97.42%</div><div class="metric-lbl">Accuracy</div></div>', unsafe_allow_html=True)
col2.markdown('<div class="metric-card"><div class="metric-val">97.36%</div><div class="metric-lbl">F1 Score</div></div>', unsafe_allow_html=True)
col3.markdown('<div class="metric-card"><div class="metric-val">98.51%</div><div class="metric-lbl">Recall</div></div>', unsafe_allow_html=True)
col4.markdown('<div class="metric-card"><div class="metric-val">XGBoost</div><div class="metric-lbl">Model</div></div>', unsafe_allow_html=True)

st.divider()

# --- Girdi ---
st.markdown('<div class="section-title">🔆 Sensor Degerleri</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    irradiation = st.number_input("Irradiation (W/m²)", min_value=0.0, max_value=1.5, value=0.5, step=0.01)
with c2:
    module_temp = st.number_input("Modül Sıcaklığı (°C)", min_value=0.0, max_value=80.0, value=35.0, step=0.5)
with c3:
    ambient_temp = st.number_input("Ortam Sıcaklığı (°C)", min_value=0.0, max_value=50.0, value=28.0, step=0.5)

st.markdown("")
predict_clicked = st.button("⚡  TAHMİNİ HESAPLA", use_container_width=True)

# --- Tahmin ---
if predict_clicked:
    feature_order_full = ["DAILY_YIELD", "TOTAL_YIELD", "AMBIENT_TEMPERATURE", "MODULE_TEMPERATURE", "IRRADIATION"]
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
    st.markdown('<div class="section-title">📊 Tahmin Sonucu</div>', unsafe_allow_html=True)

    if pred == 1:
        st.markdown(f"""
        <div class="result-high">
          <div class="result-title-high">✅ &nbsp;YÜKSEK GÜÇ ÜRETİMİ</div>
          <div class="result-sub">Santral verimli çalışıyor — üretim eşiğinin üzerinde</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-low">
          <div class="result-title-low">⚠️ &nbsp;DÜŞÜK GÜÇ ÜRETİMİ</div>
          <div class="result-sub">Üretim eşiğinin altında — koşullar yetersiz</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    m1, m2 = st.columns(2)
    m1.metric("Yüksek Üretim Olasılığı", f"{p_high*100:.1f}%")
    m2.metric("Düşük Üretim Olasılığı",  f"{p_low*100:.1f}%")

    st.markdown('<p style="color:white; font-weight:600; margin-bottom: 2px;">Yüksek Üretim Güveni</p>', unsafe_allow_html=True)
    st.progress(float(p_high))
    st.markdown('<p style="color:white; font-weight:600; margin-bottom: 2px; margin-top: 10px;">Düşük Üretim Güveni</p>', unsafe_allow_html=True)
    st.progress(float(p_low))

    with st.expander("📋 Giriş Değerleri Özeti"):
        df_show = pd.DataFrame({
            "Özellik": selected_features,
            "Ham Değer": [irradiation, module_temp, ambient_temp],
            "Ölçekli Değer": X_input[0].round(4),
        })
        st.dataframe(df_show, use_container_width=True, hide_index=True)

st.divider()
st.markdown('<p style="color:white; font-size: 0.8rem;">Model: XGBoost | Accuracy: 97.42% | Eşik: 544.71 W | Veri: Kaggle Solar Dataset</p>', unsafe_allow_html=True)
