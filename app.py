# ╔══════════════════════════════════════════════════════════════════════╗
# ║   MERCADO CREATIVO  ·  Dashboard PCR Premium  v3.0                  ║
# ║   Pago Contra Reembolso  ·  E-Commerce & Dropshipping               ║
# ║   Dark Indigo / Neon-Cyan / Glassmorphism UI                        ║
# ╚══════════════════════════════════════════════════════════════════════╝

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ─────────────────────────────────────────────────────────────────────────────
# 0 · PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mercado Creativo · PCR",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# 1 · GLOBAL CSS — TOTAL OVERRIDE DEL DOM DE STREAMLIT
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ─── Google Fonts ─────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* ─── Design Tokens ─────────────────────────────────────────────────────── */
:root {
  /* Backgrounds */
  --bg-base:       #0E0F1A;
  --bg-deep:       #070810;
  --bg-app:        #1E1E2D;
  --bg-card:       #27293D;
  --bg-card-alt:   #2A2C42;
  --bg-glass:      rgba(30, 30, 45, 0.50);
  --bg-glass-2:    rgba(39, 41, 61, 0.65);
  --bg-input:      rgba(255,255,255,0.04);

  /* Borders */
  --b-rim:         rgba(255,255,255,0.06);
  --b-rim-2:       rgba(255,255,255,0.10);
  --b-cyan:        rgba(0,242,255,0.22);
  --b-green:       rgba(0,255,133,0.20);

  /* Accent palette */
  --cyan:    #00F2FF;
  --green:   #00FF85;
  --magenta: #FF3CAC;
  --amber:   #FFBE45;
  --red:     #FF4D6A;
  --indigo:  #636EFA;
  --violet:  #B39DDB;
  --white:   #EAECF4;

  /* Text */
  --t1: #EAECF4;
  --t2: #9BA3C4;
  --t3: #4E5474;

  /* Type */
  --ff: 'Outfit', sans-serif;
  --fm: 'JetBrains Mono', monospace;

  /* Misc */
  --blur:   12px;
  --blur-2: 24px;
  --r:      12px;
  --r-lg:   18px;
  --sh:     0 4px 40px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.03);
}

/* ─── RESET & BASE ──────────────────────────────────────────────────────── */
*, *::before, *::after  { box-sizing: border-box; }
html, body              { font-family: var(--ff) !important; background: var(--bg-deep) !important; }
p, li, span, div, label { font-family: var(--ff) !important; color: var(--t1); }
h1,h2,h3,h4,h5,h6      { font-family: var(--ff) !important; color: var(--t1) !important; font-weight: 800 !important; }
::-webkit-scrollbar     { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--b-cyan); border-radius: 4px; }

/* ─── STREAMLIT APP SHELL ───────────────────────────────────────────────── */
.stApp {
  background: var(--bg-deep) !important;
  background-image:
    radial-gradient(ellipse 80% 55% at 0% -10%,  rgba(0,242,255,0.055) 0%, transparent 60%),
    radial-gradient(ellipse 60% 45% at 100% 0%,  rgba(99,110,250,0.04) 0%, transparent 55%),
    radial-gradient(ellipse 50% 35% at 50% 110%, rgba(0,255,133,0.03)  0%, transparent 50%) !important;
}
.block-container  { padding: 1rem 2.2rem 4rem !important; max-width: 100% !important; }
.main             { background: transparent !important; }

/* ─── HIDE STREAMLIT CHROME ─────────────────────────────────────────────── */
#MainMenu, header, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stHeader"]             { display: none !important; visibility: hidden !important; }

/* ─── SIDEBAR ───────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: var(--bg-glass) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  border-right: 1px solid var(--b-rim) !important;
  box-shadow: 4px 0 60px rgba(0,0,0,0.7) !important;
}
section[data-testid="stSidebar"] > div:first-child {
  background: transparent !important;
}
section[data-testid="stSidebar"] * { color: var(--t1) !important; }
[data-testid="stSidebarCollapseButton"] { color: var(--t2) !important; }

/* ─── INPUTS / SELECTS ──────────────────────────────────────────────────── */
[data-baseweb="select"] > div,
[data-baseweb="input"]  > div {
  background: var(--bg-input) !important;
  border: 1px solid var(--b-rim-2) !important;
  border-radius: var(--r) !important;
  color: var(--t1) !important;
}
[data-baseweb="select"] *,
[data-baseweb="input"]  * { color: var(--t1) !important; background: transparent !important; }
[data-baseweb="popover"] > div { background: var(--bg-card) !important; border: 1px solid var(--b-rim-2) !important; border-radius: var(--r) !important; }
[data-baseweb="menu"] li { color: var(--t1) !important; }
[data-baseweb="menu"] li:hover { background: var(--bg-card-alt) !important; }
.stSelectbox label, .stMultiSelect label { color: var(--t3) !important; font-size: 0.68rem !important; text-transform: uppercase !important; letter-spacing: 0.09em !important; font-family: var(--fm) !important; }

/* ─── TABS ──────────────────────────────────────────────────────────────── */
[data-baseweb="tab-list"]  { background: transparent !important; border-bottom: 1px solid var(--b-rim) !important; gap: 2px !important; }
[data-baseweb="tab"] {
  background: transparent !important;
  border: none !important;
  color: var(--t3) !important;
  font-family: var(--ff) !important;
  font-size: 0.84rem !important;
  font-weight: 600 !important;
  padding: 10px 20px !important;
  border-radius: var(--r) var(--r) 0 0 !important;
  transition: all 0.2s !important;
}
[data-baseweb="tab"]:hover { color: var(--t2) !important; background: var(--bg-input) !important; }
[aria-selected="true"][data-baseweb="tab"] {
  background: rgba(0,242,255,0.08) !important;
  color: var(--cyan) !important;
  border-bottom: 2px solid var(--cyan) !important;
}
[data-baseweb="tab-highlight"] { display: none !important; }
[data-baseweb="tab-border"]    { display: none !important; }

