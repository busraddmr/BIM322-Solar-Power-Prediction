import pickle
import numpy as np
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Solar Güç Tahmini",
    page_icon="âš¡",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', 'Segoe UI', sans-serif; }

/* Arka plan */
.stApp {
    background: linear-gradient(145deg, #0a0f1e 0%, #0d1b2a 30%, #0f2240 60%, #1a1a2e 100%);
    min-height: 100vh;
}

/* YÄ±ldÄ±z efekti */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        radial-gradient(1px 1px at 10% 20%, rgba(255,220,100,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 80% 10%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 55% 75%, rgba(255,220,100,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 25% 85%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 55%, rgba(255,200,50,0.5) 0%, transparent 100%),
        radial-gradient(2px 2px at 45% 35%, rgba(255,220,100,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 90%, rgba(255,255,255,0.3) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}

/* Hero */
.hero-wrap {
    position: relative;
    border-radius: 24px;
    overflow: hidden;
    margin-bottom: 32px;
    padding: 2px;
    background: linear-gradient(135deg, #f59e0b, #10b981, #3b82f6, #f59e0b);
    background-size: 300% 300%;
    animation: borderGlow 6s ease infinite;
}
@keyframes borderGlow {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.hero-inner {
    background: linear-gradient(135deg, #0d1b2a 0%, #0f2240 50%, #1a1a2e 100%);
    border-radius: 22px;
    padding: 44px 36px 36px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero-inner::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 300px; height: 200px;
    background: radial-gradient(ellipse, rgba(245,158,11,0.18) 0%, transparent 70%);
    pointer-events: none;
}
.sun-icon {
    font-size: 3.4rem;
    display: block;
    margin-bottom: 12px;
    filter: drop-shadow(0 0 18px rgba(245,158,11,0.9));
    animation: pulse 3s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); filter: drop-shadow(0 0 18px rgba(245,158,11,0.9)); }
    50%       { transform: scale(1.08); filter: drop-shadow(0 0 28px rgba(245,158,11,1)); }
}
.hero-title {
    color: #fff;
    font-size: 2.2rem;
    font-weight: 900;
    margin: 0 0 8px;
    letter-spacing: -1px;
    text-shadow: 0 2px 24px rgba(245,158,11,0.4);
}
.hero-title span { color: #f59e0b; }
.hero-sub {
    color: rgba(255,255,255,0.55);
    font-size: 0.88rem;
    font-weight: 400;
    margin: 0;
    line-height: 1.7;
}
.hero-badge {
    display: inline-block;
    background: rgba(245,158,11,0.15);
    border: 1px solid rgba(245,158,11,0.4);
    color: #f59e0b;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 4px 14px;
    border-radius: 20px;
    margin-top: 14px;
    letter-spacing: 0.5px;
}

/* Stat chips */
.stat-row {
    display: flex;
    gap: 14px;
    margin-bottom: 28px;
}
.stat-chip {
    flex: 1;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 18px 16px;
    text-align: center;
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}
.stat-chip:hover {
    background: rgba(255,255,255,0.08);
    border-color: rgba(245,158,11,0.4);
    transform: translateY(-2px);
}
.stat-chip .icon { font-size: 1.5rem; margin-bottom: 6px; display: block; }
.stat-chip .val  { font-size: 1.5rem; font-weight: 800; color: #fff; line-height: 1; }
.stat-chip .unit { font-size: 0.7rem; color: rgba(255,255,255,0.45); font-weight: 500; margin-top: 2px; }
.stat-chip .lbl  { font-size: 0.72rem; color: rgba(255,255,255,0.5); margin-top: 6px; font-weight: 500; letter-spacing: 0.3px; }

/* Kart */
.glass-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 28px 28px 24px;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(245,158,11,0.5), transparent);
}
.glass-card-title {
    font-size: 0.82rem;
    font-weight: 700;
    color: rgba(255,255,255,0.5);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.glass-card-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.08);
}

/* Input etiketleri */
label, .stNumberInput label, [data-testid="stWidgetLabel"] {
    color: rgba(255,255,255,0.7) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    text-transform: uppercase !important;
}

/* Number input */
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    padding: 12px !important;
}
.stNumberInput > div > div > input:focus {
    border-color: rgba(245,158,11,0.6) !important;
    box-shadow: 0 0 0 3px rgba(245,158,11,0.12) !important;
}

/* Buton */
div.stButton > button {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 40%, #10b981 100%);
    background-size: 200% 200%;
    color: #fff;
    border: none;
    border-radius: 14px;
    font-size: 1rem;
    font-weight: 800;
    padding: 16px 0;
    width: 100%;
    cursor: pointer;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    transition: all 0.3s ease;
    box-shadow: 0 8px 32px rgba(245,158,11,0.35);
    position: relative;
    overflow: hidden;
}
div.stButton > button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent);
    opacity: 0;
    transition: opacity 0.3s;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(245,158,11,0.5);
}
div.stButton > button:hover::before { opacity: 1; }
div.stButton > button:active { transform: translateY(0); }

/* SonuÃ§ kutularÄ± */
.result-card {
    border-radius: 20px;
    padding: 32px 28px;
    text-align: center;
    margin: 20px 0;
    position: relative;
    overflow: hidden;
}
.result-high {
    background: linear-gradient(135deg, rgba(16,185,129,0.15) 0%, rgba(5,150,105,0.1) 100%);
    border: 1.5px solid rgba(16,185,129,0.5);
}
.result-high::before {
    content: '';
    position: absolute;
    top: -50%; left: 50%;
    transform: translateX(-50%);
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(16,185,129,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.result-low {
    background: linear-gradient(135deg, rgba(245,158,11,0.15) 0%, rgba(217,119,6,0.1) 100%);
    border: 1.5px solid rgba(245,158,11,0.5);
}
.result-low::before {
    content: '';
    position: absolute;
    top: -50%; left: 50%;
    transform: translateX(-50%);
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(245,158,11,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.result-icon { font-size: 2.8rem; margin-bottom: 10px; display: block; }
.result-title-high { color: #34d399; font-size: 1.5rem; font-weight: 900; letter-spacing: -0.5px; margin: 0 0 6px; }
.result-title-low  { color: #fbbf24; font-size: 1.5rem; font-weight: 900; letter-spacing: -0.5px; margin: 0 0 6px; }
.result-desc { color: rgba(255,255,255,0.55); font-size: 0.88rem; margin: 0; line-height: 1.5; }

/* OlasÄ±lÄ±k */
.prob-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin: 20px 0 8px;
}
.prob-box {
    border-radius: 16px;
    padding: 22px 16px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.prob-box-high {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
}
.prob-box-low {
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.3);
}
.prob-val-high { font-size: 2.4rem; font-weight: 900; color: #34d399; line-height: 1; }
.prob-val-low  { font-size: 2.4rem; font-weight: 900; color: #fbbf24; line-height: 1; }
.prob-lbl { font-size: 0.72rem; color: rgba(255,255,255,0.5); font-weight: 600; margin-top: 6px; letter-spacing: 0.5px; text-transform: uppercase; }

/* Progress bar */
.bar-wrap { margin: 8px 0 4px; }
.bar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.bar-title { font-size: 0.75rem; color: rgba(255,255,255,0.45); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.bar-pct   { font-size: 0.8rem; font-weight: 700; color: #34d399; }
.bar-track {
    background: rgba(255,255,255,0.07);
    border-radius: 99px;
    height: 8px;
    overflow: hidden;
}
.bar-fill-high {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #10b981, #34d399);
    box-shadow: 0 0 12px rgba(16,185,129,0.5);
    transition: width 0.8s ease;
}
.bar-fill-low {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #d97706, #fbbf24);
    box-shadow: 0 0 12px rgba(245,158,11,0.5);
    transition: width 0.8s ease;
}

/* Tablo */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stDataFrame"] * { color: #fff !important; }
.stDataFrame thead tr th {
    background: rgba(255,255,255,0.08) !important;
    color: #fff !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
}
.stDataFrame tbody tr td { color: #fff !important; }
[data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th { color: #fff !important; }

/* Expander */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 12px !important;
    color: rgba(255,255,255,0.65) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.02) !important;
    border-radius: 0 0 12px 12px !important;
}

/* Streamlit alert kutularÄ±nÄ± gizle */
.stAlert { display: none; }

/* Footer */
.footer-wrap {
    margin-top: 36px;
    padding: 20px 0 12px;
    border-top: 1px solid rgba(255,255,255,0.07);
    text-align: center;
}
.footer-pills { display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }
.footer-pill {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.7rem;
    color: rgba(255,255,255,0.45);
    font-weight: 500;
}
.footer-pill strong { color: rgba(255,255,255,0.7); }
.footer-copy { font-size: 0.68rem; color: rgba(255,255,255,0.2); }

/* Kolon boÅŸluklarÄ± */
[data-testid="column"] { padding: 0 6px !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(245,158,11,0.3); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)


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

st.markdown("""
<div class="hero-wrap">
  <div class="hero-inner">
    <span class="sun-icon">â˜€ï¸</span>
    <h1 class="hero-title">Solar <span>GÃ¼Ã§ Ãœretim</span> Tahmini</h1>
    <p class="hero-sub">
      BIM 322 â€“ Makine Ã–ÄŸrenmesi ve UygulamalarÄ±<br>
      Busra Demir &amp; Nazenin Tatar
    </p>
    <span class="hero-badge">âš¡ XGBoost Â· Accuracy 97.42%</span>
  </div>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="glass-card">
  <div class="glass-card-title">ğŸ”† SensÃ¶r DeÄŸerleri</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    irradiation = st.number_input(
        "Irradiation (W/mÂ²)",
        min_value=0.0, max_value=1.5,
        value=0.5, step=0.01,
        help="GÃ¼neÅŸ Ä±ÅŸÄ±nÄ±mÄ± yoÄŸunluÄŸu â€” tipik aralÄ±k: 0 â€“ 1.22"
    )

with col2:
    module_temp = st.number_input(
        "ModÃ¼l SÄ±caklÄ±ÄŸÄ± (Â°C)",
        min_value=0.0, max_value=80.0,
        value=35.0, step=0.5,
        help="Panel yÃ¼zey sÄ±caklÄ±ÄŸÄ±"
    )

with col3:
    ambient_temp = st.number_input(
        "Ortam SÄ±caklÄ±ÄŸÄ± (Â°C)",
        min_value=0.0, max_value=50.0,
        value=28.0, step=0.5,
        help="Ã‡evre hava sÄ±caklÄ±ÄŸÄ±"
    )


st.markdown(f"""
<div class="stat-row">
  <div class="stat-chip">
    <span class="icon">â˜€ï¸</span>
    <div class="val">{irradiation:.2f}</div>
    <div class="unit">W/mÂ²</div>
    <div class="lbl">IÅŸÄ±nÄ±m</div>
  </div>
  <div class="stat-chip">
    <span class="icon">ğŸŒ¡ï¸</span>
    <div class="val">{module_temp:.1f}</div>
    <div class="unit">Â°C</div>
    <div class="lbl">ModÃ¼l SÄ±caklÄ±ÄŸÄ±</div>
  </div>
  <div class="stat-chip">
    <span class="icon">ğŸŒ¤ï¸</span>
    <div class="val">{ambient_temp:.1f}</div>
    <div class="unit">Â°C</div>
    <div class="lbl">Ortam SÄ±caklÄ±ÄŸÄ±</div>
  </div>
</div>
""", unsafe_allow_html=True)


predict_clicked = st.button("âš¡  Tahmini Hesapla", use_container_width=True)


if predict_clicked:
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

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="glass-card-title">ğŸ“Š Tahmin Sonucu</div>', unsafe_allow_html=True)

    # SonuÃ§ kutusu
    if pred == 1:
        st.markdown(f"""
        <div class="result-card result-high">
          <span class="result-icon">âœ…</span>
          <div class="result-title-high">YÃœKSEK GÃœÃ‡ ÃœRETÄ°MÄ°</div>
          <p class="result-desc">Santral verimli Ã§alÄ±ÅŸÄ±yor â€” Ã¼retim eÅŸiÄŸinin Ã¼zerinde.</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-card result-low">
          <span class="result-icon">âš ï¸</span>
          <div class="result-title-low">DÃœÅÃœK GÃœÃ‡ ÃœRETÄ°MÄ°</div>
          <p class="result-desc">Ãœretim eÅŸiÄŸinin altÄ±nda â€” koÅŸullar yetersiz.</p>
        </div>""", unsafe_allow_html=True)

    # OlasÄ±lÄ±k kutularÄ±
    st.markdown(f"""
    <div class="prob-grid">
      <div class="prob-box prob-box-high">
        <div class="prob-val-high">{p_high*100:.1f}%</div>
        <div class="prob-lbl">YÃ¼ksek GÃ¼Ã§ OlasÄ±lÄ±ÄŸÄ±</div>
      </div>
      <div class="prob-box prob-box-low">
        <div class="prob-val-low">{p_low*100:.1f}%</div>
        <div class="prob-lbl">DÃ¼ÅŸÃ¼k GÃ¼Ã§ OlasÄ±lÄ±ÄŸÄ±</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # GÃ¼ven Ã§ubuklarÄ±
    st.markdown(f"""
    <div class="bar-wrap">
      <div class="bar-header">
        <span class="bar-title">YÃ¼ksek GÃ¼Ã§ GÃ¼veni</span>
        <span class="bar-pct">{p_high*100:.1f}%</span>
      </div>
      <div class="bar-track">
        <div class="bar-fill-high" style="width:{p_high*100:.1f}%"></div>
      </div>
    </div>
    <div class="bar-wrap" style="margin-top:12px">
      <div class="bar-header">
        <span class="bar-title">DÃ¼ÅŸÃ¼k GÃ¼Ã§ GÃ¼veni</span>
        <span class="bar-pct" style="color:#fbbf24">{p_low*100:.1f}%</span>
      </div>
      <div class="bar-track">
        <div class="bar-fill-low" style="width:{p_low*100:.1f}%"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("ğŸ“‹ GiriÅŸ DeÄŸerleri Ã–zeti"):
        df_show = pd.DataFrame({
            "Ã–zellik": selected_features,
            "Ham DeÄŸer": [irradiation, module_temp, ambient_temp],
            "Ã–lÃ§ekli DeÄŸer": X_input[0].round(4),
        })
        st.dataframe(df_show, use_container_width=True, hide_index=True)

st.markdown("""
<div class="footer-wrap">
  <div class="footer-pills">
    <div class="footer-pill">Model: <strong>XGBoost</strong></div>
    <div class="footer-pill">Accuracy: <strong>97.42%</strong></div>
    <div class="footer-pill">F1 Score: <strong>97.36%</strong></div>
    <div class="footer-pill">EÅŸik: <strong>544.71 W</strong></div>
    <div class="footer-pill">Veri: <strong>Kaggle Solar Dataset</strong></div>
  </div>
  <div class="footer-copy">BIM 322 â€“ Busra Demir &amp; Nazenin Tatar Â· 2026</div>
</div>
""", unsafe_allow_html=True)

