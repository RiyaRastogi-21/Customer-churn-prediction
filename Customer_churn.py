import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChurnSense | Retention Intelligence",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Theme State ────────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

ALL_THEMES = ["☀️ Light", "🌙 Dark", "🔮 Indigo", "🌿 Emerald", "🌹 Rose", "🌅 Sunset", "🌊 Midnight Blue"]
THEME_KEY  = {t: t.split(" ", 1)[1] for t in ALL_THEMES}  # strip emoji for dict key

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")

    theme_choice_display = st.selectbox(
        "🎨 Interface Theme",
        ALL_THEMES,
        index=[THEME_KEY[t] for t in ALL_THEMES].index(st.session_state.theme),
        help="Choose a color scheme for the entire dashboard"
    )
    st.session_state.theme = THEME_KEY[theme_choice_display]

    # Theme colour preview swatch
    swatch_colors = {
        "Light":         ["#6366f1", "#10b981", "#f59e0b", "#ef4444", "#f0f2f5"],
        "Dark":          ["#818cf8", "#34d399", "#fbbf24", "#f87171", "#0f1117"],
        "Indigo":        ["#a5b4fc", "#6ee7b7", "#fcd34d", "#fca5a5", "#1e1b4b"],
        "Emerald":       ["#10b981", "#059669", "#34d399", "#6ee7b7", "#022c22"],
        "Rose":          ["#f43f5e", "#e11d48", "#fb7185", "#fda4af", "#1a0a10"],
        "Sunset":        ["#f97316", "#ea580c", "#fb923c", "#fdba74", "#1c0f05"],
        "Midnight Blue": ["#3b82f6", "#2563eb", "#60a5fa", "#93c5fd", "#0c1929"],
    }
    sw = swatch_colors.get(st.session_state.theme, swatch_colors["Light"])
    st.markdown(f"""
    <div style="display:flex;gap:4px;margin:8px 0 14px 0">
        <div style="width:28px;height:14px;border-radius:4px;background:{sw[0]}"></div>
        <div style="width:28px;height:14px;border-radius:4px;background:{sw[1]}"></div>
        <div style="width:28px;height:14px;border-radius:4px;background:{sw[2]}"></div>
        <div style="width:28px;height:14px;border-radius:4px;background:{sw[3]}"></div>
        <div style="width:28px;height:14px;border-radius:4px;background:{sw[4]};border:1px solid #aaa"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🗂️ Navigation")
    step_option = st.selectbox("Select Section", ["Overview", "Customer Profile", "Risk Analysis", "Retention Playbook", "Business Impact"], index=0)

    st.markdown("---")
    st.markdown("### 📊 Data Summary")
    with st.expander("View Dataset Statistics", expanded=False):
        st.markdown("""
- **Total Records:** 7,043 customers
- **Churn Rate:** 26.5% (actual)
- **Avg. Tenure:** 32.4 months
- **Avg. Monthly Charge:** $64.76
- **Avg. Total Charges:** $2,283
- **Contract Split:**
  - Month-to-month: 55%
  - One year: 21%
  - Two year: 24%
- **Internet Split:**
  - Fiber Optic: 44%
  - DSL: 34%
  - No Internet: 22%
""")

    st.markdown("---")
    st.markdown("### 📘 About")
    st.markdown("""
**ChurnSense v2.0**  
Retention Intelligence Platform  

- **Model:** Random Forest  
- **Features:** 19 customer attributes  
- **Dataset:** Telco Customer Churn  
- **Accuracy:** ~80% on held-out test set  

---
**Risk Thresholds**  
🟢 Low Risk: < 30%  
🟡 Moderate Risk: 30–60%  
🔴 High Risk: > 60%  

---
Developed by **Riya Rastogi**  
© 2026 All rights reserved.
""")

# ── Theme Variables ────────────────────────────────────────────────────────────
T = st.session_state.theme

if T == "Dark":
    BG          = "#0f1117"
    SURFACE     = "#1a1f2e"
    SURFACE2    = "#242938"
    BORDER      = "rgba(255,255,255,0.07)"
    TEXT_PRIMARY= "#f1f5f9"
    TEXT_SEC    = "#94a3b8"
    TEXT_MUTED  = "#64748b"
    NAV_BG      = "#0d1017"
    PANEL_SHADOW= "0 1px 6px rgba(0,0,0,0.4)"
    KPI_BG      = "#1a1f2e"
    KPI_VAL_CLR = "#f1f5f9"
    LABEL_CLR   = "#c7d2fe"
    PANEL_TITLE = "#e0e7ff"
    MINI_BG     = "#242938"
    FOOTER_BORDER="#2d3748"
    FOOTER_CLR  = "#64748b"
    GAUGE_TRACK = "#2d3748"
    IMPACT_TRACK= "#2d3748"
    VERDICT_BG  = "#242938"
    REC_BG      = "#1e2535"
    REC_URGENT_BG="#2d1a1a"
    REC_WARN_BG ="#2d2510"
    REC_BORDER  = "rgba(255,255,255,0.06)"
    INPUT_CLR   = "#c7d2fe"
elif T == "Indigo":
    BG          = "#1e1b4b"
    SURFACE     = "#312e81"
    SURFACE2    = "#3730a3"
    BORDER      = "rgba(199,210,254,0.15)"
    TEXT_PRIMARY= "#eef2ff"
    TEXT_SEC    = "#a5b4fc"
    TEXT_MUTED  = "#818cf8"
    NAV_BG      = "#13103d"
    PANEL_SHADOW= "0 2px 10px rgba(0,0,0,0.4)"
    KPI_BG      = "#312e81"
    KPI_VAL_CLR = "#eef2ff"
    LABEL_CLR   = "#c7d2fe"
    PANEL_TITLE = "#e0e7ff"
    MINI_BG     = "#3730a3"
    FOOTER_BORDER="rgba(199,210,254,0.15)"
    FOOTER_CLR  = "#818cf8"
    GAUGE_TRACK = "#3730a3"
    IMPACT_TRACK= "#3730a3"
    VERDICT_BG  = "#3730a3"
    REC_BG      = "#312e81"
    REC_URGENT_BG="#4c1d1d"
    REC_WARN_BG ="#44370f"
    REC_BORDER  = "rgba(199,210,254,0.12)"
    INPUT_CLR   = "#c7d2fe"
elif T == "Emerald":
    BG          = "#022c22"
    SURFACE     = "#064e3b"
    SURFACE2    = "#065f46"
    BORDER      = "rgba(110,231,183,0.15)"
    TEXT_PRIMARY= "#ecfdf5"
    TEXT_SEC    = "#6ee7b7"
    TEXT_MUTED  = "#34d399"
    NAV_BG      = "#012018"
    PANEL_SHADOW= "0 2px 10px rgba(0,0,0,0.45)"
    KPI_BG      = "#064e3b"
    KPI_VAL_CLR = "#ecfdf5"
    LABEL_CLR   = "#6ee7b7"
    PANEL_TITLE = "#d1fae5"
    MINI_BG     = "#065f46"
    FOOTER_BORDER="rgba(110,231,183,0.15)"
    FOOTER_CLR  = "#34d399"
    GAUGE_TRACK = "#065f46"
    IMPACT_TRACK= "#065f46"
    VERDICT_BG  = "#065f46"
    REC_BG      = "#064e3b"
    REC_URGENT_BG="#4c1d1d"
    REC_WARN_BG ="#44370f"
    REC_BORDER  = "rgba(110,231,183,0.12)"
    INPUT_CLR   = "#a7f3d0"
elif T == "Rose":
    BG          = "#1a0a10"
    SURFACE     = "#2d1320"
    SURFACE2    = "#3d1a2e"
    BORDER      = "rgba(251,113,133,0.15)"
    TEXT_PRIMARY= "#fff1f2"
    TEXT_SEC    = "#fda4af"
    TEXT_MUTED  = "#fb7185"
    NAV_BG      = "#14080c"
    PANEL_SHADOW= "0 2px 10px rgba(0,0,0,0.45)"
    KPI_BG      = "#2d1320"
    KPI_VAL_CLR = "#fff1f2"
    LABEL_CLR   = "#fda4af"
    PANEL_TITLE = "#ffe4e6"
    MINI_BG     = "#3d1a2e"
    FOOTER_BORDER="rgba(251,113,133,0.15)"
    FOOTER_CLR  = "#fb7185"
    GAUGE_TRACK = "#3d1a2e"
    IMPACT_TRACK= "#3d1a2e"
    VERDICT_BG  = "#3d1a2e"
    REC_BG      = "#2d1320"
    REC_URGENT_BG="#4c1d1d"
    REC_WARN_BG ="#44370f"
    REC_BORDER  = "rgba(251,113,133,0.12)"
    INPUT_CLR   = "#fecdd3"
elif T == "Sunset":
    BG          = "#1c0f05"
    SURFACE     = "#341d0e"
    SURFACE2    = "#44280f"
    BORDER      = "rgba(251,146,60,0.15)"
    TEXT_PRIMARY= "#fff7ed"
    TEXT_SEC    = "#fdba74"
    TEXT_MUTED  = "#fb923c"
    NAV_BG      = "#150b03"
    PANEL_SHADOW= "0 2px 10px rgba(0,0,0,0.45)"
    KPI_BG      = "#341d0e"
    KPI_VAL_CLR = "#fff7ed"
    LABEL_CLR   = "#fdba74"
    PANEL_TITLE = "#ffedd5"
    MINI_BG     = "#44280f"
    FOOTER_BORDER="rgba(251,146,60,0.15)"
    FOOTER_CLR  = "#fb923c"
    GAUGE_TRACK = "#44280f"
    IMPACT_TRACK= "#44280f"
    VERDICT_BG  = "#44280f"
    REC_BG      = "#341d0e"
    REC_URGENT_BG="#4c1d1d"
    REC_WARN_BG ="#44370f"
    REC_BORDER  = "rgba(251,146,60,0.12)"
    INPUT_CLR   = "#fed7aa"
elif T == "Midnight Blue":
    BG          = "#0c1929"
    SURFACE     = "#152238"
    SURFACE2    = "#1e2d47"
    BORDER      = "rgba(96,165,250,0.15)"
    TEXT_PRIMARY= "#eff6ff"
    TEXT_SEC    = "#93c5fd"
    TEXT_MUTED  = "#60a5fa"
    NAV_BG      = "#081220"
    PANEL_SHADOW= "0 2px 10px rgba(0,0,0,0.45)"
    KPI_BG      = "#152238"
    KPI_VAL_CLR = "#eff6ff"
    LABEL_CLR   = "#93c5fd"
    PANEL_TITLE = "#dbeafe"
    MINI_BG     = "#1e2d47"
    FOOTER_BORDER="rgba(96,165,250,0.15)"
    FOOTER_CLR  = "#60a5fa"
    GAUGE_TRACK = "#1e2d47"
    IMPACT_TRACK= "#1e2d47"
    VERDICT_BG  = "#1e2d47"
    REC_BG      = "#152238"
    REC_URGENT_BG="#3b1a1a"
    REC_WARN_BG ="#3b2f0f"
    REC_BORDER  = "rgba(96,165,250,0.12)"
    INPUT_CLR   = "#bfdbfe"
else:  # Light
    BG          = "#f0f2f5"
    SURFACE     = "#ffffff"
    SURFACE2    = "#f8fafc"
    BORDER      = "#e2e8f0"
    TEXT_PRIMARY= "#0f172a"
    TEXT_SEC    = "#475569"
    TEXT_MUTED  = "#94a3b8"
    NAV_BG      = "#1a1f2e"
    PANEL_SHADOW= "0 1px 4px rgba(0,0,0,0.07)"
    KPI_BG      = "#ffffff"
    KPI_VAL_CLR = "#0f172a"
    LABEL_CLR   = "#6366f1"
    PANEL_TITLE = "#1e293b"
    MINI_BG     = "#f8fafc"
    FOOTER_BORDER="#e2e8f0"
    FOOTER_CLR  = "#94a3b8"
    GAUGE_TRACK = "#f1f5f9"
    IMPACT_TRACK= "#f1f5f9"
    VERDICT_BG  = "#f8fafc"
    REC_BG      = "#fafafa"
    REC_URGENT_BG="#fff5f5"
    REC_WARN_BG ="#fffbeb"
    REC_BORDER  = "#e2e8f0"
    INPUT_CLR   = "#374151"

# ── Dynamic CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background: {BG};
    color: {TEXT_PRIMARY};
}}

#MainMenu, footer, header {{ visibility: hidden; }}

/* Sidebar styling */
section[data-testid="stSidebar"] {{
    background: {SURFACE} !important;
    border-right: 1px solid {BORDER};
}}
section[data-testid="stSidebar"] * {{
    color: {TEXT_PRIMARY} !important;
}}

/* ── Top Nav ── */
.top-nav {{
    background: {NAV_BG};
    color: #fff;
    padding: 14px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 0 0 14px 14px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}}
.nav-logo {{
    font-size: 1.45rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #fff;
}}
.nav-logo span {{ color: #818cf8; }}
.nav-right {{
    font-size: 0.8rem;
    color: #94a3b8;
}}
.nav-right b {{ color: #c7d2fe; }}

/* ── Section Labels ── */
.section-label {{
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: {LABEL_CLR};
    margin: 22px 0 10px 0;
}}

/* ── KPI Tile ── */
.kpi-tile {{
    background: {KPI_BG};
    border-radius: 12px;
    padding: 20px 22px;
    box-shadow: {PANEL_SHADOW};
    border-left: 4px solid #6366f1;
    transition: all 0.25s ease;
    height: 100%;
}}
.kpi-tile:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99,102,241,0.18);
}}
.kpi-tile.green  {{ border-left-color: #10b981; }}
.kpi-tile.amber  {{ border-left-color: #f59e0b; }}
.kpi-tile.red    {{ border-left-color: #ef4444; }}
.kpi-tile.blue   {{ border-left-color: #3b82f6; }}
.kpi-tile.purple {{ border-left-color: #8b5cf6; }}

.kpi-label {{ font-size: 0.72rem; font-weight: 700; color: {TEXT_MUTED}; text-transform: uppercase; letter-spacing: 0.6px; }}
.kpi-value {{ font-size: 1.9rem; font-weight: 800; color: {KPI_VAL_CLR}; line-height: 1.2; margin-top: 6px; }}
.kpi-sub   {{ font-size: 0.75rem; color: {TEXT_MUTED}; margin-top: 4px; line-height: 1.4; }}

/* ── Panel ── */
.panel {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 22px 24px;
    box-shadow: {PANEL_SHADOW};
    margin-bottom: 20px;
    height: 100%;
}}
.panel-title {{
    font-size: 0.95rem;
    font-weight: 700;
    color: {PANEL_TITLE};
    border-bottom: 1px solid {BORDER};
    padding-bottom: 12px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}}

/* ── Probability Result ── */
.result-probability {{
    font-size: 3.8rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -2px;
}}
.result-label {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 12px;
}}
.risk-low   {{ color: #059669; }}
.risk-med   {{ color: #d97706; }}
.risk-high  {{ color: #dc2626; }}
.badge-low  {{ background: #d1fae5; color: #059669; border: 1px solid #6ee7b7; }}
.badge-med  {{ background: #fef3c7; color: #b45309; border: 1px solid #fcd34d; }}
.badge-high {{ background: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }}

/* ── Mini Metric Boxes ── */
.mini-box {{
    flex: 1;
    background: {MINI_BG};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 14px 16px;
}}
.mini-label {{ font-size: 0.68rem; color: {TEXT_MUTED}; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }}
.mini-val-red   {{ font-size: 1.75rem; font-weight: 800; color: #dc2626; line-height: 1.2; margin-top: 4px; }}
.mini-val-green {{ font-size: 1.75rem; font-weight: 800; color: #059669; line-height: 1.2; margin-top: 4px; }}

/* ── Gauge Bar ── */
.gauge-track {{
    background: {GAUGE_TRACK};
    border-radius: 50px;
    height: 14px;
    width: 100%;
    overflow: hidden;
    margin: 16px 0 6px 0;
}}
.gauge-fill {{
    height: 100%;
    border-radius: 50px;
    transition: width 0.8s ease;
}}
.gauge-low  {{ background: linear-gradient(90deg,#6ee7b7,#10b981); }}
.gauge-med  {{ background: linear-gradient(90deg,#fcd34d,#f59e0b); }}
.gauge-high {{ background: linear-gradient(90deg,#fca5a5,#ef4444); }}
.gauge-labels {{
    display: flex;
    justify-content: space-between;
    font-size: 0.68rem;
    color: {TEXT_MUTED};
    margin-top: 4px;
}}

/* ── Verdict Box ── */
.verdict-box {{
    margin-top: 14px;
    padding: 12px 14px;
    background: {VERDICT_BG};
    border: 1px solid {BORDER};
    border-radius: 8px;
    font-size: 0.82rem;
    color: {TEXT_SEC};
    line-height: 1.6;
}}

/* ── Feature Impact ── */
.impact-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 0;
    border-bottom: 1px solid {BORDER};
}}
.impact-name {{ flex: 0 0 140px; font-size: 0.8rem; color: {TEXT_SEC}; font-weight: 600; }}
.impact-bar-track {{ flex: 1; background: {IMPACT_TRACK}; border-radius: 4px; height: 8px; overflow: hidden; }}
.impact-bar-fill  {{ height: 100%; border-radius: 4px; }}
.impact-val {{ flex: 0 0 42px; font-size: 0.78rem; text-align: right; font-weight: 700; }}
.impact-reason {{ font-size: 0.7rem; color: {TEXT_MUTED}; padding: 2px 0 8px 150px; line-height: 1.4; }}

/* ── Recommendation Cards ── */
.rec-card {{
    border: 1px solid {REC_BORDER};
    border-left: 4px solid #6366f1;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 11px;
    background: {REC_BG};
}}
.rec-card.urgent  {{ border-left-color: #ef4444; background: {REC_URGENT_BG}; }}
.rec-card.warning {{ border-left-color: #f59e0b; background: {REC_WARN_BG}; }}
.rec-head {{ font-size: 0.87rem; font-weight: 700; color: {PANEL_TITLE}; margin-bottom: 5px; }}
.rec-body {{ font-size: 0.79rem; color: {TEXT_SEC}; line-height: 1.55; }}
.rec-tag  {{
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 2px 8px;
    border-radius: 4px;
    margin-bottom: 6px;
}}
.tag-urgent  {{ background: #fee2e2; color: #b91c1c; }}
.tag-warning {{ background: #fef3c7; color: #b45309; }}
.tag-info    {{ background: #e0e7ff; color: #4338ca; }}

/* ── Summary Row ── */
.summary-strip {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
    display: flex;
    gap: 0;
    align-items: stretch;
}}
.strip-item {{
    flex: 1;
    text-align: center;
    padding: 8px 12px;
    border-right: 1px solid {BORDER};
}}
.strip-item:last-child {{ border-right: none; }}
.strip-label {{ font-size: 0.68rem; color: {TEXT_MUTED}; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }}
.strip-val   {{ font-size: 1.1rem; font-weight: 800; color: {TEXT_PRIMARY}; margin-top: 4px; }}

/* ── Profile Table Row ── */
.profile-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid {BORDER};
    font-size: 0.81rem;
}}
.profile-row:last-child {{ border-bottom: none; }}
.profile-key  {{ color: {TEXT_MUTED}; font-weight: 600; flex: 0 0 140px; }}
.profile-val  {{ color: {TEXT_PRIMARY}; font-weight: 700; text-align: right; }}

/* ── Benchmark Bar Row ── */
.bench-row {{
    padding: 8px 0;
    border-bottom: 1px solid {BORDER};
    font-size: 0.8rem;
}}
.bench-row:last-child {{ border-bottom: none; }}
.bench-labels {{ display: flex; justify-content: space-between; margin-bottom: 5px; }}
.bench-name {{ color: {TEXT_SEC}; font-weight: 600; }}
.bench-vals {{ font-size: 0.72rem; color: {TEXT_MUTED}; }}
.bench-track {{ background: {GAUGE_TRACK}; border-radius: 6px; height: 8px; overflow: hidden; }}
.bench-fill  {{ height: 100%; border-radius: 6px; }}

/* ── Action Timeline ── */
.timeline-item {{
    display: flex;
    gap: 14px;
    padding: 10px 0;
    border-bottom: 1px solid {BORDER};
    align-items: flex-start;
}}
.timeline-item:last-child {{ border-bottom: none; }}
.tl-dot {{
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 800;
    flex-shrink: 0;
    margin-top: 2px;
}}
.tl-dot-red    {{ background: #fee2e2; color: #b91c1c; }}
.tl-dot-amber  {{ background: #fef3c7; color: #b45309; }}
.tl-dot-blue   {{ background: #e0e7ff; color: #4338ca; }}
.tl-dot-green  {{ background: #d1fae5; color: #065f46; }}
.tl-content {{ flex: 1; }}
.tl-timing {{ font-size: 0.7rem; font-weight: 700; color: {TEXT_MUTED}; text-transform: uppercase; letter-spacing: 0.5px; }}
.tl-action {{ font-size: 0.82rem; font-weight: 700; color: {PANEL_TITLE}; margin: 2px 0; }}
.tl-detail {{ font-size: 0.75rem; color: {TEXT_SEC}; line-height: 1.4; }}

/* ── Footer ── */
.footer {{
    margin-top: 44px;
    padding: 20px 0 12px 0;
    text-align: center;
    border-top: 1px solid {FOOTER_BORDER};
    font-size: 0.78rem;
    color: {FOOTER_CLR};
    line-height: 1.7;
}}

/* ── Input overrides ── */
label {{ font-size: 0.81rem !important; font-weight: 600 !important; color: {INPUT_CLR} !important; }}
hr.light {{ border: none; border-top: 1px solid {BORDER}; margin: 14px 0; }}
</style>
""", unsafe_allow_html=True)