/* ─── BUTTONS ───────────────────────────────────────────────────────────── */
.stButton > button {
  background: var(--bg-glass-2) !important;
  border: 1px solid var(--b-rim-2) !important;
  border-radius: var(--r) !important;
  color: var(--t1) !important;
  font-family: var(--ff) !important;
  font-weight: 600 !important;
  transition: all 0.25s !important;
}
.stButton > button:hover {
  border-color: var(--b-cyan) !important;
  color: var(--cyan) !important;
  background: rgba(0,242,255,0.06) !important;
  box-shadow: 0 0 20px rgba(0,242,255,0.12) !important;
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #00b8cc, #0066bb) !important;
  border: none !important; color: #fff !important;
}

/* ─── RADIO ─────────────────────────────────────────────────────────────── */
[data-testid="stRadio"] > div      { gap: 6px !important; flex-wrap: wrap !important; }
[data-testid="stRadio"] label      {
  background: var(--bg-glass-2) !important; border: 1px solid var(--b-rim) !important;
  border-radius: 8px !important; padding: 6px 15px !important;
  color: var(--t2) !important; font-size: 0.8rem !important; font-weight: 600 !important;
  transition: all 0.2s !important; cursor: pointer !important;
}
[data-testid="stRadio"] [aria-checked="true"] ~ label,
[data-testid="stRadio"] label:has(input:checked) {
  border-color: var(--b-cyan) !important; color: var(--cyan) !important;
  background: rgba(0,242,255,0.07) !important;
}

/* ─── EXPANDER ──────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
  background: var(--bg-card) !important; border: 1px solid var(--b-rim) !important;
  border-radius: var(--r) !important; overflow: hidden !important;
}
[data-testid="stExpander"] summary { color: var(--t1) !important; font-family: var(--ff) !important; font-weight: 600 !important; }
[data-testid="stExpander"] summary:hover { color: var(--cyan) !important; }
[data-testid="stExpander"] svg { fill: var(--t2) !important; }

/* ─── DATAFRAME / TABLE ─────────────────────────────────────────────────── */
[data-testid="stDataFrame"],
[data-testid="stDataFrame"] > div { background: var(--bg-card) !important; border-radius: var(--r) !important; }
.dvn-scroller { background: transparent !important; }
.col_heading, .blank, th { background: var(--bg-card-alt) !important; color: var(--t3) !important; font-family: var(--fm) !important; font-size: 0.68rem !important; }
td { color: var(--t1) !important; font-family: var(--ff) !important; font-size: 0.82rem !important; background: transparent !important; }
tr:hover td { background: rgba(255,255,255,0.02) !important; }

/* ─── SLIDER / NUMBER INPUT ─────────────────────────────────────────────── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"]   input {
  background: var(--bg-input) !important; border: 1px solid var(--b-rim-2) !important;
  border-radius: 8px !important; color: var(--t1) !important; font-family: var(--fm) !important;
}

/* ─── CUSTOM COMPONENT CLASSES ──────────────────────────────────────────── */

/* TopBar */
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 0 22px; margin-bottom: 20px;
  border-bottom: 1px solid var(--b-rim);
}
.brand-wrap  { display: flex; align-items: center; gap: 14px; }
.brand-icon  {
  width: 42px; height: 42px; border-radius: 12px;
  background: linear-gradient(135deg, rgba(0,242,255,0.15), rgba(0,255,133,0.08));
  border: 1px solid var(--b-cyan); display: flex; align-items: center; justify-content: center;
  font-size: 1.4rem; box-shadow: 0 0 20px rgba(0,242,255,0.15);
}
.brand-name  { font-size: 1.5rem; font-weight: 900; color: var(--white); letter-spacing: -0.04em; }
.brand-name  em { color: var(--cyan); font-style: normal; }
.brand-sub   { font-size: 0.65rem; color: var(--t3); font-family: var(--fm); letter-spacing: 0.08em; text-transform: uppercase; margin-top: 1px; }
.badge-live  {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 5px 14px; border-radius: 30px;
  background: rgba(0,255,133,0.07); border: 1px solid rgba(0,255,133,0.18);
  font-family: var(--fm); font-size: 0.68rem; font-weight: 700; color: var(--green);
  letter-spacing: 0.08em; text-transform: uppercase;
}
.badge-live::before {
  content: ''; width: 8px; height: 8px; border-radius: 50%; background: var(--green);
  box-shadow: 0 0 10px var(--green); animation: blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100% { opacity:1; transform:scale(1); } 50% { opacity:0.4; transform:scale(0.7); } }
.badge-ts {
  padding: 5px 14px; border-radius: 30px;
  background: var(--bg-input); border: 1px solid var(--b-rim);
  font-family: var(--fm); font-size: 0.68rem; color: var(--t2); letter-spacing: 0.05em;
}

/* Section Divider */
.sec-div {
  display: flex; align-items: center; gap: 12px; margin: 28px 0 18px;
}
.sec-div-label {
  font-size: 0.62rem; font-weight: 700; font-family: var(--fm);
  letter-spacing: 0.15em; text-transform: uppercase; color: var(--t3); white-space: nowrap;
}
.sec-div-dot {
  width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0;
}
.sec-div-line { flex:1; height: 1px; background: linear-gradient(90deg, var(--b-rim-2), transparent); }

/* KPI Card */
.kcard {
  background: var(--bg-card);
  border: 1px solid var(--b-rim);
  border-radius: var(--r-lg);
  padding: 20px 18px 16px;
  position: relative; overflow: hidden;
  transition: transform 0.3s cubic-bezier(.34,1.56,.64,1), border-color 0.25s, box-shadow 0.3s;
  box-shadow: var(--sh);
}
.kcard::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  border-radius: var(--r-lg) var(--r-lg) 0 0;
}
.kcard::after {
  content: ''; position: absolute; inset: 0; border-radius: var(--r-lg);
  background: linear-gradient(145deg, rgba(255,255,255,0.022) 0%, transparent 60%);
  pointer-events: none;
}
.kcard:hover { transform: translateY(-5px); box-shadow: 0 20px 70px rgba(0,0,0,0.65); }
.kcard.c  { border-color: rgba(0,242,255,0.12);  } .kcard.c::before  { background: linear-gradient(90deg,#00F2FF,#4D8DFF); } .kcard.c:hover  { border-color: rgba(0,242,255,0.30); box-shadow: 0 20px 70px rgba(0,0,0,0.6), 0 0 40px rgba(0,242,255,0.08); }
.kcard.g  { border-color: rgba(0,255,133,0.12);  } .kcard.g::before  { background: linear-gradient(90deg,#00FF85,#00C87A); } .kcard.g:hover  { border-color: rgba(0,255,133,0.30); box-shadow: 0 20px 70px rgba(0,0,0,0.6), 0 0 40px rgba(0,255,133,0.07); }
.kcard.r  { border-color: rgba(255,77,106,0.12); } .kcard.r::before  { background: linear-gradient(90deg,#FF4D6A,#FF3CAC); } .kcard.r:hover  { border-color: rgba(255,77,106,0.30); box-shadow: 0 20px 70px rgba(0,0,0,0.6), 0 0 40px rgba(255,77,106,0.08); }
.kcard.a  { border-color: rgba(255,190,69,0.12); } .kcard.a::before  { background: linear-gradient(90deg,#FFBE45,#FF9100); } .kcard.a:hover  { border-color: rgba(255,190,69,0.30); }
.kcard.i  { border-color: rgba(99,110,250,0.12); } .kcard.i::before  { background: linear-gradient(90deg,#636EFA,#00F2FF); } .kcard.i:hover  { border-color: rgba(99,110,250,0.30); }
.kcard.v  { border-color: rgba(179,157,219,0.12);} .kcard.v::before  { background: linear-gradient(90deg,#B39DDB,#FF3CAC); } .kcard.v:hover  { border-color: rgba(179,157,219,0.30); }

.kcard-lbl { font-size: 0.60rem; font-weight: 700; font-family: var(--fm); text-transform: uppercase; letter-spacing: 0.12em; color: var(--t3); margin-bottom: 3px; }
.kcard-val { font-size: 2.1rem; font-weight: 900; color: var(--white); letter-spacing: -0.05em; line-height: 1; margin: 6px 0 5px; }
.kcard-sub { font-size: 0.73rem; font-weight: 500; }
.kcard-ico { position: absolute; top: 16px; right: 16px; font-size: 1.8rem; opacity: 0.12; }
.pos { color: var(--green); }
.neg { color: var(--red); }
.neu { color: var(--t2); }

/* Chart Wrapper */
.cw {
  background: var(--bg-card); border: 1px solid var(--b-rim);
  border-radius: var(--r-lg); padding: 20px 20px 14px;
  box-shadow: var(--sh); position: relative; overflow: hidden;
}
.cw::after {
  content: ''; position: absolute; inset: 0; border-radius: var(--r-lg);
  background: linear-gradient(145deg, rgba(255,255,255,0.018) 0%, transparent 55%);
  pointer-events: none;
}
.cw-title { font-size: 1rem; font-weight: 800; color: var(--white); letter-spacing: -0.03em; margin-bottom: 2px; }
.cw-sub   { font-size: 0.63rem; font-weight: 600; font-family: var(--fm); color: var(--t3); letter-spacing: 0.09em; text-transform: uppercase; margin-bottom: 14px; }

/* Courier table */
.ct-row {
  display: grid;
  grid-template-columns: 160px 1fr 72px 78px 70px;
  gap: 10px; align-items: center;
  padding: 10px 14px; border-bottom: 1px solid var(--b-rim);
  font-size: 0.81rem; transition: background 0.15s;
}
.ct-row:hover { background: rgba(255,255,255,0.018); }
.ct-row:last-child { border-bottom: none; }
.ct-hdr  { font-size: 0.6rem; font-family: var(--fm); letter-spacing: 0.1em; text-transform: uppercase; color: var(--t3); background: rgba(255,255,255,0.025); border-radius: 8px 8px 0 0; }
.ct-name { font-weight: 700; color: var(--white); }

/* Progress */
.pb { display: flex; align-items: center; gap: 8px; }
.pb-bg { flex: 1; height: 5px; border-radius: 4px; background: rgba(255,255,255,0.06); overflow: hidden; }
.pb-fill { height: 100%; border-radius: 4px; transition: width 0.7s ease; }

/* Alert */
.al {
  display: flex; gap: 12px; align-items: flex-start;
  background: rgba(255,190,69,0.06); border: 1px solid rgba(255,190,69,0.18);
  border-radius: var(--r); padding: 14px 16px; margin-bottom: 10px;
}
.al.danger  { background: rgba(255,77,106,0.06); border-color: rgba(255,77,106,0.20); }
.al.success { background: rgba(0,255,133,0.06);  border-color: rgba(0,255,133,0.18);  }
.al.info    { background: rgba(0,242,255,0.06);  border-color: rgba(0,242,255,0.18);  }
.al-ico  { font-size: 1.15rem; flex-shrink: 0; margin-top: 1px; }
.al-ttl  { font-size: 0.83rem; font-weight: 700; margin-bottom: 3px; }
.al-body { font-size: 0.75rem; color: var(--t2); line-height: 1.55; }
.al-ttl.danger  { color: var(--red);    }
.al-ttl.success { color: var(--green);  }
.al-ttl.info    { color: var(--cyan);   }
.al-ttl.warn    { color: var(--amber);  }

/* Product rank row */
.pr { display:grid; grid-template-columns:28px 1fr 65px 65px; gap:10px; align-items:center; padding:9px 12px; border-bottom:1px solid var(--b-rim); font-size:0.81rem; transition:background 0.15s; }
.pr:hover { background:rgba(255,255,255,0.018); }
.pr:last-child { border-bottom:none; }
.pr-rank { font-weight:900; font-size:1.05rem; }
.pr-name { font-weight:600; color:var(--white); font-size:0.82rem; }
.pr-sub  { font-size:0.67rem; color:var(--t3); margin-top:2px; }

/* Sidebar nav item */
.snav {
  display: flex; align-items: center; gap: 10px;
  padding: 9px 14px; border-radius: var(--r); margin-bottom: 4px;
  cursor: pointer; transition: all 0.2s; color: var(--t2);
  font-weight: 600; font-size: 0.86rem;
  border: 1px solid transparent;
}
.snav:hover  { background: var(--bg-input); color: var(--t1); }
.snav.active { background: rgba(0,242,255,0.09); color: var(--cyan); border-color: var(--b-cyan); }
.snav-ico { font-size: 1.1rem; width: 24px; text-align: center; }

/* Footer */
.footer {
  margin-top: 48px; padding-top: 20px; border-top: 1px solid var(--b-rim);
  display: flex; justify-content: space-between; align-items: center;
}
.footer-txt { font-family: var(--fm); font-size: 0.62rem; color: var(--t3); letter-spacing: 0.06em; }

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 2 · PLOT LAYOUT BASE
# ─────────────────────────────────────────────────────────────────────────────
PBASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Outfit, sans-serif", color="#9BA3C4", size=11),
    margin=dict(l=2, r=2, t=10, b=4),
    hoverlabel=dict(
        bgcolor="#27293D", bordercolor="rgba(0,242,255,0.3)",
        font=dict(family="JetBrains Mono, monospace", size=12, color="#EAECF4"),
    ),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", zeroline=False,
               tickfont=dict(size=10), linecolor="rgba(255,255,255,0.04)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", zeroline=False,
               tickfont=dict(size=10), linecolor="rgba(255,255,255,0.04)"),
)


# ─────────────────────────────────────────────────────────────────────────────
# 3 · DATOS FICTICIOS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def generate_fake_data():
    rng  = np.random.default_rng(2024)
    hoje = datetime.today()
    N    = 90  # días

    dates      = [hoje - timedelta(days=N-i) for i in range(N)]
    trend      = np.linspace(0, 15_000_000, N)
    seasonal   = 4_000_000 * np.sin(np.linspace(0, 4*np.pi, N))
    noise_v    = rng.normal(0, 2_200_000, N)
    ventas     = np.clip(20_000_000 + trend + seasonal + noise_v, 8_000_000, None)
    pauta      = ventas * rng.uniform(0.11, 0.21, N)
    utilidad   = ventas * rng.uniform(0.27, 0.40, N)
    pedidos    = (ventas / rng.uniform(58_000, 90_000, N)).astype(int)

    ts = pd.DataFrame({
        "fecha":    dates,
        "ventas":   ventas.astype(int),
        "pauta":    pauta.astype(int),
        "utilidad": utilidad.astype(int),
        "pedidos":  pedidos,
    })

    CIUDADES     = ["Bogotá","Medellín","Cali","Barranquilla","Bucaramanga","Cartagena","Pereira","Cúcuta","Santa Marta","Ibagué"]
    TRANSPORTES  = ["Servientrega","Interrapidísimo","TCC","Coordinadora","Envia"]
    PRODUCTOS    = ["Faja Reductora XL","Crema Anticelulítica","Kit Dental Blanqueador","Vitamina C 1000mg","Masaje Cervical Eléctrico","Colágeno 500g","Sérum Retinol","Plancha Rizadora 3en1"]
    ESTATUSES    = ["ENTREGADO","EN REPARTO","CANCELADO","NOVEDAD","BDG PROV"]
    W_EST        = [0.53, 0.21, 0.14, 0.07, 0.05]

    NP = 1_400
    orders = pd.DataFrame({
        "ciudad":         rng.choice(CIUDADES, NP),
        "transportadora": rng.choice(TRANSPORTES, NP),
        "producto":       rng.choice(PRODUCTOS, NP),
        "estatus":        rng.choice(ESTATUSES, NP, p=W_EST),
        "valor":          rng.integers(38_000, 310_000, NP),
        "flete":          rng.integers(7_500, 42_000, NP),
        "dias":           rng.integers(1, 15, NP),
    })
    return ts, orders

ts, orders = generate_fake_data()


# ─────────────────────────────────────────────────────────────────────────────
# 4 · KPI RESUMEN
# ─────────────────────────────────────────────────────────────────────────────
T  = len(orders)
ent = (orders.estatus == "ENTREGADO").sum()
can = (orders.estatus == "CANCELADO").sum()
rep = (orders.estatus == "EN REPARTO").sum()
nov = (orders.estatus == "NOVEDAD").sum()
bdg = (orders.estatus == "BDG PROV").sum()

tasa_ent  = round(ent / T * 100, 1)
tasa_can  = round(can / T * 100, 1)
tasa_con  = round((T - can) / T * 100, 1)
tasa_dev  = round(nov / T * 100, 1)

v_total   = int(ts.ventas.sum())
u_total   = int(ts.utilidad.sum())
p_total   = int(ts.pauta.sum())
margen    = round(u_total / v_total * 100, 1)
roas      = round(v_total / p_total, 2)
ticket    = int(orders.valor.mean())
flete_avg = int(orders.flete.mean())


# ─────────────────────────────────────────────────────────────────────────────
# 5 · SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:8px 0 20px">
      <div style="font-family:'Outfit',sans-serif;font-size:1.2rem;font-weight:900;color:#EAECF4;letter-spacing:-0.04em">Mercado<em style="color:#00F2FF">Creativo</em></div>
      <div style="font-size:0.62rem;color:#4E5474;font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:0.1em;margin-top:2px">Dashboard PCR · v3.0</div>
    </div>
    <div style="height:1px;background:rgba(255,255,255,0.06);margin-bottom:20px"></div>
    """, unsafe_allow_html=True)

    nav_items = [
        ("⬡", "Panel Principal",    True),
        ("◈", "Monitor de Pedidos", False),
        ("◉", "Transportadoras",    False),
        ("◌", "Productos",          False),
        ("◍", "Ciudades",           False),
        ("○", "Configuración",      False),
    ]
    for ico, label, active in nav_items:
        css = "active" if active else ""
        st.markdown(f'<div class="snav {css}"><span class="snav-ico">{ico}</span>{label}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.6rem;color:#4E5474;font-family:JetBrains Mono;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:12px">Filtros rápidos</div>', unsafe_allow_html=True)

    ciudad_sb  = st.selectbox("Ciudad", ["Todas"] + sorted(orders.ciudad.unique().tolist()))
    trans_sb   = st.selectbox("Transportadora", ["Todas"] + sorted(orders.transportadora.unique().tolist()))
    prod_sb    = st.selectbox("Producto", ["Todos"] + sorted(orders.producto.unique().tolist()))

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    # Resumen lateral
    st.markdown(f"""
    <div style="background:rgba(0,242,255,0.06);border:1px solid rgba(0,242,255,0.15);border-radius:12px;padding:14px">
      <div style="font-size:0.6rem;font-family:JetBrains Mono;color:#4E5474;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px">Snapshot hoy</div>
      <div style="display:flex;justify-content:space-between;margin-bottom:6px">
        <span style="font-size:0.77rem;color:#9BA3C4">Total pedidos</span>
        <span style="font-family:JetBrains Mono;font-size:0.8rem;color:#00F2FF;font-weight:700">{T:,}</span>
      </div>
      <div style="display:flex;justify-content:space-between;margin-bottom:6px">
        <span style="font-size:0.77rem;color:#9BA3C4">Entregados</span>
        <span style="font-family:JetBrains Mono;font-size:0.8rem;color:#00FF85;font-weight:700">{ent:,}</span>
      </div>
      <div style="display:flex;justify-content:space-between;margin-bottom:6px">
        <span style="font-size:0.77rem;color:#9BA3C4">Cancelados</span>
        <span style="font-family:JetBrains Mono;font-size:0.8rem;color:#FF4D6A;font-weight:700">{can:,}</span>
      </div>
      <div style="display:flex;justify-content:space-between">
        <span style="font-size:0.77rem;color:#9BA3C4">En tránsito</span>
        <span style="font-family:JetBrains Mono;font-size:0.8rem;color:#FFBE45;font-weight:700">{rep+bdg:,}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 6 · FILTRO
# ─────────────────────────────────────────────────────────────────────────────
df = orders.copy()
if ciudad_sb != "Todas": df = df[df.ciudad == ciudad_sb]
if trans_sb  != "Todas": df = df[df.transportadora == trans_sb]
if prod_sb   != "Todos": df = df[df.producto == prod_sb]


# ─────────────────────────────────────────────────────────────────────────────
# 7 · TOP BAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
  <div class="brand-wrap">
    <div class="brand-icon">⬡</div>
    <div>
      <div class="brand-name">Mercado<em>Creativo</em></div>
      <div class="brand-sub">Pago Contra Reembolso · Panel de Operaciones</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:10px">
    <div class="badge-live">En Vivo</div>
    <div class="badge-ts">{datetime.now().strftime('%d %b %Y · %H:%M')}</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# helper
# ─────────────────────────────────────────────────────────────────────────────
def sec(label, color):
    st.markdown(f"""
    <div class="sec-div">
      <div class="sec-div-dot" style="background:{color};box-shadow:0 0 8px {color}88"></div>
      <div class="sec-div-label">{label}</div>
      <div class="sec-div-line"></div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 8 · INDICADORES CIRCULARES  (go.Indicator / gauge ring)
# ─────────────────────────────────────────────────────────────────────────────
sec("Indicadores Clave de Rendimiento", "#00F2FF")

def ring(value, title, bar_color, max_v=100, suffix="%", reference=None):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta" if reference else "gauge+number",
        value=value,
        number=dict(
            suffix=suffix,
            font=dict(family="Outfit, sans-serif", size=40, color="#EAECF4"),
            valueformat=".1f",
        ),
        delta=dict(
            reference=reference,
            increasing=dict(color="#00FF85"),
            decreasing=dict(color="#FF4D6A"),
            font=dict(size=13, family="JetBrains Mono"),
        ) if reference else None,
        title=dict(
            text=f"<span style='font-family:JetBrains Mono;font-size:10px;color:#4E5474;text-transform:uppercase;letter-spacing:0.12em'>{title}</span>",
        ),
        gauge=dict(
            axis=dict(range=[0, max_v], visible=False, showticklabels=False),
            bar=dict(color=bar_color, thickness=0.28, line=dict(width=0, color="rgba(0,0,0,0)")),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            steps=[dict(range=[0, max_v], color="rgba(255,255,255,0.05)")],
            threshold=dict(line=dict(color=bar_color, width=3), thickness=0.32, value=value),
        ),
    ))
    fig.update_layout(
        **{k: v for k, v in PBASE.items() if k not in ("xaxis", "yaxis")},
        height=215,
        margin=dict(l=22, r=22, t=30, b=8),
        xaxis=dict(visible=False), yaxis=dict(visible=False),
    )
    return fig

ring_data = [
    (tasa_ent,  "Tasa de Entrega",      "#00F2FF", tasa_ent-3),
    (tasa_con,  "Tasa de Confirmación", "#00FF85", tasa_con-2),
    (tasa_dev,  "Tasa de Devolución",   "#FF4D6A", None),
    (margen,    "Margen de Ganancia",   "#FFBE45", margen-2),
]

r_cols = st.columns(4)
for col, (val, tit, clr, ref) in zip(r_cols, ring_data):
    with col:
        st.markdown('<div class="cw" style="padding:12px 8px 6px">', unsafe_allow_html=True)
        st.plotly_chart(ring(val, tit, clr, reference=ref),
                        use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 9 · KPI CARDS  (6 métricas)
# ─────────────────────────────────────────────────────────────────────────────
sec("Resumen Financiero & Operacional", "#00FF85")

kpis = [
    ("Ventas Totales",  f"${v_total/1e6:.1f}M",  "▲ +18.4% vs mes ant.", "pos", "c", "💰"),
    ("Utilidad Neta",   f"${u_total/1e6:.1f}M",  f"Margen {margen}%",    "pos", "g", "📈"),
    ("Inversión Pauta", f"${p_total/1e6:.1f}M",  f"ROAS {roas}×",        "neu", "i", "📣"),
    ("Ticket Promedio", f"${ticket:,}",           "por pedido",           "neu", "v", "🛍"),
    ("Flete Promedio",  f"${flete_avg:,}",        f"{tasa_dev:.1f}% novedades","neg","r","🚚"),
    ("En Tránsito",     f"{rep+bdg:,}",           "pedidos activos",      "neu", "a", "📦"),
]
k_cols = st.columns(6)
for col, (lbl, val, sub, sub_c, css, ico) in zip(k_cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kcard {css}">
          <div class="kcard-ico">{ico}</div>
          <div class="kcard-lbl">{lbl}</div>
          <div class="kcard-val">{val}</div>
          <div class="kcard-sub {sub_c}">{sub}</div>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 10 · GRÁFICOS PRINCIPALES  (3 columnas)
# ─────────────────────────────────────────────────────────────────────────────
sec("Análisis de Ventas · Estatus de Pedidos · Transportadoras", "#636EFA")

ga, gb, gc = st.columns([2.4, 1.2, 1.4])

# ── GA: ÁREA — Ventas vs Pauta ───────────────────────────────────────────────
with ga:
    st.markdown('<div class="cw">', unsafe_allow_html=True)
    st.markdown('<div class="cw-title">Ventas vs Inversión en Pauta</div><div class="cw-sub">Tendencia diaria · últimos 90 días</div>', unsafe_allow_html=True)

    ts_sm = ts.copy()
    ts_sm["v_sm"] = ts_sm.ventas.rolling(6, center=True).mean().fillna(ts_sm.ventas)
    ts_sm["p_sm"] = ts_sm.pauta.rolling(6, center=True).mean().fillna(ts_sm.pauta)
    ts_sm["u_sm"] = ts_sm.utilidad.rolling(6, center=True).mean().fillna(ts_sm.utilidad)

    fa = go.Figure()
    # Relleno sutil cyan
    fa.add_trace(go.Scatter(
        x=ts_sm.fecha, y=ts_sm.v_sm, name="Ventas",
        mode="lines", fill="tozeroy",
        fillcolor="rgba(0,242,255,0.07)",
        line=dict(color="#00F2FF", width=2.8),
        hovertemplate="<b>%{x|%d %b}</b><br>Ventas: $%{y:,.0f}<extra></extra>",
    ))
    # Pauta punteada amber
    fa.add_trace(go.Scatter(
        x=ts_sm.fecha, y=ts_sm.p_sm, name="Pauta",
        mode="lines", fill="tozeroy",
        fillcolor="rgba(255,190,69,0.05)",
        line=dict(color="#FFBE45", width=1.8, dash="dot"),
        hovertemplate="<b>%{x|%d %b}</b><br>Pauta: $%{y:,.0f}<extra></extra>",
    ))
    # Utilidad emerald
    fa.add_trace(go.Scatter(
        x=ts_sm.fecha, y=ts_sm.u_sm, name="Utilidad",
        mode="lines",
        line=dict(color="#00FF85", width=1.6),
        hovertemplate="<b>%{x|%d %b}</b><br>Utilidad: $%{y:,.0f}<extra></extra>",
    ))

    fa.update_layout(
        **PBASE, height=295,
        legend=dict(orientation="h", x=0, y=-0.20, font=dict(size=10)),
        yaxis=dict(tickprefix="$", tickformat=".2s", gridcolor="rgba(255,255,255,0.04)", zeroline=False),
        xaxis=dict(showgrid=False, tickformat="%d %b", tickfont=dict(size=9)),
        margin=dict(l=2, r=2, t=4, b=4),
    )
    st.plotly_chart(fa, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── GB: BARRAS HORIZONTALES — Estatus ────────────────────────────────────────
with gb:
    st.markdown('<div class="cw">', unsafe_allow_html=True)
    st.markdown('<div class="cw-title">Estado de Pedidos</div><div class="cw-sub">Distribución actual filtrada</div>', unsafe_allow_html=True)

    sts = df.estatus.value_counts().reset_index()
    sts.columns = ["Estatus", "Cnt"]
    C_MAP = {"ENTREGADO":"#00FF85","EN REPARTO":"#00F2FF","CANCELADO":"#FF4D6A","NOVEDAD":"#FFBE45","BDG PROV":"#B39DDB"}
    sts["clr"] = sts.Estatus.map(C_MAP).fillna("#636EFA")

    fb = go.Figure()
    for _, row in sts.iterrows():
        fb.add_trace(go.Bar(
            x=[row.Cnt], y=[row.Estatus], orientation="h", name=row.Estatus,
            marker=dict(color=row.clr, opacity=0.88, line=dict(width=0)),
            text=f"  {row.Cnt:,}", textposition="outside",
            textfont=dict(color=row.clr, size=11, family="JetBrains Mono"),
            hovertemplate=f"<b>{row.Estatus}</b><br>Pedidos: {row.Cnt:,}<extra></extra>",
        ))

    fb.update_layout(
        **PBASE, height=295, showlegend=False, barmode="overlay",
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, tickfont=dict(size=10, color="#9BA3C4")),
        margin=dict(l=2, r=30, t=4, b=4),
    )
    st.plotly_chart(fb, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── GC: BARRAS AGRUPADAS — Transportadoras ───────────────────────────────────
with gc:
    st.markdown('<div class="cw">', unsafe_allow_html=True)
    st.markdown('<div class="cw-title">Transportadoras</div><div class="cw-sub">Entrega vs Cancelación (%)</div>', unsafe_allow_html=True)

    ts_g = df.groupby("transportadora").apply(lambda x: pd.Series({
        "Entrega":     round(len(x[x.estatus=="ENTREGADO"]) / len(x) * 100, 1),
        "Cancelación": round(len(x[x.estatus=="CANCELADO"]) / len(x) * 100, 1),
        "Novedad":     round(len(x[x.estatus=="NOVEDAD"])   / len(x) * 100, 1),
    })).reset_index()

    fc = go.Figure()
    for serie, clr in [("Entrega","#00FF85"),("Cancelación","#FF4D6A"),("Novedad","#FFBE45")]:
        fc.add_trace(go.Bar(
            x=ts_g.transportadora, y=ts_g[serie], name=serie,
            marker=dict(color=clr, opacity=0.85, line=dict(width=0)),
            hovertemplate=f"<b>%{{x}}</b><br>{serie}: %{{y:.1f}}%<extra></extra>",
        ))

    fc.update_layout(
        **PBASE, height=295, barmode="group",
        legend=dict(orientation="h", x=0, y=-0.22, font=dict(size=9)),
        xaxis=dict(tickfont=dict(size=8), showgrid=False),
        yaxis=dict(ticksuffix="%", gridcolor="rgba(255,255,255,0.04)", zeroline=False),
        margin=dict(l=2, r=2, t=4, b=4),
    )
    st.plotly_chart(fc, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 11 · TABLA TRANSPORTADORAS + ALERTAS
# ─────────────────────────────────────────────────────────────────────────────
sec("Rendimiento por Transportadora · Alertas del Sistema", "#FF3CAC")

tc, ac = st.columns([2.0, 1.0])

with tc:
    st.markdown('<div class="cw">', unsafe_allow_html=True)
    st.markdown('<div class="cw-title">Detalle de Transportadoras</div><div class="cw-sub">Pedidos · tasa · flete · tiempo de entrega</div>', unsafe_allow_html=True)

    td = df.groupby("transportadora").agg(
        Pedidos=("transportadora","count"),
        Entregados=("estatus", lambda x: (x=="ENTREGADO").sum()),
        Cancelados=("estatus", lambda x: (x=="CANCELADO").sum()),
        Flete=("flete","mean"),
        Dias=("dias","mean"),
    ).reset_index().sort_values("Pedidos", ascending=False)
    td["Tasa"] = round(td.Entregados / td.Pedidos * 100, 1)

    st.markdown("""
    <div class="ct-row ct-hdr">
      <div>Transportadora</div><div>Tasa de entrega</div>
      <div>Pedidos</div><div>Flete prom.</div><div>Días prom.</div>
    </div>""", unsafe_allow_html=True)

    for _, r in td.iterrows():
        p   = r["Tasa"]
        clr = "#00FF85" if p >= 55 else "#FFBE45" if p >= 40 else "#FF4D6A"
        st.markdown(f"""
        <div class="ct-row">
          <div class="ct-name">{r['transportadora']}</div>
          <div>
            <div class="pb">
              <div class="pb-bg"><div class="pb-fill" style="width:{p}%;background:{clr};box-shadow:0 0 7px {clr}88"></div></div>
              <span style="font-family:JetBrains Mono;font-size:0.73rem;color:{clr};font-weight:700;min-width:40px">{p}%</span>
            </div>
          </div>
          <div style="color:#9BA3C4;font-family:JetBrains Mono;font-size:0.78rem">{r['Pedidos']:,}</div>
          <div style="color:#9BA3C4;font-family:JetBrains Mono;font-size:0.78rem">${r['Flete']:,.0f}</div>
          <div style="color:#9BA3C4;font-family:JetBrains Mono;font-size:0.78rem">{r['Dias']:.1f}d</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with ac:
    st.markdown('<div class="cw" style="height:100%">', unsafe_allow_html=True)
    st.markdown('<div class="cw-title">🔔 Alertas del Sistema</div><div class="cw-sub">Tiempo real · acción requerida</div>', unsafe_allow_html=True)

    alerts = [
        ("danger",  "⛔", "Cancelación Crítica",
         f"Tasa {tasa_can:.1f}% supera el umbral del 12%. Revisar proceso de confirmación inmediatamente."),
        ("warn",    "🚚", "Novedades Sin Resolver",
         f"{nov:,} pedidos con novedad activa. Contactar transportadoras."),
        ("success", "✅", "Meta de Entrega",
         f"Tasa de entrega {tasa_ent:.1f}% — por encima de la meta del 50%."),
        ("info",    "📊", f"ROAS · {roas}×",
         f"Retorno sobre pauta aceptable. Meta: 3.5×. Revisar creativos con menor rendimiento."),
    ]
    for tipo, ico, ttl, msg in alerts:
        al_css = "danger" if tipo=="danger" else "success" if tipo=="success" else "info" if tipo=="info" else ""
        ttl_css = tipo if tipo in ("danger","success","info") else "warn"
        st.markdown(f"""
        <div class="al {al_css}">
          <div class="al-ico">{ico}</div>
          <div>
            <div class="al-ttl {ttl_css}">{ttl}</div>
            <div class="al-body">{msg}</div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 12 · TOP PRODUCTOS + MAPA CIUDADES
# ─────────────────────────────────────────────────────────────────────────────
sec("Top Productos & Distribución Geográfica", "#B39DDB")

pc, cc = st.columns(2)

with pc:
    st.markdown('<div class="cw">', unsafe_allow_html=True)
    st.markdown('<div class="cw-title">🏆 Top Productos por Pedidos</div><div class="cw-sub">Filtro activo · volumen + tasa</div>', unsafe_allow_html=True)

    tp = df.groupby("producto").agg(
        Pedidos=("producto","count"),
        Entregados=("estatus", lambda x: (x=="ENTREGADO").sum()),
        Valor=("valor","sum"),
    ).reset_index().sort_values("Pedidos", ascending=False).head(8)
    tp["Tasa"] = round(tp.Entregados / tp.Pedidos * 100, 0).astype(int)
    tot_p = tp.Pedidos.sum()

    PCLRS = ["#00F2FF","#00FF85","#FFBE45","#FF4D6A","#B39DDB","#636EFA","#FF3CAC","#FFCB57"]
    for rank, (_, r) in enumerate(tp.iterrows()):
        pct  = r.Pedidos / tot_p * 100
        clr  = PCLRS[rank % len(PCLRS)]
        t_clr = "#00FF85" if r.Tasa > 55 else "#FFBE45" if r.Tasa > 40 else "#FF4D6A"
        st.markdown(f"""
        <div class="pr">
          <div class="pr-rank" style="color:{clr}">{rank+1}</div>
          <div>
            <div class="pr-name">{r.producto}</div>
            <div class="pb" style="margin-top:4px">
              <div class="pb-bg"><div class="pb-fill" style="width:{pct:.0f}%;background:{clr};opacity:0.65"></div></div>
              <span style="font-size:0.67rem;color:{clr};font-family:JetBrains Mono;min-width:30px">{pct:.0f}%</span>
            </div>
          </div>
          <div style="text-align:right;font-family:JetBrains Mono;font-size:0.77rem;color:#9BA3C4">{r.Pedidos:,}</div>
          <div style="text-align:right;font-size:0.73rem;color:{t_clr};font-weight:700">{r.Tasa}% ent.</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with cc:
    st.markdown('<div class="cw">', unsafe_allow_html=True)
    st.markdown('<div class="cw-title">📍 Pedidos por Ciudad</div><div class="cw-sub">Color = tasa de entrega</div>', unsafe_allow_html=True)

    cs = df.groupby("ciudad").agg(
        Pedidos=("ciudad","count"),
        Entregados=("estatus", lambda x: (x=="ENTREGADO").sum()),
        Flete=("flete","mean"),
    ).reset_index().sort_values("Pedidos", ascending=False)
    cs["Tasa"] = round(cs.Entregados / cs.Pedidos * 100, 1)

    fd = go.Figure(go.Bar(
        x=cs.ciudad, y=cs.Pedidos,
        marker=dict(
            color=cs.Tasa,
            colorscale=[[0,"#FF4D6A"],[0.45,"#FFBE45"],[1,"#00FF85"]],
            showscale=True, colorbar=dict(
                thickness=7, len=0.75, title=dict(text="Tasa %", font=dict(size=9, color="#4E5474")),
                tickfont=dict(size=9, color="#9BA3C4"), x=1.02,
            ),
            line=dict(width=0),
        ),
        text=cs.Pedidos, textposition="outside",
        textfont=dict(size=9, color="#9BA3C4", family="JetBrains Mono"),
        hovertemplate="<b>%{x}</b><br>Pedidos: %{y:,}<br>Tasa entrega: %{marker.color:.1f}%<extra></extra>",
    ))
    fd.update_layout(
        **PBASE, height=310,
        xaxis=dict(tickfont=dict(size=9), showgrid=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        margin=dict(l=2, r=30, t=4, b=4),
    )
    st.plotly_chart(fd, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 13 · TABLA EXPLORER
# ─────────────────────────────────────────────────────────────────────────────
sec("Explorador de Pedidos", "#00F2FF")

with st.expander(f"📋  Ver todos los pedidos filtrados  ·  {len(df):,} registros", expanded=False):
    show = df[["ciudad","transportadora","producto","estatus","valor","flete","dias"]].copy()
    show.columns = ["Ciudad","Transportadora","Producto","Estatus","Valor $","Flete $","Días"]
    st.dataframe(
        show,
        use_container_width=True,
        height=370,
        column_config={
            "Valor $":  st.column_config.NumberColumn(format="$%d"),
            "Flete $":  st.column_config.NumberColumn(format="$%d"),
            "Días":     st.column_config.NumberColumn("Días entrega"),
        },
    )


# ─────────────────────────────────────────────────────────────────────────────
# 14 · FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <div class="footer-txt">MERCADO CREATIVO · DASHBOARD PCR v3.0 · PANEL DE OPERACIONES</div>
  <div class="footer-txt">ÚLTIMA ACTUALIZACIÓN · {datetime.now().strftime('%d %b %Y %H:%M:%S')}</div>
</div>
""", unsafe_allow_html=True)