# ── Load assets ────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_assets():
    model    = joblib.load('churn_model.pkl')
    encoders = joblib.load('encoders.pkl')
    columns  = joblib.load('columns.pkl')
    return model, encoders, columns

model, encoders, columns = load_assets()

# ── Top Navigation Bar ─────────────────────────────────────────────────────────
theme_badge_map = {
    "Light": "☀️ Light",
    "Dark": "🌙 Dark",
    "Indigo": "🔮 Indigo",
    "Emerald": "🌿 Emerald",
    "Rose": "🌹 Rose",
    "Sunset": "🌅 Sunset",
    "Midnight Blue": "🌊 Midnight Blue"
}
theme_badge = theme_badge_map.get(T, "☀️ Light")
st.markdown(f"""
<div class="top-nav">
    <div class="nav-logo">📡 Churn<span>Sense</span>
        <span style="font-size:0.8rem;font-weight:400;color:#64748b;margin-left:10px">Retention Intelligence Platform v2.0</span>
    </div>
    <div class="nav-right">
        Theme: <b>{theme_badge}</b> &nbsp;•&nbsp;
        Telecom Analytics &nbsp;•&nbsp;
        <b>Customer 360 View</b> &nbsp;•&nbsp;
        Model: <b>Random Forest Classifier</b>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Platform Overview — Industry Benchmarks (2026)</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
tiles = [
    (k1, "blue",   "Avg. Industry Churn Rate",         "21.3%",  "Telecom sector — Annual 2026"),
    (k2, "green",  "Proactive Retention Rate",          "68%",    "Success with targeted outreach"),
    (k3, "amber",  "Avg. Customer Lifetime Value",      "$1,840", "Based on 30-month avg. tenure"),
    (k4, "red",    "Cost to Acquire New Customer",      "$315",   "vs $52 to retain existing"),
    (k5, "purple", "Avg. Monthly Revenue per User",     "$64.80", "Telecom ARPU — Q1 2026"),
]
for col, cls, lbl, val, sub in tiles:
    with col:
        st.markdown(f"""
        <div class="kpi-tile {cls}">
            <div class="kpi-label">{lbl}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Main Layout ────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([3, 2], gap="large")

# ═══════════════════════════════════════════════════════════════════════════════
# LEFT — Customer Input Form
# ═══════════════════════════════════════════════════════════════════════════════
with left_col:

    # ── Section 1: Demographics ──────────────────────────────────────────────
    st.markdown('<div class="section-label">Section 1 — Customer Demographics</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">👤 Personal Information</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        gender = st.selectbox("Gender", encoders['gender'].classes_)
    with c2:
        senior_label   = st.selectbox("Senior Citizen", ["No", "Yes"])
        senior_citizen = 1 if senior_label == "Yes" else 0
    with c3:
        partner    = st.selectbox("Has Partner", encoders['Partner'].classes_)
    with c4:
        dependents = st.selectbox("Has Dependents", encoders['Dependents'].classes_)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Section 2: Account & Billing ─────────────────────────────────────────
    st.markdown('<div class="section-label">Section 2 — Account & Billing Information</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">💳 Billing & Contract</div>', unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    with b1:
        tenure   = st.slider("Tenure (months)", 0, 72, 12)
        contract = st.selectbox("Contract Type", encoders['Contract'].classes_)
    with b2:
        monthly_charges  = st.slider("Monthly Charges ($)", 18.0, 125.0, 65.0, 0.5)
        paperless_billing= st.selectbox("Paperless Billing", encoders['PaperlessBilling'].classes_)
    with b3:
        default_total  = round(tenure * monthly_charges, 2)
        total_charges  = st.number_input("Total Charges ($)", 0.0, 10000.0, float(default_total), 50.0)
        payment_method = st.selectbox("Payment Method", encoders['PaymentMethod'].classes_)

    # Show auto-calculated hint
    if abs(total_charges - default_total) < 0.01:
        st.caption(f"💡 Total Charges auto-estimated as tenure × monthly charges = ${default_total:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Section 3: Subscribed Services ───────────────────────────────────────
    st.markdown('<div class="section-label">Section 3 — Subscribed Services</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📡 Active Service Subscriptions</div>', unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(f"<div style='font-size:0.75rem;font-weight:700;color:{LABEL_CLR};margin-bottom:6px'>PHONE</div>", unsafe_allow_html=True)
        phone_service = st.selectbox("Phone Service", encoders['PhoneService'].classes_)
        if phone_service == "No":
            multiple_lines = "No phone service"
            st.caption("⚠️ Multiple Lines: N/A (No Phone)")
        else:
            ml_opts        = [x for x in encoders['MultipleLines'].classes_ if x != "No phone service"]
            multiple_lines = st.selectbox("Multiple Lines", ml_opts)
        internet_service = st.selectbox("Internet Service", encoders['InternetService'].classes_)

    no_inet  = (internet_service == "No")
    svc_opts = [x for x in encoders['OnlineSecurity'].classes_ if x != "No internet service"]

    with s2:
        st.markdown(f"<div style='font-size:0.75rem;font-weight:700;color:{LABEL_CLR};margin-bottom:6px'>SECURITY & PROTECTION</div>", unsafe_allow_html=True)
        if no_inet:
            online_security  = "No internet service"
            device_protection= "No internet service"
            streaming_tv     = "No internet service"
            st.info("⚠️ Internet required for these services")
        else:
            online_security  = st.selectbox("Online Security",   svc_opts)
            device_protection= st.selectbox("Device Protection", svc_opts)
            streaming_tv     = st.selectbox("Streaming TV",       svc_opts)

    with s3:
        st.markdown(f"<div style='font-size:0.75rem;font-weight:700;color:{LABEL_CLR};margin-bottom:6px'>BACKUP & SUPPORT</div>", unsafe_allow_html=True)
        if no_inet:
            online_backup    = "No internet service"
            tech_support     = "No internet service"
            streaming_movies = "No internet service"
        else:
            online_backup    = st.selectbox("Online Backup",     svc_opts)
            tech_support     = st.selectbox("Tech Support",      svc_opts)
            streaming_movies = st.selectbox("Streaming Movies",  svc_opts)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Customer Summary Strip ────────────────────────────────────────────────
    svc_count = sum([
        phone_service == "Yes",
        multiple_lines == "Yes",
        internet_service != "No",
        online_security == "Yes",
        online_backup == "Yes",
        device_protection == "Yes",
        tech_support == "Yes",
        streaming_tv == "Yes",
        streaming_movies == "Yes",
    ])
    st.markdown(f"""
    <div class="summary-strip">
        <div class="strip-item">
            <div class="strip-label">Tenure</div>
            <div class="strip-val">{tenure} mo</div>
        </div>
        <div class="strip-item">
            <div class="strip-label">Monthly Bill</div>
            <div class="strip-val">${monthly_charges:.0f}</div>
        </div>
        <div class="strip-item">
            <div class="strip-label">Total Spent</div>
            <div class="strip-val">${total_charges:,.0f}</div>
        </div>
        <div class="strip-item">
            <div class="strip-label">Active Services</div>
            <div class="strip-val">{svc_count} / 9</div>
        </div>
        <div class="strip-item">
            <div class="strip-label">Contract</div>
            <div class="strip-val" style="font-size:0.9rem">{contract}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# RIGHT — Prediction & Analysis
# ═══════════════════════════════════════════════════════════════════════════════
with right_col:

    # ── Build encoded input vector ────────────────────────────────────────────
    raw = {
        'gender': gender,           'SeniorCitizen': senior_citizen,
        'Partner': partner,         'Dependents': dependents,
        'tenure': tenure,           'PhoneService': phone_service,
        'MultipleLines': multiple_lines, 'InternetService': internet_service,
        'OnlineSecurity': online_security, 'OnlineBackup': online_backup,
        'DeviceProtection': device_protection, 'TechSupport': tech_support,
        'StreamingTV': streaming_tv, 'StreamingMovies': streaming_movies,
        'Contract': contract,       'PaperlessBilling': paperless_billing,
        'PaymentMethod': payment_method, 'MonthlyCharges': monthly_charges,
        'TotalCharges': total_charges
    }
    encoded = {col: (encoders[col].transform([raw[col]])[0] if col in encoders else raw[col]) for col in columns}
    df_input   = pd.DataFrame([encoded])[columns]
    probs      = model.predict_proba(df_input)[0]
    churn_pct  = float(probs[1]) * 100
    retain_pct = float(probs[0]) * 100

    # Risk tier
    if churn_pct < 30:
        tier = "low";  badge_cls = "badge-low";  risk_cls = "risk-low";  gauge_cls = "gauge-low"
        tier_label = "Low Risk"; tier_icon = "🟢"
        verdict = "Customer appears stable. Standard engagement and periodic check-ins are recommended."
    elif churn_pct < 60:
        tier = "med";  badge_cls = "badge-med";  risk_cls = "risk-med";  gauge_cls = "gauge-med"
        tier_label = "Moderate Risk"; tier_icon = "🟡"
        verdict = "Elevated churn signal detected. Proactive retention outreach is strongly advised within 7 days."
    else:
        tier = "high"; badge_cls = "badge-high"; risk_cls = "risk-high"; gauge_cls = "gauge-high"
        tier_label = "High Risk"; tier_icon = "🔴"
        verdict = "Critical churn risk. Immediate CRM intervention required — escalate to retention team now."

    # ── Prediction Panel ──────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Prediction Output</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="panel">
        <div class="panel-title">📊 Churn Probability Score</div>
        <div class="result-probability {risk_cls}">{churn_pct:.1f}%</div>
        <span class="result-label {badge_cls}">{tier_icon} {tier_label}</span>
        <div class="gauge-track">
            <div class="gauge-fill {gauge_cls}" style="width:{churn_pct}%"></div>
        </div>
        <div class="gauge-labels">
            <span>0% — Stable</span><span>30%</span><span>60%</span><span>100% — Churned</span>
        </div>
        <hr class="light">
        <div style="display:flex;gap:14px;margin-top:4px">
            <div class="mini-box">
                <div class="mini-label">Will Churn</div>
                <div class="mini-val-red">{churn_pct:.1f}%</div>
            </div>
            <div class="mini-box">
                <div class="mini-label">Will Stay</div>
                <div class="mini-val-green">{retain_pct:.1f}%</div>
            </div>
            <div class="mini-box">
                <div class="mini-label">Risk Tier</div>
                <div style="font-size:1rem;font-weight:800;margin-top:4px;color:{'#dc2626' if tier=='high' else '#d97706' if tier=='med' else '#059669'}">{tier_label}</div>
            </div>
        </div>
        <div class="verdict-box">
            <b>Model Verdict:</b> {verdict}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Feature Risk Signals ──────────────────────────────────────────────────
    st.markdown('<div class="section-label">Feature Risk Analysis</div>', unsafe_allow_html=True)

    feature_signals = []
    if contract == "Month-to-month":
        feature_signals.append(("Contract Type", 92, "#ef4444", "Month-to-month is the #1 churn predictor"))
    elif contract == "One year":
        feature_signals.append(("Contract Type", 38, "#f59e0b", "One-year contract — moderate retention signal"))
    else:
        feature_signals.append(("Contract Type", 8,  "#10b981", "Two-year contract — strong loyalty indicator"))

    if tenure <= 6:
        feature_signals.append(("Tenure", 85, "#ef4444", f"Only {tenure}mo — critical early churn window"))
    elif tenure <= 18:
        feature_signals.append(("Tenure", 52, "#f59e0b", f"{tenure}mo — customer still building loyalty"))
    elif tenure <= 36:
        feature_signals.append(("Tenure", 28, "#f59e0b", f"{tenure}mo — moderately loyal"))
    else:
        feature_signals.append(("Tenure", 9,  "#10b981", f"{tenure}mo — established long-term customer"))

    if payment_method == "Electronic check":
        feature_signals.append(("Payment Method", 78, "#ef4444", "Electronic check: high involuntary churn rate"))
    elif payment_method == "Mailed check":
        feature_signals.append(("Payment Method", 50, "#f59e0b", "Mailed check: moderate friction risk"))
    else:
        feature_signals.append(("Payment Method", 12, "#10b981", "Auto-pay enrolled: low payment failure risk"))

    if monthly_charges > 90:
        feature_signals.append(("Monthly Charges", 72, "#ef4444", f"${monthly_charges:.0f}/mo — top quartile, price-sensitive"))
    elif monthly_charges > 60:
        feature_signals.append(("Monthly Charges", 42, "#f59e0b", f"${monthly_charges:.0f}/mo — moderate spend tier"))
    else:
        feature_signals.append(("Monthly Charges", 18, "#10b981", f"${monthly_charges:.0f}/mo — low spend, low sensitivity"))

    if not no_inet:
        if tech_support == "No":
            feature_signals.append(("Tech Support", 66, "#ef4444", "No support: unresolved issues = churn trigger"))
        if online_security == "No":
            feature_signals.append(("Online Security", 55, "#f59e0b", "No security: lower product stickiness"))
        if online_backup == "No" and device_protection == "No":
            feature_signals.append(("Backup / Protection", 40, "#f59e0b", "No add-ons: less embedded in ecosystem"))

    if senior_citizen == 1:
        feature_signals.append(("Senior Citizen", 46, "#f59e0b", "Senior segment: higher churn propensity"))
    if dependents == "No" and partner == "No":
        feature_signals.append(("Household Profile", 38, "#f59e0b", "Single, no dependents: lower switching cost"))

    feature_signals.sort(key=lambda x: x[1], reverse=True)
    feature_signals = feature_signals[:7]

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">⚡ Top Risk Signals</div>', unsafe_allow_html=True)
    for fname, score, color, reason in feature_signals:
        st.markdown(f"""
        <div class="impact-row">
            <div class="impact-name">{fname}</div>
            <div class="impact-bar-track">
                <div class="impact-bar-fill" style="width:{score}%;background:{color}"></div>
            </div>
            <div class="impact-val" style="color:{color}">{score}%</div>
        </div>
        <div class="impact-reason">{reason}</div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Retention Playbook + Health Overview Side by Side ──────────────────────
    playbook_col, health_col = st.columns([1, 1], gap="large")

    with playbook_col:
        st.markdown('<div class="section-label">CRM Recommended Actions</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">🛡️ Retention Playbook</div>', unsafe_allow_html=True)

        recs = []
        if contract == "Month-to-month":
            recs.append(("urgent", "Contract Upgrade Offer",
                "Propose a 1-year or 2-year contract with 10–15% monthly discount and a free month. "
                "Customers on long-term contracts are 3× less likely to churn."))
        if tenure <= 6:
            recs.append(("urgent", "Early Lifecycle Intervention",
                "Assign a dedicated Customer Success manager for the first 90 days. "
                "Schedule a personalised onboarding call within 48 hours."))
        if payment_method == "Electronic check":
            recs.append(("warning", "Auto-Pay Enrollment Campaign",
                "Offer a $5/month credit to switch to bank transfer or credit card auto-pay. "
                "Electronic check failures drive 22% of involuntary churn."))
        if not no_inet and tech_support == "No":
            recs.append(("warning", "Complimentary Tech Support Trial",
                "Activate 3-month complimentary Tech Support. Unresolved technical issues are "
                "cited in 42% of churn exit surveys."))
        if not no_inet and online_security == "No":
            recs.append(("info", "Security Bundle Upsell",
                "Offer Online Security + Online Backup at $5/month introductory rate. "
                "Security bundles increase 12-month retention by 18%."))
        if monthly_charges > 85:
            recs.append(("warning", "Rate Review & Loyalty Discount",
                f"At ${monthly_charges:.0f}/month this customer is in the top cost quartile. "
                "Offer a loyalty discount or plan consultation to prevent price-triggered churn."))
        if paperless_billing == "No":
            recs.append(("info", "Paperless Billing Incentive",
                "Incentivise paperless billing with a $2 monthly credit. "
                "Reduces payment friction and increases customer portal engagement by 31%."))
        if not no_inet and streaming_tv == "No" and streaming_movies == "No":
            recs.append(("info", "Entertainment Bundle Offer",
                "Offer a trial of Streaming TV + Movies bundle. "
                "Entertainment subscribers show 25% lower churn rates."))
        if not recs:
            recs.append(("info", "Routine Engagement Check-in",
                "No immediate risk signals. Maintain monthly satisfaction surveys and "
                "review for upsell opportunities at next billing cycle."))

        priority_map = {"urgent": "🚨 Urgent", "warning": "⚠️ Recommended", "info": "ℹ️ Suggested"}
        tag_map      = {"urgent": "tag-urgent", "warning": "tag-warning",   "info": "tag-info"}
        card_map     = {"urgent": "rec-card urgent", "warning": "rec-card warning", "info": "rec-card"}

        for rtype, title, body in recs:
            st.markdown(f"""
            <div class="{card_map[rtype]}">
                <span class="rec-tag {tag_map[rtype]}">{priority_map[rtype]}</span>
                <div class="rec-head">{title}</div>
                <div class="rec-body">{body}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with health_col:
        st.markdown('<div class="section-label">Customer Health Overview</div>', unsafe_allow_html=True)

        # Compute individual health scores (0–100, higher = healthier)
        tenure_health   = min(100, int((tenure / 72) * 100))
        spend_health    = max(0, 100 - int(((monthly_charges - 18) / (125 - 18)) * 100))
        contract_health = {"Month-to-month": 15, "One year": 60, "Two year": 100}[contract]
        payment_health  = {"Electronic check": 20, "Mailed check": 50,
                           "Bank transfer (automatic)": 95, "Credit card (automatic)": 95}.get(payment_method, 70)
        services_health = min(100, int((svc_count / 9) * 100))
        overall_health  = int((tenure_health + contract_health + payment_health + services_health) / 4)

        health_color = "#059669" if overall_health >= 65 else "#d97706" if overall_health >= 40 else "#dc2626"
        health_label = "Healthy" if overall_health >= 65 else "At Risk" if overall_health >= 40 else "Critical"

        health_bars = [
            ("Tenure Stability",    tenure_health,   "#6366f1"),
            ("Price Sensitivity",   spend_health,    "#3b82f6"),
            ("Contract Strength",   contract_health, "#8b5cf6"),
            ("Payment Reliability", payment_health,  "#10b981"),
            ("Service Adoption",    services_health, "#f59e0b"),
        ]

        bars_html = "".join([f"""
        <div style="margin-bottom:10px">
            <div style="display:flex;justify-content:space-between;font-size:0.75rem;margin-bottom:4px">
                <span style="color:{TEXT_SEC};font-weight:600">{name}</span>
                <span style="color:{color};font-weight:700">{score}%</span>
            </div>
            <div style="background:{GAUGE_TRACK};border-radius:6px;height:7px;overflow:hidden">
                <div style="width:{score}%;height:100%;background:{color};border-radius:6px"></div>
            </div>
        </div>
        """ for name, score, color in health_bars])

        st.markdown(f"""
        <div class="panel">
            <div class="panel-title">💚 Customer Health Score</div>
            <div style="display:flex;align-items:center;gap:20px;margin-bottom:18px">
                <div style="text-align:center;flex:0 0 80px">
                    <div style="font-size:2.4rem;font-weight:900;color:{health_color};line-height:1">{overall_health}</div>
                    <div style="font-size:0.7rem;font-weight:700;color:{health_color};text-transform:uppercase;letter-spacing:0.5px">{health_label}</div>
                </div>
                <div style="flex:1;font-size:0.8rem;color:{TEXT_SEC};line-height:1.6;border-left:3px solid {health_color};padding-left:14px">
                    {'Strong account with good tenure, contract commitment, and stable payments.' if overall_health >= 65 else
                     'Several risk factors detected. Targeted retention actions recommended to stabilise this account.' if overall_health >= 40 else
                     'Multiple critical signals. This customer is at high risk of leaving without immediate intervention.'}
                </div>
            </div>
            {bars_html}
        </div>
        """, unsafe_allow_html=True)

# ── Business Impact Row (always visible) ──────────────────────────────────────
st.markdown('<div class="section-label">Business Impact Estimate</div>', unsafe_allow_html=True)
ltv_at_risk = round(total_charges + (monthly_charges * max(0, 30 - tenure)), 2)
roi_ratio   = round(315 / 52, 1)

i1, i2, i3, i4 = st.columns(4)
i1.markdown(f"""
<div class="kpi-tile red">
    <div class="kpi-label">Revenue at Risk</div>
    <div class="kpi-value">${ltv_at_risk:,.0f}</div>
    <div class="kpi-sub">Projected LTV loss if this customer churns</div>
</div>""", unsafe_allow_html=True)

i2.markdown(f"""
<div class="kpi-tile amber">
    <div class="kpi-label">Replacement Acquisition Cost</div>
    <div class="kpi-value">$315</div>
    <div class="kpi-sub">Industry avg. cost to acquire a new subscriber</div>
</div>""", unsafe_allow_html=True)

i3.markdown(f"""
<div class="kpi-tile green">
    <div class="kpi-label">Retention Action Cost</div>
    <div class="kpi-value">~$52</div>
    <div class="kpi-sub">Avg. cost of proactive retention campaign</div>
</div>""", unsafe_allow_html=True)

i4.markdown(f"""
<div class="kpi-tile purple">
    <div class="kpi-label">Retention vs Acquisition ROI</div>
    <div class="kpi-value">{roi_ratio}×</div>
    <div class="kpi-sub">Retaining is {roi_ratio}× cheaper than acquiring</div>
</div>""", unsafe_allow_html=True)

# ── Full-Width Bottom Intelligence Report ──────────────────────────────────────
st.markdown('<div class="section-label">Customer Intelligence Report</div>', unsafe_allow_html=True)

b_col1, b_col2, b_col3 = st.columns([1, 1, 1], gap="large")

# ── Column 1: Customer Profile Snapshot ────────────────────────────────────────
with b_col1:
    profile_color = "#dc2626" if churn_pct >= 60 else "#d97706" if churn_pct >= 30 else "#059669"
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🧾 Customer Profile Snapshot</div>', unsafe_allow_html=True)

    profile_rows = [
        ("Gender",            gender),
        ("Senior Citizen",    senior_label),
        ("Partner",           partner),
        ("Dependents",        dependents),
        ("Tenure",            f"{tenure} months"),
        ("Contract",          contract),
        ("Monthly Charges",   f"${monthly_charges:.2f}"),
        ("Total Charges",     f"${total_charges:,.2f}"),
        ("Payment Method",    payment_method),
        ("Paperless Billing", paperless_billing),
        ("Internet Service",  internet_service),
        ("Phone Service",     phone_service),
        ("Active Services",   f"{svc_count} / 9"),
        ("Churn Score",       f"{churn_pct:.1f}%"),
    ]
    rows_html = "".join([
        f'<div class="profile-row">'
        f'<span class="profile-key">{k}</span>'
        f'<span class="profile-val" style="color:{profile_color if k=="Churn Score" else TEXT_PRIMARY}">{v}</span>'
        f'</div>'
        for k, v in profile_rows
    ])
    st.markdown(rows_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Column 2: Benchmark Comparison ─────────────────────────────────────────────
with b_col2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📈 Customer vs. Industry Benchmark</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:0.75rem;color:{TEXT_MUTED};margin-bottom:14px">How this customer compares to the average telco subscriber (2026 data)</div>', unsafe_allow_html=True)

    # industry averages
    industry_avg_tenure   = 29.0
    industry_avg_monthly  = 64.8
    industry_avg_total    = 1880.0
    industry_churn_rate   = 21.3
    industry_svc_count    = 4.5

    benchmarks = [
        ("Tenure",           tenure,          industry_avg_tenure,   72,     "months",   "#6366f1"),
        ("Monthly Charges",  monthly_charges, industry_avg_monthly,  125,    "$/mo",     "#3b82f6"),
        ("Total Charges",    total_charges,   industry_avg_total,    10000,  "$",        "#8b5cf6"),
        ("Churn Risk",       churn_pct,       industry_churn_rate,   100,    "%",        profile_color),
        ("Active Services",  svc_count,       industry_svc_count,    9,      "/ 9",      "#10b981"),
    ]

    for name, val, avg, max_val, unit, color in benchmarks:
        cust_pct  = min(100, round((val / max_val) * 100, 1))
        avg_pct   = min(100, round((avg / max_val) * 100, 1))
        val_fmt   = f"{val:.0f}{unit}" if unit not in ["$/mo", "$"] else f"${val:,.0f}"
        avg_fmt   = f"{avg:.0f}{unit}" if unit not in ["$/mo", "$"] else f"${avg:,.0f}"
        st.markdown(f"""
        <div class="bench-row">
            <div class="bench-labels">
                <span class="bench-name">{name}</span>
                <span class="bench-vals">You: <b style="color:{TEXT_PRIMARY}">{val_fmt}</b> &nbsp; Avg: {avg_fmt}</span>
            </div>
            <div style="position:relative;margin-bottom:3px">
                <div class="bench-track">
                    <div class="bench-fill" style="width:{cust_pct}%;background:{color}"></div>
                </div>
                <div style="position:absolute;top:-1px;left:{avg_pct}%;width:2px;height:10px;background:{TEXT_MUTED};border-radius:2px" title="Industry avg"></div>
            </div>
            <div style="font-size:0.68rem;color:{TEXT_MUTED}">Industry avg at {avg_pct:.0f}% mark (dashed line)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Column 3: Action Timeline ───────────────────────────────────────────────────
with b_col3:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🗓️ Recommended Action Timeline</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:0.75rem;color:{TEXT_MUTED};margin-bottom:14px">Prioritised CRM actions based on churn risk score of <b style="color:{profile_color}">{churn_pct:.1f}%</b></div>', unsafe_allow_html=True)

    # Build timeline based on risk and features
    timeline = []

    if churn_pct >= 60:
        timeline.append(("tl-dot-red",   "Now — Within 24 hrs",
            "Escalate to Retention Team",
            "Flag account as Priority 1 in CRM. Assign senior retention specialist immediately."))
    elif churn_pct >= 30:
        timeline.append(("tl-dot-amber", "Now — Within 48 hrs",
            "Schedule Outreach Call",
            "Contact customer via preferred channel. Probe satisfaction and flag any service issues."))
    else:
        timeline.append(("tl-dot-green", "This Week",
            "Routine NPS Survey",
            "Send automated Net Promoter Score survey. Log satisfaction score in CRM."))

    if contract == "Month-to-month":
        timeline.append(("tl-dot-red", "Day 3–5",
            "Contract Upgrade Offer",
            "Send personalised email with 1-yr / 2-yr contract discount. Follow up by phone if no response."))

    if payment_method == "Electronic check":
        timeline.append(("tl-dot-amber", "Day 5–7",
            "Auto-Pay Migration",
            "Send SMS + email offering $5/month credit to switch to auto-pay. Redirect to self-serve portal."))

    if not no_inet and tech_support == "No":
        timeline.append(("tl-dot-blue", "Week 2",
            "Activate Tech Support Trial",
            "Provision 3-month complimentary Tech Support. Send activation confirmation with support hotline."))

    if not no_inet and online_security == "No":
        timeline.append(("tl-dot-blue", "Week 2–3",
            "Security Bundle Promotion",
            "Push in-app notification for Online Security + Backup bundle at introductory $5/month."))

    timeline.append(("tl-dot-green", "Month 1",
        "Follow-Up Satisfaction Check",
        "Automated CSAT survey after all retention actions. Update churn score in platform."))

    timeline.append(("tl-dot-green", "Month 3",
        "Loyalty Review & Upsell",
        "Review account health. If retained, identify upsell opportunities (streaming, security bundles)."))

    for dot_cls, timing, action, detail in timeline:
        num = timeline.index((dot_cls, timing, action, detail)) + 1
        st.markdown(f"""
        <div class="timeline-item">
            <div class="tl-dot {dot_cls}">{num}</div>
            <div class="tl-content">
                <div class="tl-timing">{timing}</div>
                <div class="tl-action">{action}</div>
                <div class="tl-detail">{detail}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
    <b>ChurnSense — Retention Intelligence Platform</b> &nbsp;|&nbsp; Version 2.0<br>
    Developed by <b>Riya Rastogi</b> &nbsp;|&nbsp;
    Model: <b>Random Forest Classifier</b> trained on Telco Customer Churn Dataset &nbsp;|&nbsp;
    For internal analytics and CRM decision support only.<br>
    <span style="font-size:0.71rem">© 2026 Riya Rastogi. All rights reserved.</span>
</div>
""", unsafe_allow_html=True)
