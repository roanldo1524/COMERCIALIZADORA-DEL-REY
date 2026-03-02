import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="VisióN360",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── TOKENS DE DISEÑO PURPLE INFOGRAPHIC ── */
:root {
    --bg:           #0d0a1a;
    --bg-deep:      #080612;
    --bg-card:      #13102a;
    --bg-card-2:    #1a1535;
    --bg-card-3:    #201a40;
    --bg-hover:     #211c42;
    --border:       #2e2558;
    --border-2:     #3d3470;
    --border-glow:  rgba(139,92,246,0.35);
    --primary:      #7c3aed;
    --primary-2:    #9333ea;
    --primary-3:    #a855f7;
    --magenta:      #e040fb;
    --pink:         #f472b6;
    --cyan:         #22d3ee;
    --orange:       #fb923c;
    --success:      #34d399;
    --warning:      #fbbf24;
    --danger:       #f87171;
    --gold:         #fcd34d;
    --glow-purple:  rgba(124,58,237,0.2);
    --glow-magenta: rgba(224,64,251,0.15);
    --text-1:       #f0ecff;
    --text-2:       #b8b0d8;
    --text-3:       #8878b8;
    --font-display: 'Plus Jakarta Sans', sans-serif;
    --font-body:    'DM Sans', sans-serif;
    --font-mono:    'DM Mono', monospace;
    --r-sm:  10px;
    --r-md:  14px;
    --r-lg:  18px;
    --r-xl:  24px;
    --shadow: 0 4px 24px rgba(0,0,0,0.5);
    --shadow-card: 0 2px 20px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04);
    --shadow-glow: 0 0 40px rgba(124,58,237,0.18);
}

/* ── BASE ── */
html, body, [class*="css"] {
    font-family: var(--font-body);
    color: var(--text-1);
}

.stApp {
    background-color: var(--bg-deep);
    background-image:
        radial-gradient(ellipse 90% 60% at 15% 0%,   rgba(124,58,237,0.22)  0%, transparent 55%),
        radial-gradient(ellipse 70% 50% at 85% 0%,   rgba(168,85,247,0.12)  0%, transparent 50%),
        radial-gradient(ellipse 60% 40% at 50% 100%, rgba(224,64,251,0.10)  0%, transparent 55%),
        radial-gradient(ellipse 40% 30% at 100% 50%, rgba(34,211,238,0.06)  0%, transparent 45%);
}
.block-container { padding: 1.4rem 2rem; max-width: 100% !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #100d22 0%, #0d0a1a 60%, #080612 100%);
    border-right: 1px solid var(--border);
    box-shadow: 4px 0 32px rgba(0,0,0,0.5);
}
section[data-testid="stSidebar"] * { color: var(--text-1) !important; }
section[data-testid="stSidebar"] .stRadio label {
    padding: 8px 12px !important;
    border-radius: var(--r-sm) !important;
    transition: all 0.2s !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    color: var(--text-2) !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(124,58,237,0.15) !important;
    color: var(--text-1) !important;
}

/* ── TIPOGRAFÍA ── */
h1, h2, h3, .display {
    font-family: var(--font-display) !important;
    letter-spacing: -0.02em;
    color: var(--text-1) !important;
}

/* ══════════════════════════════════════
   TARJETAS KPI — estilo cuadrito premium
══════════════════════════════════════ */
.kpi {
    background: linear-gradient(145deg, var(--bg-card-2) 0%, var(--bg-card) 100%);
    border: 1px solid var(--border);
    border-radius: var(--r-lg);
    padding: 20px 16px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
    box-shadow: var(--shadow-card);
}
/* Textura cuadrícula sutil */
.kpi::after {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.018) 1px, transparent 1px);
    background-size: 20px 20px;
    pointer-events: none;
    border-radius: var(--r-lg);
}
/* Brillo superior */
.kpi::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: var(--r-lg) var(--r-lg) 0 0;
    z-index: 1;
}
.kpi:hover {
    transform: translateY(-3px);
    border-color: var(--border-2);
    box-shadow: var(--shadow-glow);
}
.kpi.gold::before   { background: linear-gradient(90deg, #f59e0b, #fcd34d, #fb923c); }
.kpi.green::before  { background: linear-gradient(90deg, #10b981, #34d399); }
.kpi.red::before    { background: linear-gradient(90deg, #ef4444, #f87171); }
.kpi.blue::before   { background: linear-gradient(90deg, var(--primary), var(--primary-3)); }
.kpi.purple::before { background: linear-gradient(90deg, var(--primary-2), var(--magenta)); }
.kpi.cyan::before   { background: linear-gradient(90deg, var(--cyan), #67e8f9); }

.kpi-num {
    font-family: var(--font-display);
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--text-1);
    margin: 8px 0 4px;
    letter-spacing: -0.03em;
    line-height: 1;
}
.kpi-label {
    font-family: var(--font-body);
    font-size: 0.67rem;
    color: var(--text-2);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.kpi-sub { font-size: 0.77rem; color: var(--success); font-weight: 500; margin-top: 5px; }

/* ══════════════════════════════════════
   CARDS SECCIÓN — cuadrícula premium
══════════════════════════════════════ */
.prod-card {
    background: linear-gradient(135deg, var(--bg-card-2) 0%, var(--bg-card) 100%);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    padding: 14px 16px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 14px;
    position: relative;
    overflow: hidden;
    transition: all 0.2s;
    box-shadow: var(--shadow-card);
}
.prod-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
    background-size: 16px 16px;
    pointer-events: none;
}
.prod-card:hover { border-color: var(--border-glow); transform: translateX(3px); }
.prod-rank {
    font-family: var(--font-display);
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--gold);
    min-width: 36px;
}
.prod-name { font-size: 0.87rem; font-weight: 600; color: var(--text-1); }
.prod-val  { font-size: 0.75rem; color: var(--text-2); margin-top: 2px; }

/* ── ALERTAS ── */
.alerta-r {
    background: rgba(248,113,113,0.07);
    border: 1px solid rgba(248,113,113,0.22);
    border-left: 3px solid #f87171;
    border-radius: var(--r-sm);
    padding: 10px 14px;
    margin: 5px 0;
    font-size: 0.82rem;
    color: var(--text-1);
}
.alerta-a {
    background: rgba(251,191,36,0.07);
    border: 1px solid rgba(251,191,36,0.2);
    border-left: 3px solid #fbbf24;
    border-radius: var(--r-sm);
    padding: 10px 14px;
    margin: 5px 0;
    font-size: 0.82rem;
    color: var(--text-1);
}

/* ── INSIGHT CARD ── */
.insight {
    background: linear-gradient(135deg, var(--bg-card-2), var(--bg-card));
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    padding: 18px;
    margin-bottom: 10px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-card);
}
.insight::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.012) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.012) 1px, transparent 1px);
    background-size: 18px 18px;
    pointer-events: none;
}
.insight-titulo {
    font-family: var(--font-display);
    font-size: 0.9rem;
    color: var(--gold);
    font-weight: 700;
    margin-bottom: 7px;
    letter-spacing: -0.01em;
}
.insight-texto { font-size: 0.83rem; color: var(--text-2); line-height: 1.65; }

/* ── BADGES ── */
.badge-r { background:rgba(248,113,113,0.12); color:#fca5a5; border:1px solid rgba(248,113,113,0.3); border-radius:20px; padding:2px 10px; font-size:0.7rem; font-weight:700; }
.badge-a { background:rgba(251,191,36,0.12);  color:#fef08a; border:1px solid rgba(251,191,36,0.3);  border-radius:20px; padding:2px 10px; font-size:0.7rem; font-weight:700; }
.badge-v { background:rgba(52,211,153,0.12);  color:#6ee7b7; border:1px solid rgba(52,211,153,0.3);  border-radius:20px; padding:2px 10px; font-size:0.7rem; font-weight:700; }
.badge-g { background:rgba(252,211,77,0.12);  color:#fef08a; border:1px solid rgba(252,211,77,0.3);  border-radius:20px; padding:2px 10px; font-size:0.7rem; font-weight:700; }

/* ── SECCIÓN TÍTULO ── */
.seccion-titulo {
    font-family: var(--font-display);
    font-size: 1.2rem;
    font-weight: 800;
    color: var(--text-1);
    border-bottom: 1px solid var(--border);
    padding-bottom: 10px;
    margin: 22px 0 15px 0;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #f0ecff, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── TABS STREAMLIT ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: var(--r-md) !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: var(--r-sm) !important;
    color: var(--text-2) !important;
    font-family: var(--font-body) !important;
    font-size: 0.81rem !important;
    font-weight: 600 !important;
    padding: 8px 14px !important;
    transition: all 0.18s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary), var(--magenta)) !important;
    color: #fff !important;
    box-shadow: 0 2px 16px rgba(124,58,237,0.4) !important;
}

/* ── INPUTS ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    color: var(--text-1) !important;
}
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    color: var(--text-1) !important;
    font-family: var(--font-mono) !important;
}

/* ── BOTONES ── */
.stButton > button {
    background: linear-gradient(135deg, var(--primary), var(--magenta)) !important;
    border: none !important;
    border-radius: var(--r-sm) !important;
    color: #fff !important;
    font-family: var(--font-body) !important;
    font-weight: 700 !important;
    font-size: 0.83rem !important;
    padding: 9px 20px !important;
    transition: all 0.18s !important;
    box-shadow: 0 2px 16px rgba(124,58,237,0.3) !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(224,64,251,0.4) !important;
}

/* ── TABLA ── */
.stDataFrame {
    border-radius: var(--r-lg) !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
}

/* ── UPLOADER ── */
.stFileUploader {
    background: var(--bg-card) !important;
    border: 2px dashed var(--border-2) !important;
    border-radius: var(--r-lg) !important;
}
.stFileUploader:hover { border-color: var(--primary) !important; }

/* ── EXPANDERS ── */
.stExpander {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-md) !important;
    box-shadow: var(--shadow-card) !important;
}

/* ── MÉTRICAS ── */
div[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    font-weight: 800 !important;
    color: var(--text-1) !important;
}
div[data-testid="stMetricLabel"] {
    font-family: var(--font-body) !important;
    color: var(--text-2) !important;
}

/* ── LEGIBILIDAD WIDGETS ── */
label, .stRadio label, .stSelectbox label, .stMultiSelect label,
.stNumberInput label, .stTextInput label, .stSlider label,
div[data-testid="stWidgetLabel"] p,
div[data-testid="stWidgetLabel"], p, li {
    color: #d4ccf0 !important;
    font-family: var(--font-body) !important;
}
.stRadio [data-testid="stMarkdownContainer"] p {
    color: #d4ccf0 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}
.stRadio div[role="radiogroup"] label span { color: #d4ccf0 !important; }
.stSelectbox div[data-baseweb="select"] span,
.stSelectbox div[data-baseweb="select"] div { color: #f0ecff !important; }
small, .stCaption, div[data-testid="stCaptionContainer"] { color: #a098c8 !important; }
.stExpander summary p, .stExpander details summary span {
    color: #d4ccf0 !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab"] { color: #b0a8d8 !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--border-2); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }

hr { border-color: var(--border) !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# COLUMNAS EXACTAS DROPI
# ═══════════════════════════════════════════════════════════
C_FECHA     = "FECHA"
C_FECHA_MOV = "FECHA DE ÚLTIMO MOVIMIENTO"
C_ID        = "ID"
C_GUIA      = "NÚMERO GUIA"
C_ESTATUS   = "ESTATUS"
C_CLIENTE   = "NOMBRE CLIENTE"
C_DEPTO     = "DEPARTAMENTO DESTINO"
C_CIUDAD    = "CIUDAD DESTINO"
C_DIRECCION = "DIRECCION"
C_TRANSP    = "TRANSPORTADORA"
C_TOTAL     = "TOTAL DE LA ORDEN"
C_GANANCIA  = "GANANCIA"
C_FLETE     = "PRECIO FLETE"
C_PRODUCTO  = "PRODUCTO"
C_VARIACION = "VARIACION"
C_CANTIDAD  = "CANTIDAD"
C_TAGS      = "TAGS"
C_NOVEDAD   = "NOVEDAD"
C_ESTATUS_FIN = "ESTATUS FINANCIERO"
C_NOV_SOL   = "FUE SOLUCIONADA LA NOVEDAD"
C_TIENDA    = "TIENDA"
C_VENDEDOR  = "VENDEDOR"
C_INDEMN    = "CONTADOR DE INDEMNIZACIONES"
C_ULT_MOV   = "ÚLTIMO MOVIMIENTO"

# ═══════════════════════════════════════════════════════════
# TAGS
# ═══════════════════════════════════════════════════════════
TAGS_SEG = ["prioridad de rastreo","en proceso indemnizacion","en proceso indemnización","reclamo en oficinas","cambios de estatus","cambios de estado"]
TAGS_EST = ["por flete elevado","cancelado por proveedor","cancelado por stock"]
TAGS_CR  = ["cancelado por el cliente","cancelado por cliente - viajes","cancelado por reseñas","cancelado por precio","cancelado por datos incompletos","cancelado por alta devolucion","cancelado por alta devolución","sin cobertura","no abonaron"]
TAGS_NCR = ["se vuelve a subir","cancelado por pedido repetido","de pruebas"]
TAGS_INF = ["duplicado entre tiendas","recompra","garantia","garantía","dinero","reprogramada","confirmaciones erradas","pendiente por subir"]

def clasificar_tag(tag):
    t = tag.lower().strip()
    if any(x in t for x in TAGS_SEG):  return 'seguimiento'
    if any(x in t for x in TAGS_EST):  return 'estrategico'
    if any(x in t for x in TAGS_CR):   return 'cancelacion_real'
    if any(x in t for x in TAGS_NCR):  return 'no_cancelacion'
    if any(x in t for x in TAGS_INF):  return 'informativo'
    return 'otro'

def parse_tags(val):
    if pd.isna(val) or str(val).strip() == '': return []
    return [t.strip() for t in str(val).split(',') if t.strip()]

def horas_desde(fecha):
    try:
        if pd.isna(fecha): return None
        return (datetime.now() - pd.to_datetime(fecha)).total_seconds() / 3600
    except: return None

def fmt_money(n):
    if n >= 1e9:  return f"${n/1e9:.2f}B"
    if n >= 1e6:  return f"${n/1e6:.1f}M"
    return f"${n:,.0f}"

def kpi(color, label, num, sub=""):
    s = f'<div class="kpi-sub">{sub}</div>' if sub else ''
    return f'<div class="kpi {color}"><div class="kpi-label">{label}</div><div class="kpi-num">{num}</div>{s}</div>'

PLOT_LAYOUT = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color='#d4ccf0', size=12),
    title_font=dict(family='Plus Jakarta Sans', color='#f0ecff', size=15),
    legend=dict(font=dict(color='#c8c0e8', size=11), bgcolor='rgba(0,0,0,0)'),
    margin=dict(l=10, r=10, t=48, b=10)
)
AXIS_STYLE = dict(gridcolor='#2e2558', linecolor='#2e2558', tickfont=dict(color='#a098c8', family='DM Mono'))
COLORES_ELEGANTES = ['#a855f7','#34d399','#fcd34d','#f87171','#22d3ee','#e040fb','#fbbf24','#f472b6','#14b8a6','#fb923c']

# ═══════════════════════════════════════════════════════════
# SIDEBAR — Purple Premium Style
# ═══════════════════════════════════════════════════════════

# CSS específico para el sidebar premium
st.markdown("""
<style>
/* ── SIDEBAR FONDO DEGRADADO PURPLE ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(160deg,
        #1a0a2e 0%,
        #2d1060 25%,
        #1e0a40 50%,
        #150830 75%,
        #0d0520 100%) !important;
    border-right: 1px solid rgba(168,85,247,0.25) !important;
    box-shadow: 4px 0 40px rgba(0,0,0,0.6) !important;
}

/* ── RADIO BUTTONS — convertir en nav items ── */
section[data-testid="stSidebar"] .stRadio > div {
    display: flex !important;
    flex-direction: column !important;
    gap: 2px !important;
}
/* Ocultar el círculo nativo del radio */
section[data-testid="stSidebar"] .stRadio input[type="radio"] {
    display: none !important;
}
/* Cada label = un nav item */
section[data-testid="stSidebar"] .stRadio label {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    padding: 11px 14px !important;
    margin: 1px 6px !important;
    border-radius: 12px !important;
    cursor: pointer !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    color: rgba(220,200,255,0.72) !important;
    border: 1px solid transparent !important;
    transition: all 0.2s ease !important;
    background: transparent !important;
    position: relative !important;
    overflow: hidden !important;
    min-height: 48px !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(168,85,247,0.15) !important;
    color: #f0ecff !important;
    border-color: rgba(168,85,247,0.25) !important;
}
/* Label seleccionado */
section[data-testid="stSidebar"] .stRadio label[data-baseweb] {
    background: transparent !important;
}
section[data-testid="stSidebar"] .stRadio [aria-checked="true"] ~ label,
section[data-testid="stSidebar"] .stRadio input:checked + div label,
section[data-testid="stSidebar"] .stRadio div[data-testid="stMarkdownContainer"]:has(input:checked) label {
    background: linear-gradient(135deg, rgba(124,58,237,0.65), rgba(168,85,247,0.4)) !important;
    color: #ffffff !important;
    border-color: rgba(168,85,247,0.5) !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.3) !important;
}
/* Truco: usar :has para el item activo */
section[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: linear-gradient(135deg, rgba(124,58,237,0.65), rgba(168,85,247,0.4)) !important;
    color: #ffffff !important;
    border-color: rgba(168,85,247,0.5) !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.3) !important;
}
/* El span de texto del radio */
section[data-testid="stSidebar"] .stRadio label > div {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    width: 100% !important;
}
section[data-testid="stSidebar"] .stRadio label p {
    margin: 0 !important;
    font-size: 0.88rem !important;
    font-weight: inherit !important;
    color: inherit !important;
    line-height: 1.3 !important;
}
/* Ícono cuadrito para cada label */
section[data-testid="stSidebar"] .stRadio label::before {
    content: '';
    width: 32px;
    height: 32px;
    min-width: 32px;
    border-radius: 9px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    display: flex;
    align-items: center;
    justify-content: center;
}
/* Línea activa a la izquierda */
section[data-testid="stSidebar"] .stRadio label:has(input:checked)::after {
    content: '';
    position: absolute;
    left: 0; top: 20%; bottom: 20%;
    width: 3px;
    background: linear-gradient(180deg, #c084fc, #e040fb);
    border-radius: 0 4px 4px 0;
}

/* Sección labels */
.nav-section {
    font-size: 0.58rem;
    color: rgba(200,180,255,0.45);
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 0 16px;
    margin: 16px 0 4px;
    font-family: 'DM Sans', sans-serif;
}
.nav-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(168,85,247,0.3), transparent);
    margin: 10px 16px;
}
.op-badge {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px;
    margin: 2px 6px;
    border-radius: 12px;
    cursor: pointer;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.84rem;
    font-weight: 500;
    color: rgba(220,200,255,0.65);
    border: 1px solid transparent;
    transition: all 0.2s;
}
.op-badge:hover { background: rgba(255,255,255,0.05); }
.op-badge.active {
    background: rgba(255,255,255,0.07);
    border-color: rgba(255,255,255,0.12);
    color: #f0ecff;
    font-weight: 700;
}
.op-dot {
    width: 9px; height: 9px;
    border-radius: 50%;
    flex-shrink: 0;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:

    # ── Logo ──
    st.markdown("""
    <div style="padding:28px 16px 16px;text-align:center">
        <div style="display:inline-flex;align-items:center;justify-content:center;
                    width:58px;height:58px;border-radius:18px;margin-bottom:14px;
                    background:linear-gradient(135deg,#7c3aed 0%,#e040fb 100%);
                    box-shadow:0 8px 32px rgba(168,85,247,0.55),
                               inset 0 1px 0 rgba(255,255,255,0.2)">
            <span style="font-size:1.6rem;line-height:1;filter:drop-shadow(0 2px 4px rgba(0,0,0,0.3))">🌐</span>
        </div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.5rem;font-weight:800;
                    letter-spacing:-0.03em;line-height:1;margin-bottom:6px">
            <span style="color:#f0ecff">Visió</span><span style="background:linear-gradient(90deg,#c084fc,#e040fb);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">N360</span>
        </div>
        <div style="font-family:'DM Sans',sans-serif;font-size:0.62rem;
                    color:rgba(200,180,255,0.5);font-weight:600;letter-spacing:0.1em;
                    text-transform:uppercase">
            Inteligencia Comercial
        </div>
    </div>
    <div class="nav-divider"></div>
    """, unsafe_allow_html=True)

    # ── Menú ANÁLISIS ──
    st.markdown('<div class="nav-section">Análisis</div>', unsafe_allow_html=True)
    vista = st.radio("_nav_analisis", [
        "📊  Panel Ejecutivo",
        "📈  P&G",
        "💹  Finanzas",
        "🔮  Proyecciones",
        "🧠  Asesor Financiero",
        "📡  Tendencias & Clima",
    ], label_visibility="collapsed")

    st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-section">Operacional</div>', unsafe_allow_html=True)

    vista2 = st.radio("_nav_op", [
        "📦  Operaciones",
        "🚦  Monitor de Estatus",
        "📣  Marketing",
        "🛍️  Catálogo",
        "🤖  Asistente IA",
    ], label_visibility="collapsed")

    # Detectar cuál grupo tocó el usuario por último
    if "last_group" not in st.session_state:
        st.session_state.last_group  = "analisis"
    if "prev_vista" not in st.session_state:
        st.session_state.prev_vista  = vista
        st.session_state.prev_vista2 = vista2

    if vista != st.session_state.prev_vista:
        st.session_state.last_group  = "analisis"
        st.session_state.prev_vista  = vista
    elif vista2 != st.session_state.prev_vista2:
        st.session_state.last_group  = "operacional"
        st.session_state.prev_vista2 = vista2

    vista_activa = vista if st.session_state.last_group == "analisis" else vista2

    st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)

    # ── Operación activa ──
    st.markdown('<div class="nav-section">Operación Activa</div>', unsafe_allow_html=True)

    OPERACIONES = {
        "🤖  LUCID BOT":      {"pais": "🇨🇴 Colombia", "moneda": "COP", "color": "#a78bfa", "dot": "#7c3aed",
                               "bg": "rgba(124,58,237,0.12)", "border": "rgba(124,58,237,0.4)"},
        "✨  ESSENTYA":        {"pais": "🇨🇴 Colombia", "moneda": "COP", "color": "#f9a8d4", "dot": "#ec4899",
                               "bg": "rgba(236,72,153,0.10)", "border": "rgba(236,72,153,0.35)"},
        "🐂  EL TORO":         {"pais": "🇨🇴 Colombia", "moneda": "COP", "color": "#fca5a5", "dot": "#ef4444",
                               "bg": "rgba(239,68,68,0.10)",  "border": "rgba(239,68,68,0.35)"},
        "🛒  Carrito Naranja": {"pais": "🇨🇱 Chile",    "moneda": "CLP", "color": "#fdba74", "dot": "#f97316",
                               "bg": "rgba(249,115,22,0.10)", "border": "rgba(249,115,22,0.35)"},
    }

    operacion = st.radio("_operacion", list(OPERACIONES.keys()), label_visibility="collapsed")
    op_info = OPERACIONES[operacion]
    es_clp  = op_info["moneda"] == "CLP"

    # Render visual de operaciones
    ops_html = ""
    for op_key, op_data in OPERACIONES.items():
        is_sel = op_key == operacion
        cls = "op-badge active" if is_sel else "op-badge"
        ops_html += f'''<div class="{cls}">
            <div class="op-dot" style="background:{op_data["dot"]};
                box-shadow:{"0 0 8px " + op_data["dot"] if is_sel else "none"}"></div>
            <span>{op_key.split("  ")[1]}</span>
            <span style="margin-left:auto;font-size:0.68rem;
                color:{"rgba(200,180,255,0.5)" if not is_sel else op_data["color"]}">
                {op_data["moneda"]}
            </span>
        </div>'''
    st.markdown(ops_html, unsafe_allow_html=True)

    # Badge país activo
    st.markdown(
        f'<div style="margin:8px 16px;padding:8px 12px;border-radius:10px;'
        f'background:{op_info["bg"]};border:1px solid {op_info["border"]};'
        f'font-size:0.78rem;color:{op_info["color"]};font-weight:600;font-family:DM Sans,sans-serif">'
        f'{op_info["pais"]} &nbsp;·&nbsp; {op_info["moneda"]}</div>',
        unsafe_allow_html=True
    )

    # TRM solo para Carrito Naranja
    trm_clp_cop = 4.2
    if es_clp:
        st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-section">💱 Conversión CLP → COP</div>', unsafe_allow_html=True)
        trm_clp_cop = st.number_input(
            "1 CLP = ? COP",
            min_value=1.0, max_value=20.0,
            value=4.2, step=0.1,
            help="Tasa de cambio CLP a COP"
        )
        st.markdown(f'<div style="font-size:0.74rem;color:rgba(200,180,255,0.5);padding:2px 8px">= ${trm_clp_cop:.2f} COP por CLP</div>', unsafe_allow_html=True)

    st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)

    # ── Importar datos ──
    st.markdown('<div class="nav-section">Importar Datos</div>', unsafe_allow_html=True)
    archivo = st.file_uploader(
        f"📁 {operacion.split('  ')[1]}",
        type=["xlsx","xls"],
        help="Exporta el reporte de órdenes desde Dropi"
    )

    if archivo:
        st.markdown(
            f'<div style="margin:8px;padding:10px 12px;border-radius:10px;text-align:center;'
            f'background:{op_info["bg"]};border:1px solid {op_info["border"]};'
            f'font-size:0.78rem;color:{op_info["color"]};font-weight:700">'
            f'✅ {operacion.split("  ")[1]} · Cargado</div>',
            unsafe_allow_html=True
        )

    # ── Footer ──
    st.markdown("""
    <div style="padding:16px;margin-top:8px;text-align:center">
        <div style="font-size:0.6rem;color:rgba(200,180,255,0.3);font-family:'DM Sans',sans-serif;
                    letter-spacing:0.05em">
            VisióN360 · v2.0 · Colombia
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="position:fixed;bottom:20px;left:0;width:260px;text-align:center">
        <div style="font-size:0.7rem;color:#6b7a9e">VisióN360 · v2.0 · Colombia</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# SIN ARCHIVO
# ═══════════════════════════════════════════════════════════
if archivo is None:
    html_bienvenida = (
        '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;'
        'min-height:72vh;text-align:center;padding:40px">'

        '<div style="display:inline-flex;align-items:center;justify-content:center;'
        'width:90px;height:90px;border-radius:24px;margin-bottom:28px;'
        'background:linear-gradient(135deg,#5b6cfc 0%,#00d4ff 100%);'
        'box-shadow:0 16px 48px rgba(99,102,241,0.3)">'
        '<span style="font-size:3rem;line-height:1">&#127758;</span>'
        '</div>'

        '<div style="font-family:Plus Jakarta Sans,sans-serif;font-size:3.2rem;font-weight:800;'
        'color:#e8ecf7;letter-spacing:-0.03em;line-height:1;margin-bottom:10px">'
        'Visi&#243;'
        '<span style="background:linear-gradient(90deg,#c084fc,#e040fb);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'background-clip:text">N360</span>'
        '</div>'

        '<div style="font-family:DM Sans,sans-serif;font-size:1rem;color:#7a8aaa;'
        'font-weight:500;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:36px">'
        'Todo tu negocio &nbsp;&middot;&nbsp; Una sola vista'
        '</div>'

        '<div style="width:60px;height:2px;'
        'background:linear-gradient(90deg,#c084fc,#e040fb);'
        'border-radius:2px;margin-bottom:36px"></div>'

        '<div style="font-size:0.95rem;color:#a8b4d0;max-width:380px;line-height:1.9;'
        'font-family:DM Sans,sans-serif;margin-bottom:28px">'
        'Selecciona tu operaci&#243;n y sube<br>tu reporte de Dropi para comenzar'
        '</div>'

        '<div style="background:linear-gradient(135deg,rgba(99,102,241,0.12),rgba(6,182,212,0.12));'
        'border:1px solid rgba(99,102,241,0.3);border-radius:14px;padding:16px 32px;'
        'font-family:DM Sans,sans-serif;color:#a5b4fc;font-size:0.88rem;font-weight:500">'
        '&#8592; &nbsp; Importar datos desde el panel lateral'
        '</div>'
        '</div>'
    )
    st.markdown(html_bienvenida, unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════════════════════
# CARGAR DATOS
# ═══════════════════════════════════════════════════════════
@st.cache_data
def cargar(f):
    df = pd.read_excel(f)
    df.columns = [str(c).strip() for c in df.columns]
    return df

with st.spinner("Procesando datos..."):
    df = cargar(archivo)

for col_f in [C_FECHA, C_FECHA_MOV]:
    if col_f in df.columns:
        df[col_f] = pd.to_datetime(df[col_f], dayfirst=True, errors='coerce')

if C_FECHA_MOV in df.columns:
    df['_h_mov'] = df[C_FECHA_MOV].apply(horas_desde)
    df['_d_mov'] = df['_h_mov'].apply(lambda h: round(h/24,1) if h is not None else None)

if C_FECHA in df.columns:
    df['_h_ped'] = df[C_FECHA].apply(horas_desde)
    df['_d_ped'] = df['_h_ped'].apply(lambda h: round(h/24,1) if h is not None else None)
    df['_mes']   = df[C_FECHA].dt.to_period('M').astype(str)
    df['_dia']   = df[C_FECHA].dt.day

for col_n in [C_TOTAL, C_GANANCIA, C_FLETE, C_CANTIDAD]:
    if col_n in df.columns:
        df[col_n] = pd.to_numeric(df[col_n], errors='coerce').fillna(0)

# Conversión CLP → COP para Carrito Naranja
if es_clp and trm_clp_cop > 0:
    for col_n in [C_TOTAL, C_GANANCIA, C_FLETE]:
        if col_n in df.columns:
            df[col_n] = df[col_n] * trm_clp_cop
    st.toast(f"💱 Valores convertidos: 1 CLP = {trm_clp_cop} COP", icon="🇨🇱")

if C_TAGS in df.columns:
    df['_tags_lista'] = df[C_TAGS].apply(parse_tags)

total = len(df)

def contar(patron):
    if C_ESTATUS not in df.columns: return 0
    return len(df[df[C_ESTATUS].astype(str).str.upper().str.contains(patron, na=False)])

entregados = contar('ENTREGADO')
cancelados = contar('CANCELADO')
devolucion = contar('DEVOLUCI')
novedades  = contar('NOVEDAD')
en_proceso = total - entregados - cancelados - devolucion
pct_ent    = round(entregados/total*100,1) if total else 0
tot_venta  = df[C_TOTAL].sum()    if C_TOTAL    in df.columns else 0
tot_gan    = df[C_GANANCIA].sum() if C_GANANCIA in df.columns else 0
pct_gan    = round(tot_gan/tot_venta*100,1) if tot_venta else 0


# ═══════════════════════════════════════════════════════════
# ██████  VISTA 1: VENTAS & ANÁLISIS
# ═══════════════════════════════════════════════════════════
if "Panel Ejecutivo" in vista_activa or "P&G" in vista_activa or "Proyecciones" in vista_activa or "Finanzas" in vista_activa or "Marketing" in vista_activa or "Catálogo" in vista_activa:

    # Header
    op_nombre = operacion.split("  ")[1]
    op_color  = op_info["color"]
    op_pais   = op_info["pais"]
    op_moneda = op_info["moneda"]

    modulo_nombre = vista_activa.split("  ")[1] if "  " in vista_activa else vista_activa.strip()
    clp_badge = (f"&nbsp;&nbsp;&middot;&nbsp;&nbsp;<span style='color:#f97316;font-size:0.78rem'>"
                 f"&#x1F4B1; CLP&#8594;COP @ {trm_clp_cop}</span>") if es_clp else ""

    st.markdown(
        f'<div style="margin-bottom:28px;background:linear-gradient(135deg,#12151f,#161929);'
        f'border:1px solid #2e2558;border-radius:16px;padding:24px 28px">'
        f'<div style="display:flex;align-items:center;gap:16px">'
        f'<div style="width:4px;height:54px;background:{op_color};border-radius:4px"></div>'
        f'<div>'
        f'<div style="font-size:0.68rem;color:#7a8aaa;font-weight:700;letter-spacing:0.12em;'
        f'text-transform:uppercase;margin-bottom:5px">{op_pais} &nbsp;·&nbsp; {op_moneda}</div>'
        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-size:1.9rem;font-weight:800;'
        f'color:#e8ecf7;line-height:1;margin-bottom:6px">{op_nombre}</div>'
        f'<div style="color:#a8b4d0;font-size:0.83rem">'
        f'{modulo_nombre} &nbsp;·&nbsp; {total:,} pedidos analizados{clp_badge}'
        f'</div></div></div></div>',
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════════════════════════════════
    # 📅 FILTRO UNIVERSAL — Por Mes / Por Semana
    # Estándar en todos los módulos del sistema
    # ══════════════════════════════════════════════════════════════════
    _hoy = pd.Timestamp.now().normalize()

    _uf_c1, _uf_c2, _uf_c3 = st.columns([1.2, 2, 2.5])

    with _uf_c1:
        _modo_periodo = st.radio(
            "Período",
            ["📅 Por Mes", "📆 Por Semana"],
            horizontal=False,
            label_visibility="collapsed",
            key="filtro_universal_modo"
        )

    # ── Opciones según modo ──
    if "Mes" in _modo_periodo:
        if '_mes' in df.columns and len(df['_mes'].dropna()) > 0:
            _meses_disp = sorted(df['_mes'].dropna().unique().tolist(), reverse=True)
        else:
            _meses_disp = [_hoy.to_period('M').strftime('%Y-%m')]
        _meses_lbl = []
        for _m in _meses_disp:
            try:    _meses_lbl.append(pd.Period(_m, 'M').strftime('%B %Y').capitalize())
            except: _meses_lbl.append(str(_m))

        with _uf_c2:
            _idx_mes_uf = st.selectbox(
                "Mes",
                list(range(len(_meses_disp))),
                index=0,
                format_func=lambda i: _meses_lbl[i] if i < len(_meses_lbl) else str(i),
                key="filtro_universal_mes",
                label_visibility="collapsed"
            )
        # Validación defensiva contra None
        if _idx_mes_uf is None: _idx_mes_uf = 0
        _idx_mes_uf = max(0, min(_idx_mes_uf, len(_meses_disp) - 1))
        _periodo_sel = _meses_disp[_idx_mes_uf]
        _periodo_lbl = _meses_lbl[_idx_mes_uf]

        if '_mes' in df.columns:
            df = df[df['_mes'] == _periodo_sel].copy()

    else:  # Por Semana
        if '_mes' in df.columns and len(df['_mes'].dropna()) > 0:
            _meses_disp_s = sorted(df['_mes'].dropna().unique().tolist(), reverse=True)
        else:
            _meses_disp_s = [_hoy.to_period('M').strftime('%Y-%m')]

        with _uf_c2:
            _idx_mes_s = st.selectbox(
                "Mes base",
                list(range(len(_meses_disp_s))),
                index=0,
                format_func=lambda i: pd.Period(_meses_disp_s[i], 'M').strftime('%B %Y').capitalize() if i < len(_meses_disp_s) else str(i),
                key="filtro_univ_mes_base",
                label_visibility="collapsed"
            )
        if _idx_mes_s is None: _idx_mes_s = 0
        _idx_mes_s = max(0, min(_idx_mes_s, len(_meses_disp_s) - 1))
        _mes_base_s = _meses_disp_s[_idx_mes_s]

        # Calcular semanas del mes seleccionado
        _inicio_mes_s = pd.Period(_mes_base_s, 'M').start_time
        _fin_mes_s    = pd.Period(_mes_base_s, 'M').end_time
        _semanas_mes  = []
        _cur = _inicio_mes_s
        _sw_n = 1
        while _cur <= _fin_mes_s:
            _fin_sem = min(_cur + pd.Timedelta(days=6), _fin_mes_s)
            _semanas_mes.append({
                "lbl": f"Semana {_sw_n} ({_cur.strftime('%d/%m')} – {_fin_sem.strftime('%d/%m')})",
                "ini": _cur,
                "fin": _fin_sem
            })
            _cur = _fin_sem + pd.Timedelta(days=1)
            _sw_n += 1

        with _uf_c3:
            _idx_sem = st.selectbox(
                "Semana",
                range(len(_semanas_mes)),
                index=0,
                format_func=lambda i: _semanas_mes[i]["lbl"],
                key="filtro_universal_semana",
                label_visibility="collapsed"
            )
        _sem_sel   = _semanas_mes[_idx_sem]
        _periodo_lbl = _sem_sel["lbl"]

        if C_FECHA in df.columns:
            df = df[
                (df[C_FECHA] >= _sem_sel["ini"]) &
                (df[C_FECHA] <= _sem_sel["fin"])
            ].copy()

    # ── Badge informativo ──
    _badge_col = "#5b6cfc" if "Mes" in _modo_periodo else "#7c3aed"
    _badge_ico = "📅" if "Mes" in _modo_periodo else "📆"
    st.markdown(
        f'<div style="background:{_badge_col}10;border:1px solid {_badge_col}33;'
        f'border-radius:8px;padding:5px 12px;font-size:0.72rem;color:#a8b4d0;'
        f'display:inline-block;margin-bottom:4px">'
        f'{_badge_ico} <b style="color:{_badge_col}">{_periodo_lbl}</b>'
        f' &nbsp;·&nbsp; <b style="color:#e8ecf7">{len(df):,} pedidos</b></div>',
        unsafe_allow_html=True
    )

    # ── Recalcular totales globales con df filtrado ──
    total      = len(df)
    entregados = contar('ENTREGADO') if total else 0
    cancelados = contar('CANCELADO') if total else 0
    devolucion = contar('DEVOLUCI')  if total else 0
    tot_venta  = df[C_TOTAL].sum()    if C_TOTAL    in df.columns else 0
    tot_gan    = df[C_GANANCIA].sum() if C_GANANCIA in df.columns else 0
    pct_gan    = round(tot_gan/tot_venta*100,1) if tot_venta else 0

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── KPIs financieros (análisis) ──
    ticket_prom = round(tot_venta / total, 0) if total else 0
    pct_cancel  = round(cancelados/total*100,1) if total else 0
    pct_dev_g   = round(devolucion/total*100,1) if total else 0

    # ── KPIs globales — ocultar en P&G (tiene su propia vista limpia) ──
    if "P&G" not in vista_activa:
        c1,c2,c3,c4,c5,c6 = st.columns(6)
        with c1: st.markdown(kpi("cyan","💰 Ventas Totales",fmt_money(tot_venta)), unsafe_allow_html=True)
        with c2: st.markdown(kpi("green","✅ Ganancia Neta",fmt_money(tot_gan),f"{pct_gan}% margen"), unsafe_allow_html=True)
        with c3: st.markdown(kpi("blue","📦 Pedidos",f"{total:,}",f"{entregados:,} entregados"), unsafe_allow_html=True)
        with c4: st.markdown(kpi("gold","🎫 Ticket Promedio",fmt_money(ticket_prom)), unsafe_allow_html=True)
        with c5: st.markdown(kpi("red","❌ Cancelación",f"{pct_cancel}%",f"{cancelados:,} pedidos"), unsafe_allow_html=True)
        with c6: st.markdown(kpi("purple","🔁 Devolución",f"{pct_dev_g}%",f"{devolucion:,} pedidos"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── NAVEGACIÓN INTERACTIVA ──
    st.markdown('<div class="seccion-titulo">Explorar datos</div>', unsafe_allow_html=True)

    # Sub-navegación según módulo activo
    if "P&G" in vista_activa:
        nav = "💰 P&G"
    elif "Proyecciones" in vista_activa:
        nav = "🔮 Proyecciones"
    elif "Finanzas" in vista_activa:
        nav = "💹 Finanzas"
    elif "Catálogo" in vista_activa:
        nav = "🛍️ Catálogo"
    elif "Marketing" in vista_activa:
        nav = "📣 Marketing"
    else:
        nav = st.radio("", ["🫀 Pulso del Negocio","🎯 El Marcador","🚨 Centro de Mando"],
                       horizontal=True, label_visibility="collapsed")


    # ── P&G COMPLETO ──
    if nav == "💰 P&G":
        st.markdown('<div class="seccion-titulo">📈 Estado de Pérdidas y Ganancias</div>', unsafe_allow_html=True)

        # ── Selector de mes ──
        meses_pg = sorted(df['_mes'].dropna().unique().tolist(), reverse=True) if '_mes' in df.columns else []
        mes_pg = st.selectbox("📅 Mes", meses_pg if meses_pg else ["Sin datos"], key="mes_pg")
        df_pg = df[df['_mes'] == mes_pg].copy() if '_mes' in df.columns and mes_pg != "Sin datos" else df.copy()

        # ── Helper: filtrar por semana ──
        def sem(df_base, n):
            if n == 0: return df_base
            r = {1:(1,8),2:(9,16),3:(17,24),4:(25,31)}
            i,f = r[n]
            return df_base[df_base[C_FECHA].dt.day.between(i,f)] if C_FECHA in df_base.columns else df_base

        # ── Calcular métricas Dropi por período ──
        def metricas_dropi(dfs):
            shopify    = dfs[C_TOTAL].sum()    if C_TOTAL    in dfs.columns else 0
            cancelado  = dfs[dfs[C_ESTATUS].astype(str).str.upper().str.contains('CANCELAD',na=False)][C_TOTAL].sum() if C_ESTATUS in dfs.columns and C_TOTAL in dfs.columns else 0
            devolucion = dfs[dfs[C_ESTATUS].astype(str).str.upper().str.contains('DEVOLUCI',na=False)][C_TOTAL].sum() if C_ESTATUS in dfs.columns and C_TOTAL in dfs.columns else 0
            novedad    = dfs[dfs[C_ESTATUS].astype(str).str.upper().str.contains('NOVEDAD',na=False)][C_TOTAL].sum()  if C_ESTATUS in dfs.columns and C_TOTAL in dfs.columns else 0
            reparto    = dfs[dfs[C_ESTATUS].astype(str).str.upper().str.contains('REPARTO',na=False)][C_TOTAL].sum()  if C_ESTATUS in dfs.columns and C_TOTAL in dfs.columns else 0
            recaudo    = shopify - cancelado - devolucion - novedad - reparto
            c_proveedor = dfs["PRECIO PROVEEDOR X CANTIDAD"].sum() if "PRECIO PROVEEDOR X CANTIDAD" in dfs.columns else 0
            # Flete entregados vs devoluciones
            mask_ent = dfs[C_ESTATUS].astype(str).str.upper().str.contains('ENTREGAD',na=False) if C_ESTATUS in dfs.columns else pd.Series([True]*len(dfs))
            mask_dev = dfs[C_ESTATUS].astype(str).str.upper().str.contains('DEVOLUCI',na=False) if C_ESTATUS in dfs.columns else pd.Series([False]*len(dfs))
            flete_ent = dfs[mask_ent][C_FLETE].sum() if C_FLETE in dfs.columns else 0
            flete_dev = dfs[mask_dev][C_FLETE].sum() if C_FLETE in dfs.columns else 0
            costo_total = c_proveedor + flete_ent + flete_dev
            margen_bruto = recaudo - costo_total
            return dict(shopify=shopify,cancelado=cancelado,devolucion=devolucion,
                        novedad=novedad,reparto=reparto,recaudo=recaudo,
                        c_proveedor=c_proveedor,flete_ent=flete_ent,flete_dev=flete_dev,
                        costo_total=costo_total,margen_bruto=margen_bruto)

        periodos = {
            "Sem I\n1-8":    sem(df_pg,1),
            "Sem II\n9-16":  sem(df_pg,2),
            "Sem III\n17-24":sem(df_pg,3),
            "Sem IV\n25-31": sem(df_pg,4),
            "Total Mes":     df_pg
        }
        met = {k: metricas_dropi(v) for k,v in periodos.items()}

        # ── INPUTS MANUALES ──
        st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)

        with st.expander("✏️ Ingresar costos manuales (Marketing · Admin · Imports)", expanded=False):
            st.caption("Ingresa los valores del mes completo en pesos COP. Se distribuyen proporcionalmente por semana.")
            col_m1, col_m2, col_m3 = st.columns(3)

            with col_m1:
                st.markdown('<div style="font-size:0.72rem;color:#fcd34d;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px">📣 MARKETING</div>', unsafe_allow_html=True)
                pauta        = st.number_input("Pauta (Ads)",         0, 500000000, 0, 100000, key="m_pauta",      format="%d")
                lucid_bot    = st.number_input("Lucid Bot",           0, 50000000,  0, 10000,  key="m_lucidbot",   format="%d")
                open_ia      = st.number_input("Open IA",             0, 20000000,  0, 10000,  key="m_openia",     format="%d")
                luci_voice   = st.number_input("Luci Voice",          0, 20000000,  0, 10000,  key="m_lucivoz",    format="%d")
                contingencias= st.number_input("Contingencias",       0, 20000000,  0, 10000,  key="m_conting",    format="%d")
                plat_spy     = st.number_input("Plataformas Spy",     0, 10000000,  0, 10000,  key="m_platspy",    format="%d")
                dominios     = st.number_input("Dominios / GoDaddy",  0, 5000000,   0, 10000,  key="m_dominios",   format="%d")
                total_mkt    = pauta+lucid_bot+open_ia+luci_voice+contingencias+plat_spy+dominios
                st.markdown(f'<div style="background:rgba(201,168,76,0.1);border-radius:6px;padding:8px;text-align:center;color:#fef08a;font-size:0.85rem"><b>Total: {fmt_money(total_mkt)}</b></div>', unsafe_allow_html=True)

            with col_m2:
                st.markdown('<div style="font-size:0.72rem;color:#a855f7;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px">🏢 ADMINISTRATIVOS</div>', unsafe_allow_html=True)
                adm_coord    = st.number_input("Coord Leidy",             0, 20000000, 0, 100000, key="a_coord",   format="%d")
                adm_logis    = st.number_input("Samanta Logística",       0, 20000000, 0, 100000, key="a_logis",   format="%d")
                adm_sandra   = st.number_input("Sandra Confirmación",     0, 20000000, 0, 100000, key="a_sandra",  format="%d")
                adm_cont     = st.number_input("Contador",                0, 10000000, 0, 100000, key="a_contad",  format="%d")
                adm_ceo      = st.number_input("C.E.O. - Ronaldo",        0, 20000000, 0, 100000, key="a_ceo",     format="%d")
                total_adm    = adm_coord+adm_logis+adm_sandra+adm_cont+adm_ceo
                st.markdown(f'<div style="background:rgba(99,102,241,0.1);border-radius:6px;padding:8px;text-align:center;color:#a5b4fc;font-size:0.85rem"><b>Total: {fmt_money(total_adm)}</b></div>', unsafe_allow_html=True)

            with col_m3:
                st.markdown('<div style="font-size:0.72rem;color:#22d3ee;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px">📦 IMPORTACIONES</div>', unsafe_allow_html=True)
                imp_compras  = st.number_input("Importaciones & Compras", 0, 200000000, 0, 100000, key="i_comp",   format="%d")
                imp_sky      = st.number_input("Sky Carga USA-Col",       0, 50000000,  0, 100000, key="i_sky",    format="%d")
                imp_tax8     = st.number_input("Impuesto 8x1000",         0, 5000000,   0, 10000,  key="i_tax8",   format="%d")
                imp_banco    = st.number_input("Costos Bancarios",        0, 5000000,   0, 10000,  key="i_banco",  format="%d")
                imp_activ    = st.number_input("Actividades & Capac.",    0, 10000000,  0, 10000,  key="i_activ",  format="%d")
                total_imp    = imp_compras+imp_sky+imp_tax8+imp_banco+imp_activ
                st.markdown(f'<div style="background:rgba(6,182,212,0.1);border-radius:6px;padding:8px;text-align:center;color:#6aeeff;font-size:0.85rem"><b>Total: {fmt_money(total_imp)}</b></div>', unsafe_allow_html=True)

        # Distribuir costos manuales por semana (proporcional a ingresos)
        shopify_total = met["Total Mes"]["shopify"] or 1
        def factor(k):
            return met[k]["shopify"] / shopify_total if shopify_total else 0.25

        manuales = {}
        for k in met.keys():
            f = factor(k)
            manuales[k] = dict(
                mkt_items={
                    "Pauta":          pauta*f,
                    "Lucid Bot":      lucid_bot*f,
                    "Open IA":        open_ia*f,
                    "Luci Voice":     luci_voice*f,
                    "Contingencias":  contingencias*f,
                    "Plat. Spy":      plat_spy*f,
                    "Dominios":       dominios*f,
                },
                total_mkt=total_mkt*f,
                adm_items={
                    "Coord Leidy":    adm_coord*f,
                    "Sam. Logística": adm_logis*f,
                    "S. Confirmación":adm_sandra*f,
                    "Contador":       adm_cont*f,
                    "C.E.O.":         adm_ceo*f,
                },
                total_adm=total_adm*f,
                imp_items={
                    "Importaciones":  imp_compras*f,
                    "Sky Carga":      imp_sky*f,
                    "Imp. 8x1000":    imp_tax8*f,
                    "C. Bancarios":   imp_banco*f,
                    "Actividades":    imp_activ*f,
                },
                total_imp=total_imp*f,
            )

        # ── TABLA P&G VISUAL ──
        def pct(val, base):
            return f"{round(val/base*100,1)}%" if base else "—"

        # ── Estilos base para tabla cuadriculada ──
        TD  = "padding:9px 14px;border-right:1px solid #1e2337;border-bottom:1px solid #1e2337;"
        TDN = "padding:9px 14px;border-bottom:1px solid #1e2337;"   # última columna, sin border-right
        HDR = "padding:10px 14px;text-align:right;background:#0d0c18;font-size:0.67rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;border-right:1px solid #1e2337;border-bottom:2px solid #1e2337;"
        HDRL= "padding:10px 14px;text-align:left; background:#0d0c18;font-size:0.67rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;border-right:1px solid #1e2337;border-bottom:2px solid #1e2337;min-width:180px"

        COL_COLORS = {
            "Sem I\n1-8":    "#c0392b","Sem II\n9-16": "#d4ac0d",
            "Sem III\n17-24":"#7fb3d3","Sem IV\n25-31":"#a9dfbf",
            "Total Mes":     "#27ae60"
        }

        def fila_seccion(label, color="#e8ecf7", bg="transparent"):
            return (
                f'<tr style="background:{bg}">'
                f'<td colspan="100%" style="{TDN}color:{color};font-family:Plus Jakarta Sans,sans-serif;'
                f'font-weight:800;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.07em;'
                f'background:{bg}">{label}</td></tr>'
            )

        def fila_pg(label, vals_dict, base_dict, invertir=False, destacar=False,
                    color_label="#8892b0", semanas_keys=None):
            """
            vals_dict:  {semana_key: valor_float}
            base_dict:  {semana_key: base_float}  — para calcular %
            semanas_keys: lista de columnas a mostrar (subset de cols_hdr)
            """
            if semanas_keys is None: semanas_keys = list(vals_dict.keys())
            bg_row = "rgba(201,168,76,0.07)" if destacar else "rgba(0,0,0,0)"
            fw     = "700" if destacar else "400"
            html   = f'<tr style="background:{bg_row}">'
            html  += f'<td style="{TDN}color:{color_label};font-weight:{fw};font-size:0.82rem;white-space:nowrap">{label}</td>'
            last_k = semanas_keys[-1]
            for k in semanas_keys:
                v    = vals_dict.get(k, 0)
                base = base_dict.get(k, 1)
                p    = v / base * 100 if base else 0
                # Color según lógica
                if invertir:
                    pc = "#ef4444" if p > 25 else "#fbbf24" if p > 15 else "#34d399"
                elif destacar:
                    pc = "#34d399" if p >= 55 else "#fbbf24" if p >= 40 else "#ef4444"
                else:
                    pc = "#e8ecf7"
                bg_p   = "rgba(239,68,68,0.1)" if pc=="#ef4444" else \
                         "rgba(245,158,11,0.1)" if pc=="#fbbf24" else "transparent"
                is_last = k == last_k
                td_sty  = TDN if is_last else TD
                val_txt  = f"${v:,.1f}" if abs(v) < 10_000 else f"${v/1_000_000:.3f}M" if abs(v) >= 1_000_000 else f"${v/1_000:.1f}K"
                pct_txt  = f"{p:.1f}%"
                html += (
                    f'<td style="{td_sty}text-align:right;font-size:0.82rem;color:#a8b4d0;font-weight:{fw}">'
                    f'{val_txt}</td>'
                    f'<td style="{td_sty}text-align:right;background:{bg_p};color:{pc};font-weight:700;font-size:0.78rem">'
                    f'{pct_txt}</td>'
                )
            html += '</tr>'
            return html

        def build_pg_html(semanas_keys):
            """Construye la tabla P&G solo para las semanas indicadas."""
            shopifys_s  = {k: met[k]["shopify"]      for k in semanas_keys}
            recaudos_s  = {k: met[k]["recaudo"]       for k in semanas_keys}
            mbrutos_s   = {k: met[k]["margen_bruto"]  for k in semanas_keys}
            marg_ops_s  = {k: met[k]["margen_bruto"] - manuales[k]["total_mkt"] for k in semanas_keys}
            ebitdas_s   = {k: marg_ops_s[k] - manuales[k]["total_adm"] - manuales[k]["total_imp"] for k in semanas_keys}
            imptos_s    = {k: met[k]["shopify"] * (imp_tasa/100) for k in semanas_keys}
            net_inv_s   = {k: ebitdas_s[k] * (red_inv/100) for k in semanas_keys}
            netos_s     = {k: ebitdas_s[k] - imptos_s[k] - net_inv_s[k] for k in semanas_keys}

            # Header
            hdr_cols = ""
            last_k = semanas_keys[-1]
            for k in semanas_keys:
                cc     = COL_COLORS.get(k,"#5b6cfc")
                label  = k.replace("\n","<br>")
                is_l   = k == last_k
                brd    = "" if is_l else "border-right:1px solid #1e2337;"
                hdr_cols += (
                    f'<th colspan="2" style="padding:10px 8px;text-align:center;background:{cc};'
                    f'color:#fff;font-family:Plus Jakarta Sans,sans-serif;font-size:0.75rem;font-weight:800;'
                    f'letter-spacing:0.04em;{brd}">{label}</th>'
                )

            h = (
                f'<div style="overflow-x:auto;border-radius:10px;border:2px solid #1e2337;margin-top:10px">'
                f'<table style="width:100%;border-collapse:collapse;background:#0d0a1a;'
                f'font-family:DM Sans,sans-serif">'
                f'<thead><tr style="background:#0d0c18">'
                f'<th style="{HDRL}">Concepto</th>{hdr_cols}'
                f'</tr></thead><tbody>'
            )

            # ── BLOQUE 1: RECAUDO ──
            h += fila_seccion("⚙️ Operación Logística", "#10b981", "rgba(16,185,129,0.05)")
            h += fila_pg("SHOPIFY — Total Pedidos", shopifys_s, shopifys_s, destacar=True, color_label="#10b981", semanas_keys=semanas_keys)
            h += fila_pg("  Deducciones (Cancel. + Dev. + Nov.)",
                         {k: met[k]["cancelado"]+met[k]["devolucion"]+met[k]["novedad"] for k in semanas_keys},
                         shopifys_s, invertir=True, semanas_keys=semanas_keys)
            h += fila_pg("  En Reparto (Tránsito)", {k:met[k]["reparto"] for k in semanas_keys},
                         shopifys_s, invertir=True, semanas_keys=semanas_keys)
            h += fila_pg("RECAUDO NETO", recaudos_s, shopifys_s, destacar=True, color_label="#f0c060", semanas_keys=semanas_keys)

            # ── BLOQUE 2: COSTO VENTA ──
            h += fila_seccion("📦 Costo de Venta", "#ef4444", "rgba(239,68,68,0.04)")
            h += fila_pg("  V/R Producto Entregado", {k:met[k]["c_proveedor"] for k in semanas_keys}, recaudos_s, invertir=True, semanas_keys=semanas_keys)
            h += fila_pg("  Flete de Entrega",       {k:met[k]["flete_ent"]   for k in semanas_keys}, recaudos_s, invertir=True, semanas_keys=semanas_keys)
            h += fila_pg("  Flete de Devolución",    {k:met[k]["flete_dev"]   for k in semanas_keys}, recaudos_s, invertir=True, semanas_keys=semanas_keys)
            h += fila_pg("TOTAL COSTO",              {k:met[k]["costo_total"] for k in semanas_keys}, recaudos_s, invertir=True, destacar=True, color_label="#ef4444", semanas_keys=semanas_keys)
            h += fila_pg("▶ MARGEN BRUTO / WALLET",  mbrutos_s, recaudos_s, destacar=True, color_label="#f0c060", semanas_keys=semanas_keys)

            # ── BLOQUE 3: MARKETING ──
            h += fila_seccion("📣 Ret. Inversión Marketing", "#f59e0b", "rgba(245,158,11,0.04)")
            for nm in ["Pauta","Lucid Bot","Open IA","Luci Voice","Contingencias","Plat. Spy","Dominios"]:
                h += fila_pg(f"  {nm}", {k:manuales[k]["mkt_items"].get(nm,0) for k in semanas_keys}, recaudos_s, invertir=True, semanas_keys=semanas_keys)
            h += fila_pg("TOTAL MARKETING", {k:manuales[k]["total_mkt"] for k in semanas_keys}, recaudos_s, invertir=True, destacar=True, color_label="#f59e0b", semanas_keys=semanas_keys)
            h += fila_pg("▶ MARGEN OPERACIONAL", marg_ops_s, recaudos_s, destacar=True, color_label="#a5b4fc", semanas_keys=semanas_keys)

            # ── BLOQUE 4: IMPORTS & ADMIN ──
            h += fila_seccion("🌐 Importaciones & Costos Bancarios", "#00d4ff", "rgba(6,182,212,0.03)")
            for nm in ["Importaciones","Sky Carga","Imp. 8x1000","C. Bancarios","Actividades"]:
                h += fila_pg(f"  {nm}", {k:manuales[k]["imp_items"].get(nm,0) for k in semanas_keys}, recaudos_s, invertir=True, semanas_keys=semanas_keys)
            h += fila_pg("TOTAL IMPORTS", {k:manuales[k]["total_imp"] for k in semanas_keys}, recaudos_s, invertir=True, destacar=True, color_label="#6aeeff", semanas_keys=semanas_keys)

            h += fila_seccion("🏢 Administrativos", "#7c3aed", "rgba(139,92,246,0.03)")
            for nm in ["Coord Leidy","Sam. Logística","S. Confirmación","Contador","C.E.O."]:
                h += fila_pg(f"  {nm}", {k:manuales[k]["adm_items"].get(nm,0) for k in semanas_keys}, recaudos_s, invertir=True, semanas_keys=semanas_keys)
            h += fila_pg("TOTAL ADMINISTRACIÓN", {k:manuales[k]["total_adm"] for k in semanas_keys}, recaudos_s, invertir=True, destacar=True, color_label="#9d6ffd", semanas_keys=semanas_keys)

            # ── BLOQUE 5: RESULTADO FINAL ──
            h += fila_seccion("📊 Resultado Final", "#f0c060", "rgba(201,168,76,0.05)")
            h += fila_pg("EBITDA", ebitdas_s, recaudos_s, destacar=True, color_label="#f0c060", semanas_keys=semanas_keys)
            h += fila_pg(f"  Impuestos ({imp_tasa:.1f}% configurable)", imptos_s, recaudos_s, invertir=True, semanas_keys=semanas_keys)
            h += fila_pg(f"  Red de Inversión ({red_inv:.1f}%)", net_inv_s, recaudos_s, invertir=True, semanas_keys=semanas_keys)
            h += fila_pg("▶ MARGEN NETO FINAL", netos_s, recaudos_s, destacar=True, color_label="#fde68a", semanas_keys=semanas_keys)

            h += "</tbody></table></div>"
            return h

        # ── INPUTS ADICIONALES: Impuestos y Red de Inversión ──
        # Defaults (se sobreescriben si el usuario abre el expander)
        imp_tasa      = float(st.session_state.get('pg_imp_tasa', 8.0))
        iva_excl      = float(st.session_state.get('pg_iva_excl', 80.0))
        red_inv       = float(st.session_state.get('pg_red_inv', 0.0))
        ing_adicional = 0
        with st.expander("⚙️ Configurar Impuestos · Red de Inversión · Ingresos adicionales", expanded=False):
            ci1,ci2,ci3 = st.columns(3)
            with ci1:
                st.markdown('<div style="font-size:0.7rem;color:#fcd34d;font-weight:800;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:8px">📊 IMPUESTOS</div>', unsafe_allow_html=True)
                imp_tasa = st.number_input("% Impuesto aplicable", 0.0, 50.0,
                                           float(st.session_state.get('pg_imp_tasa',8.0)), step=0.5, key="pg_imp_tasa",
                                           help="Ej: 8% retención, 19% IVA, etc.")
                iva_excl = st.number_input("% Base excluida de IVA", 0.0, 100.0,
                                           float(st.session_state.get('pg_iva_excl',80.0)), step=5.0, key="pg_iva_excl",
                                           help="Ej: 80% excluido → impuesto sobre el 20% restante")
                st.caption(f"Impuesto efectivo: {imp_tasa * (1-iva_excl/100):.2f}% del total")
            with ci2:
                st.markdown('<div style="font-size:0.7rem;color:#a855f7;font-weight:800;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:8px">🌐 RED DE INVERSIÓN</div>', unsafe_allow_html=True)
                red_inv = st.number_input("% Red de Inversión", 0.0, 50.0,
                                          float(st.session_state.get('pg_red_inv',0.0)), step=0.5, key="pg_red_inv",
                                          help="% del EBITDA destinado a red de inversión o socios")
                st.caption(f"Se descuenta del EBITDA antes del margen neto")
            with ci3:
                st.markdown('<div style="font-size:0.7rem;color:#10b981;font-weight:800;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:8px">💵 INGRESOS ADICIONALES</div>', unsafe_allow_html=True)
                ing_adicional = st.number_input("Ingresos adicionales (COP)", 0, 500_000_000, 0, 100_000, key="pg_ing_adicional", format="%d")
                st.caption("Se suman al recaudo del mes completo")

        # ── VISTA: TOTAL MES (siempre visible) ──
        st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.9rem;margin:16px 0 8px">📊 Total del Mes</div>', unsafe_allow_html=True)
        st.markdown(build_pg_html(["Total Mes"]), unsafe_allow_html=True)

        # ── VISTA SEMANAL DESPLEGABLE ──
        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        with st.expander("📅 Ver detalle por semanas (Sem I · II · III · IV)", expanded=False):
            all_sems = [k for k in met.keys() if k != "Total Mes"]
            st.markdown(build_pg_html(all_sems), unsafe_allow_html=True)

            # Sub-pestañas por semana individual
            st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.68rem;color:#a8b4d0;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px">▸ Semana individual</div>', unsafe_allow_html=True)
            sem_tabs = st.tabs([k.replace("\n"," ") for k in all_sems])
            for ti, tk in zip(sem_tabs, all_sems):
                with ti:
                    n_sem = len(sem(df_pg, list(met.keys()).index(tk)+1))
                    st.caption(f"{n_sem:,} pedidos · {COL_COLORS.get(tk,'#8892b0')} color de semana")
                    st.markdown(build_pg_html([tk]), unsafe_allow_html=True)

        # ── Gráfica resumen ──
        st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
        cols_hdr = list(met.keys())
        shopifys  = {k:met[k]["shopify"]     for k in cols_hdr}
        recaudos  = {k:met[k]["recaudo"]     for k in cols_hdr}
        mbrutos   = {k:met[k]["margen_bruto"]for k in cols_hdr}
        ebitdas   = {k:met[k]["margen_bruto"]-manuales[k]["total_mkt"]-manuales[k]["total_adm"]-manuales[k]["total_imp"] for k in cols_hdr}
        imptos    = {k:met[k]["shopify"]*(imp_tasa/100) for k in cols_hdr}
        netos     = {k:ebitdas[k]-imptos[k] for k in cols_hdr}

        xs = [k.replace("\n"," ") for k in cols_hdr]
        fig_pg2 = go.Figure()
        fig_pg2.add_trace(go.Bar(x=xs, y=[met[k]["shopify"]/1e6     for k in cols_hdr], name="Shopify",      marker_color="#5b6cfc", opacity=0.85))
        fig_pg2.add_trace(go.Bar(x=xs, y=[met[k]["recaudo"]/1e6     for k in cols_hdr], name="Recaudo",      marker_color="#00d4ff", opacity=0.85))
        fig_pg2.add_trace(go.Bar(x=xs, y=[mbrutos[k]/1e6            for k in cols_hdr], name="Margen Bruto", marker_color="#10b981", opacity=0.85))
        fig_pg2.add_trace(go.Bar(x=xs, y=[netos[k]/1e6              for k in cols_hdr], name="Margen Neto",  marker_color="#f0c060", opacity=0.85))
        fig_pg2.add_trace(go.Scatter(
            x=xs, y=[netos[k]/max(met[k]["shopify"],1)*100 for k in cols_hdr],
            name="Margen Neto %", yaxis="y2",
            line=dict(color="#fde68a",width=3), marker=dict(size=8)
        ))
        fig_pg2.update_layout(
            **PLOT_LAYOUT, barmode="group", height=380,
            title="P&G por Período — Millones COP",
            xaxis=AXIS_STYLE,
            yaxis=dict(title="M COP", **AXIS_STYLE),
            yaxis2=dict(title="Margen %", overlaying="y", side="right",
                        gridcolor="rgba(0,0,0,0)",
                        tickfont=dict(color="#fde68a"), ticksuffix="%")
        )
        st.plotly_chart(fig_pg2, use_container_width=True)


    # ══════════════════════════════════════════════════════════════════
    # 🔮 PROYECCIONES — REDISEÑO COMPLETO
    # Punto de partida automático · crecimiento % configurable
    # Ingresos + Gastos + Capacidad financiera proyectados
    # ══════════════════════════════════════════════════════════════════
    elif nav == "🔮 Proyecciones":
        st.markdown('<div class="seccion-titulo">🔮 Motor de Proyecciones</div>', unsafe_allow_html=True)

        _proy_c1, _proy_c2 = st.tabs([
            "🟣 Capa 1 — Proyección Autónoma (sin Excel)",
            "🔵 Capa 2 — Meta vs Real (con Excel)"
        ])

        # ════════════════════════════════════════════════════════════════
        # 🟣 CAPA 1 — PROYECCIÓN AUTÓNOMA
        # Basada en temporadas, clima, problemas del consumidor e histórico mínimo
        # No depende de un Excel actualizado
        # ════════════════════════════════════════════════════════════════
        with _proy_c1:
            from datetime import date as _dc1
            _hoy_c1 = _dc1.today()
            _mes_c1 = _hoy_c1.month
            _anio_c1 = _hoy_c1.year

            MESES_ES_C1 = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",
                           7:"Julio",8:"Agosto",9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"}

            # ── Factores de estacionalidad por mes (multiplicadores sobre promedio base) ──
            ESTACIONALIDAD_CO = {
                1: 0.85,  # Enero — post-navidad, caída
                2: 0.90,  # Febrero — San Valentín leve
                3: 1.10,  # Marzo — Día Mujer, pico
                4: 0.95,  # Abril — Semana Santa
                5: 1.35,  # Mayo — Día de la Madre 🔴 pico máximo
                6: 0.90,  # Junio — vacaciones escolares
                7: 0.85,  # Julio — vacaciones
                8: 1.05,  # Agosto — regreso clases, Feria Flores
                9: 1.25,  # Septiembre — Amor y Amistad 🔴
                10: 1.00, # Octubre — Halloween creciendo
                11: 1.40, # Noviembre — Black Friday 🔴 pico máximo
                12: 1.50, # Diciembre — Navidad 🔴 pico absoluto
            }
            ESTACIONALIDAD_CL = {
                1: 1.30,  # Enero — verano chileno
                2: 1.20,  # Febrero — verano
                3: 1.05,  # Marzo — regreso escolar
                4: 0.90,  # Abril — otoño
                5: 1.30,  # Mayo — Día Madre Chile 🔴
                6: 1.20,  # Junio — CyberDay + Día Padre 🔴
                7: 0.85,  # Julio — vacaciones invierno
                8: 0.80,  # Agosto
                9: 1.40,  # Septiembre — Fiestas Patrias 🔴
                10: 1.00,
                11: 1.35, # Noviembre — Black Friday 🔴
                12: 1.45, # Diciembre — Navidad 🔴
            }

            # ── Usar histórico real si existe, o estimado manual ──
            _tiene_hist = ('_mes' in df.columns and C_TOTAL in df.columns and len(df['_mes'].unique()) >= 1)

            st.markdown(
                '<div style="background:rgba(139,92,246,0.08);border:1px solid #7c3aed33;'
                'border-radius:14px;padding:18px 22px;margin-bottom:18px">'
                '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#9333ea;font-size:0.92rem;margin-bottom:6px">'
                '🟣 Proyección Autónoma — No depende de tu Excel</div>'
                '<div style="color:#a8b4d0;font-size:0.78rem">Calculada con estacionalidad del mercado colombiano/chileno, '
                'eventos comerciales del año y el promedio base que configures. '
                'Si el Excel cambia, esta proyección NO cambia — es tu brújula estratégica estable.</div>'
                '</div>',
                unsafe_allow_html=True
            )

            # ── Configuración base ──
            _cc1a, _cc1b, _cc1c, _cc1d = st.columns(4)
            with _cc1a:
                _pais_c1 = st.radio("🌍 Mercado", ["🇨🇴 Colombia", "🇨🇱 Chile"],
                                    horizontal=True, key="c1_pais", label_visibility="collapsed")
            with _cc1b:
                _base_manual_c1 = st.number_input(
                    "💵 Venta base promedio mensual (COP)",
                    min_value=0, max_value=5_000_000_000,
                    value=int(df[C_TOTAL].mean() * len(df[df['_mes'] == df['_mes'].iloc[-1]]) if _tiene_hist and C_TOTAL in df.columns else 50_000_000),
                    step=1_000_000,
                    key="c1_base_manual",
                    label_visibility="collapsed"
                )
                st.caption("Base mensual promedio de ventas")
            with _cc1c:
                _n_meses_c1 = st.selectbox("📅 Meses a proyectar", [3,6,9,12], index=1,
                                            key="c1_nmeses", label_visibility="collapsed")
                st.caption("Meses a proyectar")
            with _cc1d:
                _ajuste_c1 = st.slider("⚡ Ajuste estratégico %", -30, 50, 0, step=5,
                                        key="c1_ajuste", label_visibility="collapsed")
                st.caption(f"Ajuste manual: {'+' if _ajuste_c1>=0 else ''}{_ajuste_c1}%")

            _estac = ESTACIONALIDAD_CO if "Colombia" in _pais_c1 else ESTACIONALIDAD_CL
            _base_c1 = _base_manual_c1 * (1 + _ajuste_c1 / 100)

            # ── Calcular proyección mes a mes ──
            _filas_c1 = []
            for _i in range(1, _n_meses_c1 + 1):
                import calendar as _cal_mod
                _mes_fut = ((_mes_c1 - 1 + _i) % 12) + 1
                _anio_fut = _anio_c1 + ((_mes_c1 - 1 + _i) // 12)
                _factor   = _estac.get(_mes_fut, 1.0)
                _venta_c1 = _base_c1 * _factor

                # Eventos del mes
                EVENTOS_CLAVE = {
                    (5, "CO"): ("💐 Día de la Madre", "#ef4444"),
                    (9, "CO"): ("🤝 Amor y Amistad", "#ef4444"),
                    (11, "CO"): ("🖤 Black Friday", "#ef4444"),
                    (12, "CO"): ("🎄 Navidad", "#ef4444"),
                    (3, "CO"): ("🌸 Día de la Mujer", "#f59e0b"),
                    (5, "CL"): ("💐 Día Madre Chile", "#ef4444"),
                    (6, "CL"): ("💻 CyberDay", "#ef4444"),
                    (9, "CL"): ("🇨🇱 Fiestas Patrias", "#ef4444"),
                    (11, "CL"): ("🖤 Black Friday", "#ef4444"),
                    (12, "CL"): ("🎄 Navidad", "#ef4444"),
                }
                _pais_key_c1 = "CO" if "Colombia" in _pais_c1 else "CL"
                _evento = EVENTOS_CLAVE.get((_mes_fut, _pais_key_c1), None)

                _filas_c1.append({
                    "mes_n": _mes_fut,
                    "anio_n": _anio_fut,
                    "label": f"{MESES_ES_C1[_mes_fut][:3]} {_anio_fut}",
                    "factor": _factor,
                    "venta": _venta_c1,
                    "evento": _evento,
                    "pct_vs_base": (_factor - 1) * 100,
                })

            # ── Tabla visual de proyección ──
            st.markdown(
                '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.85rem;margin-bottom:12px">'
                '📋 Proyección mes a mes — basada en estacionalidad del mercado</div>',
                unsafe_allow_html=True
            )

            _col_w_c1 = [1.2] + [1] * _n_meses_c1
            _th_c1 = st.columns(_col_w_c1)
            with _th_c1[0]:
                st.markdown('<div style="font-size:0.65rem;color:#a8b4d0;font-weight:800;text-transform:uppercase">Concepto</div>', unsafe_allow_html=True)
            for _ci, _fila in enumerate(_filas_c1):
                _col_ev = _fila["evento"][1] if _fila["evento"] else "#1e2337"
                _ev_lbl = _fila["evento"][0] if _fila["evento"] else ""
                with _th_c1[_ci + 1]:
                    st.markdown(
                        f'<div style="text-align:center;background:#13102a;border-radius:8px;padding:6px 4px;'
                        f'border:1px solid {_col_ev}55">'
                        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-size:0.72rem;color:#e8ecf7;font-weight:800">{_fila["label"]}</div>'
                        f'<div style="font-size:0.58rem;color:{"#ef4444" if _fila["pct_vs_base"]>15 else "#10b981" if _fila["pct_vs_base"]>0 else "#8892b0"}">'
                        f'{"+" if _fila["pct_vs_base"]>=0 else ""}{_fila["pct_vs_base"]:.0f}% vs base</div>'
                        f'{"<div style=font-size:0.58rem;color:" + _col_ev + ">" + _ev_lbl + "</div>" if _ev_lbl else ""}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

            # Fila: ventas proyectadas
            _row_c1 = st.columns(_col_w_c1)
            with _row_c1[0]:
                st.markdown('<div style="font-size:0.72rem;color:#9333ea;font-weight:700;padding:4px 0">💰 Ventas proyectadas</div>', unsafe_allow_html=True)
            for _ci, _fila in enumerate(_filas_c1):
                with _row_c1[_ci + 1]:
                    st.markdown(
                        f'<div style="text-align:center;padding:4px 2px">'
                        f'<div style="font-size:0.76rem;color:#9333ea;font-weight:800">{fmt_money(_fila["venta"])}</div>'
                        f'</div>', unsafe_allow_html=True
                    )

            # Fila: factor estacional
            _row_c1b = st.columns(_col_w_c1)
            with _row_c1b[0]:
                st.markdown('<div style="font-size:0.72rem;color:#fcd34d;font-weight:700;padding:4px 0">📊 Factor estacional</div>', unsafe_allow_html=True)
            for _ci, _fila in enumerate(_filas_c1):
                _fc = "#ef4444" if _fila["factor"] >= 1.3 else "#f59e0b" if _fila["factor"] >= 1.1 else "#10b981" if _fila["factor"] >= 1.0 else "#8892b0"
                with _row_c1b[_ci + 1]:
                    st.markdown(
                        f'<div style="text-align:center;padding:4px 2px">'
                        f'<div style="font-size:0.76rem;color:{_fc};font-weight:800">×{_fila["factor"]:.2f}</div>'
                        f'</div>', unsafe_allow_html=True
                    )

            # ── Gráfica de proyección autónoma ──
            _xs_c1 = [f["label"] for f in _filas_c1]
            _ys_c1 = [f["venta"] / 1e6 for f in _filas_c1]
            _facs_c1 = [f["factor"] for f in _filas_c1]

            _fig_c1 = go.Figure()
            _fig_c1.add_trace(go.Bar(
                x=_xs_c1, y=_ys_c1,
                marker_color=[
                    "#ef4444" if f >= 1.3 else "#f59e0b" if f >= 1.1 else "#5b6cfc" if f >= 1.0 else "#252a3d"
                    for f in _facs_c1
                ],
                name="Venta proyectada",
                hovertemplate='%{x}<br>$%{y:.1f}M COP<extra></extra>',
                opacity=0.85
            ))
            # Línea base
            _fig_c1.add_hline(
                y=_base_c1 / 1e6, line_dash="dot", line_color="#7c3aed",
                annotation_text=f"Base: {fmt_money(_base_c1)}", annotation_font_color="#a08afd"
            )
            _fig_c1.update_layout(
                **PLOT_LAYOUT, height=340,
                title=f"Proyección Autónoma {_n_meses_c1} meses · {_pais_c1.split()[-1]}",
                xaxis=AXIS_STYLE, yaxis=dict(title="Millones COP", **AXIS_STYLE)
            )
            st.plotly_chart(_fig_c1, use_container_width=True)

            # ── KPIs resumen ──
            _tot_c1 = sum(f["venta"] for f in _filas_c1)
            _mes_pico_c1 = max(_filas_c1, key=lambda x: x["venta"])
            _mes_bajo_c1 = min(_filas_c1, key=lambda x: x["venta"])
            _eventos_c1  = [f for f in _filas_c1 if f["evento"]]

            _kc1, _kc2, _kc3, _kc4 = st.columns(4)
            with _kc1: st.markdown(kpi("purple", f"💰 Total {_n_meses_c1} meses", fmt_money(_tot_c1), "proyección autónoma"), unsafe_allow_html=True)
            with _kc2: st.markdown(kpi("red", "📈 Mes pico", fmt_money(_mes_pico_c1["venta"]), _mes_pico_c1["label"]), unsafe_allow_html=True)
            with _kc3: st.markdown(kpi("blue", "📉 Mes bajo", fmt_money(_mes_bajo_c1["venta"]), _mes_bajo_c1["label"]), unsafe_allow_html=True)
            with _kc4: st.markdown(kpi("gold", "🎯 Eventos clave", str(len(_eventos_c1)), "en el período"), unsafe_allow_html=True)

            # ── Alertas de eventos próximos ──
            if _eventos_c1:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.85rem;margin-bottom:10px">'
                    '🚨 Eventos Comerciales Clave en el Período</div>',
                    unsafe_allow_html=True
                )
                for _ev_f in _eventos_c1:
                    _ev_col = _ev_f["evento"][1]
                    st.markdown(
                        f'<div style="background:{_ev_col}10;border:1px solid {_ev_col}33;border-radius:10px;'
                        f'padding:12px 16px;margin-bottom:8px;display:flex;align-items:center;gap:12px">'
                        f'<span style="font-size:1.2rem">{_ev_f["evento"][0].split()[0]}</span>'
                        f'<div style="flex:1">'
                        f'<span style="color:#e8ecf7;font-weight:700;font-size:0.84rem">{_ev_f["evento"][0]}</span>'
                        f'<span style="color:#a8b4d0;font-size:0.74rem;margin-left:8px">— {_ev_f["label"]}</span>'
                        f'</div>'
                        f'<div style="text-align:right">'
                        f'<div style="color:{_ev_col};font-weight:800;font-size:0.9rem">{fmt_money(_ev_f["venta"])}</div>'
                        f'<div style="color:#a8b4d0;font-size:0.7rem">×{_ev_f["factor"]:.2f} vs base</div>'
                        f'</div></div>',
                        unsafe_allow_html=True
                    )

            st.markdown(
                '<div style="background:rgba(139,92,246,0.05);border:1px dashed #7c3aed44;border-radius:10px;'
                'padding:14px 18px;margin-top:14px;font-size:0.76rem;color:#a8b4d0;line-height:1.7">'
                '🟣 <b style="color:#9333ea">Esta proyección es estable y estratégica.</b> '
                'No importa si mañana cambias el Excel — los factores estacionales del mercado no cambian. '
                'Úsala para planificar importaciones, pauta y personal con 2-3 meses de anticipación.</div>',
                unsafe_allow_html=True
            )

        # ════════════════════════════════════════════════════════════════
        # 🔵 CAPA 2 — META VS REAL (DEPENDIENTE DE EXCEL)
        # ════════════════════════════════════════════════════════════════
        with _proy_c2:

            if '_mes' not in df.columns or C_TOTAL not in df.columns or len(df['_mes'].unique()) < 2:
                st.info("⬆️ Se necesitan al menos 2 meses de datos para generar proyecciones.")
            else:
                # ── Calcular histórico ──
                MESES_ES_P = {1:"Ene",2:"Feb",3:"Mar",4:"Abr",5:"May",6:"Jun",
                              7:"Jul",8:"Ago",9:"Sep",10:"Oct",11:"Nov",12:"Dic"}
                def fmt_mes_p(m):
                    try: y,mo = str(m).split('-'); return f"{MESES_ES_P[int(mo)]} {y[-2:]}"
                    except: return str(m)

                v_mes_p = df.groupby('_mes').agg(
                    Ventas    = (C_TOTAL,   'sum'),
                    Pedidos   = (C_TOTAL,   'count'),
                    Ganancia  = (C_GANANCIA,'sum') if C_GANANCIA in df.columns else (C_TOTAL,'count'),
                ).reset_index().sort_values('_mes')
                v_mes_p['Mes_Label'] = v_mes_p['_mes'].apply(fmt_mes_p)

                # Últimos 3 y 6 meses
                ult1  = v_mes_p['Ventas'].iloc[-1]
                ult3  = v_mes_p['Ventas'].tail(3).mean()
                ult6  = v_mes_p['Ventas'].tail(6).mean()
                ult3_min = v_mes_p['Ventas'].tail(3).min()
                ult3_max = v_mes_p['Ventas'].tail(3).max()
                gan_pct_hist = (v_mes_p['Ganancia'].tail(3).mean() / ult3 * 100) if ult3 else 0
                mes_actual_p  = v_mes_p['Mes_Label'].iloc[-1]

                # ── BLOQUE: PUNTO DE PARTIDA ──
                st.markdown(
                    '<div style="background:linear-gradient(135deg,#12151f,#161929);border:1px solid #2e2558;'
                    'border-radius:14px;padding:20px 24px;margin-bottom:20px">'
                    '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.92rem;margin-bottom:14px">'
                    '📍 Punto de Partida — ¿desde dónde proyectamos?</div>',
                    unsafe_allow_html=True
                )

                bp1, bp2, bp3, bp4 = st.columns(4)
                with bp1:
                    st.markdown(
                        f'<div style="text-align:center">'
                        f'<div style="font-size:0.6rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;margin-bottom:4px">Último mes ({mes_actual_p})</div>'
                        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:#a855f7;font-size:1.2rem">{fmt_money(ult1)}</div>'
                        f'</div>', unsafe_allow_html=True
                    )
                with bp2:
                    st.markdown(
                        f'<div style="text-align:center">'
                        f'<div style="font-size:0.6rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;margin-bottom:4px">Promedio 3 meses</div>'
                        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:#22d3ee;font-size:1.2rem">{fmt_money(ult3)}</div>'
                        f'<div style="font-size:0.62rem;color:#7a8aaa;margin-top:2px">entre {fmt_money(ult3_min)} y {fmt_money(ult3_max)}</div>'
                        f'</div>', unsafe_allow_html=True
                    )
                with bp3:
                    st.markdown(
                        f'<div style="text-align:center">'
                        f'<div style="font-size:0.6rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;margin-bottom:4px">Promedio 6 meses</div>'
                        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:#10b981;font-size:1.2rem">{fmt_money(ult6)}</div>'
                        f'</div>', unsafe_allow_html=True
                    )
                with bp4:
                    st.markdown(
                        f'<div style="text-align:center">'
                        f'<div style="font-size:0.6rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;margin-bottom:4px">Margen promedio</div>'
                        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:#fcd34d;font-size:1.2rem">{gan_pct_hist:.1f}%</div>'
                        f'<div style="font-size:0.62rem;color:#7a8aaa;margin-top:2px">últimos 3 meses</div>'
                        f'</div>', unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)

                # ── CONFIGURADOR ──
                st.markdown(
                    '<div style="background:#13102a;border:1px solid #2e2558;border-radius:14px;'
                    'padding:20px 24px;margin-bottom:20px">',
                    unsafe_allow_html=True
                )
                st.markdown(
                    '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.88rem;margin-bottom:16px">'
                    '⚙️ Configurar Proyección</div>',
                    unsafe_allow_html=True
                )

                cfg1, cfg2, cfg3, cfg4 = st.columns(4)
                with cfg1:
                    base_proy = st.radio(
                        "📍 Punto de partida",
                        ["Último mes", "Promedio 3 meses", "Promedio 6 meses", "Manual"],
                        key="proy_base", horizontal=False
                    )
                with cfg2:
                    n_meses_proy = st.selectbox(
                        "📅 Meses a proyectar",
                        [3, 6, 9, 12], index=1, key="proy_nmeses"
                    )
                    fecha_inicio_ref = pd.Timestamp.now()
                    meses_label_proy = []
                    for mi in range(1, n_meses_proy + 1):
                        m_fut = fecha_inicio_ref + pd.DateOffset(months=mi)
                        meses_label_proy.append(m_fut.strftime("%b %Y"))

                with cfg3:
                    crecimiento_proy = st.number_input(
                        "📈 Crecimiento mensual %", -50.0, 200.0,
                        float(st.session_state.get('proy_crec', 10.0)),
                        step=5.0, key="proy_crec"
                    )
                    # Sugerencia automática
                    if len(v_mes_p) >= 2:
                        crec_real = (v_mes_p['Ventas'].iloc[-1] / v_mes_p['Ventas'].iloc[-2] - 1) * 100
                    else:
                        crec_real = 0
                    st.caption(f"Tu crecimiento real último mes: {crec_real:+.1f}%")

                with cfg4:
                    if base_proy == "Manual":
                        base_val_proy = st.number_input(
                            "💵 Base manual (COP)", 0, 5_000_000_000,
                            int(ult3), 1_000_000, key="proy_manual", format="%d"
                        )
                    else:
                        base_val_proy = {"Último mes": ult1,
                                         "Promedio 3 meses": ult3,
                                         "Promedio 6 meses": ult6}[base_proy]
                        st.metric("Base seleccionada", fmt_money(base_val_proy))

                st.markdown('</div>', unsafe_allow_html=True)

                # ── CALCULAR PROYECCIONES ──
                # Gastos estimados como % histórico
                gastos_op_hist = st.session_state.get('nomina_total', 0) + \
                                 sum(st.session_state.get('costos_fijos', {}).values()) + \
                                 sum(st.session_state.get('pauta_dict', {}).values())
                pct_gastos_hist = gastos_op_hist / ult3 if ult3 else 0.35
                tasa_imp_proy   = float(st.session_state.get('diag_imp', 8.0)) * \
                                  (1 - float(st.session_state.get('diag_iva_excl', 80.0)) / 100)

                filas_proy = []
                for i in range(1, n_meses_proy + 1):
                    ventas_i   = base_val_proy * ((1 + crecimiento_proy / 100) ** i)
                    gan_i      = ventas_i * (gan_pct_hist / 100)
                    gastos_i   = ventas_i * pct_gastos_hist
                    imp_i      = (ventas_i - gastos_i) * (tasa_imp_proy / 100)
                    util_i     = gan_i - gastos_i - imp_i
                    pedidos_i  = int(ventas_i / (ult1 / len(df[df['_mes'] == v_mes_p['_mes'].iloc[-1]])) ) if len(df[df['_mes'] == v_mes_p['_mes'].iloc[-1]]) else 0
                    filas_proy.append({
                        'Mes': meses_label_proy[i - 1],
                        'Ventas': ventas_i, 'Ganancia': gan_i,
                        'Gastos': gastos_i, 'Impuesto': imp_i,
                        'Utilidad': util_i, 'Pedidos_est': pedidos_i,
                    })

                # ── CUADRO RESUMEN MENSUAL ──
                st.markdown(
                    '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.88rem;margin-bottom:10px">'
                    '📋 Proyección Detallada — mes a mes</div>',
                    unsafe_allow_html=True
                )

                # Header tabla
                col_widths = [1.2] + [1]*n_meses_proy
                th_cols = st.columns(col_widths)
                with th_cols[0]:
                    st.markdown('<div style="font-size:0.65rem;color:#a8b4d0;font-weight:800;text-transform:uppercase">Concepto</div>', unsafe_allow_html=True)
                for ci, fp in enumerate(filas_proy):
                    with th_cols[ci+1]:
                        crec_i = (fp['Ventas'] / filas_proy[ci-1]['Ventas'] - 1)*100 if ci > 0 else crecimiento_proy
                        st.markdown(
                            f'<div style="text-align:center;background:#13102a;border-radius:8px;padding:6px 4px;border:1px solid #2e2558">'
                            f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-size:0.72rem;color:#e8ecf7;font-weight:800">{fp["Mes"]}</div>'
                            f'<div style="font-size:0.6rem;color:{"#10b981" if crec_i>=0 else "#ef4444"}">'
                            f'{"+" if crec_i>=0 else ""}{crec_i:.0f}% vs ant.</div>'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

                # Filas de datos
                conceptos_proy = [
                    ("💰 Ingresos proyectados",   "Ventas",    "#5b6cfc"),
                    ("📈 Ganancia bruta est.",     "Ganancia",  "#10b981"),
                    ("🏢 Gastos operativos est.", "Gastos",    "#ef4444"),
                    ("🏛️ Impuesto estimado",      "Impuesto",  "#f0c060"),
                    ("✅ Utilidad neta est.",      "Utilidad",  "#e8ecf7"),
                ]
                for lbl_c, key_c, col_c in conceptos_proy:
                    row_cols = st.columns(col_widths)
                    es_util = key_c == "Utilidad"
                    with row_cols[0]:
                        st.markdown(
                            f'<div style="font-size:0.72rem;color:{col_c};font-weight:700;padding:4px 0">{lbl_c}</div>',
                            unsafe_allow_html=True
                        )
                    for ci, fp in enumerate(filas_proy):
                        val_c = fp[key_c]
                        c_val = ("#10b981" if val_c >= 0 else "#ef4444") if es_util else col_c
                        with row_cols[ci+1]:
                            st.markdown(
                                f'<div style="text-align:center;padding:4px 2px;'
                                f'background:{"rgba(16,185,129,0.05)" if es_util and val_c>0 else "rgba(239,68,68,0.05)" if es_util and val_c<0 else "transparent"};'
                                f'border-radius:6px">'
                                f'<div style="font-size:0.75rem;color:{c_val};font-weight:{"800" if es_util else "600"}">'
                                f'{fmt_money(abs(val_c))}</div>'
                                f'<div style="font-size:0.6rem;color:#7a8aaa">'
                                f'{val_c/fp["Ventas"]*100:.0f}%</div>'
                                f'</div>',
                                unsafe_allow_html=True
                            )

                # ── GRÁFICA COMBINADA ──
                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
                hist_xs  = list(v_mes_p['Mes_Label'])
                hist_ys  = list(v_mes_p['Ventas'] / 1e6)
                proy_xs  = [hist_xs[-1]] + [fp['Mes'] for fp in filas_proy]
                proy_ys  = [hist_ys[-1]] + [fp['Ventas'] / 1e6 for fp in filas_proy]
                proy_gan = [hist_ys[-1] * gan_pct_hist / 100] + [fp['Ganancia'] / 1e6 for fp in filas_proy]
                proy_ut  = [0] + [fp['Utilidad'] / 1e6 for fp in filas_proy]

                fig_proy = go.Figure()
                fig_proy.add_trace(go.Scatter(
                    x=hist_xs, y=hist_ys, name='Ventas Históricas',
                    line=dict(color=op_color, width=3), marker=dict(size=7),
                    hovertemplate='%{x}<br>%{y:.2f}M COP<extra></extra>'
                ))
                fig_proy.add_trace(go.Scatter(
                    x=proy_xs, y=proy_ys, name='Ventas Proyectadas',
                    line=dict(color='#f0c060', width=3, dash='dash'),
                    marker=dict(size=8, symbol='diamond'),
                    hovertemplate='%{x}<br>%{y:.2f}M COP<extra></extra>'
                ))
                fig_proy.add_trace(go.Scatter(
                    x=proy_xs, y=proy_gan, name='Ganancia Proy.',
                    line=dict(color='#10b981', width=2, dash='dot'),
                    marker=dict(size=6),
                ))
                fig_proy.add_trace(go.Bar(
                    x=[fp['Mes'] for fp in filas_proy],
                    y=[fp['Utilidad'] / 1e6 for fp in filas_proy],
                    name='Utilidad Neta Proy.',
                    marker_color=['#10b981' if fp['Utilidad'] >= 0 else '#ef4444' for fp in filas_proy],
                    opacity=0.6, yaxis='y'
                ))
                fig_proy.update_layout(
                    **PLOT_LAYOUT, height=420,
                    title=f"Proyección {n_meses_proy} meses · Base: {base_proy} · +{crecimiento_proy:.0f}%/mes",
                    xaxis=AXIS_STYLE,
                    yaxis=dict(title='Millones COP', **AXIS_STYLE),
                    barmode='overlay'
                )
                st.plotly_chart(fig_proy, use_container_width=True)

                # ── KPIs RESUMEN ──
                total_v   = sum(fp['Ventas']   for fp in filas_proy)
                total_g   = sum(fp['Ganancia'] for fp in filas_proy)
                total_u   = sum(fp['Utilidad'] for fp in filas_proy)
                mejor_mes = max(filas_proy, key=lambda x: x['Ventas'])

                pk1,pk2,pk3,pk4 = st.columns(4)
                with pk1: st.markdown(kpi("cyan",  "💰 Ingresos totales",  fmt_money(total_v),    f"{n_meses_proy} meses"), unsafe_allow_html=True)
                with pk2: st.markdown(kpi("green", "📈 Ganancia total est.",fmt_money(total_g),    f"{total_g/total_v*100:.1f}% margen"), unsafe_allow_html=True)
                with pk3: st.markdown(kpi("gold",  "📅 Mejor mes proy.",   fmt_money(mejor_mes['Ventas']), mejor_mes['Mes']), unsafe_allow_html=True)
                with pk4:
                    c_u = "green" if total_u >= 0 else "red"
                    st.markdown(kpi(c_u, "✅ Utilidad neta total", fmt_money(total_u), f"{total_u/total_v*100:.1f}% del ingreso"), unsafe_allow_html=True)

                # ── CAPACIDAD FINANCIERA ──
                st.markdown("<hr style='border-color:#1e2337;margin:20px 0'>", unsafe_allow_html=True)
                st.markdown(
                    '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.92rem;margin-bottom:6px">'
                    '🏋️ Capacidad Financiera — ¿Tienes el músculo para este crecimiento?</div>'
                    '<div style="font-size:0.72rem;color:#a8b4d0;margin-bottom:14px">'
                    'Cuánto capital necesitas para sostener este ritmo de crecimiento sin presión</div>',
                    unsafe_allow_html=True
                )

                # Capital requerido = gastos fijos × 3 meses (reserva) + pauta próximo mes
                capital_reserva   = gastos_op_hist * 3
                capital_pauta_mes = sum(st.session_state.get('pauta_dict', {}).values())
                capital_inv_prod  = filas_proy[0]['Ventas'] * 0.40  # ~40% de las ventas en inventario
                capital_total_req = capital_reserva + capital_pauta_mes + capital_inv_prod

                cf1, cf2, cf3, cf4 = st.columns(4)
                with cf1:
                    st.markdown(
                        f'<div style="background:rgba(6,182,212,0.07);border:1px solid #00d4ff44;'
                        f'border-radius:12px;padding:14px;text-align:center">'
                        f'<div style="font-size:0.6rem;color:#22d3ee;font-weight:800;text-transform:uppercase;margin-bottom:4px">🏦 Reserva operativa</div>'
                        f'<div style="font-size:0.58rem;color:#7a8aaa;margin-bottom:6px">3 meses de costos fijos</div>'
                        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:#22d3ee;font-size:1rem">{fmt_money(capital_reserva)}</div>'
                        f'</div>', unsafe_allow_html=True
                    )
                with cf2:
                    st.markdown(
                        f'<div style="background:rgba(139,92,246,0.07);border:1px solid #7c3aed44;'
                        f'border-radius:12px;padding:14px;text-align:center">'
                        f'<div style="font-size:0.6rem;color:#9333ea;font-weight:800;text-transform:uppercase;margin-bottom:4px">📣 Capital pauta</div>'
                        f'<div style="font-size:0.58rem;color:#7a8aaa;margin-bottom:6px">Inversión publicidad mes 1</div>'
                        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:#9333ea;font-size:1rem">{fmt_money(capital_pauta_mes)}</div>'
                        f'</div>', unsafe_allow_html=True
                    )
                with cf3:
                    st.markdown(
                        f'<div style="background:rgba(201,168,76,0.07);border:1px solid #f0c06044;'
                        f'border-radius:12px;padding:14px;text-align:center">'
                        f'<div style="font-size:0.6rem;color:#fcd34d;font-weight:800;text-transform:uppercase;margin-bottom:4px">📦 Capital inventario</div>'
                        f'<div style="font-size:0.58rem;color:#7a8aaa;margin-bottom:6px">~40% ventas mes 1</div>'
                        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:#fcd34d;font-size:1rem">{fmt_money(capital_inv_prod)}</div>'
                        f'</div>', unsafe_allow_html=True
                    )
                with cf4:
                    st.markdown(
                        f'<div style="background:rgba(99,102,241,0.12);border:2px solid #5b6cfc;'
                        f'border-radius:12px;padding:14px;text-align:center">'
                        f'<div style="font-size:0.6rem;color:#a855f7;font-weight:800;text-transform:uppercase;margin-bottom:4px">💪 CAPITAL TOTAL REQ.</div>'
                        f'<div style="font-size:0.58rem;color:#7a8aaa;margin-bottom:6px">para operar sin presión</div>'
                        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:#a855f7;font-size:1.1rem">{fmt_money(capital_total_req)}</div>'
                        f'</div>', unsafe_allow_html=True
                    )

                # Frase cierre
                st.markdown(
                    f'<div style="background:rgba(99,102,241,0.05);border:1px dashed #5b6cfc44;'
                    f'border-radius:10px;padding:14px 18px;margin-top:14px;font-size:0.76rem;color:#a8b4d0;line-height:1.7">'
                    f'💡 <b style="color:#fcd34d">Diagnóstico de capacidad:</b> '
                    f'Para sostener un crecimiento del <b style="color:#a855f7">{crecimiento_proy:.0f}% mensual</b> '
                    f'durante <b style="color:#a855f7">{n_meses_proy} meses</b>, necesitas un músculo financiero mínimo de '
                    f'<b style="color:#10b981">{fmt_money(capital_total_req)}</b>. '
                    f'Si la utilidad neta proyectada es <b style="color:{"#10b981" if total_u>=0 else "#ef4444"}">{fmt_money(total_u)}</b>, '
                    f'{"el negocio puede autofinanciarse parcialmente." if total_u > 0 else "necesitarás capital externo o reducir la tasa de crecimiento."}'
                    f'</div>',
                    unsafe_allow_html=True
                )

    # ══════════════════════════════════════════════════════════════════
    # 🫀 PULSO DEL NEGOCIO — PANEL EJECUTIVO REVOLUCIONARIO
    # ══════════════════════════════════════════════════════════════════
    elif "Pulso" in nav:
        from datetime import date, timedelta
        import calendar

        # ══════════════════════════════════════════════════════
        # SELECTOR DE MES POR NOMBRE
        # ══════════════════════════════════════════════════════
        MESES_ES = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",
                    7:"Julio",8:"Agosto",9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"}

        meses_disp = sorted(df['_mes'].dropna().unique().tolist(), reverse=True) if '_mes' in df.columns else []
        def _fmt_mes(m):
            try:
                y,mo = str(m).split('-'); return f"{MESES_ES[int(mo)]} {y}"
            except: return str(m)

        opciones_mes = meses_disp if meses_disp else [date.today().strftime("%Y-%m")]
        labels_mes   = [_fmt_mes(m) for m in opciones_mes]

        hdr_sel, _, _ = st.columns([1.4,2,2])
        with hdr_sel:
            idx_mes = st.selectbox("📅 Período analizado", range(len(opciones_mes)),
                                   format_func=lambda i: labels_mes[i], key="pulso_mes_sel")
        mes_sel = opciones_mes[idx_mes]
        mes_ant = opciones_mes[idx_mes+1] if idx_mes+1 < len(opciones_mes) else None

        df_act = df[df['_mes'] == mes_sel].copy() if '_mes' in df.columns else df.copy()
        df_ant = df[df['_mes'] == mes_ant].copy() if mes_ant and '_mes' in df.columns else pd.DataFrame()

        def _cnt(dframe, kw):
            return dframe[C_ESTATUS].astype(str).str.upper().str.contains(kw, na=False).sum() \
                   if C_ESTATUS in dframe.columns else 0

        n_tot  = len(df_act)
        n_ent  = _cnt(df_act, 'ENTREGAD')
        n_can  = _cnt(df_act, 'CANCELAD')
        n_dev  = _cnt(df_act, 'DEVOLUCI')
        n_proc = max(0, n_tot - n_ent - n_can - n_dev)

        ventas_act = df_act[C_TOTAL].sum()    if C_TOTAL    in df_act.columns else 0
        gan_act    = df_act[C_GANANCIA].sum() if C_GANANCIA in df_act.columns else 0
        flete_act  = df_act[C_FLETE].sum()    if C_FLETE    in df_act.columns else 0
        pauta_act  = sum(st.session_state.get('pauta_dict', {}).values())

        # Mes anterior
        n_tot_ant  = len(df_ant)
        n_ent_ant  = _cnt(df_ant, 'ENTREGAD') if len(df_ant) else 0
        n_can_ant  = _cnt(df_ant, 'CANCELAD') if len(df_ant) else 0
        n_dev_ant  = _cnt(df_ant, 'DEVOLUCI') if len(df_ant) else 0
        ventas_ant = df_ant[C_TOTAL].sum() if C_TOTAL in df_ant.columns and len(df_ant) else 0
        gan_ant    = df_ant[C_GANANCIA].sum() if C_GANANCIA in df_ant.columns and len(df_ant) else 0

        tasa_ent     = n_ent / n_tot * 100 if n_tot else 0
        tasa_dev     = n_dev / n_tot * 100 if n_tot else 0
        tasa_can     = n_can / n_tot * 100 if n_tot else 0
        tasa_ent_ant = n_ent_ant / n_tot_ant * 100 if n_tot_ant else 0
        tasa_dev_ant = n_dev_ant / n_tot_ant * 100 if n_tot_ant else 0
        tasa_can_ant = n_can_ant / n_tot_ant * 100 if n_tot_ant else 0
        margen       = gan_act / ventas_act * 100 if ventas_act else 0
        margen_ant   = gan_ant / ventas_ant * 100 if ventas_ant else 0

        # ══════════════════════════════════════════════════════
        # METAS DEL P&G — configurables
        # ══════════════════════════════════════════════════════
        with st.expander("⚙️ Configurar metas del P&G", expanded=False):
            pg1,pg2,pg3,pg4,pg5 = st.columns(5)
            with pg1: meta_ent      = st.number_input("🎯 Meta entrega %",     0.0,100.0, float(st.session_state.get('pg_meta_ent',65.0)),  step=1.0, key="pg_meta_ent")
            with pg2: meta_dev      = st.number_input("🎯 Meta devolución %",  0.0,100.0, float(st.session_state.get('pg_meta_dev',12.0)),  step=1.0, key="pg_meta_dev")
            with pg3: meta_can      = st.number_input("🎯 Meta cancelación %", 0.0,100.0, float(st.session_state.get('pg_meta_can',10.0)),  step=1.0, key="pg_meta_can")
            with pg4: meta_mrgn     = st.number_input("🎯 Meta margen bruto %",0.0,100.0, float(st.session_state.get('pg_meta_mrgn',55.0)), step=1.0, key="pg_meta_mrgn")
            with pg5: meta_pauta_mm = st.number_input("📣 Presupuesto máx pauta ($M)", 0.0, 500.0, float(st.session_state.get('pg_pauta_max',50.0)), step=1.0, key="pg_pauta_max")
        meta_pauta_max = meta_pauta_mm * 1_000_000

        # ══════════════════════════════════════════════════════
        # 🧮 SCORE vs METAS P&G — EXPLICACIÓN MATEMÁTICA
        #
        # Cada métrica se convierte en un logro (0→1) respecto a su meta P&G:
        #   Entrega:    logro = real / meta        (mayor = mejor) → peso 30 pts
        #   Margen:     logro = real / meta        (mayor = mejor) → peso 30 pts
        #   Devolución: logro = meta / real        (menor = mejor; si real≤meta → logro=1) → peso 20 pts
        #   Cancelación:logro = meta / real        (menor = mejor; si real≤meta → logro=1) → peso 20 pts
        #
        # Score = Σ min(logro, 1.0) × peso_pts  →  rango 0–100
        # Clasificación: ≥80 Excelente · ≥55 Atención · <55 Crítico
        # ══════════════════════════════════════════════════════
        logro_ent  = min(tasa_ent / meta_ent,  1.0) if meta_ent  else 0.0
        logro_mrgn = min(margen   / meta_mrgn, 1.0) if meta_mrgn else 0.0
        logro_dev  = min(meta_dev / tasa_dev,  1.0) if tasa_dev  else 1.0
        logro_can  = min(meta_can / tasa_can,  1.0) if tasa_can  else 1.0

        pts_ent  = logro_ent  * 30
        pts_mrgn = logro_mrgn * 30
        pts_dev  = logro_dev  * 20
        pts_can  = logro_can  * 20
        score_total = int(pts_ent + pts_mrgn + pts_dev + pts_can)

        score_color = "#10b981" if score_total >= 80 else "#f59e0b" if score_total >= 55 else "#ef4444"
        score_label = "EXCELENTE" if score_total >= 80 else "ATENCIÓN" if score_total >= 55 else "CRÍTICO"
        score_emoji = "🟢" if score_total >= 80 else "🟡" if score_total >= 55 else "🔴"

        # ── Layout: Velocímetro + Desglose con fórmulas ──
        col_gauge, col_break = st.columns([1, 1.7])

        with col_gauge:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score_total,
                number={'font':{'size':54,'color':score_color,'family':'Plus Jakarta Sans'}},
                gauge={
                    'axis':{'range':[0,100],'tickwidth':1,'tickcolor':'#1e2337',
                            'tickvals':[0,25,50,75,100],'tickfont':{'color':'#8892b0','size':10}},
                    'bar':{'color':score_color,'thickness':0.2},
                    'bgcolor':'#12151f','borderwidth':0,
                    'steps':[
                        {'range':[0,40],  'color':'rgba(239,68,68,0.12)'},
                        {'range':[40,70], 'color':'rgba(245,158,11,0.12)'},
                        {'range':[70,100],'color':'rgba(16,185,129,0.12)'},
                    ],
                    'threshold':{'line':{'color':'white','width':3},'thickness':0.8,'value':score_total}
                },
                title={'text':f"<b>SALUD DEL NEGOCIO</b><br><span style='font-size:11px;color:{score_color}'>"
                             f"{score_emoji} {score_label} · vs Metas P&G</span>",
                       'font':{'color':'#e8ecf7','size':12,'family':'Plus Jakarta Sans'}}
            ))
            _gl = {k:v for k,v in PLOT_LAYOUT.items() if k != 'margin'}
            fig_gauge.update_layout(**_gl, height=260, margin=dict(t=50,b=5,l=15,r=15))
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_break:
            # Cabecera con explicación
            st.markdown(
                '<div style="background:#0f0e1d;border:1px solid #2e2558;border-radius:12px;'
                'padding:14px 18px;margin-bottom:12px;margin-top:8px">'
                '<div style="font-size:0.65rem;color:#fcd34d;font-weight:800;text-transform:uppercase;'
                'letter-spacing:0.07em;margin-bottom:10px">🧮 Metodología matemática del Score de Salud</div>'
                '<div style="font-size:0.7rem;color:#a8b4d0;line-height:1.7;margin-bottom:10px">'
                'El score mide <b style="color:#e8ecf7">qué tan cerca estás de cumplir cada meta del P&G</b>, '
                'no el valor absoluto. Para métricas donde mayor es mejor '
                '(entrega, margen): <code style="background:#13102a;color:#a855f7;padding:1px 5px;border-radius:3px">Logro = Real ÷ Meta</code>. '
                'Para métricas donde menor es mejor '
                '(devolución, cancelación): <code style="background:#13102a;color:#f59e0b;padding:1px 5px;border-radius:3px">Logro = Meta ÷ Real</code>. '
                'En ambos casos el logro se <b style="color:#fcd34d">limita a máximo 1.0</b>.</div>'
                '<div style="background:#13102a;border:1px solid #2e2558;border-radius:8px;'
                'padding:10px 14px;margin-bottom:10px;font-size:0.68rem;color:#a8b4d0;line-height:1.9">'
                '<b style="color:#fcd34d">Fórmula:</b><br>'
                '<code style="color:#22d3ee">Score = min(Ent/MetaEnt,1)×30 + min(Mrg/MetaMrg,1)×30 '
                '+ min(MetaDev/Dev,1)×20 + min(MetaCan/Can,1)×20</code><br>'
                '<span style="color:#7a8aaa">Rango 0-100 · </span>'
                '<span style="color:#10b981">≥80 EXCELENTE</span>'
                '<span style="color:#7a8aaa"> · </span>'
                '<span style="color:#f59e0b">≥55 ATENCIÓN</span>'
                '<span style="color:#7a8aaa"> · </span>'
                '<span style="color:#ef4444">&lt;55 CRÍTICO</span></div>'
                '<div style="font-size:0.67rem;color:#a8b4d0;line-height:1.6">'
                '⚖️ <b style="color:#c8d0e8">Pesos:</b> '
                '<span style="color:#a855f7">Entrega 30pts</span> — cumplimiento logístico · '
                '<span style="color:#10b981">Margen 30pts</span> — salud financiera · '
                '<span style="color:#f59e0b">Devolución 20pts</span> — calidad producto/proceso · '
                '<span style="color:#ef4444">Cancelación 20pts</span> — intención de compra vs operación. '
                'Los 3 indicadores logísticos suman 70pts; el financiero 30pts.'
                '</div></div>',
                unsafe_allow_html=True
            )
            # Barras de desglose
            componentes = [
                ("🚚 Entrega",     pts_ent,  30, tasa_ent, meta_ent,  False, "#5b6cfc"),
                ("💰 Margen",      pts_mrgn, 30, margen,   meta_mrgn, False, "#10b981"),
                ("↩️ Devolución",  pts_dev,  20, tasa_dev, meta_dev,  True,  "#f59e0b"),
                ("❌ Cancelación", pts_can,  20, tasa_can, meta_can,  True,  "#ef4444"),
            ]
            for lbl, pts, maxpts, real, meta, invert, col_c in componentes:
                pct_b  = pts / maxpts * 100
                c_b    = "#10b981" if pct_b >= 80 else "#f59e0b" if pct_b >= 50 else "#ef4444"
                cumple = (real <= meta) if invert else (real >= meta)
                formula_str = f"= {meta:.1f}÷{real:.1f}" if invert else f"= {real:.1f}÷{meta:.1f}"
                st.markdown(
                    f'<div style="margin-bottom:8px">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;font-size:0.72rem;margin-bottom:2px">'
                    f'<span style="color:#c8d0e8;font-weight:600">{lbl}</span>'
                    f'<span style="color:{c_b};font-weight:800">{pts:.1f}/{maxpts} pts</span>'
                    f'</div>'
                    f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:3px">'
                    f'<code style="background:#13102a;color:{col_c};font-size:0.62rem;padding:1px 6px;border-radius:4px">'
                    f'Real {real:.1f}% · Meta {meta:.1f}% · Logro {formula_str} = {min(pts/maxpts,1):.2f}</code>'
                    f'<span style="font-size:0.65rem;{"color:#10b981" if cumple else "color:#ef4444"};font-weight:700">'
                    f'{"✓ META" if cumple else "✗ BAJO"}</span>'
                    f'</div>'
                    f'<div style="background:#1e2337;border-radius:100px;height:7px;overflow:hidden">'
                    f'<div style="background:{c_b};width:{pct_b:.0f}%;height:100%;border-radius:100px"></div>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )

        st.markdown("<hr style='border-color:#1e2337;margin:12px 0'>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════
        # KPIs PRINCIPALES — Pedidos Totales es el protagonista
        # ══════════════════════════════════════════════════════
        k1,k2,k3,k4,k5,k6 = st.columns(6)
        with k1:
            # Pedidos totales — protagonista con estilo especial
            delta_tot = n_tot - n_tot_ant
            delta_col = "#10b981" if delta_tot >= 0 else "#ef4444"
            delta_sym = "▲" if delta_tot >= 0 else "▼"
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#5b6cfc25,#5b6cfc08);'
                f'border:2px solid #5b6cfc;border-radius:14px;padding:14px 10px;text-align:center">'
                f'<div style="font-size:0.62rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;'
                f'letter-spacing:0.06em;margin-bottom:4px">📦 PEDIDOS TOTALES</div>'
                f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:#a855f7;font-size:1.7rem;'
                f'margin:2px 0;line-height:1">{n_tot:,}</div>'
                f'<div style="font-size:0.7rem;color:{delta_col};font-weight:700;margin-top:4px">'
                f'{delta_sym} {abs(delta_tot):,} vs mes ant.</div>'
                f'</div>', unsafe_allow_html=True
            )
        with k2: st.markdown(kpi("green","✅ Entregados",  f"{n_ent:,}",        f"{tasa_ent:.1f}% · meta {meta_ent:.0f}%"), unsafe_allow_html=True)
        with k3: st.markdown(kpi("red",  "❌ Cancelados",  f"{n_can:,}",        f"{tasa_can:.1f}% · meta {meta_can:.0f}%"), unsafe_allow_html=True)
        with k4: st.markdown(kpi("gold", "↩️ Devueltos",  f"{n_dev:,}",        f"{tasa_dev:.1f}% · meta {meta_dev:.0f}%"), unsafe_allow_html=True)
        with k5: st.markdown(kpi("cyan", "⏳ En Proceso",  f"{n_proc:,}",       "pedidos activos"),                         unsafe_allow_html=True)
        with k6: st.markdown(kpi("blue", "💰 Ventas",      fmt_money(ventas_act),f"Margen {margen:.1f}%"),                  unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════
        # BARRA DE PAUTA — Presupuesto P&G vs Inversión Real
        # Alerta si pauta > 18% de facturación
        # ══════════════════════════════════════════════════════
        st.markdown(
            '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.88rem;margin-bottom:10px">'
            '📣 Control de Presupuesto de Pauta Publicitaria</div>',
            unsafe_allow_html=True
        )
        pauta_pct_ing  = pauta_act / ventas_act * 100 if ventas_act else 0
        pauta_pct_ppto = pauta_act / meta_pauta_max * 100 if meta_pauta_max else 0
        excede_18      = pauta_pct_ing > 18
        c_pauta        = "#ef4444" if excede_18 else "#10b981"
        estado_pauta   = "🔴 EXCEDE el 18% de la facturación — presupuesto en riesgo" if excede_18 \
                         else "🟢 Dentro del límite saludable (≤18% de facturación)"
        st.markdown(
            f'<div style="background:#13102a;border:1px solid {c_pauta}44;border-radius:14px;padding:18px 22px;margin-bottom:14px">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px">'
            f'<div>'
            f'<div style="font-size:0.68rem;color:#a8b4d0;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px">Inversión real en pauta</div>'
            f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:{c_pauta};font-size:1.25rem">{fmt_money(pauta_act)}</div>'
            f'</div>'
            f'<div style="text-align:right">'
            f'<div style="font-size:0.68rem;color:#a8b4d0;margin-bottom:4px">Presupuesto máx. P&G</div>'
            f'<div style="font-size:1rem;font-weight:700;color:#fcd34d">{fmt_money(meta_pauta_max)}</div>'
            f'</div>'
            f'</div>'
            f'<div style="font-size:0.68rem;color:#a8b4d0;margin-bottom:4px">Utilizado del presupuesto P&G ({pauta_pct_ppto:.1f}%)</div>'
            f'<div style="background:#1e2337;border-radius:100px;height:16px;overflow:hidden;margin-bottom:10px;position:relative">'
            f'<div style="background:linear-gradient(90deg,{c_pauta}dd,{c_pauta}88);'
            f'width:{min(pauta_pct_ppto,100):.1f}%;height:100%;border-radius:100px"></div>'
            f'<span style="position:absolute;right:8px;top:50%;transform:translateY(-50%);'
            f'font-size:0.65rem;font-weight:800;color:white">{min(pauta_pct_ppto,100):.1f}%</span>'
            f'</div>'
            f'<div style="font-size:0.68rem;color:#a8b4d0;margin-bottom:4px">% sobre facturación — límite máximo 18%</div>'
            f'<div style="background:#1e2337;border-radius:100px;height:16px;overflow:hidden;margin-bottom:10px;position:relative">'
            f'<div style="background:linear-gradient(90deg,{c_pauta}dd,{c_pauta}88);'
            f'width:{min(pauta_pct_ing/18*100,100):.1f}%;height:100%;border-radius:100px"></div>'
            f'<span style="position:absolute;right:8px;top:50%;transform:translateY(-50%);'
            f'font-size:0.65rem;font-weight:800;color:white">{pauta_pct_ing:.1f}%</span>'
            f'</div>'
            f'<div style="display:flex;justify-content:space-between;align-items:center">'
            f'<span style="font-size:0.75rem;color:{c_pauta};font-weight:700">{estado_pauta}</span>'
            f'<span style="font-size:0.7rem;color:#7a8aaa">{fmt_money(pauta_act)} de {fmt_money(meta_pauta_max)}</span>'
            f'</div></div>',
            unsafe_allow_html=True
        )

        # ══════════════════════════════════════════════════════
        # CUADRO DE EFICIENCIA PUBLICITARIA
        # Pérdidas por cancelación y devolución + CPA + ROAS
        # Fórmula pérdida: (pauta_total / n_tot) × n_problematicos
        # ══════════════════════════════════════════════════════
        st.markdown(
            '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.88rem;margin-bottom:10px">'
            '💸 Eficiencia Publicitaria — Pérdidas e Indicadores</div>',
            unsafe_allow_html=True
        )
        cpm_unitario  = pauta_act / n_tot  if n_tot  else 0   # Costo por pedido (todos)
        cpa_unitario  = pauta_act / n_ent  if n_ent  else 0   # CPA real (solo entregados)
        perdida_can   = cpm_unitario * n_can                   # Pauta quemada en cancelados
        perdida_dev   = cpm_unitario * n_dev                   # Pauta quemada en devueltos
        total_perdido = perdida_can + perdida_dev
        roas          = ventas_act / pauta_act if pauta_act else 0
        c_roas        = "#10b981" if roas >= 3 else "#f59e0b" if roas >= 1.5 else "#ef4444"

        pub1,pub2,pub3,pub4 = st.columns(4)
        def pub_card(titulo, subtitulo, valor_str, formula_str, color_top, nota=""):
            nota_html = f'<div style="font-size:0.65rem;color:{color_top};font-weight:700;margin-top:4px">{nota}</div>' if nota else ''
            return (
                f'<div style="background:#13102a;border:1px solid {color_top}44;'
                f'border-top:3px solid {color_top};border-radius:12px;padding:14px;text-align:center">'
                f'<div style="font-size:0.62rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;'
                f'letter-spacing:0.05em;margin-bottom:4px;line-height:1.3">{titulo}</div>'
                f'<div style="font-size:0.6rem;color:#7a8aaa;margin-bottom:6px;line-height:1.3">{subtitulo}</div>'
                f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:{color_top};font-size:1.1rem">{valor_str}</div>'
                f'<div style="font-size:0.62rem;color:#7a8aaa;margin-top:5px;line-height:1.4">{formula_str}</div>'
                f'{nota_html}'
                f'</div>'
            )
        with pub1:
            st.markdown(pub_card(
                "CPA", "Costo por pedido entregado",
                fmt_money(cpa_unitario),
                f"Pauta ÷ {n_ent:,} entregados", "#00d4ff"
            ), unsafe_allow_html=True)
        with pub2:
            st.markdown(pub_card(
                "💸 Pérdida — Cancelaciones",
                f"({fmt_money(cpm_unitario)}/ped) × {n_can:,} cancelados",
                fmt_money(perdida_can),
                f"Pauta({fmt_money(pauta_act)}) ÷ {n_tot:,} × {n_can:,}", "#ef4444",
                f"= {perdida_can/pauta_act*100:.1f}% de la pauta" if pauta_act else ""
            ), unsafe_allow_html=True)
        with pub3:
            st.markdown(pub_card(
                "💸 Pérdida — Devoluciones",
                f"({fmt_money(cpm_unitario)}/ped) × {n_dev:,} devueltos",
                fmt_money(perdida_dev),
                f"Pauta({fmt_money(pauta_act)}) ÷ {n_tot:,} × {n_dev:,}", "#f59e0b",
                f"= {perdida_dev/pauta_act*100:.1f}% de la pauta" if pauta_act else ""
            ), unsafe_allow_html=True)
        with pub4:
            st.markdown(pub_card(
                "ROAS", "Retorno sobre inversión publicitaria",
                f"{roas:.1f}x",
                f"Ventas ÷ Pauta", c_roas,
                "✓ Óptimo ≥ 3x" if roas >= 3 else "⚠ Revisar < 3x"
            ), unsafe_allow_html=True)

        if total_perdido > 0 and pauta_act > 0:
            pct_perdido = total_perdido / pauta_act * 100
            st.markdown(
                f'<div style="background:rgba(239,68,68,0.07);border:1px dashed #ef444466;'
                f'border-radius:10px;padding:10px 16px;margin-top:10px;'
                f'display:flex;justify-content:space-between;align-items:center">'
                f'<div><span style="font-size:0.78rem;color:#ef4444;font-weight:700">'
                f'💸 Total pauta perdida (cancelaciones + devoluciones)</span>'
                f'<div style="font-size:0.65rem;color:#a8b4d0;margin-top:2px">'
                f'= (Pauta total ÷ Pedidos totales) × (Cancelados + Devueltos) · '
                f'= ({fmt_money(cpm_unitario)}/ped) × {n_can+n_dev:,} pedidos</div></div>'
                f'<div style="text-align:right">'
                f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#ef4444;font-size:1.1rem">{fmt_money(total_perdido)}</div>'
                f'<div style="font-size:0.65rem;color:#ef4444">{pct_perdido:.1f}% de la pauta total</div>'
                f'</div></div>',
                unsafe_allow_html=True
            )

        st.markdown("<hr style='border-color:#1e2337;margin:14px 0'>", unsafe_allow_html=True)



    elif "El Marcador" in nav:
        from datetime import date, timedelta

        # ══════════════════════════════════════════════════════
        # SELECTOR DE MES POR NOMBRE (igual que Pulso)
        # ══════════════════════════════════════════════════════
        _MESES_MK = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",
                     7:"Julio",8:"Agosto",9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"}
        def _fmt_m(m):
            try: y,mo=str(m).split('-'); return f"{_MESES_MK[int(mo)]} {y}"
            except: return str(m)

        _meses_mk = sorted(df['_mes'].dropna().unique().tolist(), reverse=True) if '_mes' in df.columns else []
        _opciones_mk = _meses_mk if _meses_mk else [date.today().strftime("%Y-%m")]
        _labels_mk   = [_fmt_m(m) for m in _opciones_mk]

        _hdr_mk, _, _ = st.columns([1.5,2,2])
        with _hdr_mk:
            _idx_mk = st.selectbox("📅 Comparar mes", range(len(_opciones_mk)),
                                   format_func=lambda i: _labels_mk[i], key="marcador_mes_sel")
        _mes_mk  = _opciones_mk[_idx_mk]
        _mes_ant = _opciones_mk[_idx_mk+1] if _idx_mk+1 < len(_opciones_mk) else None

        df_act = df[df['_mes'] == _mes_mk].copy()  if '_mes' in df.columns else df.copy()
        df_ant = df[df['_mes'] == _mes_ant].copy() if _mes_ant and '_mes' in df.columns else pd.DataFrame()

        def _ce(dframe, kw):
            return dframe[C_ESTATUS].astype(str).str.upper().str.contains(kw,na=False).sum() \
                   if C_ESTATUS in dframe.columns else 0

        n_tot    = len(df_act);   n_tot_ant  = len(df_ant)
        n_ent    = _ce(df_act,'ENTREGAD'); n_ent_ant = _ce(df_ant,'ENTREGAD') if len(df_ant) else 0
        n_dev    = _ce(df_act,'DEVOLUCI'); n_dev_ant = _ce(df_ant,'DEVOLUCI') if len(df_ant) else 0
        n_can    = _ce(df_act,'CANCELAD'); n_can_ant = _ce(df_ant,'CANCELAD') if len(df_ant) else 0

        ventas_act = df_act[C_TOTAL].sum()    if C_TOTAL    in df_act.columns else 0
        gan_act    = df_act[C_GANANCIA].sum() if C_GANANCIA in df_act.columns else 0
        ventas_ant = df_ant[C_TOTAL].sum()    if C_TOTAL    in df_ant.columns and len(df_ant) else 0
        gan_ant    = df_ant[C_GANANCIA].sum() if C_GANANCIA in df_ant.columns and len(df_ant) else 0

        # Tasas (%)
        tasa_ent_act = n_ent / n_tot * 100     if n_tot     else 0
        tasa_dev_act = n_dev / n_tot * 100     if n_tot     else 0
        tasa_can_act = n_can / n_tot * 100     if n_tot     else 0
        margen_act   = gan_act / ventas_act * 100 if ventas_act else 0

        tasa_ent_ant = n_ent_ant / n_tot_ant * 100 if n_tot_ant else 0
        tasa_dev_ant = n_dev_ant / n_tot_ant * 100 if n_tot_ant else 0
        tasa_can_ant = n_can_ant / n_tot_ant * 100 if n_tot_ant else 0
        margen_ant   = gan_ant   / ventas_ant * 100 if ventas_ant else 0

        st.markdown('<div class="seccion-titulo">🎯 El Marcador</div>', unsafe_allow_html=True)

        label_ant = _fmt_m(_mes_ant) if _mes_ant else "mes ant."

        # ══════════════════════════════════════════════════════
        # FUNCIÓN DE TARJETA — DOS TIPOS DE VARIACIÓN:
        #
        #  modo="pct_relativa"  → Variación relativa %
        #     Δ% = (act - ant) / ant × 100
        #     Uso: ventas, ganancia, pedidos (valores absolutos)
        #     Ejemplo: ventas subieron 23.5%
        #
        #  modo="pp"  → Diferencia en Puntos Porcentuales
        #     Δpp = tasa_act - tasa_ant   (ambas ya en %)
        #     Uso: % entrega, % devolución, % cancelación, % margen
        #     Ejemplo: devolución pasó de 8% a 10% → "subimos 2 pp"
        #     Regla: para métricas "malo si sube" se invierte el color
        # ══════════════════════════════════════════════════════
        def marcador_card(titulo, val_act, val_ant, fmt_fn, icono, color_base,
                          modo="pct_relativa", malo_si_sube=False, unidad=""):
            sin_ant = val_ant == 0 or _mes_ant is None

            if modo == "pp":
                # ── Puntos Porcentuales ──
                # El DELTA es el protagonista: si dev pasó de 8% a 10% → mostramos "+2 pp"
                delta_pp = val_act - val_ant
                sube     = delta_pp > 0
                c_delta  = ("#ef4444" if sube else "#10b981") if malo_si_sube \
                           else ("#10b981" if sube else "#ef4444")
                if abs(delta_pp) < 0.05:
                    delta_hero = "= 0 pp"
                    txt_accion = "sin cambio"
                    c_delta    = "#8892b0"
                elif sube:
                    delta_hero = f"+{abs(delta_pp):.1f} pp"
                    txt_accion = f"aumentamos {abs(delta_pp):.1f} pp"
                else:
                    delta_hero = f"−{abs(delta_pp):.1f} pp"
                    txt_accion = f"bajamos {abs(delta_pp):.1f} pp"
                txt_comparativo = f"{label_ant}: {fmt_fn(val_ant)}  →  ahora: {fmt_fn(val_act)}"

            else:
                # ── Variación relativa % ──
                # El DELTA es el protagonista: si ventas subieron de 10M a 12M → mostramos "+20%"
                delta_pct = (val_act - val_ant) / val_ant * 100 if not sin_ant else 0
                sube      = delta_pct > 0
                c_delta   = ("#ef4444" if sube else "#10b981") if malo_si_sube \
                            else ("#10b981" if sube else "#ef4444")
                if sin_ant:
                    delta_hero = "—"
                    txt_accion = "sin datos del mes anterior"
                    txt_comparativo = f"ahora: {fmt_fn(val_act)}"
                    c_delta    = "#8892b0"
                elif abs(delta_pct) < 0.1:
                    delta_hero = "= 0%"
                    txt_accion = "sin cambio"
                    txt_comparativo = f"{label_ant}: {fmt_fn(val_ant)}  →  ahora: {fmt_fn(val_act)}"
                    c_delta    = "#8892b0"
                elif sube:
                    delta_hero = f"+{abs(delta_pct):.1f}%"
                    txt_accion = f"subimos {abs(delta_pct):.1f}%"
                    txt_comparativo = f"{label_ant}: {fmt_fn(val_ant)}  →  ahora: {fmt_fn(val_act)}"
                else:
                    delta_hero = f"−{abs(delta_pct):.1f}%"
                    txt_accion = f"bajamos {abs(delta_pct):.1f}%"
                    txt_comparativo = f"{label_ant}: {fmt_fn(val_ant)}  →  ahora: {fmt_fn(val_act)}"

            # ── HTML: DELTA como número grande, valor actual pequeño ──
            return (
                f'<div style="background:#13102a;border:1px solid #2e2558;border-radius:14px;'
                f'padding:16px 12px;border-top:3px solid {color_base};text-align:center;height:100%">'
                # Icono + título
                f'<div style="font-size:1.3rem;margin-bottom:4px">{icono}</div>'
                f'<div style="font-size:0.62rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;'
                f'letter-spacing:0.07em;margin-bottom:10px;line-height:1.3">{titulo}</div>'
                # DELTA — protagonista
                f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:{c_delta};'
                f'font-size:1.6rem;margin-bottom:4px;line-height:1">{delta_hero}</div>'
                # Texto acción natural
                f'<div style="font-size:0.72rem;color:{c_delta};font-weight:600;margin-bottom:10px">'
                f'{txt_accion}</div>'
                # Barra divisora sutil
                f'<div style="border-top:1px solid #1e2337;padding-top:8px">'
                # Comparativo → fila pequeña
                f'<div style="font-size:0.63rem;color:#7a8aaa;line-height:1.5">{txt_comparativo}</div>'
                f'</div></div>'
            )

        # ── Fila 1: Métricas monetarias/conteo (variación relativa %) ──
        st.markdown(
            '<div style="font-size:0.65rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;'
            'letter-spacing:0.08em;margin-bottom:8px">'
            '📊 Variación relativa — ¿cuánto % subió o bajó el valor?</div>',
            unsafe_allow_html=True
        )
        mc1,mc2,mc3,mc4 = st.columns(4)
        with mc1: st.markdown(marcador_card("Ventas brutas",  ventas_act, ventas_ant, fmt_money,         "💰","#5b6cfc"), unsafe_allow_html=True)
        with mc2: st.markdown(marcador_card("Ganancia neta",  gan_act,    gan_ant,    fmt_money,         "📈","#10b981"), unsafe_allow_html=True)
        with mc3: st.markdown(marcador_card("Pedidos totales",n_tot,      n_tot_ant,  lambda x:f"{int(x):,}","📦","#00d4ff"), unsafe_allow_html=True)
        with mc4: st.markdown(marcador_card("Entregados",     n_ent,      n_ent_ant,  lambda x:f"{int(x):,}","✅","#10b981"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Fila 2: Tasas porcentuales (diferencia en Puntos Porcentuales) ──
        st.markdown(
            '<div style="font-size:0.65rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;'
            'letter-spacing:0.08em;margin-bottom:8px">'
            '📐 Variación en puntos porcentuales — ¿cuánto pp subió o bajó la tasa?</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div style="background:#161525;border:1px solid #2e2558;border-radius:8px;padding:8px 14px;'
            'margin-bottom:10px;font-size:0.68rem;color:#a8b4d0;line-height:1.6">'
            '💡 <b style="color:#fcd34d">¿Qué son los puntos porcentuales (pp)?</b> '
            'Si la devolución era <b>8%</b> el mes anterior y ahora es <b>10%</b>, '
            'el delta es <b style="color:#ef4444">+2 pp</b> — no un "25% de aumento". '
            'Los pp miden la diferencia directa entre dos tasas. '
            'Aquí mostramos únicamente esa variación, no el porcentaje actual.</div>',
            unsafe_allow_html=True
        )
        pp1,pp2,pp3,pp4 = st.columns(4)
        with pp1: st.markdown(marcador_card("% Entrega",    tasa_ent_act, tasa_ent_ant, lambda x:f"{x:.1f}%","🚚","#00d4ff", modo="pp", malo_si_sube=False), unsafe_allow_html=True)
        with pp2: st.markdown(marcador_card("% Devolución", tasa_dev_act, tasa_dev_ant, lambda x:f"{x:.1f}%","↩️","#f59e0b", modo="pp", malo_si_sube=True),  unsafe_allow_html=True)
        with pp3: st.markdown(marcador_card("% Cancelación",tasa_can_act, tasa_can_ant, lambda x:f"{x:.1f}%","❌","#ef4444", modo="pp", malo_si_sube=True),  unsafe_allow_html=True)
        with pp4: st.markdown(marcador_card("% Margen",     margen_act,   margen_ant,   lambda x:f"{x:.1f}%","💰","#10b981", modo="pp", malo_si_sube=False), unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#1e2337;margin:16px 0'>", unsafe_allow_html=True)

        # FIN EL MARCADOR


    elif "Centro" in nav or "Mando" in nav:
        from datetime import date, timedelta
        hoy = date.today()
        mes_actual = hoy.strftime('%Y-%m')
        mes_ant = (hoy.replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
        df_act = df[df['_mes'] == mes_actual].copy() if '_mes' in df.columns else df.copy()
        df_ant = df[df['_mes'] == mes_ant].copy() if '_mes' in df.columns else pd.DataFrame()
        def _pct(val): return df_act[C_ESTATUS].astype(str).str.upper().str.contains(val,na=False).sum() if C_ESTATUS in df_act.columns else 0
        n_tot=len(df_act); n_ent=_pct('ENTREGAD'); n_dev=_pct('DEVOLUCI'); n_can=_pct('CANCELAD'); n_proc=n_tot-n_ent-n_can-n_dev
        ventas_act=df_act[C_TOTAL].sum() if C_TOTAL in df_act.columns else 0
        gan_act=df_act[C_GANANCIA].sum() if C_GANANCIA in df_act.columns else 0
        ventas_ant=df_ant[C_TOTAL].sum() if C_TOTAL in df_ant.columns and len(df_ant) else 0
        tasa_ent=n_ent/n_tot*100 if n_tot else 0; tasa_dev=n_dev/n_tot*100 if n_tot else 0; tasa_can=n_can/n_tot*100 if n_tot else 0
        margen=gan_act/ventas_act*100 if ventas_act else 0
        score_ent=min(tasa_ent/80*35,35); score_mrgn=min(margen/30*25,25)
        score_dev=max(0,20-tasa_dev*1.5); score_can=max(0,20-tasa_can*1.0)
        score_total=int(score_ent+score_mrgn+score_dev+score_can)
        score_color='#10b981' if score_total>=75 else '#f59e0b' if score_total>=50 else '#ef4444'
        score_label='EXCELENTE' if score_total>=75 else 'ATENCIÓN' if score_total>=50 else 'CRÍTICO'
        st.markdown('<div class="seccion-titulo">🚨 Centro de Mando — Alertas Prioritarias</div>', unsafe_allow_html=True)
        # ══════════════════════════════════════════
        # 🚨 COMPONENTE 5 — CENTRO DE MANDO
        # ══════════════════════════════════════════
        st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:1rem;margin-bottom:14px">🚨 Centro de Mando — Alertas Prioritarias</div>', unsafe_allow_html=True)

        alertas_cmd = []
        if tasa_dev > 15:
            alertas_cmd.append({"nivel":1,"icono":"🔴","titulo":"Devoluciones críticas",
                "msg":f"Tu tasa de devolución es {tasa_dev:.1f}% — el doble del umbral saludable (7%).",
                "accion":"Revisa las ciudades con más devoluciones en el Mapa Colombia.", "color":"#ef4444"})
        if tasa_can > 15:
            alertas_cmd.append({"nivel":1,"icono":"🔴","titulo":"Cancelaciones elevadas",
                "msg":f"{tasa_can:.1f}% de cancelación — revisa el proceso de confirmación.",
                "accion":"Refuerza el equipo de confirmación y revisa tiempos de respuesta.", "color":"#ef4444"})
        if margen < 15:
            alertas_cmd.append({"nivel":1,"icono":"🔴","titulo":"Margen en riesgo",
                "msg":f"Margen bruto de {margen:.1f}% — por debajo del mínimo recomendado (15%).",
                "accion":"Revisa costos de producto y pauta en el módulo Finanzas.", "color":"#ef4444"})
        if n_proc > n_tot * 0.4:
            alertas_cmd.append({"nivel":2,"icono":"🟡","titulo":"Alta cartera en tránsito",
                "msg":f"{n_proc:,} pedidos ({n_proc/n_tot*100:.0f}%) aún en proceso — capital inmovilizado.",
                "accion":"Monitorea con las transportadoras los pedidos más antiguos.", "color":"#f59e0b"})
        if tasa_ent < 60:
            alertas_cmd.append({"nivel":2,"icono":"🟡","titulo":"Entrega por debajo del objetivo",
                "msg":f"Solo {tasa_ent:.1f}% de entrega efectiva — el objetivo es ≥80%.",
                "accion":"Identifica las transportadoras con menor rendimiento.", "color":"#f59e0b"})
        if ventas_ant > 0 and ventas_act < ventas_ant * 0.85:
            alertas_cmd.append({"nivel":2,"icono":"🟡","titulo":"Caída en ventas",
                "msg":f"Ventas {(1-ventas_act/ventas_ant)*100:.0f}% por debajo del mes anterior.",
                "accion":"Aumenta pauta o revisa el catálogo de productos.", "color":"#f59e0b"})
        if score_total >= 75:
            alertas_cmd.append({"nivel":3,"icono":"🟢","titulo":"Operación saludable",
                "msg":f"Score de salud {score_total}/100 — el negocio opera dentro de los parámetros ideales.",
                "accion":"Mantén el ritmo y analiza oportunidades de escalar.", "color":"#10b981"})

        alertas_cmd.sort(key=lambda x: x['nivel'])

        if alertas_cmd:
            acols = st.columns(min(len(alertas_cmd), 3))
            for idx, alerta in enumerate(alertas_cmd[:6]):
                with acols[idx % 3]:
                    st.markdown(
                        f'<div style="background:#13102a;border:1px solid {alerta["color"]}44;'
                        f'border-left:4px solid {alerta["color"]};border-radius:12px;padding:16px;margin-bottom:12px">'
                        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">'
                        f'<span style="font-size:1.1rem">{alerta["icono"]}</span>'
                        f'<span style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.85rem">{alerta["titulo"]}</span>'
                        f'</div>'
                        f'<div style="font-size:0.78rem;color:#a8b4d0;margin-bottom:10px;line-height:1.5">{alerta["msg"]}</div>'
                        f'<div style="background:{alerta["color"]}15;border-radius:8px;padding:8px 10px">'
                        f'<span style="font-size:0.72rem;color:{alerta["color"]};font-weight:700">⚡ Acción: </span>'
                        f'<span style="font-size:0.72rem;color:#c8d0e8">{alerta["accion"]}</span>'
                        f'</div></div>',
                        unsafe_allow_html=True
                    )

        st.markdown("<hr style='border-color:#1e2337;margin:16px 0'>", unsafe_allow_html=True)

        # ══════════════════════════════════════════
        # 💬 COMPONENTE 6 — EL NEGOCIO TE HABLA
        # ══════════════════════════════════════════
        st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:1rem;margin-bottom:14px">💬 El Negocio te Habla</div>', unsafe_allow_html=True)

        # Generar resumen dinámico en lenguaje natural
        prod_top = ""
        if C_PRODUCTO in df_act.columns and C_GANANCIA in df_act.columns:
            top = df_act.groupby(C_PRODUCTO)[C_GANANCIA].sum().idxmax() if len(df_act) else ""
            prod_top = f" Tu producto más rentable fue <b style='color:#fcd34d'>{str(top)[:40]}</b>." if top else ""

        ciudad_prob = ""
        if C_CIUDAD in df_act.columns and C_ESTATUS in df_act.columns:
            devs_ciudad = df_act[df_act[C_ESTATUS].astype(str).str.upper().str.contains('DEVOLUCI',na=False)].groupby(C_CIUDAD).size()
            if len(devs_ciudad):
                c_prob = devs_ciudad.idxmax()
                ciudad_prob = f" Las devoluciones se concentran principalmente en <b style='color:#f59e0b'>{c_prob}</b>."

        delta_pct = (ventas_act - ventas_ant) / ventas_ant * 100 if ventas_ant else 0
        comparativo = (
            f"un <b style='color:#10b981'>+{delta_pct:.0f}%</b> más que el mes anterior" if delta_pct >= 0
            else f"un <b style='color:#ef4444'>{delta_pct:.0f}%</b> menos que el mes anterior"
        )

        alertas_criticas = sum(1 for a in alertas_cmd if a['nivel'] == 1)
        txt_alertas = (
            f"Tienes <b style='color:#ef4444'>{alertas_criticas} alerta{'s' if alertas_criticas!=1 else ''} crítica{'s' if alertas_criticas!=1 else ''}</b> que requieren atención inmediata."
            if alertas_criticas else
            "<b style='color:#10b981'>No tienes alertas críticas</b> — la operación fluye bien."
        )

        resumen_txt = (
            f"Este mes llevás <b style='color:#a855f7'>{n_tot:,} pedidos</b> procesados, "
            f"de los cuales <b style='color:#10b981'>{n_ent:,} fueron entregados</b> — {comparativo}. "
            f"Tu tasa de entrega es del <b style='color:#10b981'>{tasa_ent:.1f}%</b>"
            + (f", sin embargo la devolución subió al <b style='color:#f59e0b'>{tasa_dev:.1f}%</b>.{ciudad_prob}" if tasa_dev > 7 else f" con devolución controlada en {tasa_dev:.1f}%.") +
            f" {txt_alertas}{prod_top} "
            f"El score de salud del negocio hoy es <b style='color:{score_color}'>{score_total}/100 — {score_label}</b>."
        )

        st.markdown(
            f'<div style="background:linear-gradient(135deg,#12151f,#161929);'
            f'border:1px solid #2e2558;border-radius:16px;padding:24px 28px;'
            f'border-left:4px solid {score_color};position:relative">'
            f'<div style="font-size:2rem;position:absolute;top:18px;right:22px;opacity:0.15">🤖</div>'
            f'<div style="font-size:0.68rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;'
            f'letter-spacing:0.1em;margin-bottom:12px">📡 Resumen automático · {hoy.strftime("%d de %B %Y")}</div>'
            f'<div style="font-size:0.9rem;color:#c8d0e8;line-height:1.8;font-family:DM Sans,sans-serif">'
            f'{resumen_txt}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # ══════════════════════════════════════════════════════════════════
        # 🤖 ALERTAS IA — ANÁLISIS DE CALIDAD DE DIRECCIONES
        # Detecta: direcciones incompletas, barrios/torres problemáticos,
        # cancelaciones por datos deficientes, anomalías geográficas
        # ══════════════════════════════════════════════════════════════════
        st.markdown("<hr style='border-color:#1e2337;margin:20px 0'>", unsafe_allow_html=True)
        st.markdown(
            '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:1rem;margin-bottom:4px">'
            '🤖 IA — Análisis de Calidad de Direcciones</div>'
            '<div style="font-size:0.72rem;color:#a8b4d0;margin-bottom:14px">'
            'Detecta cancelaciones por dirección incompleta, barrios problemáticos y anomalías geográficas</div>',
            unsafe_allow_html=True
        )

        # Columnas que necesitamos
        C_DIR   = next((c for c in df_act.columns if any(x in c.upper() for x in ["DIREC","ADDRESS","CALLE","DOMICILIO"])), None)
        C_BARRIO= next((c for c in df_act.columns if any(x in c.upper() for x in ["BARRIO","NEIGHBORHOOD","SECTOR","COLONIA"])), None)
        C_TORRE = next((c for c in df_act.columns if any(x in c.upper() for x in ["TORRE","APTO","APARTAMENTO","UNIDAD","BLOQUE","PISO"])), None)
        C_DEPTO = next((c for c in df_act.columns if any(x in c.upper() for x in ["DEPARTAMENTO","ESTADO","PROVINCIA","REGION"])), C_CIUDAD if C_CIUDAD in df_act.columns else None)

        # ── PALABRAS CLAVE de dirección incompleta ──
        PALABRAS_INCOMPLETA = [
            "incompleta","incomplete","sin direc","no hay dir","falta dir",
            "datos incompletos","sin datos","pendiente","n/a","na","ninguna",
            "s/d","sd","xx","000","sin info","no aplica","---","???"
        ]

        alertas_dir = []

        # ── 1. Cancelaciones por dirección incompleta ──
        df_can_act = df_act[df_act[C_ESTATUS].astype(str).str.upper().str.contains('CANCELAD', na=False)] if C_ESTATUS in df_act.columns else pd.DataFrame()
        n_can_dir_inc = 0
        if C_DIR and len(df_can_act):
            mask_inc = df_can_act[C_DIR].astype(str).str.lower().apply(
                lambda v: any(p in v for p in PALABRAS_INCOMPLETA) or len(v.strip()) < 10
            )
            n_can_dir_inc = int(mask_inc.sum())
            pct_can_dir = n_can_dir_inc / len(df_can_act) * 100 if len(df_can_act) else 0
            if n_can_dir_inc > 0:
                nivel_d = "🔴" if pct_can_dir > 10 else "🟡"
                alertas_dir.append({
                    "icono": nivel_d,
                    "titulo": "Cancelaciones por dirección incompleta",
                    "msg": f"{n_can_dir_inc:,} cancelaciones ({pct_can_dir:.1f}% del total cancelado) tienen dirección deficiente o incompleta.",
                    "detalle": "Estas NO son cancelaciones operativas reales — hay intención de compra pero falló la captura de datos.",
                    "accion": "Actualiza el bot para solicitar dirección completa: barrio + calle + número + referencia.",
                    "color": "#f59e0b" if pct_can_dir <= 10 else "#ef4444",
                    "impacto": "recuperable"
                })

        # ── 2. Tags NOVEDADES con dirección incompleta ──
        if C_TAGS in df_act.columns:
            tags_dir = df_act[C_TAGS].astype(str).str.lower()
            n_tag_dir = tags_dir.apply(lambda t: any(p in t for p in
                ["datos incompletos","sin direc","dirección incorrecta","direc incorrecta",
                 "no existe","dir no existe","domicilio no encontrado"])).sum()
            if n_tag_dir > 0:
                alertas_dir.append({
                    "icono": "🔴" if n_tag_dir > n_tot * 0.05 else "🟡",
                    "titulo": "Novedades etiquetadas: dirección incorrecta",
                    "msg": f"{n_tag_dir:,} pedidos tienen tag relacionado con problemas de dirección.",
                    "detalle": "El bot posiblemente no está solicitando correctamente los datos de entrega.",
                    "accion": "Revisa el flujo de captura del bot: pide número de puerta, barrio, referencia y confirmación.",
                    "color": "#ef4444" if n_tag_dir > n_tot * 0.05 else "#f59e0b",
                    "impacto": "bot"
                })

        # ── 3. Barrios con alta concentración de devoluciones ──
        if C_BARRIO and C_ESTATUS in df_act.columns:
            df_dev_b = df_act[df_act[C_ESTATUS].astype(str).str.upper().str.contains('DEVOLUCI', na=False)]
            if len(df_dev_b):
                barrios_dev = df_dev_b[C_BARRIO].astype(str).value_counts().head(5)
                barrios_prob = barrios_dev[barrios_dev > 3]
                if len(barrios_prob):
                    top_b = barrios_prob.index[0]
                    alertas_dir.append({
                        "icono": "🟡",
                        "titulo": f"Barrio problemático: {top_b}",
                        "msg": f"{barrios_prob.iloc[0]:,} devoluciones provienen de '{top_b}'.",
                        "detalle": "Patrón geográfico de devolución — puede indicar cobertura deficiente o problemas de acceso.",
                        "accion": f"Evalúa si la transportadora cubre bien '{top_b}'. Considera ruta alternativa o confirmación extra.",
                        "color": "#f59e0b",
                        "impacto": "geografico"
                    })

        # ── 4. Torres/Aptos con alta cancelación ──
        if C_TORRE and C_ESTATUS in df_act.columns:
            df_can_t = df_act[df_act[C_ESTATUS].astype(str).str.upper().str.contains('CANCELAD', na=False)]
            if len(df_can_t):
                torres_can = df_can_t[C_TORRE].astype(str).value_counts()
                torres_prob = torres_can[(torres_can > 2) & (~torres_can.index.str.lower().isin(["","nan","none","0"]))]
                if len(torres_prob):
                    top_t = torres_prob.index[0]
                    alertas_dir.append({
                        "icono": "🟡",
                        "titulo": f"Concentración de cancelaciones: {top_t}",
                        "msg": f"{torres_prob.iloc[0]:,} cancelaciones en la misma torre/unidad '{top_t}'.",
                        "detalle": "Múltiples cancelaciones del mismo punto de entrega pueden indicar dirección ficticia o bloqueo.",
                        "accion": "Verifica si es una dirección de alto riesgo o si hay pedidos duplicados.",
                        "color": "#f59e0b",
                        "impacto": "anomalia"
                    })

        # ── 5. Flete > umbral ──
        flete_prom = df_act[C_FLETE].mean() if C_FLETE in df_act.columns and len(df_act) else 0
        flete_max_razonable = flete_prom * 2.5
        if C_FLETE in df_act.columns and flete_prom > 0:
            n_flete_alto = int((df_act[C_FLETE] > flete_max_razonable).sum())
            if n_flete_alto > 0:
                alertas_dir.append({
                    "icono": "🟡",
                    "titulo": "Fletes atípicamente altos",
                    "msg": f"{n_flete_alto:,} pedidos tienen flete > {fmt_money(flete_max_razonable)} (2.5× el promedio de {fmt_money(flete_prom)}).",
                    "detalle": "Posibles rutas de difícil acceso o datos de ciudad/depto incorrectos que generan recargos.",
                    "accion": "Revisa que ciudad y departamento estén correctamente cargados en el Excel.",
                    "color": "#f59e0b",
                    "impacto": "costos"
                })

        # ── 6. Alertas de cancelación cerca del límite ──
        meta_can_lim = float(st.session_state.get('pg_meta_can', 10.0))
        if tasa_can >= meta_can_lim * 0.8 and tasa_can < meta_can_lim:
            alertas_dir.append({
                "icono": "🟡",
                "titulo": f"Cancelación cerca del límite ({tasa_can:.1f}% / meta {meta_can_lim:.0f}%)",
                "msg": f"Estás a {meta_can_lim - tasa_can:.1f} pp del límite de cancelación. El sistema activa análisis preventivo.",
                "detalle": f"Con {n_can:,} cancelaciones actuales, {int((meta_can_lim/100*n_tot) - n_can)} más cancelaciones activarían la alerta roja.",
                "accion": "Refuerza confirmación y revisa direcciones del backlog pendiente.",
                "color": "#f59e0b",
                "impacto": "preventivo"
            })

        # ── RENDER alertas IA ──
        if not alertas_dir:
            st.markdown(
                '<div style="background:rgba(16,185,129,0.07);border:1px solid #10b98144;'
                'border-radius:12px;padding:18px;text-align:center">'
                '<div style="font-size:1.3rem;margin-bottom:6px">✅</div>'
                '<div style="color:#10b981;font-weight:700;font-size:0.9rem">Sin anomalías de dirección detectadas</div>'
                '<div style="font-size:0.72rem;color:#a8b4d0;margin-top:4px">'
                f'Analizados {n_tot:,} pedidos · {n_can:,} cancelaciones · sin patrones de riesgo geográfico</div>'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            # KPIs resumen IA
            ia1, ia2, ia3 = st.columns(3)
            n_criticas_d = sum(1 for a in alertas_dir if a['icono'] == "🔴")
            n_atencion_d = sum(1 for a in alertas_dir if a['icono'] == "🟡")
            n_recup = sum(1 for a in alertas_dir if a.get('impacto') == 'recuperable')
            with ia1: st.markdown(kpi("red",   "🔴 Alertas críticas",  f"{n_criticas_d}", "Requieren acción inmediata"), unsafe_allow_html=True)
            with ia2: st.markdown(kpi("gold",  "🟡 Alertas atención",  f"{n_atencion_d}", "Monitorear"), unsafe_allow_html=True)
            with ia3: st.markdown(kpi("green", "♻️ Recuperables",      f"{n_recup}", "Cancel. por datos incompletos"), unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            for alerta_d in alertas_dir:
                impacto_badges = {
                    "recuperable": ("🟢 Recuperable", "#10b981"),
                    "bot":         ("🤖 Problema de Bot", "#7c3aed"),
                    "geografico":  ("🗺️ Patrón Geográfico", "#00d4ff"),
                    "anomalia":    ("⚠️ Anomalía", "#f59e0b"),
                    "costos":      ("💸 Impacto en Costos", "#f97416"),
                    "preventivo":  ("🛡️ Preventivo", "#5b6cfc"),
                }
                imp_key = alerta_d.get('impacto', '')
                imp_lbl, imp_col = impacto_badges.get(imp_key, ("📌 Alerta", "#8892b0"))
                st.markdown(
                    f'<div style="background:#13102a;border:1px solid {alerta_d["color"]}33;'
                    f'border-left:4px solid {alerta_d["color"]};border-radius:12px;padding:16px 18px;margin-bottom:10px">'
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">'
                    f'<div style="display:flex;align-items:center;gap:8px">'
                    f'<span style="font-size:1rem">{alerta_d["icono"]}</span>'
                    f'<span style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.88rem">{alerta_d["titulo"]}</span>'
                    f'</div>'
                    f'<span style="background:{imp_col}18;color:{imp_col};border:1px solid {imp_col}44;'
                    f'border-radius:20px;padding:2px 10px;font-size:0.65rem;font-weight:800;white-space:nowrap">{imp_lbl}</span>'
                    f'</div>'
                    f'<div style="font-size:0.8rem;color:#a8b4d0;margin-bottom:6px;line-height:1.5">{alerta_d["msg"]}</div>'
                    f'<div style="font-size:0.72rem;color:#7a8aaa;margin-bottom:10px;font-style:italic">{alerta_d["detalle"]}</div>'
                    f'<div style="background:{alerta_d["color"]}12;border-radius:8px;padding:8px 12px">'
                    f'<span style="font-size:0.72rem;color:{alerta_d["color"]};font-weight:800">⚡ Acción: </span>'
                    f'<span style="font-size:0.72rem;color:#c8d0e8">{alerta_d["accion"]}</span>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )

        # Columnas disponibles para diagnóstico
        cols_dir_disponibles = [c for c in [C_DIR, C_BARRIO, C_TORRE, C_DEPTO] if c]
        if not cols_dir_disponibles:
            st.markdown(
                '<div style="background:rgba(124,58,237,0.1);border:1px dashed #2e3650;'
                'border-radius:10px;padding:14px;margin-top:10px;font-size:0.75rem;color:#a8b4d0">'
                '📋 <b style="color:#c8d0e8">Para activar el análisis completo de direcciones</b>, '
                'asegúrate de que tu Excel tenga columnas como: '
                '<b>DIRECCIÓN, BARRIO, TORRE, DEPARTAMENTO</b>. '
                'Actualmente se detecta solo por tags y estatus.'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            cols_str = " · ".join([f"<b style='color:#a855f7'>{c}</b>" for c in cols_dir_disponibles])
            st.markdown(
                f'<div style="font-size:0.68rem;color:#7a8aaa;margin-top:6px">'
                f'🔍 Columnas de dirección detectadas: {cols_str}</div>',
                unsafe_allow_html=True
            )


    # ── EVOLUCIÓN MENSUAL (mantenido como referencia interna) ──
    elif "Evolución_Mensual_Legado" in nav and '_mes' in df.columns and C_TOTAL in df.columns:
        v_mes = df.groupby('_mes').agg(
            Ventas=(C_TOTAL, 'sum'),
            Ganancia=(C_GANANCIA, 'sum') if C_GANANCIA in df.columns else (C_TOTAL,'count'),
            Ordenes=(C_TOTAL,'count')
        ).reset_index().sort_values('_mes')

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=v_mes['_mes'], y=v_mes['Ventas']/1e6,
            name='Ventas', marker=dict(color='#5b6cfc', opacity=0.85),
        ))
        if C_GANANCIA in df.columns:
            fig.add_trace(go.Bar(
                x=v_mes['_mes'], y=v_mes['Ganancia']/1e6,
                name='Ganancia', marker=dict(color='#10b981', opacity=0.85),
            ))
        fig.add_trace(go.Scatter(
            x=v_mes['_mes'], y=v_mes['Ordenes'],
            name='Órdenes', yaxis='y2',
            line=dict(color='#f0c060', width=3),
            marker=dict(size=8, color='#f0c060')
        ))
        fig.update_layout(
            **PLOT_LAYOUT,
            barmode='group', height=420,
            title='Evolución Mensual de Ventas',
            xaxis=AXIS_STYLE,
            yaxis=dict(title='Millones COP', **AXIS_STYLE),
            yaxis2=dict(title='Órdenes', overlaying='y', side='right',
                       gridcolor='rgba(0,0,0,0)', tickfont=dict(color='#f0c060'))
        )
        st.plotly_chart(fig, use_container_width=True)

        # Días pico
        if '_dia' in df.columns:
            dias_venta = df.groupby('_dia')[C_TOTAL].sum().reset_index()
            dias_venta.columns = ['Día','Ventas']
            fig_d = px.area(dias_venta, x='Día', y='Ventas',
                           title='Ventas por Día del Mes (patrón quincenas)',
                           color_discrete_sequence=['#f0c060'])
            fig_d.update_traces(fillcolor='rgba(201,168,76,0.15)', line=dict(color='#f0c060',width=2))
            fig_d.update_layout(**PLOT_LAYOUT, height=280, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
            st.plotly_chart(fig_d, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════
    # 📣 MARKETING — MAPA, PRODUCTO ESTRELLA, INSIGHTS
    # ══════════════════════════════════════════════════════════════════
    elif nav == "📣 Marketing":
        mkt_nav = st.radio("", [
            "🗺️ Mapa de Calor",
            "⭐ Producto Estrella",
            "📅 Calendario Comercial",
            "🤝 Recomendaciones IA",
            "💡 Insights",
        ], horizontal=True, label_visibility="collapsed", key="mkt_nav")
        st.markdown("<br>", unsafe_allow_html=True)

        # ── MAPA COLOMBIA ──
        if "Mapa" in mkt_nav:
            if C_DEPTO in df.columns:
                dep_data = df.groupby(C_DEPTO).agg(
                    Pedidos=(C_TOTAL,'count'),
                    Ventas=(C_TOTAL,'sum') if C_TOTAL in df.columns else (C_DEPTO,'count'),
                    Ganancia=(C_GANANCIA,'sum') if C_GANANCIA in df.columns else (C_DEPTO,'count')
                ).reset_index().sort_values('Pedidos', ascending=False)
                dep_data.columns = ['Departamento','Pedidos','Ventas','Ganancia']

                # Coordenadas aproximadas departamentos Colombia
                coords = {
                    'CUNDINAMARCA':[4.60,-74.08],'BOGOTA':[4.60,-74.08],'BOGOTÁ':[4.60,-74.08],
                    'ANTIOQUIA':[6.25,-75.56],'MEDELLÍN':[6.25,-75.56],'MEDELLIN':[6.25,-75.56],
                    'VALLE DEL CAUCA':[3.43,-76.52],'CALI':[3.43,-76.52],
                    'ATLANTICO':[10.99,-74.81],'ATLÁNTICO':[10.99,-74.81],'BARRANQUILLA':[10.99,-74.81],
                    'BOLIVAR':[10.39,-75.51],'BOLÍVAR':[10.39,-75.51],'CARTAGENA':[10.39,-75.51],
                    'SANTANDER':[7.13,-73.12],'BUCARAMANGA':[7.13,-73.12],
                    'NORTE DE SANTANDER':[7.89,-72.51],'CUCUTA':[7.89,-72.51],'CÚCUTA':[7.89,-72.51],
                    'BOYACA':[5.53,-73.36],'BOYACÁ':[5.53,-73.36],
                    'TOLIMA':[4.09,-75.15],'IBAGUE':[4.09,-75.15],'IBAGUÉ':[4.09,-75.15],
                    'CALDAS':[5.07,-75.51],'MANIZALES':[5.07,-75.51],
                    'RISARALDA':[4.81,-75.69],'PEREIRA':[4.81,-75.69],
                    'QUINDIO':[4.53,-75.68],'QUINDÍO':[4.53,-75.68],'ARMENIA':[4.53,-75.68],
                    'HUILA':[2.53,-75.52],'NEIVA':[2.53,-75.52],
                    'NARIÑO':[1.21,-77.28],'NARINO':[1.21,-77.28],'PASTO':[1.21,-77.28],
                    'CAUCA':[2.44,-76.61],'POPAYAN':[2.44,-76.61],'POPAYÁN':[2.44,-76.61],
                    'CORDOBA':[8.74,-75.88],'CÓRDOBA':[8.74,-75.88],'MONTERIA':[8.74,-75.88],'MONTERÍA':[8.74,-75.88],
                    'SUCRE':[9.30,-75.39],'SINCELEJO':[9.30,-75.39],
                    'MAGDALENA':[11.24,-74.20],'SANTA MARTA':[11.24,-74.20],
                    'CESAR':[9.33,-73.36],'VALLEDUPAR':[9.33,-73.36],
                    'GUAJIRA':[11.54,-72.91],'LA GUAJIRA':[11.54,-72.91],'RIOHACHA':[11.54,-72.91],
                    'META':[4.14,-73.63],'VILLAVICENCIO':[4.14,-73.63],
                    'CASANARE':[5.33,-71.33],'YOPAL':[5.33,-71.33],
                    'ARAUCA':[7.08,-70.76],
                    'VICHADA':[4.42,-69.28],
                    'GUAVIARE':[2.57,-72.65],
                    'VAUPES':[1.25,-70.23],'VAUPÉS':[1.25,-70.23],
                    'AMAZONAS':[-1.44,-71.57],
                    'PUTUMAYO':[0.43,-76.64],'MOCOA':[0.43,-76.64],
                    'CAQUETA':[-1.61,-75.61],'CAQUETÁ':[-1.61,-75.61],'FLORENCIA':[-1.61,-75.61],
                    'CHOCO':[5.69,-76.65],'CHOCÓ':[5.69,-76.65],'QUIBDO':[5.69,-76.65],'QUIBDÓ':[5.69,-76.65],
                    'SAN ANDRES':[12.53,-81.72],'SAN ANDRÉS':[12.53,-81.72],
                }

                dep_data['lat'] = dep_data['Departamento'].str.upper().map(lambda d: next((v[0] for k,v in coords.items() if k in d or d in k), None))
                dep_data['lon'] = dep_data['Departamento'].str.upper().map(lambda d: next((v[1] for k,v in coords.items() if k in d or d in k), None))
                dep_geo = dep_data.dropna(subset=['lat','lon'])

                if len(dep_geo) > 0:
                    fig_map = px.scatter_mapbox(
                        dep_geo, lat='lat', lon='lon',
                        size='Pedidos', color='Ventas',
                        hover_name='Departamento',
                        hover_data={'Pedidos':True,'Ventas':':,.0f','Ganancia':':,.0f','lat':False,'lon':False},
                        color_continuous_scale=['#12151f','#5b6cfc','#f0c060'],
                        size_max=50, zoom=4.5,
                        mapbox_style='carto-darkmatter',
                        title='Distribución Geográfica de Pedidos'
                    )
                    fig_map.update_layout(**PLOT_LAYOUT, height=550,
                                          mapbox=dict(center=dict(lat=4.5, lon=-74.3)))
                    st.plotly_chart(fig_map, use_container_width=True)

                # Tabla top departamentos
                st.markdown("#### Top Departamentos")
                cols_dep = st.columns(5)
                for i, row in dep_data.head(5).iterrows():
                    with cols_dep[min(list(dep_data.index).index(i), 4)]:
                        pct = round(row['Pedidos']/total*100,1)
                        st.markdown(kpi("gold" if i==0 else "blue", row['Departamento'][:15].upper(), f"{row['Pedidos']:,}", f"{pct}% del total"), unsafe_allow_html=True)

            # ── PRODUCTOS ESTRELLA ──
        elif "Estrella" in mkt_nav and C_PRODUCTO in df.columns:

            sub_prod = st.radio("", ["🥇 Por Unidades","💰 Por Ventas","📈 Por Ganancia"],
                               horizontal=True, label_visibility="collapsed")

            if "Unidades" in sub_prod:
                top = df[C_PRODUCTO].astype(str).value_counts().head(10).reset_index()
                top.columns = ['Producto','Valor']
                titulo = "Unidades vendidas"
            elif "Ventas" in sub_prod and C_TOTAL in df.columns:
                top = df.groupby(C_PRODUCTO)[C_TOTAL].sum().sort_values(ascending=False).head(10).reset_index()
                top.columns = ['Producto','Valor']
                titulo = "Ventas COP"
            else:
                top = df.groupby(C_PRODUCTO)[C_GANANCIA].sum().sort_values(ascending=False).head(10).reset_index() if C_GANANCIA in df.columns else pd.DataFrame()
                top.columns = ['Producto','Valor'] if len(top) else []
                titulo = "Ganancia COP"

            if len(top):
                med_col, right_col = st.columns([1, 1])
                with med_col:
                    emojis = ['🥇','🥈','🥉','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
                    for idx, row in top.iterrows():
                        rank = list(top.index).index(idx)
                        val_str = fmt_money(row['Valor']) if titulo != "Unidades vendidas" else f"{int(row['Valor']):,} uds"
                        pct_v = round(row['Valor']/top['Valor'].sum()*100,1)
                        st.markdown(f"""
                        <div class="prod-card">
                            <div class="prod-rank">{emojis[rank]}</div>
                            <div style="flex:1">
                                <div class="prod-name">{str(row['Producto'])[:45]}</div>
                                <div class="prod-val">{val_str} · {pct_v}% del total</div>
                            </div>
                        </div>""", unsafe_allow_html=True)

                with right_col:
                    fig_prod = px.bar(
                        top.sort_values('Valor'),
                        x='Valor', y='Producto',
                        orientation='h',
                        color='Valor',
                        color_continuous_scale=['#12151f','#5b6cfc','#f0c060'],
                        title=f'Top 10 — {titulo}'
                    )
                    fig_prod.update_layout(**PLOT_LAYOUT, height=480, coloraxis_showscale=False, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                    fig_prod.update_traces(texttemplate='%{x:,.0f}', textposition='outside',
                                           textfont=dict(color='#8892b0', size=10))
                    st.plotly_chart(fig_prod, use_container_width=True)



            # ══════════════════════════════════════════════════════════════════
            # 📅 CALENDARIO COMERCIAL COLOMBIA
            # ══════════════════════════════════════════════════════════════════
        elif "Calendario" in mkt_nav:
            st.markdown('<div class="seccion-titulo">📅 Calendario Comercial Colombia</div>', unsafe_allow_html=True)

            from datetime import date
            _hoy_cal = date.today()
            _mes_cal = _hoy_cal.month
            _año_cal = _hoy_cal.year

            # ── BASE DE DATOS FECHAS ESPECIALES COLOMBIA ──
            CALENDARIO_COL = [
                # ── ENERO ──
                {"mes":1,  "dia":1,   "nombre":"Año Nuevo",                    "ico":"🎆", "tipo":"festivo",   "impacto":"alto",
                 "tip":"Campañas de propósitos / resoluciones. Productos de salud, bienestar, organización del hogar."},
                {"mes":1,  "dia":6,   "nombre":"Día de Reyes",                  "ico":"👑", "tipo":"comercial",  "impacto":"medio",
                 "tip":"Regiones con tradición fuerte (Caribe). Juguetes, dulces, ropa infantil."},
                {"mes":1,  "dia":None,"nombre":"Enero — Regreso Escolar",       "ico":"🎒", "tipo":"temporada",  "impacto":"alto",
                 "tip":"Útiles, maletas, uniformes, accesorios. Pico de compras las 2 primeras semanas."},

                # ── FEBRERO ──
                {"mes":2,  "dia":14,  "nombre":"Día del Amor y la Amistad",     "ico":"❤️", "tipo":"comercial",  "impacto":"muy_alto",
                 "tip":"El pico más fuerte del año en regalos. Perfumes, accesorios, detalles, chocolates. Pauta desde feb 1."},
                {"mes":2,  "dia":None,"nombre":"Carnavales (Barranquilla)",      "ico":"🎭", "tipo":"regional",   "impacto":"alto",
                 "tip":"Región Caribe. Disfraces, accesorios de fiesta, bebidas. Pauta específica para Atlántico y Bolívar."},

                # ── MARZO ──
                {"mes":3,  "dia":8,   "nombre":"Día de la Mujer",               "ico":"👩", "tipo":"comercial",  "impacto":"alto",
                 "tip":"Perfumes, joyería, ropa, bienestar. Campaña inclusiva de marca. Pauta 5 días antes."},
                {"mes":3,  "dia":19,  "nombre":"Día del Padre (Colombia)",       "ico":"👨", "tipo":"comercial",  "impacto":"alto",
                 "tip":"Ropa masculina, accesorios, gadgets, deportes. Pico de compra semana anterior."},
                {"mes":3,  "dia":None,"nombre":"Semana Santa",                  "ico":"✝️", "tipo":"festivo",    "impacto":"medio",
                 "tip":"Viajes internos, gastronomía, artículos de playa y piscina. Fechas variables cada año."},

                # ── ABRIL ──
                {"mes":4,  "dia":None,"nombre":"Feria de Cali / Ferias regionales","ico":"🎪","tipo":"regional","impacto":"medio",
                 "tip":"Temporada de ferias y fiestas patronales en múltiples ciudades. Artículos de fiesta, moda."},

                # ── MAYO ──
                {"mes":5,  "dia":None,"nombre":"Día de la Madre",               "ico":"🌸", "tipo":"comercial",  "impacto":"muy_alto",
                 "tip":"El evento más grande del año en e-commerce Colombia. Perfumes, flores, ropa, joyería, accesorios del hogar. Pauta desde abr 20."},
                {"mes":5,  "dia":None,"nombre":"Temporada de lluvias (inicio)",  "ico":"🌧️", "tipo":"temporada",  "impacto":"medio",
                 "tip":"Regiones Andina y Pacífica. Impermeables, botas, artículos del hogar para humedad."},

                # ── JUNIO ──
                {"mes":6,  "dia":None,"nombre":"Mitad de año — Liquidaciones",  "ico":"🏷️", "tipo":"comercial",  "impacto":"alto",
                 "tip":"Temporada de descuentos y liquidaciones. Textiles, moda, electrodomésticos."},
                {"mes":6,  "dia":None,"nombre":"Temporada de Vacaciones Escolares","ico":"🏖️","tipo":"temporada","impacto":"alto",
                 "tip":"Juguetes, ropa de temporada, artículos de recreación y viaje."},

                # ── JULIO ──
                {"mes":7,  "dia":20,  "nombre":"Día de la Independencia",        "ico":"🇨🇴", "tipo":"festivo",   "impacto":"medio",
                 "tip":"Productos con identidad nacional. Ferias y eventos locales. Consumo de moda y recreación."},
                {"mes":7,  "dia":None,"nombre":"Temporada Baja — Mitad de año",  "ico":"📉", "tipo":"temporada",  "impacto":"bajo",
                 "tip":"Mes de análisis y planificación. Optimiza catálogo y prepara pauta para agosto."},

                # ── AGOSTO ──
                {"mes":8,  "dia":7,   "nombre":"Batalla de Boyacá (festivo)",    "ico":"⚔️", "tipo":"festivo",    "impacto":"bajo",
                 "tip":"Fin de semana largo. Turismo interno y consumo familiar."},
                {"mes":8,  "dia":None,"nombre":"Feria de las Flores — Medellín", "ico":"🌺", "tipo":"regional",   "impacto":"alto",
                 "tip":"Antioquia y zonas cafeteras. Flores, artesanías, turismo gastronómico."},
                {"mes":8,  "dia":None,"nombre":"Regreso a clases (segundo semestre)","ico":"📚","tipo":"temporada","impacto":"alto",
                 "tip":"Segunda ola de útiles escolares. Maletas, uniformes, tecnología educativa."},

                # ── SEPTIEMBRE ──
                {"mes":9,  "dia":None,"nombre":"Día del Amor y la Amistad",      "ico":"💛", "tipo":"comercial",  "impacto":"muy_alto",
                 "tip":"Versión colombiana de San Valentín. Detalles, regalos, restaurantes. Pico de ventas semanas 2 y 3 de septiembre."},
                {"mes":9,  "dia":None,"nombre":"Temporada Seca (Llanos/Caribe)", "ico":"☀️", "tipo":"regional",   "impacto":"medio",
                 "tip":"Meta, Casanare, Costa Caribe. Productos para calor: ventiladores, ropa liviana, hidratación."},

                # ── OCTUBRE ──
                {"mes":10, "dia":12,  "nombre":"Día de la Raza (festivo)",       "ico":"🌎", "tipo":"festivo",    "impacto":"bajo",
                 "tip":"Puente festivo. Buena ventana para campañas de fin de semana."},
                {"mes":10, "dia":31,  "nombre":"Halloween",                      "ico":"🎃", "tipo":"comercial",  "impacto":"alto",
                 "tip":"Disfraces, decoración, dulces, artículos de fiesta. Mercado joven y familiar. Pauta desde oct 15."},
                {"mes":10, "dia":None,"nombre":"Temporada pre-Noviembre",        "ico":"⚡", "tipo":"comercial",  "impacto":"alto",
                 "tip":"Anticipa Black Friday. Calienta audiencias, crea listas de deseos, genera expectativa."},

                # ── NOVIEMBRE ──
                {"mes":11, "dia":None,"nombre":"Black Friday / Cyber Monday",    "ico":"🖤", "tipo":"comercial",  "impacto":"muy_alto",
                 "tip":"La semana de mayor conversión del año. Descuentos, combos, flash sales. Pauta 10x desde nov 18."},
                {"mes":11, "dia":1,   "nombre":"Día de Todos los Santos",        "ico":"🕯️", "tipo":"festivo",    "impacto":"bajo",
                 "tip":"Festivo. Actividad reducida. Aprovecha para preparar creativos de Black Friday."},
                {"mes":11, "dia":None,"nombre":"Inicio Temporada Navidad",       "ico":"🎄", "tipo":"temporada",  "impacto":"muy_alto",
                 "tip":"Desde nov 15 empieza la intención de compra navideña. Activa colecciones, combos regalo."},

                # ── DICIEMBRE ──
                {"mes":12, "dia":None,"nombre":"Temporada Navidad",              "ico":"🎁", "tipo":"comercial",  "impacto":"muy_alto",
                 "tip":"El mes de mayor volumen del año. Regalos, decoración, ropa especial, electrodomésticos. Pauta máxima dic 1-23."},
                {"mes":12, "dia":8,   "nombre":"Día de las Velitas",             "ico":"🕯️", "tipo":"cultural",   "impacto":"medio",
                 "tip":"Inicio de la temporada navideña colombiana. Velas, luces, decoración festiva."},
                {"mes":12, "dia":16,  "nombre":"Inicio Novenas de Aguinaldo",    "ico":"🎶", "tipo":"cultural",   "impacto":"medio",
                 "tip":"9 días de reuniones familiares. Regalos, comidas, decoración, productos de mesa."},
                {"mes":12, "dia":25,  "nombre":"Navidad",                        "ico":"⛪", "tipo":"festivo",    "impacto":"muy_alto",
                 "tip":"Pico máximo. Ultimo jalón de ventas dic 20-24. Post-Navidad: cambios y liquidaciones."},
                {"mes":12, "dia":31,  "nombre":"Fin de Año",                     "ico":"🥂", "tipo":"festivo",    "impacto":"alto",
                 "tip":"Ropa de fiesta, accesorios, bebidas, artículos de celebración. Campaña propósitos nuevo año."},
            ]

            # ── RECOMENDACIONES POR REGIÓN ──
            RECOMENDACIONES_REGION = {
                "CUNDINAMARCA": {"temp": "Fría", "prod": ["Buzos","Chaquetas","Thermos","Cobijas"], "pico": "Ago-Nov"},
                "BOGOTA":       {"temp": "Fría", "prod": ["Buzos","Chaquetas","Thermos","Cobijas"], "pico": "Ago-Nov"},
                "ANTIOQUIA":    {"temp": "Templada", "prod": ["Ropa casual","Accesorios","Flores","Artesanías"], "pico": "Ago (Feria de Flores)"},
                "ATLANTICO":    {"temp": "Caliente", "prod": ["Ropa liviana","Ventiladores","Hidratación","Disfraces"], "pico": "Feb (Carnavales)"},
                "BOLIVAR":      {"temp": "Caliente", "prod": ["Ropa playera","Artículos de playa","Hidratación"], "pico": "Dic-Ene"},
                "VALLE DEL CAUCA": {"temp": "Templada", "prod": ["Moda","Accesorios","Artículos deportivos"], "pico": "Jun-Jul"},
                "SANTANDER":    {"temp": "Variable", "prod": ["Ropa todo clima","Artesanías","Gastronomía local"], "pico": "Jun-Jul"},
                "META":         {"temp": "Caliente/Seca", "prod": ["Ropa liviana","Protección solar","Calzado outdoor"], "pico": "Jul-Sep (sequía)"},
                "NARIÑO":       {"temp": "Fría", "prod": ["Artesanías","Lana","Ropa de abrigo"], "pico": "Sep-Dic"},
                "HUILA":        {"temp": "Templada", "prod": ["Café","Artesanías","Ropa casual"], "pico": "Jun (Festival Folclórico)"},
            }

            # ── SELECTOR DE MES ──
            cal_c1, cal_c2 = st.columns([1, 2])
            with cal_c1:
                _mes_sel_cal = st.selectbox(
                    "📅 Ver mes",
                    list(range(1, 13)),
                    index=_mes_cal - 1,
                    format_func=lambda m: ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                                           "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"][m-1],
                    key="cal_mes_sel"
                )
            with cal_c2:
                _col_impacto_fil = st.multiselect(
                    "Filtrar por impacto",
                    ["muy_alto","alto","medio","bajo"],
                    default=["muy_alto","alto"],
                    key="cal_impacto_fil",
                    format_func=lambda x: {"muy_alto":"🔥 Muy Alto","alto":"⚡ Alto","medio":"📊 Medio","bajo":"📉 Bajo"}.get(x,x)
                )

            # Eventos del mes seleccionado
            eventos_mes = [e for e in CALENDARIO_COL
                           if e["mes"] == _mes_sel_cal and e["impacto"] in _col_impacto_fil]

            # ── PRÓXIMOS EVENTOS (los siguientes 60 días) ──
            import calendar as _cal_mod
            _proximos = []
            for e in CALENDARIO_COL:
                if e["dia"]:
                    try:
                        fe = date(_año_cal, e["mes"], e["dia"])
                        dias_faltan = (fe - _hoy_cal).days
                        if 0 <= dias_faltan <= 60:
                            _proximos.append({**e, "dias_faltan": dias_faltan, "fecha": fe})
                    except:
                        pass
            _proximos.sort(key=lambda x: x["dias_faltan"])

            if _proximos:
                st.markdown(
                    '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.88rem;margin-bottom:10px">'
                    '⏰ Próximas fechas clave — próximos 60 días</div>',
                    unsafe_allow_html=True
                )
                prox_cols = st.columns(min(len(_proximos), 4))
                for pi, pe in enumerate(_proximos[:4]):
                    urgencia = "#ef4444" if pe["dias_faltan"] <= 7 else "#f59e0b" if pe["dias_faltan"] <= 21 else "#5b6cfc"
                    with prox_cols[pi]:
                        st.markdown(
                            f'<div style="background:{urgencia}10;border:1.5px solid {urgencia}55;'
                            f'border-top:3px solid {urgencia};border-radius:12px;padding:14px;text-align:center">'
                            f'<div style="font-size:1.5rem;margin-bottom:4px">{pe["ico"]}</div>'
                            f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.75rem;margin-bottom:4px">{pe["nombre"]}</div>'
                            f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:{urgencia};font-size:1.3rem">{pe["dias_faltan"]}</div>'
                            f'<div style="font-size:0.62rem;color:#a8b4d0">días para preparar</div>'
                            f'<div style="font-size:0.6rem;color:#7a8aaa;margin-top:4px">{pe["fecha"].strftime("%d/%m/%Y")}</div>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                st.markdown("<br>", unsafe_allow_html=True)

            # ── VISTA MES COMPLETO ──
            mes_nombres = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                           "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
            st.markdown(
                f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.95rem;margin-bottom:12px">'
                f'📆 {mes_nombres[_mes_sel_cal-1]} — Eventos y Estrategias</div>',
                unsafe_allow_html=True
            )

            col_imp_colors = {
                "muy_alto": ("#ef4444", "🔥 Muy Alto"),
                "alto":     ("#f59e0b", "⚡ Alto"),
                "medio":    ("#00d4ff", "📊 Medio"),
                "bajo":     ("#6b7a9e", "📉 Bajo"),
            }
            col_tipo_colors = {
                "festivo":   "#7c3aed",
                "comercial": "#10b981",
                "temporada": "#5b6cfc",
                "regional":  "#f97416",
                "cultural":  "#f0c060",
            }

            if not eventos_mes:
                st.info(f"No hay eventos de impacto seleccionado para {mes_nombres[_mes_sel_cal-1]}. Amplía los filtros de impacto.")
            else:
                for ev in eventos_mes:
                    c_imp, lbl_imp = col_imp_colors.get(ev["impacto"], ("#6b7a9e","📉"))
                    c_tipo = col_tipo_colors.get(ev["tipo"], "#8892b0")
                    dia_txt = f"Día {ev['dia']}" if ev["dia"] else "Mes completo"
                    st.markdown(
                        f'<div style="background:#13102a;border:1px solid {c_imp}33;'
                        f'border-left:4px solid {c_imp};border-radius:12px;padding:16px 18px;margin-bottom:10px">'
                        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">'
                        f'<div style="display:flex;align-items:center;gap:10px">'
                        f'<span style="font-size:1.4rem">{ev["ico"]}</span>'
                        f'<div>'
                        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.88rem">{ev["nombre"]}</div>'
                        f'<div style="font-size:0.63rem;color:#7a8aaa;margin-top:2px">{dia_txt} de {mes_nombres[_mes_sel_cal-1]}</div>'
                        f'</div></div>'
                        f'<div style="display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end">'
                        f'<span style="background:{c_imp}18;color:{c_imp};border:1px solid {c_imp}44;'
                        f'border-radius:20px;padding:2px 9px;font-size:0.62rem;font-weight:800">{lbl_imp}</span>'
                        f'<span style="background:{c_tipo}18;color:{c_tipo};border:1px solid {c_tipo}44;'
                        f'border-radius:20px;padding:2px 9px;font-size:0.62rem;font-weight:800">{ev["tipo"].capitalize()}</span>'
                        f'</div></div>'
                        f'<div style="font-size:0.78rem;color:#a8b4d0;line-height:1.6">'
                        f'💡 {ev["tip"]}'
                        f'</div></div>',
                        unsafe_allow_html=True
                    )

            # ── RECOMENDACIONES POR REGIÓN ACTIVA ──
            st.markdown("<hr style='border-color:#1e2337;margin:20px 0'>", unsafe_allow_html=True)
            st.markdown(
                '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.88rem;margin-bottom:12px">'
                '🗺️ Recomendaciones por Región — productos según tu zona de venta</div>',
                unsafe_allow_html=True
            )

            # Detectar regiones activas en los datos
            regiones_activas = []
            if C_DEPTO in df.columns:
                tops_dep = df[C_DEPTO].astype(str).str.upper().value_counts().head(6)
                for dep in tops_dep.index:
                    for key_r, info_r in RECOMENDACIONES_REGION.items():
                        if key_r in dep or dep in key_r:
                            regiones_activas.append({"dep": dep, "info": info_r, "n": tops_dep[dep]})
                            break

            if regiones_activas:
                reg_cols = st.columns(min(len(regiones_activas), 3))
                for ri, reg in enumerate(regiones_activas[:6]):
                    with reg_cols[ri % 3]:
                        prods_html = " · ".join([
                            f'<span style="background:#5b6cfc18;color:#a855f7;border:1px solid #5b6cfc33;'
                            f'border-radius:6px;padding:1px 7px;font-size:0.62rem">{p}</span>'
                            for p in reg["info"]["prod"]
                        ])
                        st.markdown(
                            f'<div style="background:#13102a;border:1px solid #2e2558;'
                            f'border-radius:12px;padding:14px;margin-bottom:10px">'
                            f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.8rem;margin-bottom:4px">'
                            f'📍 {reg["dep"].title()}</div>'
                            f'<div style="font-size:0.62rem;color:#7a8aaa;margin-bottom:8px">'
                            f'{reg["n"]:,} pedidos · Clima: {reg["info"]["temp"]} · Pico: {reg["info"]["pico"]}</div>'
                            f'<div style="display:flex;flex-wrap:wrap;gap:4px">{prods_html}</div>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
            else:
                st.info("📋 Agrega una columna DEPARTAMENTO en tu Excel para ver recomendaciones por región.")

            # ══════════════════════════════════════════════════════════════════
            # 🤝 RECOMENDACIONES IA
            # Venta cruzada · Promociones · Packs
            # ══════════════════════════════════════════════════════════════════
        elif "Recomendaciones" in mkt_nav:
            st.markdown('<div class="seccion-titulo">🤝 Recomendaciones IA de Marketing</div>', unsafe_allow_html=True)

            # _mes_cal puede no estar definido si el usuario no pasó por Calendario
            from datetime import date as _date_mkt
            _mes_cal = _date_mkt.today().month

            # ── VENTA CRUZADA ──
            st.markdown(
                '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.9rem;margin-bottom:4px">'
                '🔀 Venta Cruzada — productos que se compran juntos</div>'
                '<div style="font-size:0.72rem;color:#a8b4d0;margin-bottom:14px">'
                'Basado en clientes que compraron más de un producto en el período</div>',
                unsafe_allow_html=True
            )

            cruces = []
            if C_PRODUCTO in df.columns:
                # Agrupar por cliente si existe columna de cliente/teléfono
                C_CLI = next((c for c in df.columns if any(x in c.upper() for x in ["TELEFONO","CELULAR","CLIENTE","CUSTOMER","PHONE","CEL"])), None)
                if C_CLI:
                    df_multi = df.groupby(C_CLI)[C_PRODUCTO].apply(lambda x: list(x.astype(str).unique())).reset_index()
                    df_multi = df_multi[df_multi[C_PRODUCTO].apply(len) > 1]
                    pares = {}
                    for prods in df_multi[C_PRODUCTO]:
                        prods = sorted(set(prods))[:5]
                        for i in range(len(prods)):
                            for j in range(i+1, len(prods)):
                                key_p = (prods[i], prods[j])
                                pares[key_p] = pares.get(key_p, 0) + 1
                    top_pares = sorted(pares.items(), key=lambda x: x[1], reverse=True)[:8]
                    cruces = [{"prod_a": p[0][0], "prod_b": p[0][1], "n": p[1]} for p in top_pares]

            if cruces:
                st.markdown(
                    '<div style="font-size:0.72rem;color:#10b981;margin-bottom:10px">'
                    f'✅ Se encontraron {len(cruces)} pares de productos comprados juntos frecuentemente</div>',
                    unsafe_allow_html=True
                )
                for cr in cruces:
                    rentabilidad = ""
                    if C_GANANCIA in df.columns and C_PRODUCTO in df.columns:
                        g_a = df[df[C_PRODUCTO].astype(str)==cr["prod_a"]][C_GANANCIA].mean()
                        g_b = df[df[C_PRODUCTO].astype(str)==cr["prod_b"]][C_GANANCIA].mean()
                        rentabilidad = f" · Ganancia combinada est.: {fmt_money(g_a + g_b)}/par"
                    st.markdown(
                        f'<div style="background:#13102a;border:1px solid #5b6cfc33;border-radius:10px;'
                        f'padding:12px 16px;margin-bottom:8px;display:flex;align-items:center;gap:12px">'
                        f'<div style="background:#5b6cfc18;border-radius:8px;padding:8px 10px;'
                        f'font-size:0.78rem;color:#a855f7;font-weight:700;min-width:80px;text-align:center">'
                        f'{cr["n"]} veces</div>'
                        f'<div style="flex:1">'
                        f'<span style="font-size:0.8rem;color:#e8ecf7;font-weight:600">{str(cr["prod_a"])[:40]}</span>'
                        f'<span style="color:#fcd34d;font-size:0.9rem;margin:0 8px">+</span>'
                        f'<span style="font-size:0.8rem;color:#e8ecf7;font-weight:600">{str(cr["prod_b"])[:40]}</span>'
                        f'<div style="font-size:0.65rem;color:#7a8aaa;margin-top:2px">'
                        f'💡 Crea un pack combo con descuento del 10-15%{rentabilidad}</div>'
                        f'</div></div>',
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    '<div style="background:rgba(99,102,241,0.07);border:1px dashed #5b6cfc44;border-radius:10px;'
                    'padding:14px;font-size:0.78rem;color:#a8b4d0">'
                    '📋 Para activar análisis de venta cruzada, tu Excel necesita una columna de '
                    '<b style="color:#c8d0e8">teléfono o ID de cliente</b> que permita identificar '
                    'compras repetidas del mismo cliente. '
                    'Mientras tanto, aquí van sugerencias estratégicas basadas en patrones generales.</div>',
                    unsafe_allow_html=True
                )
                # Sugerencias basadas en datos disponibles
                if C_PRODUCTO in df.columns:
                    top_prods = df[C_PRODUCTO].astype(str).value_counts().head(5).index.tolist()
                    if len(top_prods) >= 2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown(
                            '<div style="font-size:0.75rem;color:#fcd34d;font-weight:700;margin-bottom:8px">'
                            '💡 Packs sugeridos con tus productos más vendidos:</div>',
                            unsafe_allow_html=True
                        )
                        for i in range(0, min(len(top_prods)-1, 4), 2):
                            st.markdown(
                                f'<div style="background:#13102a;border:1px solid #f0c06033;border-radius:10px;'
                                f'padding:12px 16px;margin-bottom:8px">'
                                f'<span style="font-size:0.8rem;color:#e8ecf7">{top_prods[i][:40]}</span>'
                                f'<span style="color:#fcd34d;margin:0 8px">+</span>'
                                f'<span style="font-size:0.8rem;color:#e8ecf7">{top_prods[i+1][:40]}</span>'
                                f'<div style="font-size:0.65rem;color:#7a8aaa;margin-top:4px">'
                                f'💡 Sugerencia: pack combo. Prueba con descuento del 10% al comprar ambos.</div>'
                                f'</div>',
                                unsafe_allow_html=True
                            )

            st.markdown("<hr style='border-color:#1e2337;margin:20px 0'>", unsafe_allow_html=True)

            # ── PROMOCIONES SUGERIDAS ──
            st.markdown(
                '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.9rem;margin-bottom:12px">'
                '🏷️ Estrategias de Promoción Recomendadas</div>',
                unsafe_allow_html=True
            )

            # Calcular contexto actual para personalizar las sugerencias
            _tasa_dev_mkt = devolucion / total * 100 if total else 0
            _tasa_can_mkt = cancelados / total * 100 if total else 0
            _margen_mkt   = tot_gan / tot_venta * 100 if tot_venta else 0

            promo_sugeridas = []

            # 1. Si hay muchas devoluciones → pack con garantía
            if _tasa_dev_mkt > 10:
                promo_sugeridas.append({
                    "tipo": "🛡️ Pack con Garantía",
                    "desc": f"Tu devolución está en {_tasa_dev_mkt:.1f}%. Ofrecer garantía de satisfacción o cambio incluido en el precio puede reducir el miedo a comprar y bajar la tasa de devolución.",
                    "accion": "Crea un 'Pack Garantizado' con margen del 5% adicional que cubra el costo de posible devolución.",
                    "color": "#00d4ff"
                })

            # 2. Si hay muchas cancelaciones → oferta de urgencia
            if _tasa_can_mkt > 12:
                promo_sugeridas.append({
                    "tipo": "⏱️ Oferta de Urgencia (Scarcity)",
                    "desc": f"Con {_tasa_can_mkt:.1f}% de cancelación, hay intención de compra pero la decisión se dilata. Las ofertas por tiempo limitado aumentan la conversión.",
                    "accion": "Flash Sale de 24h o '¡Últimas X unidades!'. Úsalo en el bot de confirmación para reducir el tiempo de duda.",
                    "color": "#ef4444"
                })

            # 3. Si el margen es bueno → 2x1 o descuento por volumen
            if _margen_mkt > 25:
                promo_sugeridas.append({
                    "tipo": "2️⃣ 2x1 o Descuento por Volumen",
                    "desc": f"Con {_margen_mkt:.1f}% de margen tienes espacio para ofrecer el segundo a mitad de precio o descuentos en combos sin sacrificar rentabilidad.",
                    "accion": "Prueba: 'Lleva 2 y el segundo a mitad de precio'. Proyecta que el ticket promedio sube un 60-80%.",
                    "color": "#10b981"
                })

            # 4. Siempre: regalo con la compra
            promo_sugeridas.append({
                "tipo": "🎁 Regalo con la Compra",
                "desc": "Los regalos aumentan percepción de valor sin bajar precio. Son especialmente efectivos en temporadas emocionales (Día de la Madre, Navidad, Amor y Amistad).",
                "accion": "Incluye un detalle de bajo costo (muestra, accesorio, empaque especial) que aparezca como 'gratis' en la pauta.",
                "color": "#f0c060"
            })

            # 5. Producto con menor rotación → empujarlo con descuento
            if C_PRODUCTO in df.columns and C_GANANCIA in df.columns:
                prod_menos = df.groupby(C_PRODUCTO)[C_TOTAL].count().sort_values().head(1)
                if len(prod_menos):
                    prod_bajo = prod_menos.index[0]
                    promo_sugeridas.append({
                        "tipo": f"📦 Liquidar: {str(prod_bajo)[:35]}",
                        "desc": f"'{prod_bajo}' es el producto con menor rotación. Tiene inventario parado que inmoviliza capital.",
                        "accion": "Crea un combo: compra tu producto estrella y lleva este a precio especial. Elimina el inventario sin perder margen.",
                        "color": "#f97416"
                    })

            # 6. Siempre: programa de referidos
            promo_sugeridas.append({
                "tipo": "👥 Programa de Referidos",
                "desc": "El costo de adquisición por referido es 3-5x menor que por pauta paga. Cada cliente satisfecho puede traer 1-2 clientes nuevos.",
                "accion": "Ofrece descuento al referido + beneficio al cliente que refiere. Comunícalo en el empaque o mensaje post-entrega.",
                "color": "#7c3aed"
            })

            for ps in promo_sugeridas:
                st.markdown(
                    f'<div style="background:#13102a;border:1px solid {ps["color"]}33;'
                    f'border-left:4px solid {ps["color"]};border-radius:12px;padding:16px 18px;margin-bottom:10px">'
                    f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.85rem;margin-bottom:6px">'
                    f'{ps["tipo"]}</div>'
                    f'<div style="font-size:0.78rem;color:#a8b4d0;margin-bottom:8px;line-height:1.5">{ps["desc"]}</div>'
                    f'<div style="background:{ps["color"]}10;border-radius:8px;padding:8px 12px">'
                    f'<span style="font-size:0.72rem;color:{ps["color"]};font-weight:800">⚡ Cómo aplicarlo: </span>'
                    f'<span style="font-size:0.72rem;color:#c8d0e8">{ps["accion"]}</span>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )

            # ── PRODUCTOS POR TEMPORADA (mes actual) ──
            st.markdown("<hr style='border-color:#1e2337;margin:20px 0'>", unsafe_allow_html=True)
            st.markdown(
                f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.9rem;margin-bottom:12px">'
                f'🌡️ Productos Recomendados para Esta Temporada</div>',
                unsafe_allow_html=True
            )

            PRODUCTOS_TEMPORADA = {
                (12,1,2):   {"season":"🥶 Temporada de Frío / Fin de Año",
                             "prods":["Ropa de abrigo","Cobijas","Thermos","Decoración navideña","Regalos","Chocolates"]},
                (3,4,5):    {"season":"🌸 Primavera Comercial / Temporada de Amor",
                             "prods":["Perfumes","Joyería","Flores","Ropa casual","Accesorios","Detalles regalo"]},
                (6,7,8):    {"season":"☀️ Vacaciones / Temporada de Calor",
                             "prods":["Ropa de verano","Artículos de playa","Juguetes","Deportes","Gafas de sol"]},
                (9,10,11):  {"season":"🍂 Pre-Navidad / Halloween / Black Friday",
                             "prods":["Disfraces","Decoración","Electrónicos","Ropa de temporada","Gadgets","Artículos de regalo"]},
            }

            temp_actual = None
            for meses_t, data_t in PRODUCTOS_TEMPORADA.items():
                if _mes_cal in meses_t:
                    temp_actual = data_t
                    break

            if temp_actual:
                st.markdown(
                    f'<div style="background:rgba(201,168,76,0.07);border:1px solid #f0c06033;'
                    f'border-radius:12px;padding:16px 18px;margin-bottom:12px">'
                    f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#fcd34d;font-size:0.85rem;margin-bottom:10px">'
                    f'{temp_actual["season"]}</div>'
                    f'<div style="display:flex;flex-wrap:wrap;gap:6px">',
                    unsafe_allow_html=True
                )
                for prod_t in temp_actual["prods"]:
                    st.markdown(
                        f'<span style="background:#5b6cfc18;color:#a8b4d0;border:1px solid #5b6cfc33;'
                        f'border-radius:8px;padding:4px 10px;font-size:0.75rem">{prod_t}</span>',
                        unsafe_allow_html=True
                    )
                st.markdown('</div></div>', unsafe_allow_html=True)

                # Cruce con productos actuales del catálogo
                if C_PRODUCTO in df.columns:
                    prods_cat = df[C_PRODUCTO].astype(str).str.lower().unique()
                    prods_alineados = [p for p in temp_actual["prods"]
                                       if any(p.lower().split()[0] in pc for pc in prods_cat)]
                    prods_faltantes = [p for p in temp_actual["prods"] if p not in prods_alineados]
                    if prods_alineados:
                        st.markdown(
                            f'<div style="font-size:0.72rem;color:#10b981;margin-bottom:4px">'
                            f'✅ Productos de temporada que YA tienes en catálogo: '
                            f'{", ".join(prods_alineados)}</div>',
                            unsafe_allow_html=True
                        )
                    if prods_faltantes:
                        st.markdown(
                            f'<div style="font-size:0.72rem;color:#f59e0b">'
                            f'💡 Oportunidad: productos de temporada que NO tienes aún: '
                            f'{", ".join(prods_faltantes[:4])}</div>',
                            unsafe_allow_html=True
                        )

            # ── INSIGHTS ──
        elif "Insights" in mkt_nav:
            st.markdown('<div class="seccion-titulo">💡 Insights Estratégicos Automáticos</div>', unsafe_allow_html=True)

            insights = []

            if tot_venta > 0:
                insights.append({
                    'ico':'💰','titulo':'Margen de Ganancia',
                    'texto': f"Tu margen actual es del {pct_gan}%. " +
                             ("✅ Excelente rentabilidad." if pct_gan > 30 else
                              "⚠️ Margen ajustado, revisa costos." if pct_gan > 15 else
                              "🔴 Margen crítico, acción urgente requerida.")
                })

            if total > 0:
                insights.append({
                    'ico':'📦','titulo':'Tasa de Entrega',
                    'texto': f"El {pct_ent}% de los pedidos están entregados. " +
                             ("✅ Excelente tasa de entrega." if pct_ent > 85 else
                              "⚠️ Hay oportunidad de mejora en entrega." if pct_ent > 70 else
                              "🔴 Tasa de entrega baja, revisa operación logística.")
                })

            if cancelados > 0 and total > 0:
                pct_can = round(cancelados/total*100,1)
                insights.append({
                    'ico':'❌','titulo':'Tasa de Cancelación',
                    'texto': f"{pct_can}% de cancelación ({cancelados:,} pedidos). " +
                             ("✅ Tasa controlada." if pct_can < 10 else
                              "⚠️ Tasa de cancelación alta, analiza las causas por tags." if pct_can < 20 else
                              "🔴 Cancelación crítica. Revisa la calidad del tráfico y los proveedores.")
                })

            if C_DEPTO in df.columns:
                top2_dep = df[C_DEPTO].value_counts().head(2)
                if len(top2_dep) >= 2:
                    conc = round(top2_dep.sum()/total*100,1)
                    insights.append({
                        'ico':'🗺️','titulo':'Concentración Geográfica',
                        'texto': f"{top2_dep.index[0]} y {top2_dep.index[1]} representan el {conc}% de tus pedidos. " +
                                 ("✅ Buena diversificación geográfica." if conc < 50 else
                                  "⚠️ Alta concentración — considera expandir pauta a más departamentos.")
                    })

            if C_PRODUCTO in df.columns:
                top1 = df[C_PRODUCTO].value_counts().iloc[0]
                top1_name = df[C_PRODUCTO].value_counts().index[0]
                pct_top1 = round(top1/total*100,1)
                insights.append({
                    'ico':'🏆','titulo':'Producto Estrella',
                    'texto': f'"{top1_name}" lidera con {top1:,} unidades ({pct_top1}% del total). ' +
                             ("✅ Buen balance del portafolio." if pct_top1 < 40 else
                              "⚠️ Alta dependencia de un solo producto — diversifica el catálogo.")
                })

            if '_mes' in df.columns and C_TOTAL in df.columns:
                v_mes = df.groupby('_mes')[C_TOTAL].sum().sort_values(ascending=False)
                if len(v_mes) >= 2:
                    mejor_mes = v_mes.index[0]
                    insights.append({
                        'ico':'📅','titulo':'Mejor Mes',
                        'texto': f"El mes con más ventas fue {mejor_mes} con {fmt_money(v_mes.iloc[0])}. "
                                 f"Analiza qué campaña o factor impulsó ese resultado para replicarlo."
                    })

            for ins in insights:
                st.markdown(f"""
                <div class="insight">
                    <div class="insight-titulo">{ins['ico']} {ins['titulo']}</div>
                    <div class="insight-texto">{ins['texto']}</div>
                </div>""", unsafe_allow_html=True)

            if not insights:
                st.info("Sube más datos para generar insights automáticos.")


    # ══════════════════════════════════════════════════════════════════
    # 💹 FINANZAS — MÓDULO COMPLETO
    # ══════════════════════════════════════════════════════════════════
    elif nav == "💹 Finanzas":

        # Sub-navegación interna
        fin_nav = st.radio("", [
            "💰 Diagnóstico Financiero",
            "📊 Estado de Resultados",
            "👥 Nómina",
            "⚖️ Punto de Equilibrio",
            "📈 Rentabilidad",
            "💧 Flujo de Caja",
            "📉 Análisis de Costos",
            "🎯 KPIs Financieros",
        ], horizontal=True, label_visibility="collapsed", key="fin_nav")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Datos base del período ──
        meses_fin = sorted(df['_mes'].dropna().unique().tolist(), reverse=True) if '_mes' in df.columns else []
        col_mf, _ = st.columns([2,4])
        with col_mf:
            mes_fin = st.selectbox("📅 Período", meses_fin if meses_fin else ["Sin datos"], key="mes_fin")
        if '_mes' in df.columns and mes_fin != "Sin datos":
            df_fin = df[df['_mes'] == mes_fin].copy()
        else:
            df_fin = df.copy()

        # Calcular métricas base
        C_CST_PROD = "PRECIO PROVEEDOR X CANTIDAD"
        mask_ent = df_fin[C_ESTATUS].astype(str).str.upper().str.contains('ENTREGAD', na=False) if C_ESTATUS in df_fin.columns else pd.Series([True]*len(df_fin))
        mask_can = df_fin[C_ESTATUS].astype(str).str.upper().str.contains('CANCELAD', na=False) if C_ESTATUS in df_fin.columns else pd.Series([False]*len(df_fin))
        mask_dev = df_fin[C_ESTATUS].astype(str).str.upper().str.contains('DEVOLUCI', na=False) if C_ESTATUS in df_fin.columns else pd.Series([False]*len(df_fin))

        df_ent = df_fin[mask_ent]
        n_total   = len(df_fin)
        n_ent     = int(mask_ent.sum())
        n_can     = int(mask_can.sum())
        n_dev     = int(mask_dev.sum())

        ingresos      = df_ent[C_TOTAL].sum()    if C_TOTAL    in df_ent.columns else 0
        costo_prod    = df_ent[C_CST_PROD].sum() if C_CST_PROD in df_ent.columns else 0
        flete_ent     = df_ent[C_FLETE].sum()    if C_FLETE    in df_ent.columns else 0
        flete_dev     = df_fin[mask_dev][C_FLETE].sum() if C_FLETE in df_fin.columns else 0
        ganancia_dropi= df_ent[C_GANANCIA].sum() if C_GANANCIA in df_ent.columns else 0
        utilidad_bruta= ingresos - costo_prod
        ticket_prom   = ingresos / n_ent if n_ent else 0
        margen_bruto_pct = utilidad_bruta / ingresos * 100 if ingresos else 0

        # Recuperar nómina y pauta de session_state
        nomina_total  = st.session_state.get('nomina_total', 0)
        pauta_total_fin = st.session_state.get('pauta_dict', {})
        pauta_fin     = sum(pauta_total_fin.values()) if pauta_total_fin else 0
        costos_fijos  = st.session_state.get('costos_fijos', {})
        cf_total      = sum(costos_fijos.values()) + nomina_total

        gastos_op     = flete_ent + flete_dev + pauta_fin + cf_total
        utilidad_op   = utilidad_bruta - gastos_op
        impuesto_est  = ingresos * 0.08
        utilidad_neta = utilidad_op - impuesto_est
        margen_neto_pct = utilidad_neta / ingresos * 100 if ingresos else 0

        # ══════════════════════════════════════════════════════════════════
        # 💰 DIAGNÓSTICO FINANCIERO — NUEVO TAB PRINCIPAL
        # Gastos reales · Impuestos · Flete devolución · Patrimonio
        # ══════════════════════════════════════════════════════════════════
        if "Diagnóstico" in fin_nav:
            st.markdown('<div class="seccion-titulo">💰 Diagnóstico Financiero del Período</div>', unsafe_allow_html=True)

            # ── Configuración fiscal inline ──
            with st.expander("⚙️ Configurar tasa de impuesto real", expanded=False):
                tc1, tc2, tc3 = st.columns(3)
                with tc1:
                    tasa_imp_diag = st.number_input(
                        "% Impuesto sobre ingresos", 0.0, 50.0,
                        float(st.session_state.get('diag_imp', 8.0)), step=0.5,
                        key="diag_imp",
                        help="Retención en la fuente, IVA efectivo, etc."
                    )
                with tc2:
                    pct_iva_excl = st.number_input(
                        "% Base excluida de impuesto", 0.0, 100.0,
                        float(st.session_state.get('diag_iva_excl', 80.0)), step=5.0,
                        key="diag_iva_excl",
                        help="Si el 80% está excluido, el impuesto aplica solo al 20%"
                    )
                with tc3:
                    tasa_imp_efect = tasa_imp_diag * (1 - pct_iva_excl / 100)
                    st.metric("Tasa efectiva real", f"{tasa_imp_efect:.2f}%",
                              help="= Tasa × (1 − % excluido)")
            tasa_imp_efect = float(st.session_state.get('diag_imp', 8.0)) * \
                             (1 - float(st.session_state.get('diag_iva_excl', 80.0)) / 100)

            # ── Cálculos reales ──
            ingreso_bruto     = df_fin[C_TOTAL].sum() if C_TOTAL in df_fin.columns else 0  # TODOS los pedidos
            ingreso_neto      = ingresos                                                     # solo entregados
            impuesto_real     = ingreso_neto * (tasa_imp_efect / 100)
            utilidad_neta_diag = utilidad_op - impuesto_real
            margen_util_pct   = utilidad_neta_diag / ingreso_neto * 100 if ingreso_neto else 0
            pct_imp_sobre_ing = impuesto_real / ingreso_neto * 100 if ingreso_neto else 0

            # Flete devolución como pérdida directa
            pct_flete_dev_ing = flete_dev / ingreso_neto * 100 if ingreso_neto else 0

            # Patrimonio: utilidad neta acumulada mes vs mes anterior
            mes_fin_ant = None
            meses_fin_list = sorted(df['_mes'].dropna().unique().tolist(), reverse=True) if '_mes' in df.columns else []
            if mes_fin in meses_fin_list:
                idx_f = meses_fin_list.index(mes_fin)
                mes_fin_ant = meses_fin_list[idx_f + 1] if idx_f + 1 < len(meses_fin_list) else None

            if mes_fin_ant and '_mes' in df.columns:
                df_ant_fin = df[df['_mes'] == mes_fin_ant].copy()
                mask_ent_a   = df_ant_fin[C_ESTATUS].astype(str).str.upper().str.contains('ENTREGAD', na=False) if C_ESTATUS in df_ant_fin.columns else pd.Series([True]*len(df_ant_fin))
                ing_ant_fin  = df_ant_fin[mask_ent_a][C_TOTAL].sum() if C_TOTAL in df_ant_fin.columns else 0
                gan_ant_fin  = df_ant_fin[mask_ent_a][C_GANANCIA].sum() if C_GANANCIA in df_ant_fin.columns else 0
                fd_ant       = df_ant_fin[df_ant_fin[C_ESTATUS].astype(str).str.upper().str.contains('DEVOLUCI', na=False)][C_FLETE].sum() if C_FLETE in df_ant_fin.columns else 0
                cst_ant      = df_ant_fin[mask_ent_a]["PRECIO PROVEEDOR X CANTIDAD"].sum() if "PRECIO PROVEEDOR X CANTIDAD" in df_ant_fin.columns else 0
                ub_ant       = ing_ant_fin - cst_ant
                go_ant       = fd_ant + sum(st.session_state.get('pauta_dict', {}).values()) + st.session_state.get('nomina_total', 0) + sum(st.session_state.get('costos_fijos', {}).values())
                uop_ant      = ub_ant - go_ant
                un_ant       = uop_ant - ing_ant_fin * (tasa_imp_efect / 100)
                crecimiento_patrimonio = utilidad_neta_diag - un_ant
                pct_crec = (utilidad_neta_diag - un_ant) / abs(un_ant) * 100 if un_ant else 0
                tiene_ant = True
                MESES_ES2 = {1:"Ene",2:"Feb",3:"Mar",4:"Abr",5:"May",6:"Jun",
                             7:"Jul",8:"Ago",9:"Sep",10:"Oct",11:"Nov",12:"Dic"}
                def fmt_mes_corto(m):
                    try: y,mo=str(m).split('-'); return f"{MESES_ES2[int(mo)]} {y[-2:]}"
                    except: return str(m)
            else:
                un_ant = 0; crecimiento_patrimonio = 0; pct_crec = 0; tiene_ant = False

            # ── FILA 1: 5 KPIs principales ──
            d1,d2,d3,d4,d5 = st.columns(5)

            with d1:
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,#5b6cfc20,#5b6cfc08);border:2px solid #5b6cfc;'
                    f'border-radius:14px;padding:16px 12px;text-align:center">'
                    f'<div style="font-size:0.6rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;'
                    f'letter-spacing:0.06em;margin-bottom:4px">💵 INGRESO BRUTO</div>'
                    f'<div style="font-size:0.58rem;color:#7a8aaa;margin-bottom:6px">Todos los pedidos del período</div>'
                    f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:#a855f7;font-size:1.15rem">{fmt_money(ingreso_bruto)}</div>'
                    f'<div style="font-size:0.62rem;color:#a8b4d0;margin-top:4px">Entregados: {fmt_money(ingreso_neto)}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            with d2:
                c_util = "#10b981" if utilidad_neta_diag > 0 else "#ef4444"
                st.markdown(
                    f'<div style="background:{c_util}12;border:2px solid {c_util};'
                    f'border-radius:14px;padding:16px 12px;text-align:center">'
                    f'<div style="font-size:0.6rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;'
                    f'letter-spacing:0.06em;margin-bottom:4px">📈 % UTILIDAD REAL</div>'
                    f'<div style="font-size:0.58rem;color:#7a8aaa;margin-bottom:6px">Después de todos los gastos e impuestos</div>'
                    f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:{c_util};font-size:1.4rem">{margen_util_pct:.1f}%</div>'
                    f'<div style="font-size:0.62rem;color:{c_util};margin-top:4px">{fmt_money(utilidad_neta_diag)} netos</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            with d3:
                st.markdown(
                    f'<div style="background:#f0c06012;border:2px solid #f0c060;'
                    f'border-radius:14px;padding:16px 12px;text-align:center">'
                    f'<div style="font-size:0.6rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;'
                    f'letter-spacing:0.06em;margin-bottom:4px">🏛️ IMPUESTO REAL</div>'
                    f'<div style="font-size:0.58rem;color:#7a8aaa;margin-bottom:6px">Tasa efectiva: {tasa_imp_efect:.2f}%</div>'
                    f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:#fcd34d;font-size:1.15rem">{fmt_money(impuesto_real)}</div>'
                    f'<div style="font-size:0.62rem;color:#fcd34d;margin-top:4px">{pct_imp_sobre_ing:.2f}% del ingreso neto</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            with d4:
                st.markdown(
                    f'<div style="background:#f9741620;border:2px solid #f97416;'
                    f'border-radius:14px;padding:16px 12px;text-align:center">'
                    f'<div style="font-size:0.6rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;'
                    f'letter-spacing:0.06em;margin-bottom:4px">↩️ FLETE DEVOLUCIÓN</div>'
                    f'<div style="font-size:0.58rem;color:#f97416;margin-bottom:6px">⚠️ Pérdida financiera directa</div>'
                    f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:#f97416;font-size:1.15rem">{fmt_money(flete_dev)}</div>'
                    f'<div style="font-size:0.62rem;color:#f97416;margin-top:4px">{pct_flete_dev_ing:.2f}% del ingreso</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            with d5:
                if tiene_ant:
                    c_crec = "#10b981" if crecimiento_patrimonio >= 0 else "#ef4444"
                    sym_crec = "▲" if crecimiento_patrimonio >= 0 else "▼"
                    txt_crec = f"{sym_crec} {abs(pct_crec):.1f}% vs {fmt_mes_corto(mes_fin_ant)}"
                else:
                    c_crec = "#8892b0"; txt_crec = "sin mes anterior"
                st.markdown(
                    f'<div style="background:{c_crec}12;border:2px solid {c_crec};'
                    f'border-radius:14px;padding:16px 12px;text-align:center">'
                    f'<div style="font-size:0.6rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;'
                    f'letter-spacing:0.06em;margin-bottom:4px">🏦 CRECIMIENTO PATRIMONIO</div>'
                    f'<div style="font-size:0.58rem;color:#7a8aaa;margin-bottom:6px">Δ Utilidad neta mes a mes</div>'
                    f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:{c_crec};font-size:1.15rem">{fmt_money(crecimiento_patrimonio)}</div>'
                    f'<div style="font-size:0.62rem;color:{c_crec};margin-top:4px">{txt_crec}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # ── CASCADA DE GASTOS — Tabla bancaria ──
            st.markdown(
                '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.92rem;margin-bottom:12px">'
                '🏦 Cascada Financiera — Estructura real del dinero</div>',
                unsafe_allow_html=True
            )

            def fila_cascada(concepto, valor, tipo="gasto", nivel=0, destacada=False, pct_base=None):
                """
                tipo: "ingreso" | "gasto_op" | "gasto_fin" | "impuesto" | "resultado"
                """
                colores = {
                    "ingreso":    "#5b6cfc",
                    "gasto_op":   "#ef4444",
                    "gasto_fin":  "#f97416",
                    "impuesto":   "#f0c060",
                    "resultado":  "#10b981" if valor >= 0 else "#ef4444",
                    "subtotal":   "#00d4ff",
                }
                col_v = colores.get(tipo, "#8892b0")
                if tipo == "resultado" and valor < 0:
                    col_v = "#ef4444"
                indent = "&nbsp;" * (nivel * 5)
                signo  = "−&nbsp;" if tipo in ("gasto_op","gasto_fin","impuesto") and valor > 0 else ""
                bg     = f"rgba({col_v.lstrip('#')},0.06)" if destacada else "transparent"
                bld    = "font-weight:800;" if destacada else ""
                pct_str = f"{valor/ingreso_neto*100:.1f}%" if ingreso_neto and not destacada else \
                          (f"<b>{valor/ingreso_neto*100:.1f}%</b>" if ingreso_neto else "")
                barra_w = min(abs(valor)/ingreso_bruto*100, 100) if ingreso_bruto else 0
                barra_col = col_v
                barra_html = (
                    f'<div style="background:#1e2337;border-radius:100px;height:4px;margin-top:4px;overflow:hidden;max-width:140px">'
                    f'<div style="background:{barra_col};width:{barra_w:.1f}%;height:100%;border-radius:100px"></div></div>'
                ) if not destacada else ""
                return (
                    f'<tr style="background:{bg};border-bottom:1px solid #12151f">'
                    f'<td style="padding:10px 16px;color:#c8d0e8;font-size:0.82rem;{bld}">'
                    f'{indent}{concepto}{barra_html}</td>'
                    f'<td style="padding:10px 16px;text-align:right;color:{col_v};font-size:0.85rem;{bld}">'
                    f'{signo}{fmt_money(abs(valor))}</td>'
                    f'<td style="padding:10px 16px;text-align:right;color:#7a8aaa;font-size:0.72rem">{pct_str}</td>'
                    f'</tr>'
                )

            def sep_cascada(titulo, color="#1e2337"):
                return (
                    f'<tr><td colspan="3" style="padding:6px 16px;background:#0f0e1d;'
                    f'border-bottom:1px solid {color}">'
                    f'<span style="font-size:0.65rem;color:{color};font-weight:800;text-transform:uppercase;'
                    f'letter-spacing:0.08em">{titulo}</span></td></tr>'
                )

            casc_html = (
                f'<div style="overflow-x:auto;border-radius:14px;border:1px solid #2e2558;margin-bottom:20px">'
                f'<table style="width:100%;border-collapse:collapse;background:#13102a;font-family:DM Sans,sans-serif">'
                f'<thead><tr>'
                f'<th style="padding:12px 16px;text-align:left;color:#a8b4d0;font-size:0.68rem;text-transform:uppercase;'
                f'letter-spacing:0.07em;border-bottom:2px solid #1e2337">Concepto</th>'
                f'<th style="padding:12px 16px;text-align:right;color:#a8b4d0;font-size:0.68rem;text-transform:uppercase;'
                f'letter-spacing:0.07em;border-bottom:2px solid #1e2337">Valor</th>'
                f'<th style="padding:12px 16px;text-align:right;color:#a8b4d0;font-size:0.68rem;text-transform:uppercase;'
                f'letter-spacing:0.07em;border-bottom:2px solid #1e2337">% Ingreso</th>'
                f'</tr></thead><tbody>'

                # BLOQUE 1 — INGRESOS
                + sep_cascada("① Ingresos", "#5b6cfc")
                + fila_cascada("Ingreso Bruto (todos los pedidos)", ingreso_bruto, "ingreso", destacada=True)
                + fila_cascada("Pedidos no entregados (cancelados + dev.)", ingreso_bruto - ingreso_neto, "gasto_op", nivel=1)
                + fila_cascada("INGRESO NETO COBRABLE", ingreso_neto, "subtotal", destacada=True)

                # BLOQUE 2 — COSTOS DIRECTOS
                + sep_cascada("② Costos del Producto", "#ef4444")
                + fila_cascada("Costo de Producto Vendido", costo_prod, "gasto_op", nivel=1)
                + fila_cascada("UTILIDAD BRUTA", utilidad_bruta, "resultado", destacada=True)

                # BLOQUE 3 — GASTOS OPERATIVOS
                + sep_cascada("③ Gastos Operativos", "#f59e0b")
                + fila_cascada("Flete de Entrega", flete_ent, "gasto_op", nivel=1)
                + fila_cascada("Pauta Publicitaria", pauta_fin, "gasto_op", nivel=1)
                + fila_cascada("Nómina y Equipo", nomina_total, "gasto_op", nivel=1)
                + fila_cascada("Costos Fijos Adicionales", sum(costos_fijos.values()), "gasto_op", nivel=1)
                + fila_cascada("EBITDA (Utilidad Operativa)", utilidad_op, "resultado", destacada=True)

                # BLOQUE 4 — GASTOS FINANCIEROS / PÉRDIDAS
                + sep_cascada("④ Pérdidas Financieras (Devoluciones)", "#f97416")
                + fila_cascada("↩️ Flete de Devolución", flete_dev, "gasto_fin", nivel=1)
                + fila_cascada("  → Es dinero pagado sin recuperar ingreso", 0, "gasto_fin", nivel=2)
                + fila_cascada("RESULTADO ANTES DE IMPUESTOS", utilidad_op - flete_dev, "resultado", destacada=True)

                # BLOQUE 5 — IMPUESTOS REALES
                + sep_cascada("⑤ Impuestos", "#f0c060")
                + fila_cascada(f"Impuesto efectivo ({tasa_imp_efect:.2f}% sobre ingreso neto)", impuesto_real, "impuesto", nivel=1)
                + fila_cascada(f"  Base imponible: {(1-float(st.session_state.get('diag_iva_excl',80.0))/100)*100:.0f}% · Tasa nominal: {float(st.session_state.get('diag_imp',8.0)):.1f}%", 0, "impuesto", nivel=2)

                # BLOQUE 6 — RESULTADO FINAL
                + sep_cascada("⑥ Resultado Final", "#10b981")
                + fila_cascada("▶ UTILIDAD NETA REAL", utilidad_neta_diag, "resultado", destacada=True)
                + '</tbody></table></div>'
            )
            st.markdown(casc_html, unsafe_allow_html=True)

            # ── % DE UTILIDAD — Gráfica waterfall en barras ──
            st.markdown(
                '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.88rem;margin-bottom:12px">'
                '📊 Distribución del Ingreso Neto — ¿a dónde va cada peso?</div>',
                unsafe_allow_html=True
            )

            conceptos_dist = [
                ("Costo Producto",   costo_prod,            "#ef4444"),
                ("Flete Entrega",    flete_ent,             "#f59e0b"),
                ("Flete Devolución", flete_dev,             "#f97416"),
                ("Pauta",            pauta_fin,             "#7c3aed"),
                ("Nómina",           nomina_total,          "#5b6cfc"),
                ("Costos Fijos",     sum(costos_fijos.values()), "#00d4ff"),
                ("Impuestos",        impuesto_real,         "#f0c060"),
                ("Utilidad Neta",    utilidad_neta_diag,    "#10b981" if utilidad_neta_diag >= 0 else "#ef4444"),
            ]

            dist_html = '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:16px">'
            for lbl, val, col in conceptos_dist:
                pct_d = val / ingreso_neto * 100 if ingreso_neto else 0
                dist_html += (
                    f'<div style="background:{col}12;border:1.5px solid {col}44;border-top:3px solid {col};'
                    f'border-radius:12px;padding:10px 12px;flex:1;min-width:100px;text-align:center">'
                    f'<div style="font-size:0.6rem;color:{col};font-weight:800;text-transform:uppercase;'
                    f'letter-spacing:0.05em;margin-bottom:4px">{lbl}</div>'
                    f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:{col};font-size:1.1rem">{pct_d:.1f}%</div>'
                    f'<div style="font-size:0.62rem;color:#7a8aaa;margin-top:2px">{fmt_money(val)}</div>'
                    f'<div style="background:#1e2337;border-radius:100px;height:5px;margin-top:6px;overflow:hidden">'
                    f'<div style="background:{col};width:{min(abs(pct_d),100):.0f}%;height:100%;border-radius:100px"></div>'
                    f'</div></div>'
                )
            dist_html += '</div>'
            st.markdown(dist_html, unsafe_allow_html=True)

            # ── ASESOR: DISTRIBUCIÓN RECOMENDADA ──
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.88rem;margin-bottom:4px">'
                '🤖 Asesor — ¿Cómo distribuir la utilidad disponible?</div>'
                '<div style="font-size:0.72rem;color:#a8b4d0;margin-bottom:12px">'
                'Basado en tu utilidad neta real del período</div>',
                unsafe_allow_html=True
            )

            if utilidad_neta_diag > 0:
                # Proporciones recomendadas
                dist_rec = [
                    ("🔄 Reinversión en Operación", 0.30, "#5b6cfc",
                     "Capital de trabajo, inventario, logística"),
                    ("📣 Marketing",                0.20, "#7c3aed",
                     "Pauta, creativos, nuevos canales"),
                    ("🏦 Reserva de Emergencia",    0.20, "#00d4ff",
                     "Mínimo 3 meses de costos fijos cubiertos"),
                    ("📈 Inversión / Crecimiento",  0.20, "#10b981",
                     "Nuevos productos, equipos, expansión"),
                    ("💼 Distribución / Retiro",    0.10, "#f0c060",
                     "Rentabilidad personal del negocio"),
                ]
                asesor_html = '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:10px">'
                for lbl_r, pct_r, col_r, desc_r in dist_rec:
                    monto_r = utilidad_neta_diag * pct_r
                    asesor_html += (
                        f'<div style="background:{col_r}12;border:1px solid {col_r}44;border-top:3px solid {col_r};'
                        f'border-radius:12px;padding:12px;text-align:center">'
                        f'<div style="font-size:0.62rem;color:{col_r};font-weight:800;text-transform:uppercase;'
                        f'letter-spacing:0.05em;margin-bottom:6px;line-height:1.3">{lbl_r}</div>'
                        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:{col_r};font-size:1rem">{fmt_money(monto_r)}</div>'
                        f'<div style="font-size:0.7rem;color:#fcd34d;font-weight:700;margin:3px 0">{pct_r*100:.0f}% de la utilidad</div>'
                        f'<div style="font-size:0.62rem;color:#7a8aaa;line-height:1.4">{desc_r}</div>'
                        f'</div>'
                    )
                asesor_html += '</div>'
                asesor_html += (
                    f'<div style="background:rgba(99,102,241,0.06);border:1px dashed #5b6cfc44;'
                    f'border-radius:10px;padding:12px 16px;font-size:0.75rem;color:#a8b4d0;line-height:1.7">'
                    f'💡 <b style="color:#fcd34d">Recomendación del mes:</b> '
                    f'Tienes <b style="color:#10b981">{fmt_money(utilidad_neta_diag)}</b> de utilidad neta real. '
                    f'Prioriza la <b style="color:#22d3ee">reserva de emergencia</b> si no tienes 3 meses de costos fijos '
                    f'cubiertos ({fmt_money(cf_total * 3)} objetivo). '
                    f'El flete de devolución representa <b style="color:#f97416">{fmt_money(flete_dev)}</b> de pérdida directa — '
                    f'reducirlo un 20% liberaría <b style="color:#f97416">{fmt_money(flete_dev * 0.2)}</b> mensuales.'
                    f'</div>'
                )
                st.markdown(asesor_html, unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div style="background:rgba(239,68,68,0.07);border:1px solid #ef444444;'
                    f'border-radius:12px;padding:18px;text-align:center">'
                    f'<div style="font-size:1.5rem;margin-bottom:8px">⚠️</div>'
                    f'<div style="color:#ef4444;font-weight:800;margin-bottom:6px">Utilidad neta negativa — no hay excedente para distribuir</div>'
                    f'<div style="font-size:0.78rem;color:#a8b4d0;line-height:1.6">'
                    f'El negocio gastó más de lo que generó este período. '
                    f'Revisa la estructura de costos: el flete ({fmt_money(flete_ent + flete_dev)}) '
                    f'y la pauta ({fmt_money(pauta_fin)}) representan '
                    f'{(flete_ent + flete_dev + pauta_fin) / ingreso_neto * 100:.1f}% del ingreso neto.'
                    f'</div></div>',
                    unsafe_allow_html=True
                )

        # ══════════════════════════════════════════════════════════════════
        # 👥 NÓMINA
        # ══════════════════════════════════════════════════════
        if "Nómina" in fin_nav:
            st.markdown('<div class="seccion-titulo">👥 Gestión de Nómina</div>', unsafe_allow_html=True)

            # ── Cargar empleados guardados ──
            empleados = st.session_state.get('empleados', [
                {"nombre": "Leidy (Coordinadora)",   "cargo": "Coordinadora",        "sueldo": 0, "bonificacion": 0},
                {"nombre": "Samanta (Logística)",    "cargo": "Logística",           "sueldo": 0, "bonificacion": 0},
                {"nombre": "Sandra (Confirmación)",  "cargo": "Confirmación",        "sueldo": 0, "bonificacion": 0},
                {"nombre": "Contador",               "cargo": "Contabilidad",        "sueldo": 0, "bonificacion": 0},
                {"nombre": "C.E.O. - Ronaldo",       "cargo": "CEO",                 "sueldo": 0, "bonificacion": 0},
            ])

            st.markdown('<div style="background:#13102a;border:1px solid #2e2558;border-radius:14px;padding:20px;margin-bottom:20px">', unsafe_allow_html=True)
            st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.95rem;margin-bottom:16px">📝 Equipo de Trabajo</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # ── Encabezado columnas ──
            hc1,hc2,hc3,hc4,hc5,hc6 = st.columns([3,2,1.5,2,1.5,1])
            for lbl, col in zip(["Nombre / Cargo","Sueldo Base $","Tipo Bono","Bono / Comisión","% sobre ventas","Total Mes"],
                                 [hc1,hc2,hc3,hc4,hc5,hc6]):
                col.markdown(f'<div style="font-size:0.68rem;font-weight:800;color:#a8b4d0;text-transform:uppercase;'
                             f'letter-spacing:0.06em;padding-bottom:4px">{lbl}</div>', unsafe_allow_html=True)

            # Editor de nómina
            total_sueldos = 0
            total_bonos   = 0
            empleados_editados = []

            for i, emp in enumerate(empleados):
                with st.container():
                    c1, c2, c3, c4, c5, c6 = st.columns([3, 2, 1.5, 2, 1.5, 1])
                    with c1:
                        nom = st.text_input("Nombre", value=emp['nombre'], key=f"nom_{i}", label_visibility="collapsed")
                    with c2:
                        sueldo = st.number_input("Sueldo", value=int(emp['sueldo']), step=50000, min_value=0, key=f"sld_{i}", label_visibility="collapsed")
                    with c3:
                        tipo_bono = st.selectbox("Tipo", ["Fijo $","Comisión %","Sin bono"], key=f"tipo_{i}",
                                                 index=["Fijo $","Comisión %","Sin bono"].index(emp.get('tipo_bono','Fijo $')),
                                                 label_visibility="collapsed")
                    with c4:
                        bono_base = int(emp.get('bonificacion', 0))
                        if tipo_bono == "Sin bono":
                            bono = 0
                            st.markdown('<div style="padding-top:8px;color:#7a8aaa;font-size:0.8rem">—</div>', unsafe_allow_html=True)
                        elif tipo_bono == "Comisión %":
                            pct_com = st.number_input("% Comisión", value=float(emp.get('pct_comision', 0.0)),
                                                      step=0.1, min_value=0.0, max_value=100.0, key=f"pct_{i}",
                                                      label_visibility="collapsed", format="%.1f")
                            bono = ingresos * (pct_com / 100)
                        else:
                            bono = st.number_input("Bono $", value=bono_base, step=10000, min_value=0, key=f"bon_{i}", label_visibility="collapsed")
                            pct_com = 0.0
                    with c5:
                        pct_sobre_vnt = bono / ingresos * 100 if ingresos and bono else 0
                        st.markdown(f'<div style="padding-top:8px;color:#9333ea;font-size:0.82rem;font-weight:600">'
                                    f'{"" if tipo_bono=="Sin bono" else f"{pct_sobre_vnt:.2f}%"}</div>', unsafe_allow_html=True)
                    with c6:
                        total_emp = sueldo + bono
                        st.markdown(f'<div style="padding-top:8px;color:#fcd34d;font-weight:800;font-size:0.85rem">'
                                    f'{fmt_money(total_emp)}</div>', unsafe_allow_html=True)

                    total_sueldos += sueldo
                    total_bonos   += bono
                    pct_com_val = pct_com if tipo_bono == "Comisión %" else 0.0
                    empleados_editados.append({
                        "nombre": nom, "cargo": emp.get('cargo',''), "sueldo": sueldo,
                        "bonificacion": int(bono), "tipo_bono": tipo_bono, "pct_comision": pct_com_val
                    })

            # Separador total rápido
            st.markdown(
                f'<div style="background:rgba(201,168,76,0.07);border:1px solid #f0c06044;border-radius:10px;'
                f'padding:10px 16px;margin:8px 0;display:flex;justify-content:space-between;align-items:center">'
                f'<span style="color:#a8b4d0;font-size:0.78rem;font-weight:700">SUBTOTALES</span>'
                f'<span style="color:#e8ecf7;font-size:0.82rem">Sueldos: <b style="color:#e8ecf7">{fmt_money(total_sueldos)}</b>'
                f' &nbsp;+&nbsp; Bonos/Comisiones: <b style="color:#10b981">{fmt_money(total_bonos)}</b>'
                f' &nbsp;=&nbsp; <b style="color:#fcd34d;font-size:1rem">{fmt_money(total_sueldos+total_bonos)}</b></span>'
                f'</div>', unsafe_allow_html=True
            )

            # Botones
            col_add1, col_add2, col_add3 = st.columns([2, 2, 2])
            with col_add1:
                if st.button("➕ Agregar empleado", key="btn_add_emp"):
                    empleados_editados.append({"nombre": "Nuevo empleado", "cargo": "", "sueldo": 0,
                                               "bonificacion": 0, "tipo_bono": "Fijo $", "pct_comision": 0.0})
                    st.session_state['empleados'] = empleados_editados
                    st.rerun()
            with col_add2:
                pass
            # Guardar nómina
            with col_add3:
                if st.button("💾 Guardar nómina", type="primary", key="btn_save_nom"):
                    st.session_state['empleados']     = empleados_editados
                    st.session_state['nomina_total']  = total_sueldos + total_bonos
                    st.success(f"✅ Nómina guardada — Total: {fmt_money(total_sueldos + total_bonos)}")

            nomina_mes = total_sueldos + total_bonos

            # ── Tabla resumen nómina ──
            st.markdown("<br>", unsafe_allow_html=True)
            hdr_n = "background:#161525;padding:10px 14px;font-size:0.7rem;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;color:#a8b4d0;border-bottom:2px solid #1e2337"
            td_n  = "padding:11px 14px;font-size:0.83rem;border-bottom:1px solid #161929"
            tabla_nom = (
                f'<div style="overflow-x:auto;border-radius:12px;border:1px solid #2e2558;margin-bottom:20px">'
                f'<table style="width:100%;border-collapse:collapse;background:#13102a;font-family:DM Sans,sans-serif">'
                f'<thead><tr>'
                f'<th style="{hdr_n};text-align:left">Colaborador</th>'
                f'<th style="{hdr_n};text-align:right">Sueldo Base</th>'
                f'<th style="{hdr_n};text-align:right">Bonificación</th>'
                f'<th style="{hdr_n};text-align:right">Total Mes</th>'
                f'<th style="{hdr_n};text-align:right">% de Nómina</th>'
                f'</tr></thead><tbody>'
            )
            for emp in empleados_editados:
                total_e = emp['sueldo'] + emp['bonificacion']
                pct_e   = total_e / nomina_mes * 100 if nomina_mes else 0
                tabla_nom += (
                    f'<tr style="background:rgba(255,255,255,0.01)">'
                    f'<td style="{td_n};color:#c8d0e8;font-weight:600">{emp["nombre"]}</td>'
                    f'<td style="{td_n};text-align:right;color:#e8ecf7">{fmt_money(emp["sueldo"])}</td>'
                    f'<td style="{td_n};text-align:right;color:#10b981">{fmt_money(emp["bonificacion"])}</td>'
                    f'<td style="{td_n};text-align:right;color:#fcd34d;font-weight:700">{fmt_money(total_e)}</td>'
                    f'<td style="{td_n};text-align:right;color:#a8b4d0">{pct_e:.1f}%</td>'
                    f'</tr>'
                )
            # Total
            tabla_nom += (
                f'<tr style="background:rgba(201,168,76,0.06);border-top:2px solid #f0c060">'
                f'<td style="{td_n};color:#fcd34d;font-weight:800">TOTAL NÓMINA</td>'
                f'<td style="{td_n};text-align:right;color:#fcd34d;font-weight:800">{fmt_money(total_sueldos)}</td>'
                f'<td style="{td_n};text-align:right;color:#10b981;font-weight:800">{fmt_money(total_bonos)}</td>'
                f'<td style="{td_n};text-align:right;color:#fcd34d;font-weight:800">{fmt_money(nomina_mes)}</td>'
                f'<td style="{td_n};text-align:right;color:#fcd34d;font-weight:800">100%</td>'
                f'</tr>'
                f'</tbody></table></div>'
            )
            st.markdown(tabla_nom, unsafe_allow_html=True)

            # ══════════════════════════════════════════════════
            # 🎯 PROYECCIÓN — ¿Cuánto debo vender para cubrir la nómina?
            # ══════════════════════════════════════════════════
            st.markdown('<div class="seccion-titulo" style="font-size:1rem;margin-top:8px">🎯 Proyección — ¿Cuánto debo vender para cubrir esta nómina?</div>', unsafe_allow_html=True)

            if nomina_mes > 0:
                margen_unit = ganancia_dropi / n_ent if n_ent else 0
                pedidos_necesarios = int(nomina_mes / margen_unit) if margen_unit > 0 else 0
                ventas_necesarias  = pedidos_necesarios * ticket_prom
                pct_nom_vs_util    = nomina_mes / ganancia_dropi * 100 if ganancia_dropi else 0

                # Ritmo actual del mes
                from datetime import date
                dias_mes_actual = 30
                dias_transcurridos = min(date.today().day, dias_mes_actual)
                ritmo_diario_ent = n_ent / dias_transcurridos if dias_transcurridos else 0
                dias_para_cubrir = pedidos_necesarios / ritmo_diario_ent if ritmo_diario_ent else 0

                # KPIs de proyección — los 4 que pidió
                pk1, pk2, pk3, pk4 = st.columns(4)
                with pk1:
                    st.markdown(kpi("gold", "💰 Nómina del Mes", fmt_money(nomina_mes),
                                    f"Sueldos: {fmt_money(total_sueldos)} + Bonos: {fmt_money(total_bonos)}"), unsafe_allow_html=True)
                with pk2:
                    color_ped = "green" if n_ent >= pedidos_necesarios else "red"
                    faltantes = max(0, pedidos_necesarios - n_ent)
                    st.markdown(kpi(color_ped, "📦 Pedidos Necesarios", f"{pedidos_necesarios:,}",
                                    f"✅ {n_ent:,} entregados · Faltan {faltantes:,}"), unsafe_allow_html=True)
                with pk3:
                    color_vnt = "green" if ingresos >= ventas_necesarias else "red"
                    st.markdown(kpi(color_vnt, "💵 Ventas Necesarias", fmt_money(ventas_necesarias),
                                    f"Actuales: {fmt_money(ingresos)}"), unsafe_allow_html=True)
                with pk4:
                    color_nom = "green" if pct_nom_vs_util <= 30 else "gold" if pct_nom_vs_util <= 60 else "red"
                    st.markdown(kpi(color_nom, "📊 Nómina vs Utilidad",
                                    f"{pct_nom_vs_util:.1f}%", "% de la ganancia bruta"), unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # ── KPI Días del mes ──
                dias_restantes_mes = max(0, dias_mes_actual - dias_transcurridos)
                pedidos_restantes  = max(0, pedidos_necesarios - n_ent)
                dias_necesarios    = round(pedidos_restantes / ritmo_diario_ent, 1) if ritmo_diario_ent else 0
                va_a_cubrir        = dias_necesarios <= dias_restantes_mes

                color_dias = "#10b981" if va_a_cubrir else "#ef4444"
                icono_dias = "✅" if va_a_cubrir else "🔴"
                msg_dias   = (f"Al ritmo actual ({ritmo_diario_ent:.1f} ped/día), "
                              f"{'cubrirás la nómina en' if va_a_cubrir else 'necesitarás'} "
                              f"{dias_necesarios} días — "
                              f"{'quedan' if va_a_cubrir else 'pero solo quedan'} {dias_restantes_mes} días del mes")

                st.markdown(
                    f'<div style="background:rgba({("52,211,153" if va_a_cubrir else "239,68,68")},0.07);'
                    f'border:1px solid {color_dias}44;border-radius:12px;padding:14px 20px;'
                    f'display:flex;align-items:center;gap:16px;margin-bottom:16px">'
                    f'<div style="font-size:1.8rem">{icono_dias}</div>'
                    f'<div>'
                    f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:{color_dias};font-size:0.9rem">Proyección de días</div>'
                    f'<div style="color:#a8b4d0;font-size:0.8rem;margin-top:3px">{msg_dias}</div>'
                    f'</div>'
                    f'<div style="margin-left:auto;text-align:right">'
                    f'<div style="font-size:1.6rem;font-weight:800;color:{color_dias};font-family:Plus Jakarta Sans,sans-serif">{dias_necesarios}d</div>'
                    f'<div style="font-size:0.7rem;color:#7a8aaa">necesarios</div>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # Barra de progreso visual
                pct_avance = min(n_ent / pedidos_necesarios * 100, 100) if pedidos_necesarios else 0
                color_barra = "#10b981" if pct_avance >= 100 else "#f59e0b" if pct_avance >= 60 else "#ef4444"
                icono_estado = "✅" if pct_avance >= 100 else "⚠️" if pct_avance >= 60 else "🔴"
                estado_txt = "NÓMINA CUBIERTA" if pct_avance >= 100 else f"Faltan {pedidos_necesarios - n_ent:,} pedidos para cubrir nómina"

                st.markdown(
                    f'<div style="background:#13102a;border:1px solid #2e2558;border-radius:14px;padding:20px;margin-bottom:16px">'
                    f'<div style="display:flex;justify-content:space-between;margin-bottom:10px">'
                    f'<span style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.9rem">'
                    f'{icono_estado} {estado_txt}</span>'
                    f'<span style="color:{color_barra};font-weight:800;font-size:1rem">{pct_avance:.1f}%</span>'
                    f'</div>'
                    f'<div style="background:#1e2337;border-radius:100px;height:14px;overflow:hidden">'
                    f'<div style="background:linear-gradient(90deg,{color_barra},{color_barra}cc);'
                    f'width:{pct_avance:.1f}%;height:100%;border-radius:100px;'
                    f'transition:width 0.5s ease"></div>'
                    f'</div>'
                    f'<div style="display:flex;justify-content:space-between;margin-top:8px;font-size:0.75rem;color:#7a8aaa">'
                    f'<span>{n_ent:,} entregados</span>'
                    f'<span>Meta: {pedidos_necesarios:,} pedidos</span>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # Desglose por empleado — cuántos pedidos cubre cada uno
                if margen_unit > 0:
                    st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#a8b4d0;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px">Pedidos necesarios para cubrir el sueldo de cada colaborador</div>', unsafe_allow_html=True)
                    for emp in empleados_editados:
                        total_e   = emp['sueldo'] + emp['bonificacion']
                        if total_e == 0: continue
                        peds_e    = int(total_e / margen_unit) + 1
                        pct_e_av  = min(n_ent / peds_e * 100, 100) if peds_e else 0
                        c_e       = "#10b981" if pct_e_av >= 100 else "#f59e0b" if pct_e_av >= 60 else "#ef4444"
                        check     = "✅" if pct_e_av >= 100 else "🔄"
                        st.markdown(
                            f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;'
                            f'background:#13102a;border-radius:10px;padding:10px 14px;border:1px solid #2e2558">'
                            f'<div style="min-width:22px">{check}</div>'
                            f'<div style="flex:1">'
                            f'<div style="font-size:0.82rem;color:#c8d0e8;font-weight:600">{emp["nombre"]}</div>'
                            f'<div style="background:#1e2337;border-radius:100px;height:8px;margin-top:5px;overflow:hidden">'
                            f'<div style="background:{c_e};width:{pct_e_av:.0f}%;height:100%;border-radius:100px"></div>'
                            f'</div></div>'
                            f'<div style="text-align:right;min-width:90px">'
                            f'<div style="color:#fcd34d;font-weight:700;font-size:0.82rem">{fmt_money(total_e)}</div>'
                            f'<div style="color:#7a8aaa;font-size:0.7rem">{peds_e:,} pedidos</div>'
                            f'</div></div>',
                            unsafe_allow_html=True
                        )

                # Costos fijos adicionales
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.88rem;margin-bottom:10px">🏢 Costos Fijos Adicionales (mensual)</div>', unsafe_allow_html=True)
                cf_items = st.session_state.get('costos_fijos', {
                    "Arriendo/Oficina": 0, "Plataformas y Software": 0,
                    "Servicios públicos": 0, "Otros": 0
                })
                cf_cols = st.columns(4)
                cf_nuevo = {}
                for idx, (k, v) in enumerate(cf_items.items()):
                    with cf_cols[idx % 4]:
                        cf_nuevo[k] = st.number_input(k, value=int(v), step=50000, min_value=0, key=f"cf_{k}")
                if st.button("💾 Guardar costos fijos", key="btn_cf"):
                    st.session_state['costos_fijos'] = cf_nuevo
                    st.success("✅ Costos fijos guardados")

            else:
                st.info("⬆️ Ingresa los sueldos arriba y presiona **Guardar nómina** para ver la proyección.")

        # ══════════════════════════════════════════════════════
        # 📊 ESTADO DE RESULTADOS
        # ══════════════════════════════════════════════════════
        elif "Estado de Resultados" in fin_nav:
            st.markdown('<div class="seccion-titulo">📊 Estado de Resultados (P&L)</div>', unsafe_allow_html=True)

            def fila_pl(concepto, valor, nivel=0, destacada=False, es_gasto=False):
                indent = "&nbsp;" * (nivel * 6)
                color  = "#ef4444" if es_gasto and valor > 0 else "#10b981" if valor > 0 else "#ef4444"
                bg     = "rgba(201,168,76,0.07)" if destacada else "transparent"
                bold   = "font-weight:800;" if destacada else ""
                signo  = "-" if es_gasto and valor > 0 else ""
                return (
                    f'<tr style="background:{bg}">'
                    f'<td style="padding:9px 16px;color:#c8d0e8;font-size:0.83rem;{bold}">{indent}{concepto}</td>'
                    f'<td style="padding:9px 16px;text-align:right;color:{color};font-size:0.83rem;{bold}">{signo}{fmt_money(valor)}</td>'
                    f'<td style="padding:9px 16px;text-align:right;color:#7a8aaa;font-size:0.75rem">'
                    f'{"" if ingresos == 0 else f"{valor/ingresos*100:.1f}%"}</td>'
                    f'</tr>'
                )

            pl_html = (
                f'<div style="overflow-x:auto;border-radius:14px;border:1px solid #2e2558">'
                f'<table style="width:100%;border-collapse:collapse;background:#13102a;font-family:DM Sans,sans-serif">'
                f'<thead><tr>'
                f'<th style="padding:12px 16px;text-align:left;color:#a8b4d0;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.07em;border-bottom:2px solid #1e2337">Concepto</th>'
                f'<th style="padding:12px 16px;text-align:right;color:#a8b4d0;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.07em;border-bottom:2px solid #1e2337">Valor</th>'
                f'<th style="padding:12px 16px;text-align:right;color:#a8b4d0;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.07em;border-bottom:2px solid #1e2337">% Ingreso</th>'
                f'</tr></thead><tbody>'
                + fila_pl("(+) INGRESOS — Pedidos Entregados", ingresos, destacada=True)
                + fila_pl("Costo de Productos Vendidos", costo_prod, nivel=1, es_gasto=True)
                + fila_pl("UTILIDAD BRUTA", utilidad_bruta, destacada=True)
                + '<tr><td colspan="3" style="padding:4px 16px;background:#161525"><span style="font-size:0.68rem;color:#7a8aaa;text-transform:uppercase;letter-spacing:0.06em">Gastos Operativos</span></td></tr>'
                + fila_pl("Flete de Entrega", flete_ent, nivel=1, es_gasto=True)
                + fila_pl("Flete de Devolución", flete_dev, nivel=1, es_gasto=True)
                + fila_pl("Pauta Publicitaria", pauta_fin, nivel=1, es_gasto=True)
                + fila_pl("Nómina", nomina_total, nivel=1, es_gasto=True)
                + fila_pl("Costos Fijos Adicionales", sum(costos_fijos.values()), nivel=1, es_gasto=True)
                + fila_pl("UTILIDAD OPERATIVA (EBITDA)", utilidad_op, destacada=True)
                + fila_pl("Impuesto Estimado (8%)", impuesto_est, nivel=1, es_gasto=True)
                + fila_pl("UTILIDAD NETA", utilidad_neta, destacada=True)
                + '</tbody></table></div>'
            )
            st.markdown(pl_html, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            r1,r2,r3,r4 = st.columns(4)
            with r1: st.markdown(kpi("cyan","💰 Ingresos",fmt_money(ingresos)), unsafe_allow_html=True)
            with r2: st.markdown(kpi("green","✅ Utilidad Bruta",fmt_money(utilidad_bruta),f"{margen_bruto_pct:.1f}% margen"), unsafe_allow_html=True)
            with r3: st.markdown(kpi("gold","📊 EBITDA",fmt_money(utilidad_op)), unsafe_allow_html=True)
            with r4:
                col_n = "green" if utilidad_neta > 0 else "red"
                st.markdown(kpi(col_n,"💵 Utilidad Neta",fmt_money(utilidad_neta),f"{margen_neto_pct:.1f}% margen"), unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════
        # ⚖️ PUNTO DE EQUILIBRIO
        # ══════════════════════════════════════════════════════
        elif "Equilibrio" in fin_nav:
            st.markdown('<div class="seccion-titulo">⚖️ Punto de Equilibrio</div>', unsafe_allow_html=True)

            margen_contrib = ganancia_dropi / n_ent if n_ent else 0
            pe_unidades    = int(cf_total / margen_contrib) if margen_contrib else 0
            pe_pesos       = pe_unidades * ticket_prom
            superavit      = n_ent - pe_unidades

            k1,k2,k3,k4 = st.columns(4)
            with k1: st.markdown(kpi("blue","🔧 Costos Fijos Total",fmt_money(cf_total)), unsafe_allow_html=True)
            with k2: st.markdown(kpi("gold","💡 Margen Contrib./Pedido",fmt_money(margen_contrib)), unsafe_allow_html=True)
            with k3: st.markdown(kpi("purple","⚖️ PE en Pedidos",f"{pe_unidades:,}",f"= {fmt_money(pe_pesos)}"), unsafe_allow_html=True)
            with k4:
                col_pe = "green" if superavit >= 0 else "red"
                txt_pe = f"+{superavit:,} sobre PE" if superavit >= 0 else f"{superavit:,} bajo PE"
                st.markdown(kpi(col_pe,"📦 Entregados vs PE",f"{n_ent:,}",txt_pe), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            pct_pe = min(n_ent / pe_unidades * 100, 150) if pe_unidades else 0
            color_pe = "#10b981" if pct_pe >= 100 else "#f59e0b" if pct_pe >= 70 else "#ef4444"
            st.markdown(
                f'<div style="background:#13102a;border:1px solid #2e2558;border-radius:14px;padding:24px">'
                f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;margin-bottom:14px;font-size:0.95rem">'
                f'{"✅ Por encima del punto de equilibrio" if superavit>=0 else "🔴 Por debajo del punto de equilibrio"}</div>'
                f'<div style="background:#1e2337;border-radius:100px;height:20px;overflow:hidden">'
                f'<div style="background:linear-gradient(90deg,{color_pe},{color_pe}bb);width:{min(pct_pe,100):.1f}%;height:100%;border-radius:100px"></div>'
                f'</div>'
                f'<div style="display:flex;justify-content:space-between;margin-top:10px;font-size:0.76rem;color:#7a8aaa">'
                f'<span>0 pedidos</span>'
                f'<span style="color:{color_pe};font-weight:700">PE: {pe_unidades:,} pedidos</span>'
                f'<span>{n_ent:,} entregados ({pct_pe:.0f}%)</span>'
                f'</div></div>',
                unsafe_allow_html=True
            )

        # ══════════════════════════════════════════════════════
        # 📈 RENTABILIDAD
        # ══════════════════════════════════════════════════════
        elif "Rentabilidad" in fin_nav:
            st.markdown('<div class="seccion-titulo">📈 Rentabilidad</div>', unsafe_allow_html=True)
            roi_pauta = (ganancia_dropi - pauta_fin) / pauta_fin * 100 if pauta_fin else 0
            cac       = pauta_fin / n_ent if n_ent else 0

            k1,k2,k3,k4 = st.columns(4)
            with k1: st.markdown(kpi("green","📈 Margen Bruto",f"{margen_bruto_pct:.1f}%"), unsafe_allow_html=True)
            with k2: st.markdown(kpi("gold" if margen_neto_pct>0 else "red","💵 Margen Neto",f"{margen_neto_pct:.1f}%"), unsafe_allow_html=True)
            with k3: st.markdown(kpi("cyan","🎯 ROI Pauta",f"{roi_pauta:.1f}%","Por cada $ invertido"), unsafe_allow_html=True)
            with k4: st.markdown(kpi("purple","👤 CAC",fmt_money(cac),"Costo adquisición cliente"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            g1, g2 = st.columns(2)

            with g1:
                if C_PRODUCTO in df_ent.columns and C_GANANCIA in df_ent.columns:
                    rent_prod = df_ent.groupby(C_PRODUCTO)[C_GANANCIA].sum().sort_values(ascending=True).tail(12)
                    fig_rp = go.Figure(go.Bar(
                        x=rent_prod.values, y=rent_prod.index.str[:25], orientation='h',
                        marker_color=['#10b981' if v>0 else '#ef4444' for v in rent_prod.values]
                    ))
                    fig_rp.update_layout(**PLOT_LAYOUT, height=400, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE,
                                         title='Rentabilidad por Producto (Ganancia)')
                    st.plotly_chart(fig_rp, use_container_width=True)

            with g2:
                if C_CIUDAD in df_ent.columns and C_GANANCIA in df_ent.columns:
                    rent_ciudad = df_ent.groupby(C_CIUDAD)[C_GANANCIA].sum().sort_values(ascending=True).tail(12)
                    fig_rc = go.Figure(go.Bar(
                        x=rent_ciudad.values, y=rent_ciudad.index.str[:20], orientation='h',
                        marker_color=['#10b981' if v>0 else '#ef4444' for v in rent_ciudad.values]
                    ))
                    fig_rc.update_layout(**PLOT_LAYOUT, height=400, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE,
                                         title='Rentabilidad por Ciudad')
                    st.plotly_chart(fig_rc, use_container_width=True)

        # ══════════════════════════════════════════════════════
        # 📉 ANÁLISIS DE COSTOS
        # ══════════════════════════════════════════════════════
        elif "Flujo de Caja" in fin_nav:
            st.markdown('<div class="seccion-titulo">💧 Flujo de Caja del Período</div>', unsafe_allow_html=True)

            # ── Calcular valores ──
            costo_cancel_fc = df_fin[mask_can][C_FLETE].sum() if C_FLETE in df_fin.columns else 0
            costo_dev_fc    = flete_dev
            cartera_transito= df_fin[~mask_ent & ~mask_can & ~mask_dev][C_TOTAL].sum() if C_TOTAL in df_fin.columns else 0
            entradas_total  = ingresos
            salidas_prod    = costo_prod
            salidas_flete   = flete_ent + flete_dev
            salidas_pauta   = pauta_fin
            salidas_nomina  = nomina_total
            salidas_fijos   = sum(costos_fijos.values())
            salidas_total   = salidas_prod + salidas_flete + salidas_pauta + salidas_nomina + salidas_fijos
            saldo_disp      = entradas_total - salidas_total

            # ── KPIs principales ──
            fc1, fc2, fc3, fc4 = st.columns(4)
            with fc1: st.markdown(kpi("green","💰 Entradas Totales",fmt_money(entradas_total),"Pedidos entregados"), unsafe_allow_html=True)
            with fc2: st.markdown(kpi("red","💸 Salidas Totales",fmt_money(salidas_total),"Todos los costos"), unsafe_allow_html=True)
            with fc3:
                col_sd = "green" if saldo_disp >= 0 else "red"
                st.markdown(kpi(col_sd,"🏦 Saldo Disponible",fmt_money(saldo_disp),"Entradas - Salidas"), unsafe_allow_html=True)
            with fc4: st.markdown(kpi("gold","📦 Cartera en Tránsito",fmt_money(cartera_transito),"Pedidos aún no entregados"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Tabla flujo detallada ──
            hdr_fc = "background:#161525;padding:11px 16px;font-size:0.68rem;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;color:#a8b4d0;border-bottom:2px solid #1e2337"
            td_fc  = "padding:11px 16px;font-size:0.83rem;border-bottom:1px solid #161929"

            def fila_fc(concepto, valor, tipo, icono, sub=""):
                color = "#10b981" if tipo == "entrada" else "#ef4444"
                signo = "+" if tipo == "entrada" else "-"
                bg    = "rgba(16,185,129,0.04)" if tipo=="entrada" else "rgba(239,68,68,0.04)"
                sub_html = f'<div style="font-size:0.7rem;color:#7a8aaa;margin-top:2px">{sub}</div>' if sub else ""
                return (
                    f'<tr style="background:{bg}">'
                    f'<td style="{td_fc};color:#c8d0e8">{icono} {concepto}{sub_html}</td>'
                    f'<td style="{td_fc};text-align:center;font-size:0.75rem;color:#a8b4d0">'
                    f'<span style="background:{"#10b98120" if tipo=="entrada" else "#ef444420"};'
                    f'color:{color};padding:2px 8px;border-radius:20px;font-weight:700">'
                    f'{"ENTRADA" if tipo=="entrada" else "SALIDA"}</span></td>'
                    f'<td style="{td_fc};text-align:right;color:{color};font-weight:700;font-size:0.9rem">'
                    f'{signo}{fmt_money(abs(valor))}</td>'
                    f'<td style="{td_fc};text-align:right;color:#7a8aaa;font-size:0.75rem">'
                    f'{"" if entradas_total==0 else f"{abs(valor)/entradas_total*100:.1f}% de ingresos"}</td>'
                    f'</tr>'
                )

            tabla_fc = (
                f'<div style="overflow-x:auto;border-radius:14px;border:1px solid #2e2558;margin-bottom:20px">'
                f'<table style="width:100%;border-collapse:collapse;background:#13102a;font-family:DM Sans,sans-serif">'
                f'<thead><tr>'
                f'<th style="{hdr_fc};text-align:left;min-width:220px">Concepto</th>'
                f'<th style="{hdr_fc};text-align:center">Tipo</th>'
                f'<th style="{hdr_fc};text-align:right">Valor</th>'
                f'<th style="{hdr_fc};text-align:right">% Ingreso</th>'
                f'</tr></thead><tbody>'
                + '<tr><td colspan="4" style="padding:6px 16px;background:#161525"><span style="font-size:0.68rem;color:#10b981;text-transform:uppercase;font-weight:800;letter-spacing:0.06em">▼ ENTRADAS</span></td></tr>'
                + fila_fc("Pagos recibidos — Pedidos Entregados", ingresos, "entrada", "💳", f"{n_ent:,} pedidos × {fmt_money(ticket_prom)} ticket prom.")
                + '<tr><td colspan="4" style="padding:6px 16px;background:#161525"><span style="font-size:0.68rem;color:#ef4444;text-transform:uppercase;font-weight:800;letter-spacing:0.06em">▼ SALIDAS</span></td></tr>'
                + fila_fc("Costo de Productos Vendidos", salidas_prod, "salida", "📦", f"Costo unitario × {n_ent:,} unds")
                + fila_fc("Fletes de Entrega", flete_ent, "salida", "🚚", f"{n_ent:,} pedidos entregados")
                + fila_fc("Fletes de Devolución", flete_dev, "salida", "↩️", f"{n_dev:,} devoluciones")
                + fila_fc("Pauta Publicitaria", pauta_fin, "salida", "📣", "Inversión en ads")
                + fila_fc("Nómina", nomina_total, "salida", "👥", f"{len(st.session_state.get('empleados',[]))} colaboradores")
                + fila_fc("Costos Fijos Adicionales", salidas_fijos, "salida", "🏢", "Arriendo, software, servicios")
            )

            # Fila saldo final
            color_sf = "#10b981" if saldo_disp >= 0 else "#ef4444"
            bg_sf    = "rgba(16,185,129,0.08)" if saldo_disp >= 0 else "rgba(239,68,68,0.08)"
            tabla_fc += (
                f'<tr style="background:{bg_sf};border-top:2px solid {color_sf}">'
                f'<td style="{td_fc};color:{color_sf};font-weight:800;font-size:0.9rem">🏦 SALDO NETO DEL PERÍODO</td>'
                f'<td></td>'
                f'<td style="{td_fc};text-align:right;color:{color_sf};font-weight:800;font-size:1rem">{fmt_money(saldo_disp)}</td>'
                f'<td style="{td_fc};text-align:right;color:{color_sf};font-size:0.8rem">{saldo_disp/entradas_total*100:.1f}% de ingresos</td>'
                f'</tr>'
                f'<tr style="background:rgba(201,168,76,0.06);border-top:1px dashed #f0c06044">'
                f'<td style="{td_fc};color:#fcd34d;font-weight:700">📦 Cartera en Tránsito (pedidos en proceso)</td>'
                f'<td></td>'
                f'<td style="{td_fc};text-align:right;color:#fcd34d;font-weight:700">{fmt_money(cartera_transito)}</td>'
                f'<td style="{td_fc};text-align:right;color:#7a8aaa;font-size:0.75rem">Capital inmovilizado</td>'
                f'</tr>'
                f'</tbody></table></div>'
            )
            st.markdown(tabla_fc, unsafe_allow_html=True)

            # ── Gráfica waterfall entradas vs salidas ──
            cats_wf = ["Ingresos","Productos","Fletes","Pauta","Nómina","Fijos","Saldo Neto"]
            vals_wf = [entradas_total, -salidas_prod, -salidas_flete, -salidas_pauta, -salidas_nomina, -salidas_fijos, saldo_disp]
            medidas = ["absolute","relative","relative","relative","relative","relative","total"]
            colores_wf = ["#10b981","#ef4444","#f59e0b","#00d4ff","#7c3aed","#5b6cfc",
                          "#10b981" if saldo_disp >= 0 else "#ef4444"]

            fig_wf = go.Figure(go.Waterfall(
                name="Flujo", orientation="v", measure=medidas,
                x=cats_wf, y=vals_wf,
                connector={"line":{"color":"#1e2337","width":1}},
                increasing={"marker":{"color":"#10b981"}},
                decreasing={"marker":{"color":"#ef4444"}},
                totals={"marker":{"color": "#10b981" if saldo_disp >= 0 else "#ef4444"}},
                text=[fmt_money(abs(v)) for v in vals_wf],
                textposition="outside"
            ))
            fig_wf.update_layout(**PLOT_LAYOUT, height=420,
                                  title="Cascada de Flujo de Caja",
                                  yaxis={**AXIS_STYLE, "tickprefix":"$"})
            st.plotly_chart(fig_wf, use_container_width=True)

            # ══════════════════════════════════════════════════════
            # 🌊 RÍO DEL DINERO — dentro de Flujo de Caja
            # ══════════════════════════════════════════════════════
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.92rem;margin-bottom:12px">🌊 El Río del Dinero — Flujo Visual</div>', unsafe_allow_html=True)
            _rio_ventas   = ingresos
            _rio_cprod    = costo_prod
            _rio_fent     = flete_ent
            _rio_fdev     = flete_dev
            _rio_pauta    = pauta_fin
            _rio_nom      = nomina_total
            _rio_transito = df_fin[~df_fin[C_ESTATUS].astype(str).str.upper().str.contains('ENTREGAD|CANCELAD|DEVOLUCI',na=False)][C_TOTAL].sum() if C_TOTAL in df_fin.columns and C_ESTATUS in df_fin.columns else 0
            _rio_tuyo     = _rio_ventas - _rio_cprod - _rio_fent - _rio_fdev - _rio_pauta - _rio_nom
            _bloques_rio  = [
                ("💳 Ventas",        _rio_ventas,  "#5b6cfc","Total facturado"),
                ("📦 Costo Prod.",   -_rio_cprod,  "#ef4444","Pago al proveedor"),
                ("🚚 Flete Entrega", -_rio_fent,   "#f59e0b","Envíos exitosos"),
                ("↩️ Flete Dev.",    -_rio_fdev,   "#ef4444","Pérdida devoluciones"),
                ("📣 Pauta",         -_rio_pauta,  "#7c3aed","Inversión marketing"),
                ("👥 Nómina",        -_rio_nom,    "#ec4899","Equipo"),
                ("⏳ En Tránsito",    _rio_transito,"#00d4ff","Pedidos activos"),
                ("✅ Es Tuyo",       _rio_tuyo,    "#10b981","Ganancia neta"),
            ]
            _max_rio = max(abs(b[1]) for b in _bloques_rio if b[1] != 0) or 1
            _rio_html = '<div style="display:flex;gap:8px;overflow-x:auto;padding-bottom:12px">'
            for _nm, _vl, _cl, _ds in _bloques_rio:
                _alt = max(40, int(abs(_vl) / _max_rio * 140))
                _sg  = "+" if _vl >= 0 else "-"
                _rio_html += (
                    f'<div style="flex:1;min-width:90px;display:flex;flex-direction:column;align-items:center;gap:5px">'
                    f'<div style="font-size:0.65rem;color:#a8b4d0;text-align:center;font-weight:700;'
                    f'text-transform:uppercase;letter-spacing:0.03em;line-height:1.3">{_nm}</div>'
                    f'<div style="width:100%;height:{_alt}px;background:{_cl}22;'
                    f'border:1.5px solid {_cl};border-radius:10px;'
                    f'display:flex;align-items:center;justify-content:center">'
                    f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:{_cl};font-size:0.72rem">'
                    f'{_sg}{fmt_money(abs(_vl))}</div></div>'
                    f'<div style="font-size:0.6rem;color:#7a8aaa;text-align:center;line-height:1.2">{_ds}</div>'
                    f'</div>'
                )
            _rio_html += '</div>'
            st.markdown(_rio_html, unsafe_allow_html=True)
            st.markdown("<hr style='border-color:#1e2337;margin:14px 0'>", unsafe_allow_html=True)

        elif "Costos" in fin_nav:
            st.markdown('<div class="seccion-titulo">📉 Análisis de Costos</div>', unsafe_allow_html=True)

            costo_x_ped   = (costo_prod + flete_ent) / n_ent if n_ent else 0
            costo_dev_u   = flete_dev / n_dev if n_dev else 0
            pauta_x_ped   = pauta_fin / n_ent if n_ent else 0
            costo_cancel  = df_fin[mask_can][C_FLETE].sum() if C_FLETE in df_fin.columns else 0
            cf_total_cos  = sum(costos_fijos.values())

            # Datos de cada rubro
            rubros = [
                {"nombre":"Productos Vendidos",    "valor":costo_prod,    "icono":"📦","color":"#5b6cfc","x_ped": costo_prod/n_ent if n_ent else 0},
                {"nombre":"Flete de Entrega",      "valor":flete_ent,     "icono":"🚚","color":"#00d4ff","x_ped": flete_ent/n_ent  if n_ent else 0},
                {"nombre":"Flete de Devolución",   "valor":flete_dev,     "icono":"↩️","color":"#f59e0b","x_ped": flete_dev/n_dev  if n_dev else 0},
                {"nombre":"Pauta Publicitaria",    "valor":pauta_fin,     "icono":"📣","color":"#7c3aed","x_ped": pauta_fin/n_ent  if n_ent else 0},
                {"nombre":"Nómina",                "valor":nomina_total,  "icono":"👥","color":"#ec4899","x_ped": nomina_total/n_ent if n_ent else 0},
                {"nombre":"Costos Fijos",          "valor":cf_total_cos,  "icono":"🏢","color":"#84cc16","x_ped": cf_total_cos/n_ent if n_ent else 0},
                {"nombre":"Cancelaciones (flete)", "valor":costo_cancel,  "icono":"❌","color":"#ef4444","x_ped": costo_cancel/n_can if n_can else 0},
            ]
            rubros = [r for r in rubros if r["valor"] > 0]
            total_costos = sum(r["valor"] for r in rubros)

            # ── Tarjetas grandes por rubro ──
            cols_r = st.columns(len(rubros)) if len(rubros) <= 4 else st.columns(4)
            for idx, r in enumerate(rubros):
                pct_r = r["valor"] / total_costos * 100 if total_costos else 0
                pct_ing = r["valor"] / ingresos * 100 if ingresos else 0
                with cols_r[idx % 4]:
                    st.markdown(
                        f'<div style="background:#13102a;border:1px solid {r["color"]}44;border-radius:14px;'
                        f'padding:16px;margin-bottom:12px;border-top:3px solid {r["color"]}">'
                        f'<div style="font-size:1.4rem;margin-bottom:6px">{r["icono"]}</div>'
                        f'<div style="font-size:0.72rem;color:#a8b4d0;font-weight:700;text-transform:uppercase;'
                        f'letter-spacing:0.06em;margin-bottom:6px">{r["nombre"]}</div>'
                        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:{r["color"]};font-size:1.05rem">'
                        f'{fmt_money(r["valor"])}</div>'
                        f'<div style="display:flex;gap:8px;margin-top:8px">'
                        f'<span style="background:{r["color"]}18;color:{r["color"]};padding:2px 7px;'
                        f'border-radius:20px;font-size:0.68rem;font-weight:700">{pct_r:.1f}% del costo</span>'
                        f'<span style="background:#1e2337;color:#a8b4d0;padding:2px 7px;'
                        f'border-radius:20px;font-size:0.68rem">{pct_ing:.1f}% del ingreso</span>'
                        f'</div>'
                        f'<div style="margin-top:8px;font-size:0.72rem;color:#7a8aaa">'
                        f'Por pedido: <b style="color:{r["color"]}">{fmt_money(r["x_ped"])}</b>'
                        f'</div>'
                        f'<div style="background:#1e2337;border-radius:100px;height:5px;margin-top:10px;overflow:hidden">'
                        f'<div style="background:{r["color"]};width:{min(pct_r,100):.0f}%;height:100%;border-radius:100px"></div>'
                        f'</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Tabla detallada con % ──
            hdr_ct = "background:#161525;padding:10px 14px;font-size:0.68rem;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;color:#a8b4d0;border-bottom:2px solid #1e2337"
            td_ct  = "padding:10px 14px;font-size:0.82rem;border-bottom:1px solid #161929"
            tabla_ct = (
                f'<div style="overflow-x:auto;border-radius:14px;border:1px solid #2e2558;margin-bottom:20px">'
                f'<table style="width:100%;border-collapse:collapse;background:#13102a;font-family:DM Sans,sans-serif">'
                f'<thead><tr>'
                f'<th style="{hdr_ct};text-align:left">Rubro de Costo</th>'
                f'<th style="{hdr_ct};text-align:right">Total</th>'
                f'<th style="{hdr_ct};text-align:right">% del Costo Total</th>'
                f'<th style="{hdr_ct};text-align:right">% sobre Ingresos</th>'
                f'<th style="{hdr_ct};text-align:right">Costo por Pedido</th>'
                f'</tr></thead><tbody>'
            )
            for r in rubros:
                pct_r   = r["valor"] / total_costos * 100 if total_costos else 0
                pct_ing = r["valor"] / ingresos * 100 if ingresos else 0
                bar_w   = min(pct_r, 100)
                tabla_ct += (
                    f'<tr style="background:rgba(255,255,255,0.01)">'
                    f'<td style="{td_ct};color:#c8d0e8;font-weight:600">{r["icono"]} {r["nombre"]}</td>'
                    f'<td style="{td_ct};text-align:right;color:{r["color"]};font-weight:700">{fmt_money(r["valor"])}</td>'
                    f'<td style="{td_ct};text-align:right">'
                    f'<div style="display:flex;align-items:center;gap:8px;justify-content:flex-end">'
                    f'<div style="background:#1e2337;border-radius:100px;height:6px;width:80px;overflow:hidden">'
                    f'<div style="background:{r["color"]};width:{bar_w:.0f}%;height:100%;border-radius:100px"></div>'
                    f'</div>'
                    f'<span style="color:{r["color"]};font-weight:700;min-width:40px">{pct_r:.1f}%</span>'
                    f'</div></td>'
                    f'<td style="{td_ct};text-align:right;color:#a8b4d0">{pct_ing:.1f}%</td>'
                    f'<td style="{td_ct};text-align:right;color:#e8ecf7">{fmt_money(r["x_ped"])}</td>'
                    f'</tr>'
                )
            tabla_ct += (
                f'<tr style="background:rgba(201,168,76,0.07);border-top:2px solid #f0c060">'
                f'<td style="{td_ct};color:#fcd34d;font-weight:800">TOTAL COSTOS</td>'
                f'<td style="{td_ct};text-align:right;color:#fcd34d;font-weight:800">{fmt_money(total_costos)}</td>'
                f'<td style="{td_ct};text-align:right;color:#fcd34d;font-weight:800">100%</td>'
                f'<td style="{td_ct};text-align:right;color:#fcd34d;font-weight:800">'
                f'{total_costos/ingresos*100:.1f}%</td>'
                f'<td style="{td_ct};text-align:right;color:#fcd34d;font-weight:800">'
                f'{fmt_money(total_costos/n_ent if n_ent else 0)}</td>'
                f'</tr>'
                f'</tbody></table></div>'
            )
            st.markdown(tabla_ct, unsafe_allow_html=True)

            # ── Gráfica cascada de costos ──
            nombres_wf = ["Ingresos"] + [r["nombre"] for r in rubros] + ["Margen Neto"]
            valores_wf = [ingresos] + [-r["valor"] for r in rubros] + [ingresos - total_costos]
            medidas_wf = ["absolute"] + ["relative"]*len(rubros) + ["total"]
            fig_cwf = go.Figure(go.Waterfall(
                orientation="v", measure=medidas_wf,
                x=nombres_wf, y=valores_wf,
                connector={"line":{"color":"#1e2337","width":1}},
                increasing={"marker":{"color":"#10b981"}},
                decreasing={"marker":{"color":"#ef4444"}},
                totals={"marker":{"color":"#f0c060"}},
                text=[fmt_money(abs(v)) for v in valores_wf],
                textposition="outside"
            ))
            fig_cwf.update_layout(**PLOT_LAYOUT, height=440,
                                   title="Cascada — Cómo los Costos Reducen el Ingreso",
                                   yaxis={**AXIS_STYLE, "tickprefix":"$"},
                                   xaxis={**AXIS_STYLE})
            st.plotly_chart(fig_cwf, use_container_width=True)

            # ── Barras comparativas mes a mes ──
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.92rem;margin-bottom:14px">📊 Comparativo de Costos por Mes</div>', unsafe_allow_html=True)

            C_CST_COMP = "PRECIO PROVEEDOR X CANTIDAD"
            if '_mes' in df.columns:
                meses_todos = sorted(df['_mes'].dropna().unique().tolist())

                # Calcular costos por mes para todos los meses disponibles
                filas_mes = []
                for m in meses_todos:
                    df_m_c = df[df['_mes'] == m]
                    mask_e_m = df_m_c[C_ESTATUS].astype(str).str.upper().str.contains('ENTREGAD',na=False) if C_ESTATUS in df_m_c.columns else pd.Series([True]*len(df_m_c))
                    mask_d_m = df_m_c[C_ESTATUS].astype(str).str.upper().str.contains('DEVOLUCI',na=False) if C_ESTATUS in df_m_c.columns else pd.Series([False]*len(df_m_c))
                    mask_c_m = df_m_c[C_ESTATUS].astype(str).str.upper().str.contains('CANCELAD',na=False) if C_ESTATUS in df_m_c.columns else pd.Series([False]*len(df_m_c))
                    df_e_m = df_m_c[mask_e_m]
                    n_e_m  = int(mask_e_m.sum())
                    filas_mes.append({
                        'Mes':       str(m),
                        'Productos': df_e_m[C_CST_COMP].sum() if C_CST_COMP in df_e_m.columns else 0,
                        'Flete Ent.':df_e_m[C_FLETE].sum()    if C_FLETE    in df_e_m.columns else 0,
                        'Flete Dev.':df_m_c[mask_d_m][C_FLETE].sum() if C_FLETE in df_m_c.columns else 0,
                        'Pauta':     sum(st.session_state.get('pauta_dict', {}).values()),
                        'Nómina':    st.session_state.get('nomina_total', 0),
                        'Ingresos':  df_e_m[C_TOTAL].sum() if C_TOTAL in df_e_m.columns else 0,
                    })

                df_mes_cos = pd.DataFrame(filas_mes)

                if len(df_mes_cos) > 1:
                    colores_barras = {
                        'Productos':  '#5b6cfc',
                        'Flete Ent.': '#00d4ff',
                        'Flete Dev.': '#f59e0b',
                        'Pauta':      '#7c3aed',
                        'Nómina':     '#ec4899',
                    }
                    fig_mes = go.Figure()
                    for rubro, color in colores_barras.items():
                        if rubro in df_mes_cos.columns and df_mes_cos[rubro].sum() > 0:
                            fig_mes.add_trace(go.Bar(
                                name=rubro,
                                x=df_mes_cos['Mes'],
                                y=df_mes_cos[rubro],
                                marker_color=color,
                                text=[fmt_money(v) for v in df_mes_cos[rubro]],
                                textposition='inside',
                                textfont={"size":10,"color":"white"},
                            ))
                    # Línea de ingresos como referencia
                    fig_mes.add_trace(go.Scatter(
                        name='Ingresos',
                        x=df_mes_cos['Mes'],
                        y=df_mes_cos['Ingresos'],
                        mode='lines+markers',
                        line={"color":"#10b981","width":2,"dash":"dot"},
                        marker={"size":7,"color":"#10b981"},
                    ))
                    fig_mes.update_layout(
                        **PLOT_LAYOUT,
                        height=420,
                        barmode='stack',
                        title='Costos Apilados vs Ingresos — Mes a Mes',
                        yaxis={**AXIS_STYLE, "tickprefix":"$"},
                        xaxis=AXIS_STYLE,
                        legend={"orientation":"h","y":-0.18,"x":0,"font":{"size":11,"color":"#8892b0"},"bgcolor":"rgba(0,0,0,0)"},
                    )
                    st.plotly_chart(fig_mes, use_container_width=True)

                    # ── Mini tabla resumen mes a mes ──
                    hdr_mm = "background:#161525;padding:9px 12px;font-size:0.67rem;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;color:#a8b4d0;border-bottom:1px solid #1e2337"
                    td_mm  = "padding:9px 12px;font-size:0.79rem;border-bottom:1px solid #161929"
                    tabla_mm = (
                        f'<div style="overflow-x:auto;border-radius:12px;border:1px solid #2e2558">'
                        f'<table style="width:100%;border-collapse:collapse;background:#13102a;font-family:DM Sans,sans-serif">'
                        f'<thead><tr>'
                        f'<th style="{hdr_mm};text-align:left">Mes</th>'
                        f'<th style="{hdr_mm};text-align:right;color:#a855f7">Productos</th>'
                        f'<th style="{hdr_mm};text-align:right;color:#22d3ee">Flete Ent.</th>'
                        f'<th style="{hdr_mm};text-align:right;color:#f59e0b">Flete Dev.</th>'
                        f'<th style="{hdr_mm};text-align:right;color:#9333ea">Pauta</th>'
                        f'<th style="{hdr_mm};text-align:right;color:#ec4899">Nómina</th>'
                        f'<th style="{hdr_mm};text-align:right;color:#ef4444">Total Costos</th>'
                        f'<th style="{hdr_mm};text-align:right;color:#10b981">Ingresos</th>'
                        f'<th style="{hdr_mm};text-align:right;color:#fcd34d">% Costo/Ingr.</th>'
                        f'</tr></thead><tbody>'
                    )
                    for _, row in df_mes_cos.iterrows():
                        total_c = row['Productos'] + row['Flete Ent.'] + row['Flete Dev.'] + row['Pauta'] + row['Nómina']
                        pct_ci  = total_c / row['Ingresos'] * 100 if row['Ingresos'] else 0
                        c_pct   = "#10b981" if pct_ci < 70 else "#f59e0b" if pct_ci < 90 else "#ef4444"
                        es_actual = row['Mes'] == mes_fin
                        bg_row  = "rgba(201,168,76,0.07)" if es_actual else "rgba(255,255,255,0.01)"
                        tabla_mm += (
                            f'<tr style="background:{bg_row}">'
                            f'<td style="{td_mm};color:{"#f0c060" if es_actual else "#c8d0e8"};font-weight:{"800" if es_actual else "400"}'
                            f'">{row["Mes"]}{"  ◀ actual" if es_actual else ""}</td>'
                            f'<td style="{td_mm};text-align:right;color:#a8b4d0">{fmt_money(row["Productos"])}</td>'
                            f'<td style="{td_mm};text-align:right;color:#a8b4d0">{fmt_money(row["Flete Ent."])}</td>'
                            f'<td style="{td_mm};text-align:right;color:#a8b4d0">{fmt_money(row["Flete Dev."])}</td>'
                            f'<td style="{td_mm};text-align:right;color:#a8b4d0">{fmt_money(row["Pauta"])}</td>'
                            f'<td style="{td_mm};text-align:right;color:#a8b4d0">{fmt_money(row["Nómina"])}</td>'
                            f'<td style="{td_mm};text-align:right;color:#ef4444;font-weight:700">{fmt_money(total_c)}</td>'
                            f'<td style="{td_mm};text-align:right;color:#10b981;font-weight:700">{fmt_money(row["Ingresos"])}</td>'
                            f'<td style="{td_mm};text-align:right;color:{c_pct};font-weight:800">{pct_ci:.1f}%</td>'
                            f'</tr>'
                        )
                    tabla_mm += '</tbody></table></div>'
                    st.markdown(tabla_mm, unsafe_allow_html=True)

                else:
                    st.info("Necesitas datos de al menos 2 meses para ver la comparativa mes a mes.")
            else:
                st.info("Sin datos de período disponibles para la comparativa.")


        # ══════════════════════════════════════════════════════
        # 🎯 KPIs FINANCIEROS
        # ══════════════════════════════════════════════════════
        elif "KPIs" in fin_nav:
            st.markdown('<div class="seccion-titulo">🎯 KPIs Financieros Clave</div>', unsafe_allow_html=True)

            tasa_conv    = n_ent / n_total * 100 if n_total else 0
            ebitda       = utilidad_op
            liquidez     = ingresos / cf_total if cf_total else 0
            roi_pauta_kp = (ganancia_dropi - pauta_fin) / pauta_fin * 100 if pauta_fin else 0

            kpis_fin = [
                ("🎫 Ticket Promedio",           fmt_money(ticket_prom),                       "Valor promedio por pedido entregado"),
                ("👤 CAC — Costo de Adquisición", fmt_money(pauta_fin/n_ent if n_ent else 0),  "Pauta ÷ pedidos entregados"),
                ("💱 Tasa Conv. Financiera",      f"{tasa_conv:.1f}%",                          "% pedidos que generan dinero real"),
                ("📊 EBITDA",                     fmt_money(ebitda),                            "Utilidad antes de impuestos"),
                ("💧 Índice de Liquidez",          f"{liquidez:.2f}x",                           "Ingresos ÷ Costos Fijos"),
                ("📈 ROI de Pauta",               f"{roi_pauta_kp:.1f}%",                       "Retorno sobre inversión publicitaria"),
                ("💵 Margen Bruto",               f"{margen_bruto_pct:.1f}%",                   "Utilidad bruta sobre ingresos"),
                ("💵 Margen Neto",                f"{margen_neto_pct:.1f}%",                    "Utilidad neta sobre ingresos"),
            ]

            hdr_k = "background:#161525;padding:12px 16px;font-size:0.68rem;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;color:#a8b4d0;border-bottom:2px solid #1e2337"
            td_k  = "padding:13px 16px;border-bottom:1px solid #161929;font-size:0.83rem"
            tabla_kpi = (
                f'<div style="overflow-x:auto;border-radius:14px;border:1px solid #2e2558">'
                f'<table style="width:100%;border-collapse:collapse;background:#13102a;font-family:DM Sans,sans-serif">'
                f'<thead><tr>'
                f'<th style="{hdr_k};text-align:left">Indicador</th>'
                f'<th style="{hdr_k};text-align:right">Valor</th>'
                f'<th style="{hdr_k};text-align:left">Qué mide</th>'
                f'</tr></thead><tbody>'
            )
            for nom_k, val_k, desc_k in kpis_fin:
                tabla_kpi += (
                    f'<tr style="background:rgba(255,255,255,0.01)">'
                    f'<td style="{td_k};color:#c8d0e8;font-weight:600">{nom_k}</td>'
                    f'<td style="{td_k};text-align:right;color:#fcd34d;font-weight:800;font-size:0.95rem">{val_k}</td>'
                    f'<td style="{td_k};color:#7a8aaa">{desc_k}</td>'
                    f'</tr>'
                )
            tabla_kpi += '</tbody></table></div>'
            st.markdown(tabla_kpi, unsafe_allow_html=True)


    # ══════════════════════════════════════════════════════════════════
    # 🛍️ CATÁLOGO — ANÁLISIS DE PRODUCTOS POR PAUTA PUBLICITARIA
    # ══════════════════════════════════════════════════════════════════
    elif nav == "🛍️ Catálogo":
        st.markdown('<div class="seccion-titulo">🛍️ Análisis de Productos por Pauta Publicitaria</div>', unsafe_allow_html=True)

        C_CST_PROD = "PRECIO PROVEEDOR X CANTIDAD"

        # ── Filtrar solo pedidos cerrados (Entregado, Cancelado, Devolución) ──
        def es_cerrado(est):
            e = str(est).upper()
            return any(x in e for x in ['ENTREGAD','CANCELAD','DEVOLUCI'])

        if C_ESTATUS in df.columns:
            df_cat = df[df[C_ESTATUS].apply(es_cerrado)].copy()
        else:
            df_cat = df.copy()

        # ════════════════════════════════
        # SECCIÓN 1 — CARGAR PAUTA
        # ════════════════════════════════
        st.markdown('<div style="background:#13102a;border:1px solid #2e2558;border-radius:14px;padding:18px;margin-bottom:20px">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.95rem;margin-bottom:12px">💾 Inversión Publicitaria por Producto (Pauta)</div>', unsafe_allow_html=True)

        col_pa, col_pb = st.columns([1,1])
        with col_pa:
            st.markdown('<div style="color:#a8b4d0;font-size:0.78rem;margin-bottom:8px">📁 Opción A — Subir Excel/CSV con columnas: <b>Producto, Pauta</b></div>', unsafe_allow_html=True)
            f_pauta = st.file_uploader("Cargar archivo de pauta", type=["xlsx","csv"], key="f_pauta",
                                        label_visibility="collapsed")
            if f_pauta:
                try:
                    if f_pauta.name.endswith(".csv"):
                        df_pauta = pd.read_csv(f_pauta)
                    else:
                        df_pauta = pd.read_excel(f_pauta, engine="openpyxl")
                    # Normalizar nombres de columnas
                    df_pauta.columns = [c.strip().upper() for c in df_pauta.columns]
                    col_prod_p = next((c for c in df_pauta.columns if 'PROD' in c or 'ITEM' in c or 'SKU' in c), df_pauta.columns[0])
                    col_paut_p = next((c for c in df_pauta.columns if 'PAUT' in c or 'INVER' in c or 'ADS' in c or 'PAUTA' in c), df_pauta.columns[1] if len(df_pauta.columns)>1 else None)
                    if col_paut_p:
                        pauta_dict = dict(zip(df_pauta[col_prod_p].astype(str).str.strip(),
                                               pd.to_numeric(df_pauta[col_paut_p], errors='coerce').fillna(0)))
                        st.session_state['pauta_dict'] = pauta_dict
                        st.success(f"✅ Pauta cargada: {len(pauta_dict)} productos")
                except Exception as ex:
                    st.error(f"Error leyendo archivo: {ex}")

        with col_pb:
            st.markdown('<div style="color:#a8b4d0;font-size:0.78rem;margin-bottom:8px">✏️ Opción B — Ingresar pauta manualmente por producto</div>', unsafe_allow_html=True)
            if C_PRODUCTO in df_cat.columns:
                prods_uniq = sorted(df_cat[C_PRODUCTO].dropna().astype(str).unique().tolist())
                pauta_manual = st.session_state.get('pauta_dict', {})
                with st.expander(f"Editar pauta ({len(prods_uniq)} productos)", expanded=False):
                    cols_inp = st.columns(2)
                    for i, prod in enumerate(prods_uniq):
                        with cols_inp[i % 2]:
                            val = pauta_manual.get(prod, 0)
                            nuevo = st.number_input(f"{prod[:30]}", min_value=0, value=int(val), step=1000, key=f"pauta_{i}")
                            pauta_manual[prod] = nuevo
                    if st.button("💾 Guardar pauta", key="btn_save_pauta"):
                        st.session_state['pauta_dict'] = pauta_manual
                        st.success("✅ Pauta guardada en sesión")

        st.markdown('</div>', unsafe_allow_html=True)

        pauta_dict = st.session_state.get('pauta_dict', {})
        pauta_total = sum(pauta_dict.values())

        # ════════════════════════════════
        # SECCIÓN 2 — CONTROLES
        # ════════════════════════════════
        ctrl1, ctrl2, ctrl3 = st.columns([2,2,2])
        with ctrl1:
            meses_cat = sorted(df_cat['_mes'].dropna().unique().tolist(), reverse=True) if '_mes' in df_cat.columns else []
            mes_cat = st.selectbox("📅 Mes", meses_cat if meses_cat else ["Sin datos"], key="mes_cat")
        with ctrl2:
            orden_cat = st.selectbox("📊 Ordenar por", ["% VNT","UT. BRT","% UT. PAUTA","MRGN BRT"], key="ord_cat")
        with ctrl3:
            sem_cat = st.selectbox("🗓️ Semana", ["Todas","Sem 1 (1-8)","Sem 2 (9-16)","Sem 3 (17-24)","Sem 4 (25-31)"], key="sem_cat")

        if '_mes' in df_cat.columns and mes_cat != "Sin datos":
            df_m = df_cat[df_cat['_mes'] == mes_cat].copy()
        else:
            df_m = df_cat.copy()

        # Filtrar por semana
        sem_rangos = {"Sem 1 (1-8)":(1,8),"Sem 2 (9-16)":(9,16),"Sem 3 (17-24)":(17,24),"Sem 4 (25-31)":(25,31)}
        if sem_cat != "Todas" and sem_cat in sem_rangos and C_FECHA in df_m.columns:
            ini_s, fin_s = sem_rangos[sem_cat]
            df_m = df_m[df_m[C_FECHA].dt.day.between(ini_s, fin_s)]

        if C_PRODUCTO not in df_m.columns or len(df_m) == 0:
            st.info("Sin datos de productos para este período.")
        else:
            # ════════════════════════════════
            # SECCIÓN 3 — CALCULAR MÉTRICAS
            # ════════════════════════════════
            total_peds = len(df_m)

            def calc_estatus(grp):
                total = len(grp)
                ent = grp[C_ESTATUS].astype(str).str.upper().str.contains('ENTREGAD', na=False).sum()
                cnc = grp[C_ESTATUS].astype(str).str.upper().str.contains('CANCELAD', na=False).sum()
                dvl = grp[C_ESTATUS].astype(str).str.upper().str.contains('DEVOLUCI', na=False).sum()
                cerrados = ent + cnc + dvl
                return {
                    'pedidos': total,
                    'p_entr': ent/total*100 if total else 0,
                    'p_cnc':  cnc/total*100  if total else 0,
                    'p_dvl':  dvl/total*100  if total else 0,
                    'p_cierre': cerrados/total*100 if total else 0,
                }

            filas_prod = []
            for prod, grp in df_m.groupby(C_PRODUCTO):
                est_calc = calc_estatus(grp)
                mrgn_brt = grp[C_GANANCIA].sum() if C_GANANCIA in grp.columns else 0
                ventas_prod = grp[C_TOTAL].sum() if C_TOTAL in grp.columns else 0
                pct_vnt = len(grp) / total_peds * 100 if total_peds else 0
                pauta_prod = pauta_dict.get(str(prod).strip(), 0)
                ut_brt = mrgn_brt - pauta_prod
                pct_ut_pauta = (ut_brt / pauta_prod * 100) if pauta_prod else None
                delta_inv = (pauta_prod / pauta_total * 100) if pauta_total else 0
                delta_vnt = pct_vnt - delta_inv
                filas_prod.append({
                    'PRODUCTO':    str(prod),
                    '% ENTR':      est_calc['p_entr'],
                    '% CNC':       est_calc['p_cnc'],
                    '% DVL':       est_calc['p_dvl'],
                    'CIERRE':      est_calc['p_cierre'],
                    '% VNT':       pct_vnt,
                    'MRGN BRT':    mrgn_brt,
                    'PAUTA':       pauta_prod,
                    'UT. BRT':     ut_brt,
                    '% UT. PAUTA': pct_ut_pauta,
                    'DELTA INV':   delta_inv,
                    'DELTA VNT':   delta_vnt,
                    'ventas_raw':  ventas_prod,
                    'tiene_pauta': pauta_prod > 0,
                })

            df_prod = pd.DataFrame(filas_prod)

            # Delta UT. BRT (necesita total de UT. BRT)
            ut_brt_total = df_prod['UT. BRT'].sum()
            df_prod['DELTA UT. BRT'] = df_prod['UT. BRT'] / ut_brt_total * 100 if ut_brt_total else 0

            # Ordenar
            orden_map = {"% VNT":"% VNT","UT. BRT":"UT. BRT","% UT. PAUTA":"% UT. PAUTA","MRGN BRT":"MRGN BRT"}
            sort_col = orden_map.get(orden_cat, "% VNT")
            df_prod = df_prod.sort_values(sort_col, ascending=False, na_position='last')

            # PARETO = con pauta | NO PARETO = sin pauta
            df_pareto    = df_prod[df_prod['tiene_pauta']]
            df_no_pareto = df_prod[~df_prod['tiene_pauta']]

            # ════════════════════════════════
            # SECCIÓN 4 — KPIs RÁPIDOS
            # ════════════════════════════════
            k1,k2,k3,k4,k5 = st.columns(5)
            pct_entr_g = df_m[C_ESTATUS].astype(str).str.upper().str.contains('ENTREGAD',na=False).sum()/total_peds*100 if total_peds else 0
            pct_cnc_g  = df_m[C_ESTATUS].astype(str).str.upper().str.contains('CANCELAD',na=False).sum()/total_peds*100 if total_peds else 0
            pct_dvl_g  = df_m[C_ESTATUS].astype(str).str.upper().str.contains('DEVOLUCI',na=False).sum()/total_peds*100 if total_peds else 0
            with k1: st.markdown(kpi("blue","📦 Productos",f"{len(df_prod)}"), unsafe_allow_html=True)
            with k2: st.markdown(kpi("green","✅ % Entrega Global",f"{pct_entr_g:.1f}%"), unsafe_allow_html=True)
            with k3: st.markdown(kpi("red","❌ % Cancelación",f"{pct_cnc_g:.1f}%"), unsafe_allow_html=True)
            with k4: st.markdown(kpi("gold","🔁 % Devolución",f"{pct_dvl_g:.1f}%"), unsafe_allow_html=True)
            with k5: st.markdown(kpi("purple","📣 Pauta Total",fmt_money(pauta_total)), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ════════════════════════════════
            # SECCIÓN 5 — TABLA PRINCIPAL
            # ════════════════════════════════
            def render_tabla_pauta(df_rows, titulo, color_titulo, es_pareto=True):
                if len(df_rows) == 0: return

                # HEADER
                hdr_base = "background:#161525;border-bottom:2px solid #1e2337;font-size:0.68rem;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;padding:9px 10px"
                tabla_html = (
                    f'<div style="margin-bottom:4px;font-family:Plus Jakarta Sans,sans-serif;font-size:0.75rem;'
                    f'font-weight:700;color:{color_titulo};padding:6px 0">▶ {titulo}</div>'
                    f'<div style="overflow-x:auto;border-radius:12px;border:1px solid #2e2558;margin-bottom:16px">'
                    f'<table style="width:100%;border-collapse:collapse;background:#13102a;font-family:DM Sans,sans-serif">'
                    f'<thead><tr>'
                    f'<th style="{hdr_base};text-align:left;color:#a8b4d0;min-width:160px">Producto</th>'
                    f'<th style="{hdr_base};text-align:center;color:#10b981">% ENTR</th>'
                    f'<th style="{hdr_base};text-align:center;color:#ef4444">% CNC</th>'
                    f'<th style="{hdr_base};text-align:center;color:#f59e0b">% DVL</th>'
                    f'<th style="{hdr_base};text-align:center;color:#e8ecf7;background:#2d2b35">CIERRE</th>'
                    f'<th style="{hdr_base};text-align:right;color:#10b981">% VNT</th>'
                    f'<th style="{hdr_base};text-align:right;color:#e8ecf7">MRGN BRT</th>'
                    f'<th style="{hdr_base};text-align:right;color:#22d3ee;background:#00d4ff15">PAUTA</th>'
                    f'<th style="{hdr_base};text-align:right;color:#e8ecf7">UT. BRT</th>'
                    f'<th style="{hdr_base};text-align:right;color:#fcd34d">% UT. PAUTA</th>'
                    f'<th style="{hdr_base};text-align:right;color:#9333ea">&#916; INV</th>'
                    f'<th style="{hdr_base};text-align:right;color:#9333ea">&#916; VNT</th>'
                    f'<th style="{hdr_base};text-align:right;color:#9333ea">&#916; UT. BRT</th>'
                    f'</tr></thead><tbody>'
                )

                for _, r in df_rows.iterrows():
                    prod_nom = str(r['PRODUCTO'])[:35]

                    # Colores semáforo
                    c_entr = "#10b981" if r['% ENTR'] >= 60 else "#f59e0b" if r['% ENTR'] >= 40 else "#ef4444"
                    c_cnc  = "#ef4444" if r['% CNC']  > 20  else "#f59e0b" if r['% CNC'] > 10  else "#10b981"
                    c_dvl  = "#ef4444" if r['% DVL']  > 20  else "#f59e0b" if r['% DVL'] > 10  else "#10b981"
                    c_vnt  = "#10b981" if r['% VNT']  > 20  else "#e8ecf7"
                    c_ut   = "#10b981" if (r['% UT. PAUTA'] or 0) > 50 else "#f59e0b" if (r['% UT. PAUTA'] or 0) > 0 else "#ef4444"
                    c_dvnt = "#10b981" if r['DELTA VNT'] > 0 else "#ef4444"
                    c_dut  = "#10b981" if r['DELTA UT. BRT'] > 10 else "#e8ecf7"

                    # Flecha cierre
                    flecha = "&#x25B2;" if r['CIERRE'] >= 90 else "&#x25BC;"
                    f_color = "#10b981" if r['CIERRE'] >= 90 else "#ef4444"

                    pct_ut_txt = f"{r['% UT. PAUTA']:.1f}%" if r['% UT. PAUTA'] is not None else "—"
                    pauta_txt  = fmt_money(r['PAUTA']) if r['PAUTA'] > 0 else "—"

                    td = "padding:9px 10px;font-size:0.8rem;border-bottom:1px solid #161929"
                    tabla_html += (
                        f'<tr style="background:rgba(255,255,255,0.01)" '
                        f'onmouseover="this.style.background=\'rgba(99,102,241,0.07)\'" '
                        f'onmouseout="this.style.background=\'rgba(255,255,255,0.01)\'">'
                        f'<td style="{td};color:#c8d0e8;font-weight:600;text-align:left">{prod_nom}</td>'
                        f'<td style="{td};text-align:center;color:{c_entr};font-weight:700">{r["% ENTR"]:.1f}%</td>'
                        f'<td style="{td};text-align:center;color:{c_cnc};font-weight:700">{r["% CNC"]:.1f}%</td>'
                        f'<td style="{td};text-align:center;color:{c_dvl};font-weight:700">{r["% DVL"]:.1f}%</td>'
                        f'<td style="{td};text-align:center;background:#2d2b3520">'
                        f'<span style="color:{f_color}">{flecha}</span> '
                        f'<span style="color:#e8ecf7;font-weight:700">{r["CIERRE"]:.1f}%</span></td>'
                        f'<td style="{td};text-align:right;color:{c_vnt};font-weight:700">{r["% VNT"]:.2f}%</td>'
                        f'<td style="{td};text-align:right;color:#e8ecf7">{fmt_money(r["MRGN BRT"])}</td>'
                        f'<td style="{td};text-align:right;color:#22d3ee;font-weight:700;background:#00d4ff0a">{pauta_txt}</td>'
                        f'<td style="{td};text-align:right;color:#e8ecf7">{fmt_money(r["UT. BRT"])}</td>'
                        f'<td style="{td};text-align:right;color:{c_ut};font-weight:700">{pct_ut_txt}</td>'
                        f'<td style="{td};text-align:right;color:#9333ea">{r["DELTA INV"]:.1f}%</td>'
                        f'<td style="{td};text-align:right;color:{c_dvnt};font-weight:700">'
                        f'{"+" if r["DELTA VNT"]>0 else ""}{r["DELTA VNT"]:.1f}%</td>'
                        f'<td style="{td};text-align:right;color:{c_dut};font-weight:700">{r["DELTA UT. BRT"]:.1f}%</td>'
                        f'</tr>'
                    )

                # Fila SUBTOTAL (PARETO o NO PARETO)
                label_sub = "PARETO" if es_pareto else "NO PARETO"
                color_sub  = "#f0c060" if es_pareto else "#5b6cfc"
                bg_sub     = "rgba(201,168,76,0.08)" if es_pareto else "rgba(99,102,241,0.08)"
                td_sub = f"padding:10px 10px;font-size:0.8rem;font-weight:800;border-top:2px solid {color_sub};background:{bg_sub}"
                sum_entr = df_rows['% ENTR'].mean()
                sum_cnc  = df_rows['% CNC'].mean()
                sum_dvl  = df_rows['% DVL'].mean()
                sum_cier = df_rows['CIERRE'].mean()
                sum_vnt  = df_rows['% VNT'].sum()
                sum_mrgn = df_rows['MRGN BRT'].sum()
                sum_paut = df_rows['PAUTA'].sum()
                sum_ut   = df_rows['UT. BRT'].sum()
                sum_dut  = df_rows['DELTA UT. BRT'].sum()
                pct_ut_sub = (sum_ut / sum_paut * 100) if sum_paut else None
                pct_ut_sub_txt = f"{pct_ut_sub:.1f}%" if pct_ut_sub is not None else "—"
                pauta_sub_txt = fmt_money(sum_paut) if sum_paut > 0 else "—"

                tabla_html += (
                    f'<tr>'
                    f'<td style="{td_sub};text-align:left;color:{color_sub}">{label_sub}</td>'
                    f'<td style="{td_sub};text-align:center;color:#10b981">{sum_entr:.1f}%</td>'
                    f'<td style="{td_sub};text-align:center;color:#ef4444">{sum_cnc:.1f}%</td>'
                    f'<td style="{td_sub};text-align:center;color:#f59e0b">{sum_dvl:.1f}%</td>'
                    f'<td style="{td_sub};text-align:center;color:#e8ecf7">{sum_cier:.1f}%</td>'
                    f'<td style="{td_sub};text-align:right;color:#10b981">{sum_vnt:.1f}%</td>'
                    f'<td style="{td_sub};text-align:right;color:#e8ecf7">{fmt_money(sum_mrgn)}</td>'
                    f'<td style="{td_sub};text-align:right;color:#22d3ee;background:#00d4ff0a">{pauta_sub_txt}</td>'
                    f'<td style="{td_sub};text-align:right;color:#e8ecf7">{fmt_money(sum_ut)}</td>'
                    f'<td style="{td_sub};text-align:right;color:#fcd34d">{pct_ut_sub_txt}</td>'
                    f'<td style="{td_sub};text-align:right;color:#9333ea">—</td>'
                    f'<td style="{td_sub};text-align:right;color:#9333ea">—</td>'
                    f'<td style="{td_sub};text-align:right;color:#9333ea">{sum_dut:.1f}%</td>'
                    f'</tr>'
                )

                tabla_html += '</tbody></table></div>'
                st.markdown(tabla_html, unsafe_allow_html=True)

            # Renderizar PARETO y NO PARETO
            render_tabla_pauta(df_pareto,    "CON PAUTA (PARETO)",    "#f0c060", es_pareto=True)
            render_tabla_pauta(df_no_pareto, "SIN PAUTA (NO PARETO)", "#5b6cfc", es_pareto=False)

            # ── Fila KPI's Generales al final ──
            td_g = "padding:8px 10px;font-size:0.78rem;font-weight:700;color:#a8b4d0"
            ut_brt_tot_txt  = fmt_money(ut_brt_total)
            pauta_tot_txt   = fmt_money(pauta_total) if pauta_total else "—"
            pct_ut_tot_txt  = f"{ut_brt_total/pauta_total*100:.1f}%" if pauta_total else "—"
            kpig_html = (
                f'<div style="background:#161525;border:1px solid #2e2558;border-radius:10px;padding:2px 0;margin-top:4px">'
                f'<table style="width:100%;border-collapse:collapse;font-family:DM Sans,sans-serif"><tr>'
                f'<td style="{td_g};text-align:left;min-width:160px">KPI\'s Generales</td>'
                f'<td style="{td_g};text-align:center;color:#10b981">{pct_entr_g:.1f}%</td>'
                f'<td style="{td_g};text-align:center;color:#ef4444">{pct_cnc_g:.1f}%</td>'
                f'<td style="{td_g};text-align:center;color:#f59e0b">{pct_dvl_g:.1f}%</td>'
                f'<td style="{td_g};text-align:center"></td>'
                f'<td style="{td_g};text-align:right"></td>'
                f'<td style="{td_g};text-align:right;color:#e8ecf7">{fmt_money(df_prod["MRGN BRT"].sum())}</td>'
                f'<td style="{td_g};text-align:right;color:#22d3ee">{pauta_tot_txt}</td>'
                f'<td style="{td_g};text-align:right;color:#e8ecf7">{ut_brt_tot_txt}</td>'
                f'<td style="{td_g};text-align:right;color:#fcd34d">{pct_ut_tot_txt}</td>'
                f'<td style="{td_g}" colspan="3"></td>'
                f'</tr></table></div>'
            )
            st.markdown(kpig_html, unsafe_allow_html=True)

            # ════════════════════════════════
            # SECCIÓN 6 — GRÁFICA COMPARATIVA
            # ════════════════════════════════
            st.markdown("<br>", unsafe_allow_html=True)
            g1, g2 = st.columns(2)

            with g1:
                top_p = df_prod.sort_values('UT. BRT', ascending=True).tail(12)
                fig_ut = go.Figure()
                fig_ut.add_trace(go.Bar(x=top_p['UT. BRT'], y=top_p['PRODUCTO'].str[:25],
                                        orientation='h', name='UT. BRT',
                                        marker_color=['#10b981' if v >= 0 else '#ef4444' for v in top_p['UT. BRT']]))
                fig_ut.update_layout(**PLOT_LAYOUT, height=400, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE,
                                     title='Utilidad Bruta por Producto (UT. BRT)')
                st.plotly_chart(fig_ut, use_container_width=True)

            with g2:
                top_d = df_prod[df_prod['PAUTA'] > 0].sort_values('DELTA VNT')
                colors_d = ['#10b981' if v >= 0 else '#ef4444' for v in top_d['DELTA VNT']]
                fig_dv = go.Figure(go.Bar(
                    x=top_d['DELTA VNT'], y=top_d['PRODUCTO'].str[:25],
                    orientation='h', marker_color=colors_d,
                    text=[f"{'+'if v>=0 else ''}{v:.1f}%" for v in top_d['DELTA VNT']],
                    textposition='outside'
                ))
                fig_dv.add_vline(x=0, line_color='#a8b8d0', line_width=1)
                fig_dv.update_layout(**PLOT_LAYOUT, height=400, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE,
                                     title='Delta Venta — Eficiencia de Pauta por Producto',
                                     xaxis_ticksuffix='%')
                st.plotly_chart(fig_dv, use_container_width=True)

            # ════════════════════════════════
            # SECCIÓN 7 — EXPORTAR
            # ════════════════════════════════
            import io
            buf_cat = io.BytesIO()
            df_export_cat = df_prod[['PRODUCTO','% ENTR','% CNC','% DVL','CIERRE','% VNT',
                                      'MRGN BRT','PAUTA','UT. BRT','% UT. PAUTA',
                                      'DELTA INV','DELTA VNT','DELTA UT. BRT']].copy()
            df_export_cat.to_excel(buf_cat, index=False, engine='openpyxl')
            st.download_button("⬇️ Exportar tabla a Excel", buf_cat.getvalue(),
                               file_name=f"catalogo_pauta_{mes_cat}.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ═══════════════════════════════════════════════════════════
# ██████  ASESOR FINANCIERO — MÓDULO INDEPENDIENTE
# ═══════════════════════════════════════════════════════════
elif "Asesor" in vista_activa:

    op_nombre = operacion.split("  ")[1]
    op_color  = op_info["color"]
    st.markdown(
        f'<div style="margin-bottom:28px;background:linear-gradient(135deg,#12151f,#161929);'
        f'border:1px solid #2e2558;border-radius:16px;padding:24px 28px">'
        f'<div style="display:flex;align-items:center;gap:16px">'
        f'<div style="width:4px;height:54px;background:{op_color};border-radius:4px"></div>'
        f'<div>'
        f'<div style="font-size:0.68rem;color:#7a8aaa;font-weight:700;letter-spacing:0.12em;'
        f'text-transform:uppercase;margin-bottom:5px">{op_info["pais"]} &nbsp;·&nbsp; {op_info["moneda"]}</div>'
        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-size:1.9rem;font-weight:800;'
        f'color:#e8ecf7;line-height:1;margin-bottom:6px">{op_nombre}</div>'
        f'<div style="color:#a8b4d0;font-size:0.83rem">🧠 Asesor Financiero — Distribución inteligente del capital</div>'
        f'</div></div></div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="seccion-titulo">🧠 Asesor Financiero</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.78rem;color:#a8b4d0;margin-bottom:20px">'
        'Ingresa el saldo disponible en tu cuenta bancaria y el asesor te dice exactamente cómo distribuirlo '
        'según el estado real de tu negocio.</div>',
        unsafe_allow_html=True
    )

    # ── CONTEXTO: leer métricas del negocio ──
    _hoy_af = pd.Timestamp.now()
    _mes_af = _hoy_af.to_period('M').strftime('%Y-%m')
    _df_af  = df[df['_mes'] == _mes_af].copy() if '_mes' in df.columns else df.copy()
    if len(_df_af) == 0:
        _df_af = df.copy()

    _mask_ent_af = _df_af[C_ESTATUS].astype(str).str.upper().str.contains('ENTREGAD', na=False) if C_ESTATUS in _df_af.columns else pd.Series([True]*len(_df_af))
    _mask_dev_af = _df_af[C_ESTATUS].astype(str).str.upper().str.contains('DEVOLUCI', na=False) if C_ESTATUS in _df_af.columns else pd.Series([False]*len(_df_af))
    _mask_can_af = _df_af[C_ESTATUS].astype(str).str.upper().str.contains('CANCELAD', na=False) if C_ESTATUS in _df_af.columns else pd.Series([False]*len(_df_af))

    _ing_af     = _df_af[_mask_ent_af][C_TOTAL].sum()   if C_TOTAL    in _df_af.columns else 0
    _gan_af     = _df_af[_mask_ent_af][C_GANANCIA].sum() if C_GANANCIA in _df_af.columns else 0
    _cst_af     = _df_af[_mask_ent_af]["PRECIO PROVEEDOR X CANTIDAD"].sum() if "PRECIO PROVEEDOR X CANTIDAD" in _df_af.columns else 0
    _flete_e_af = _df_af[_mask_ent_af][C_FLETE].sum()   if C_FLETE    in _df_af.columns else 0
    _flete_d_af = _df_af[_mask_dev_af][C_FLETE].sum()   if C_FLETE    in _df_af.columns else 0
    _nom_af     = float(st.session_state.get('nomina_total', 0))
    _pauta_af   = float(sum(st.session_state.get('pauta_dict', {}).values()))
    _cf_af      = float(sum(st.session_state.get('costos_fijos', {}).values()))
    _tasa_e_af  = len(_df_af[_mask_ent_af]) / len(_df_af) * 100 if len(_df_af) else 0
    _tasa_d_af  = len(_df_af[_mask_dev_af]) / len(_df_af) * 100 if len(_df_af) else 0
    _tasa_c_af  = len(_df_af[_mask_can_af]) / len(_df_af) * 100 if len(_df_af) else 0
    _gastos_fijos_total = _nom_af + _cf_af
    _gastos_op_total    = _gastos_fijos_total + _pauta_af + _flete_e_af + _flete_d_af
    _ub_af      = _ing_af - _cst_af
    _uop_af     = _ub_af - _gastos_op_total
    _tasa_imp_af= float(st.session_state.get('diag_imp', 8.0)) * (1 - float(st.session_state.get('diag_iva_excl', 80.0)) / 100)
    _imp_af     = _ing_af * (_tasa_imp_af / 100)
    _util_af    = _uop_af - _imp_af
    _margen_af  = _gan_af / _ing_af * 100 if _ing_af else 0

    # ── INPUT: SALDO BANCARIO ──
    af1, af2 = st.columns([2, 3])
    with af1:
        st.markdown(
            '<div style="background:linear-gradient(135deg,#12151f,#161929);border:2px solid #5b6cfc;'
            'border-radius:16px;padding:20px 22px;margin-bottom:16px">',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.88rem;margin-bottom:14px">'
            '🏦 ¿Cuánto tienes en el banco hoy?</div>',
            unsafe_allow_html=True
        )
        saldo_banco = st.number_input(
            "Saldo bancario disponible (COP)",
            min_value=0, max_value=10_000_000_000,
            value=int(st.session_state.get('af_saldo', 0)),
            step=1_000_000, format="%d",
            key="af_saldo",
            label_visibility="collapsed"
        )
        st.markdown(
            f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:#a855f7;font-size:1.6rem;'
            f'margin-top:8px">{fmt_money(saldo_banco)}</div>',
            unsafe_allow_html=True
        )

        _modo_asesor = st.radio(
            "Perfil del negocio",
            ["🌱 En crecimiento", "⚖️ Estable / Consolidando", "🔴 En dificultades"],
            key="af_modo", label_visibility="visible"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with af2:
        # Resumen de salud del negocio
        _score_color = "#10b981" if _tasa_e_af >= 65 and _tasa_d_af <= 12 else \
                       "#f59e0b" if _tasa_e_af >= 50 else "#ef4444"
        _salud_txt   = "Buena" if _score_color == "#10b981" else "Moderada" if _score_color == "#f59e0b" else "Crítica"
        st.markdown(
            f'<div style="background:#13102a;border:1px solid #2e2558;border-radius:14px;padding:18px 20px">'
            f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.82rem;margin-bottom:12px">'
            f'📊 Contexto del negocio — Período actual</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">',
            unsafe_allow_html=True
        )
        ctx_items = [
            ("💰 Ingresos mes",       fmt_money(_ing_af),           "#5b6cfc"),
            ("📈 Utilidad neta est.", fmt_money(_util_af),           "#10b981" if _util_af >= 0 else "#ef4444"),
            ("🚚 Tasa entrega",       f"{_tasa_e_af:.1f}%",          "#10b981" if _tasa_e_af >= 65 else "#ef4444"),
            ("↩️ Tasa devolución",    f"{_tasa_d_af:.1f}%",          "#ef4444" if _tasa_d_af > 12 else "#10b981"),
            ("🏢 Gastos fijos mes",   fmt_money(_gastos_fijos_total),"#f59e0b"),
            ("🏥 Salud del negocio",  _salud_txt,                    _score_color),
        ]
        ctx_html = ""
        for lbl_c, val_c, col_c in ctx_items:
            ctx_html += (
                f'<div style="background:#0d0a1a;border-radius:10px;padding:10px 12px">'
                f'<div style="font-size:0.6rem;color:#a8b4d0;font-weight:700;margin-bottom:3px">{lbl_c}</div>'
                f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:{col_c};font-size:0.9rem">{val_c}</div>'
                f'</div>'
            )
        st.markdown(ctx_html + '</div></div>', unsafe_allow_html=True)

    if saldo_banco <= 0:
        st.markdown(
            '<div style="background:rgba(124,58,237,0.15);border:1px dashed #2e3650;border-radius:12px;'
            'padding:20px;text-align:center;margin-top:10px">'
            '<div style="font-size:1.8rem;margin-bottom:8px">💡</div>'
            '<div style="color:#a8b4d0;font-size:0.85rem">Ingresa el saldo bancario disponible arriba para ver la distribución recomendada</div>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown("<br>", unsafe_allow_html=True)

        # ── CALCULAR DISTRIBUCIÓN SEGÚN PERFIL ──
        # Primero calcular necesidades reales del negocio
        _reserva_min      = _gastos_fijos_total * 3           # 3 meses de costos fijos
        _deuda_impuesto   = max(_imp_af, 0)                    # impuesto pendiente
        _capital_pauta    = _pauta_af if _pauta_af > 0 else saldo_banco * 0.15
        _capital_inventario = _ing_af * 0.35                  # ~35% ventas en inventario

        # Perfil: ajusta proporciones
        if "crecimiento" in _modo_asesor.lower():
            _pct_dist = {
                "operacion":  0.30,
                "marketing":  0.25,
                "reserva":    0.20,
                "crecimiento":0.15,
                "impuestos":  0.05,
                "retiro":     0.05,
            }
        elif "dificultades" in _modo_asesor.lower():
            _pct_dist = {
                "operacion":  0.40,
                "marketing":  0.10,
                "reserva":    0.30,
                "crecimiento":0.05,
                "impuestos":  0.10,
                "retiro":     0.05,
            }
        else:  # estable
            _pct_dist = {
                "operacion":  0.30,
                "marketing":  0.20,
                "reserva":    0.20,
                "crecimiento":0.15,
                "impuestos":  0.08,
                "retiro":     0.07,
            }

        _bolsillos = {
            "operacion":   {"lbl":"🔄 Operación",        "col":"#5b6cfc",  "pct":_pct_dist["operacion"],
                            "desc":"Capital de trabajo, inventario, flete, proveedor",
                            "meta": fmt_money(_capital_inventario + _flete_e_af),
                            "meta_lbl":"necesitas para próximo mes"},
            "marketing":   {"lbl":"📣 Marketing & Pauta","col":"#7c3aed",  "pct":_pct_dist["marketing"],
                            "desc":"Pauta pagada, creativos, herramientas",
                            "meta": fmt_money(_capital_pauta),
                            "meta_lbl":"pauta actual mensual"},
            "reserva":     {"lbl":"🏦 Reserva Emergencia","col":"#00d4ff","pct":_pct_dist["reserva"],
                            "desc":"Mínimo 3 meses de costos fijos cubiertos",
                            "meta": fmt_money(_reserva_min),
                            "meta_lbl":"objetivo de reserva (3 meses)"},
            "crecimiento": {"lbl":"📈 Inversión & Crec.","col":"#10b981","pct":_pct_dist["crecimiento"],
                            "desc":"Nuevos productos, equipos, expansión",
                            "meta": "—",
                            "meta_lbl":"según oportunidad"},
            "impuestos":   {"lbl":"🏛️ Obligaciones Fisc.","col":"#f0c060","pct":_pct_dist["impuestos"],
                            "desc":"Impuestos, retenciones, obligaciones DIAN",
                            "meta": fmt_money(_deuda_impuesto),
                            "meta_lbl":"impuesto estimado este mes"},
            "retiro":      {"lbl":"💼 Retiro / Utilidad","col":"#f97416","pct":_pct_dist["retiro"],
                            "desc":"Tu rentabilidad personal como empresario",
                            "meta": "—",
                            "meta_lbl":"según utilidad neta real"},
        }

        # ── TÍTULO SECCIÓN ──
        st.markdown(
            f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.95rem;margin-bottom:4px">'
            f'💡 Distribución recomendada para <span style="color:#a855f7">{fmt_money(saldo_banco)}</span></div>'
            f'<div style="font-size:0.72rem;color:#a8b4d0;margin-bottom:16px">'
            f'Perfil: {_modo_asesor} · Basado en métricas reales del período</div>',
            unsafe_allow_html=True
        )

        # ── CARDS DE DISTRIBUCIÓN ──
        _cols_af = st.columns(3)
        for bi, (key_b, bol) in enumerate(_bolsillos.items()):
            monto_b = saldo_banco * bol["pct"]
            # Alerta si el monto es insuficiente vs la meta
            try:
                _meta_num = float(bol["meta"].replace("$","").replace(",","").replace("M","e6").replace("K","e3").replace("—","0"))
            except:
                _meta_num = 0
            _suficiente = monto_b >= _meta_num if _meta_num > 0 else True
            _alerta_col = bol["col"] if _suficiente else "#ef4444"
            _alerta_ico = "✅" if _suficiente else "⚠️"

            with _cols_af[bi % 3]:
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,{bol["col"]}0d,#12151f);'
                    f'border:1.5px solid {_alerta_col}44;border-top:3px solid {_alerta_col};'
                    f'border-radius:14px;padding:16px 14px;margin-bottom:12px">'

                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">'
                    f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;'
                    f'font-size:0.78rem;line-height:1.3">{bol["lbl"]}</div>'
                    f'<span style="font-size:0.8rem">{_alerta_ico}</span>'
                    f'</div>'

                    f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:900;color:{bol["col"]};'
                    f'font-size:1.35rem;margin-bottom:2px">{fmt_money(monto_b)}</div>'
                    f'<div style="font-size:0.65rem;color:{bol["col"]};font-weight:700;margin-bottom:8px">'
                    f'{bol["pct"]*100:.0f}% del saldo</div>'

                    f'<div style="font-size:0.68rem;color:#7a8aaa;margin-bottom:8px;line-height:1.4">{bol["desc"]}</div>'

                    f'<div style="background:#0d0a1a;border-radius:8px;padding:6px 10px">'
                    f'<div style="font-size:0.6rem;color:#7a8aaa">{bol["meta_lbl"]}</div>'
                    f'<div style="font-size:0.72rem;color:{"#10b981" if _suficiente else "#ef4444"};font-weight:700">'
                    f'{bol["meta"]}'
                    f'{"  ✅ cubierto" if _suficiente and _meta_num > 0 else "  ⚠️ insuficiente" if not _suficiente else ""}'
                    f'</div></div>'

                    f'<div style="background:#1e2337;border-radius:100px;height:5px;margin-top:10px;overflow:hidden">'
                    f'<div style="background:{bol["col"]};width:{min(monto_b/_meta_num*100,100) if _meta_num else 100:.0f}%;'
                    f'height:100%;border-radius:100px"></div></div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        # ── BARRA VISUAL DE DISTRIBUCIÓN ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.8rem;margin-bottom:8px">'
            '📊 Vista proporcional del saldo</div>',
            unsafe_allow_html=True
        )
        barra_seg = ""
        for key_b, bol in _bolsillos.items():
            barra_seg += (
                f'<div style="flex:{bol["pct"]*100:.0f};background:{bol["col"]};height:28px;'
                f'display:flex;align-items:center;justify-content:center;'
                f'font-size:0.6rem;color:white;font-weight:800;white-space:nowrap;overflow:hidden;'
                f'text-overflow:ellipsis;padding:0 4px">'
                f'{bol["pct"]*100:.0f}%</div>'
            )
        st.markdown(
            f'<div style="display:flex;border-radius:10px;overflow:hidden;border:1px solid #2e2558;margin-bottom:6px">'
            f'{barra_seg}</div>',
            unsafe_allow_html=True
        )
        # Leyenda
        leyenda_html = '<div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:16px">'
        for key_b, bol in _bolsillos.items():
            leyenda_html += (
                f'<div style="display:flex;align-items:center;gap:4px">'
                f'<div style="width:10px;height:10px;border-radius:3px;background:{bol["col"]}"></div>'
                f'<span style="font-size:0.65rem;color:#a8b4d0">{bol["lbl"]}</span>'
                f'</div>'
            )
        leyenda_html += '</div>'
        st.markdown(leyenda_html, unsafe_allow_html=True)

        # ── DIAGNÓSTICO PERSONALIZADO ──
        st.markdown("<hr style='border-color:#1e2337;margin:16px 0'>", unsafe_allow_html=True)
        st.markdown(
            '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.88rem;margin-bottom:10px">'
            '🤖 Diagnóstico del Asesor</div>',
            unsafe_allow_html=True
        )

        _alertas_af = []
        _consejos_af= []

        # Reserva
        _reserva_actual = saldo_banco * _pct_dist["reserva"]
        if _reserva_actual < _reserva_min:
            _alertas_af.append({
                "ico":"🔴","txt":f"Tu reserva de emergencia ({fmt_money(_reserva_actual)}) está por debajo del mínimo recomendado "
                                 f"de 3 meses de costos fijos ({fmt_money(_reserva_min)}). Ante cualquier caída en ventas, "
                                 f"el negocio quedaría sin colchón operativo.",
                "col":"#ef4444"
            })
        else:
            _consejos_af.append(f"✅ Reserva cubierta — tienes {fmt_money(_reserva_actual)} disponibles para emergencias.")

        # Pauta
        _pauta_disponible = saldo_banco * _pct_dist["marketing"]
        if _pauta_disponible < _capital_pauta * 0.8:
            _alertas_af.append({
                "ico":"🟡","txt":f"El capital destinado a pauta ({fmt_money(_pauta_disponible)}) es menor que tu pauta actual "
                                 f"({fmt_money(_capital_pauta)}). Considera reducir temporalmente o buscar financiación.",
                "col":"#f59e0b"
            })
        else:
            _consejos_af.append(f"✅ Pauta cubierta — {fmt_money(_pauta_disponible)} disponibles para publicidad.")

        # Impuestos
        _imp_disponible = saldo_banco * _pct_dist["impuestos"]
        if _imp_disponible < _deuda_impuesto * 0.9 and _deuda_impuesto > 0:
            _alertas_af.append({
                "ico":"🔴","txt":f"El capital reservado para impuestos ({fmt_money(_imp_disponible)}) podría ser insuficiente. "
                                 f"El impuesto estimado del mes es {fmt_money(_deuda_impuesto)}.",
                "col":"#ef4444"
            })

        # Saldo muy alto sin invertir
        if saldo_banco > _ing_af * 3 and _ing_af > 0:
            _consejos_af.append(
                f"💡 Tienes un saldo muy alto vs tus ingresos mensuales. "
                f"Considera invertir el excedente en inventario, nuevos productos o instrumentos financieros."
            )

        # Devolución alta
        if _tasa_d_af > 12:
            _consejos_af.append(
                f"⚠️ Tu devolución está en {_tasa_d_af:.1f}% — cada peso destinado a marketing se pierde parcialmente. "
                f"Prioriza reducir devoluciones antes de escalar la pauta."
            )

        # Utilidad negativa
        if _util_af < 0:
            _alertas_af.append({
                "ico":"🔴","txt":f"El negocio tiene utilidad neta negativa este período ({fmt_money(_util_af)}). "
                                 f"No hay excedente real para distribuir. Usa el saldo para cubrir operación y reserva únicamente.",
                "col":"#ef4444"
            })

        # Render diagnóstico
        for al in _alertas_af:
            st.markdown(
                f'<div style="background:{al["col"]}0d;border:1px solid {al["col"]}44;border-left:4px solid {al["col"]};'
                f'border-radius:10px;padding:12px 16px;margin-bottom:8px">'
                f'<span style="font-size:0.9rem">{al["ico"]}</span> '
                f'<span style="font-size:0.78rem;color:#c8d0e8;line-height:1.6">{al["txt"]}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
        if _consejos_af:
            cons_html = '<div style="background:rgba(16,185,129,0.05);border:1px solid #10b98122;border-radius:10px;padding:14px 16px;margin-bottom:8px">'
            for c in _consejos_af:
                cons_html += f'<div style="font-size:0.78rem;color:#a8b4d0;margin-bottom:6px;line-height:1.5">{c}</div>'
            cons_html += '</div>'
            st.markdown(cons_html, unsafe_allow_html=True)

        # ── TABLA RESUMEN ──
        st.markdown("<br>", unsafe_allow_html=True)
        tbl_html = (
            '<div style="overflow-x:auto;border-radius:12px;border:1px solid #2e2558">'
            '<table style="width:100%;border-collapse:collapse;background:#13102a;font-family:DM Sans,sans-serif">'
            '<thead><tr>'
            '<th style="padding:10px 14px;text-align:left;color:#c0cce0;font-size:0.65rem;text-transform:uppercase;letter-spacing:0.07em;border-bottom:2px solid #1e2337">Bolsillo</th>'
            '<th style="padding:10px 14px;text-align:right;color:#c0cce0;font-size:0.65rem;text-transform:uppercase;letter-spacing:0.07em;border-bottom:2px solid #1e2337">% Asignado</th>'
            '<th style="padding:10px 14px;text-align:right;color:#c0cce0;font-size:0.65rem;text-transform:uppercase;letter-spacing:0.07em;border-bottom:2px solid #1e2337">Monto</th>'
            '<th style="padding:10px 14px;text-align:right;color:#c0cce0;font-size:0.65rem;text-transform:uppercase;letter-spacing:0.07em;border-bottom:2px solid #1e2337">Meta / Referencia</th>'
            '<th style="padding:10px 14px;text-align:center;color:#c0cce0;font-size:0.65rem;text-transform:uppercase;letter-spacing:0.07em;border-bottom:2px solid #1e2337">Estado</th>'
            '</tr></thead><tbody>'
        )
        for key_b, bol in _bolsillos.items():
            monto_b = saldo_banco * bol["pct"]
            try:
                _meta_n = float(bol["meta"].replace("$","").replace(",","").replace("M","e6").replace("K","e3").replace("—","0"))
            except:
                _meta_n = 0
            _ok = monto_b >= _meta_n if _meta_n > 0 else True
            _est = f'<span style="color:#10b981;font-weight:700">✅ OK</span>' if _ok else f'<span style="color:#ef4444;font-weight:700">⚠️ Bajo</span>'
            tbl_html += (
                f'<tr style="border-bottom:1px solid #1e2337">'
                f'<td style="padding:10px 14px;color:{bol["col"]};font-weight:700;font-size:0.82rem">{bol["lbl"]}</td>'
                f'<td style="padding:10px 14px;text-align:right;color:#a8b4d0;font-size:0.82rem">{bol["pct"]*100:.0f}%</td>'
                f'<td style="padding:10px 14px;text-align:right;color:{bol["col"]};font-weight:800;font-size:0.82rem">{fmt_money(monto_b)}</td>'
                f'<td style="padding:10px 14px;text-align:right;color:#7a8aaa;font-size:0.75rem">{bol["meta"]}</td>'
                f'<td style="padding:10px 14px;text-align:center;font-size:0.78rem">{_est}</td>'
                f'</tr>'
            )
        tbl_html += (
            f'<tr style="background:rgba(99,102,241,0.07)">'
            f'<td style="padding:10px 14px;color:#e8ecf7;font-weight:800;font-size:0.85rem">TOTAL</td>'
            f'<td style="padding:10px 14px;text-align:right;color:#e8ecf7;font-weight:800">100%</td>'
            f'<td style="padding:10px 14px;text-align:right;color:#a855f7;font-weight:900;font-size:0.9rem">{fmt_money(saldo_banco)}</td>'
            f'<td colspan="2"></td>'
            f'</tr>'
            '</tbody></table></div>'
        )
        st.markdown(tbl_html, unsafe_allow_html=True)




# ═══════════════════════════════════════════════════════════
# ██████  TENDENCIAS & CLIMA — INTELIGENCIA COMERCIAL
# ═══════════════════════════════════════════════════════════
elif "Tendencias" in vista_activa:
    from datetime import date as _dt_tend
    _hoy_tend = _dt_tend.today()

    st.markdown(
        '<div style="margin-bottom:20px;background:linear-gradient(135deg,#12151f,#161929);'
        'border:1px solid #2e2558;border-radius:16px;padding:22px 26px">'
        '<div style="font-family:Plus Jakarta Sans,sans-serif;font-size:1.7rem;font-weight:800;color:#e8ecf7">📡 Tendencias & Clima</div>'
        '<div style="color:#a8b4d0;font-size:0.82rem;margin-top:4px">Inteligencia comercial basada en problemas, regiones y estacionalidad</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── Tabs del módulo ──
    _tend_tab1, _tend_tab2, _tend_tab3 = st.tabs([
        "🔎 Problemas → Productos",
        "🌦️ Clima → Productos",
        "📊 Análisis Inteligente"
    ])

    # ════════════════════════════════════════
    # TAB 1 — PROBLEMAS → PRODUCTOS
    # ════════════════════════════════════════
    with _tend_tab1:
        st.markdown('<div class="seccion-titulo">🔎 Detección de Problemas del Consumidor</div>', unsafe_allow_html=True)

        # Base de conocimiento: problema → solución → región → temporada
        PROBLEMAS_COMERCIALES = {
            "Arrugas / Envejecimiento facial": {
                "ico": "👁️",
                "categoria": "Belleza & Skincare",
                "productos_sugeridos": ["Crema antiarrugas", "Sérum vitamina C", "Ácido hialurónico", "Protector solar", "Mascarilla rejuvenecedora"],
                "regiones_top": {"Bogotá": "muy_alto", "Medellín": "muy_alto", "Cali": "alto", "Barranquilla": "medio"},
                "regiones_chile": {"Santiago": "muy_alto", "Valparaíso": "alto", "Concepción": "alto"},
                "temporada_pico": [3, 4, 9, 10],  # meses
                "temporada_lbl": "Mar-Abr y Sep-Oct (pre-temporada social)",
                "insight": "En Medellín hay alta cultura estética y mayor inversión en belleza. Búsquedas elevadas de antiarrugas antes de ferias y eventos sociales.",
                "nicho": "Mujeres 30-55 años, NSE medio-alto, urbanas"
            },
            "Caída del cabello": {
                "ico": "💆",
                "categoria": "Cuidado Capilar",
                "productos_sugeridos": ["Shampoo anticaída", "Biotina suplemento", "Sérum capilar", "Minoxidil", "Keratina"],
                "regiones_top": {"Bogotá": "muy_alto", "Medellín": "alto", "Cali": "alto", "Bucaramanga": "medio"},
                "regiones_chile": {"Santiago": "muy_alto", "Antofagasta": "alto"},
                "temporada_pico": [1, 2, 7, 8],
                "temporada_lbl": "Ene-Feb y Jul-Ago (estrés post-vacaciones y cambio de estación)",
                "insight": "El estrés laboral y cambios hormonales disparan búsquedas. Mayor volumen en ciudades de alta presión laboral.",
                "nicho": "Hombres y mujeres 25-50 años, profesionales"
            },
            "Sudor excesivo / Mal olor": {
                "ico": "💧",
                "categoria": "Higiene Personal",
                "productos_sugeridos": ["Desodorante clínico", "Antitranspirante 48h", "Talco medicado", "Ropa técnica antibacterial"],
                "regiones_top": {"Barranquilla": "muy_alto", "Cartagena": "muy_alto", "Santa Marta": "alto", "Cali": "alto"},
                "regiones_chile": {"Antofagasta": "muy_alto", "Arica": "alto", "Iquique": "muy_alto"},
                "temporada_pico": [4, 5, 6, 7, 8],
                "temporada_lbl": "Abr-Ago (verano y calor extremo en costas)",
                "insight": "Costa Caribe colombiana y norte de Chile son mercados ideales. Temperatura > 30°C activa búsquedas masivas.",
                "nicho": "Hombres y mujeres 18-45 años, clima cálido"
            },
            "Sobrepeso / Control de peso": {
                "ico": "⚖️",
                "categoria": "Salud & Bienestar",
                "productos_sugeridos": ["Suplementos quemadores", "Proteína whey", "Fajas reductoras", "Té detox", "Colágeno hidrolizado"],
                "regiones_top": {"Bogotá": "muy_alto", "Medellín": "muy_alto", "Cali": "muy_alto", "Todas": "alto"},
                "regiones_chile": {"Santiago": "muy_alto", "Todas": "alto"},
                "temporada_pico": [1, 2, 3, 11, 12],
                "temporada_lbl": "Ene-Mar (año nuevo) y Nov-Dic (pre-navidad)",
                "insight": "Enero es el mes #1 de búsquedas de pérdida de peso globalmente. 'Propósitos de año nuevo' generan pico masivo.",
                "nicho": "Mujeres 25-45 años (principal), hombres secundario"
            },
            "Estrés / Ansiedad": {
                "ico": "🧠",
                "categoria": "Salud Mental & Bienestar",
                "productos_sugeridos": ["Magnesio suplemento", "Melatonina", "Ashwagandha", "CBD tópico", "Aromáticas relajantes", "Diarios de bienestar"],
                "regiones_top": {"Bogotá": "muy_alto", "Medellín": "alto", "Cali": "alto"},
                "regiones_chile": {"Santiago": "muy_alto", "Valparaíso": "alto"},
                "temporada_pico": [4, 5, 10, 11],
                "temporada_lbl": "Abr-May (mitad de año) y Oct-Nov (fin de año laboral)",
                "insight": "Grandes ciudades con alta presión laboral. Pandemia post-covid disparó búsquedas de bienestar mental permanentemente.",
                "nicho": "Profesionales 28-45 años, urbanos, NSE medio-alto"
            },
            "Dolor muscular / Articular": {
                "ico": "💪",
                "categoria": "Salud & Deportes",
                "productos_sugeridos": ["Crema analgésica", "Colágeno articular", "Vendas deportivas", "Aceite CBD tópico", "Suplemento articular"],
                "regiones_top": {"Bogotá": "alto", "Medellín": "alto", "Todas": "medio"},
                "regiones_chile": {"Todas": "alto"},
                "temporada_pico": [6, 7, 8, 1, 2],
                "temporada_lbl": "Jun-Ago (temporada deportiva) y Ene-Feb (resoluciones ejercicio)",
                "insight": "Adultos mayores de 40 años son el segmento principal. Deportistas amateur en aumento post-pandemia.",
                "nicho": "35-65 años, deportistas recreativos y adultos mayores activos"
            },
            "Piel grasa / Acné": {
                "ico": "🌿",
                "categoria": "Skincare",
                "productos_sugeridos": ["Limpiador facial poros", "Sérum niacinamida", "Hidratante oil-free", "Protector solar libre de aceite", "Mascarilla arcilla"],
                "regiones_top": {"Costa Caribe": "muy_alto", "Cali": "muy_alto", "Medellín": "alto", "Bogotá": "alto"},
                "regiones_chile": {"Norte Chile": "muy_alto", "Santiago": "alto"},
                "temporada_pico": [3, 4, 5, 6, 7, 8],
                "temporada_lbl": "Todo el año, pico en meses calurosos",
                "insight": "Climas húmedos y calurosos disparan el acné. Costa caribe y zona pacífica cálida son mercados prioritarios.",
                "nicho": "Jóvenes 15-30 años, ambos géneros"
            },
            "Insomnio / Mal dormir": {
                "ico": "🌙",
                "categoria": "Bienestar & Sueño",
                "productos_sugeridos": ["Melatonina", "Valerian root", "Antifaces sueño", "Almohadas ergonómicas", "Spray relajante"],
                "regiones_top": {"Bogotá": "muy_alto", "Medellín": "alto", "Todas": "medio"},
                "regiones_chile": {"Santiago": "muy_alto", "Todas": "alto"},
                "temporada_pico": [11, 12, 1, 5, 6],
                "temporada_lbl": "Nov-Ene (estrés navideño) y May-Jun (mitad de año laboral)",
                "insight": "Ciudades con alto ritmo laboral. Teletrabajo post-pandemia alteró ciclos del sueño masivamente.",
                "nicho": "Adultos 30-55 años, trabajadores con alta carga laboral"
            },
        }

        # ── Selector de problema ──
        _prob_sel = st.selectbox(
            "🔎 Selecciona el problema del consumidor:",
            list(PROBLEMAS_COMERCIALES.keys()),
            format_func=lambda x: f"{PROBLEMAS_COMERCIALES[x]['ico']} {x}",
            key="tend_problema_sel"
        )

        _prob = PROBLEMAS_COMERCIALES[_prob_sel]
        _mes_actual = _hoy_tend.month
        _es_temporada = _mes_actual in _prob["temporada_pico"]

        # ── Card principal del problema ──
        _color_prob = "#ef4444" if _es_temporada else "#5b6cfc"
        st.markdown(
            f'<div style="background:linear-gradient(135deg,{_color_prob}15,transparent);'
            f'border:1px solid {_color_prob}33;border-radius:14px;padding:20px 22px;margin:14px 0">'
            f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:14px">'
            f'<span style="font-size:2rem">{_prob["ico"]}</span>'
            f'<div>'
            f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:1.1rem">{_prob_sel}</div>'
            f'<div style="color:#a8b4d0;font-size:0.78rem">{_prob["categoria"]}</div>'
            f'</div>'
            f'<div style="margin-left:auto;background:{"#ef444420" if _es_temporada else "#5b6cfc20"};'
            f'color:{"#ef4444" if _es_temporada else "#5b6cfc"};padding:6px 14px;border-radius:20px;'
            f'font-size:0.78rem;font-weight:700">'
            f'{"🔴 TEMPORADA ACTIVA AHORA" if _es_temporada else "📅 Fuera de pico"}</div>'
            f'</div>'
            f'<div style="color:#c8d0e8;font-size:0.82rem;margin-bottom:12px">💡 {_prob["insight"]}</div>'
            f'<div style="display:flex;gap:8px;flex-wrap:wrap">'
            f'<span style="background:#1e2337;color:#a8b4d0;padding:4px 10px;border-radius:12px;font-size:0.72rem">👥 {_prob["nicho"]}</span>'
            f'<span style="background:#1e2337;color:#a8b4d0;padding:4px 10px;border-radius:12px;font-size:0.72rem">📅 Pico: {_prob["temporada_lbl"]}</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        _pc1, _pc2 = st.columns(2)

        with _pc1:
            st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.85rem;margin-bottom:10px">🛍️ Productos Recomendados</div>', unsafe_allow_html=True)
            for _pr in _prob["productos_sugeridos"]:
                st.markdown(f'<div style="background:#1a1535;border:1px solid #2e2558;border-radius:8px;padding:8px 12px;margin-bottom:6px;color:#c8d0e8;font-size:0.8rem">✅ {_pr}</div>', unsafe_allow_html=True)

            # Cruce con catálogo real si hay datos
            if C_PRODUCTO in df.columns:
                _prods_reales = df[C_PRODUCTO].dropna().unique()
                _match = [p for p in _prob["productos_sugeridos"] if any(p.lower() in str(r).lower() or str(r).lower() in p.lower() for r in _prods_reales)]
                if _match:
                    st.markdown(f'<div style="background:rgba(16,185,129,0.08);border:1px solid #10b981;border-radius:8px;padding:10px 12px;margin-top:8px;font-size:0.78rem;color:#10b981">✅ Tienes {len(_match)} producto(s) de este nicho en tu catálogo</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="background:rgba(245,158,11,0.08);border:1px solid #f59e0b;border-radius:8px;padding:10px 12px;margin-top:8px;font-size:0.78rem;color:#f59e0b">💡 Oportunidad: no tienes productos de este nicho aún</div>', unsafe_allow_html=True)

        with _pc2:
            st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.85rem;margin-bottom:10px">🗺️ Regiones con mayor demanda</div>', unsafe_allow_html=True)
            _RCOL = {"muy_alto": "#ef4444", "alto": "#f59e0b", "medio": "#5b6cfc", "bajo": "#8892b0"}
            _pais_tend = "Colombia" if (operacion and "Colombia" in operacion) else "Colombia"
            _regiones_mostrar = _prob["regiones_top"]
            for _reg, _niv in _regiones_mostrar.items():
                _cc = _RCOL.get(_niv, "#8892b0")
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;align-items:center;'
                    f'background:#1a1535;border:1px solid #2e2558;border-radius:8px;padding:8px 12px;margin-bottom:6px">'
                    f'<span style="color:#c8d0e8;font-size:0.8rem">📍 {_reg}</span>'
                    f'<span style="background:{_cc}20;color:{_cc};padding:3px 10px;border-radius:12px;font-size:0.7rem;font-weight:700">'
                    f'{"🔴 Muy Alta" if _niv=="muy_alto" else "🟡 Alta" if _niv=="alto" else "🔵 Media"}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            # Cruce con datos reales por departamento
            if C_DEPTO in df.columns:
                st.markdown('<div style="font-size:0.75rem;color:#a8b4d0;margin-top:10px;margin-bottom:6px">📊 Tu volumen actual por región:</div>', unsafe_allow_html=True)
                _dep_vol = df.groupby(C_DEPTO).size().sort_values(ascending=False).head(5)
                for _dep, _cnt in _dep_vol.items():
                    st.markdown(f'<div style="color:#a855f7;font-size:0.76rem;padding:4px 0">• {_dep}: {_cnt:,} pedidos</div>', unsafe_allow_html=True)

        # ── Resumen estratégico ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f'<div style="background:rgba(201,168,76,0.08);border:1px solid #f0c06044;border-radius:12px;padding:16px 18px">'
            f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#fcd34d;margin-bottom:10px">📌 Resumen Estratégico</div>'
            f'<div style="display:flex;gap:16px;flex-wrap:wrap">'
            f'<div><span style="color:#a8b4d0;font-size:0.75rem">Problema a explotar</span><br>'
            f'<span style="color:#e8ecf7;font-weight:700;font-size:0.85rem">{_prob_sel}</span></div>'
            f'<div><span style="color:#a8b4d0;font-size:0.75rem">Producto estrella</span><br>'
            f'<span style="color:#e8ecf7;font-weight:700;font-size:0.85rem">{_prob["productos_sugeridos"][0]}</span></div>'
            f'<div><span style="color:#a8b4d0;font-size:0.75rem">Región prioritaria</span><br>'
            f'<span style="color:#e8ecf7;font-weight:700;font-size:0.85rem">{list(_prob["regiones_top"].keys())[0]}</span></div>'
            f'<div><span style="color:#a8b4d0;font-size:0.75rem">Temporada pico</span><br>'
            f'<span style="color:{"#ef4444" if _es_temporada else "#f59e0b"};font-weight:700;font-size:0.85rem">'
            f'{"⚡ AHORA" if _es_temporada else _prob["temporada_lbl"]}</span></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

    # ════════════════════════════════════════
    # TAB 2 — CLIMA → PRODUCTOS
    # ════════════════════════════════════════
    with _tend_tab2:
        st.markdown('<div class="seccion-titulo">🌦️ Predicción por Clima</div>', unsafe_allow_html=True)

        ZONAS_CLIMA = {
            "🔥 Costa Caribe (Barranquilla, Cartagena, Santa Marta)": {
                "tipo": "calor", "temp": "28-35°C", "pais": "CO",
                "regiones": ["Barranquilla", "Cartagena", "Santa Marta", "Montería", "Valledupar"],
                "descripcion": "Calor extremo todo el año. Humedad muy alta.",
                "productos": [
                    ("Desodorante clínico 48h", "muy_alto"),
                    ("Protector solar SPF 50+", "muy_alto"),
                    ("Ropa ligera transpirable", "muy_alto"),
                    ("Ventiladores / enfriadores", "alto"),
                    ("Bebidas isotónicas", "alto"),
                    ("Chanclas y calzado abierto", "alto"),
                    ("Antifrizz capilar", "medio"),
                ],
                "evitar": ["Abrigos", "Thermos", "Calefacción"],
                "pico_mes": [3,4,5,6,7,8]
            },
            "🌡️ Zona Andina templada (Medellín, Cali, Pereira)": {
                "tipo": "templado", "temp": "18-26°C", "pais": "CO",
                "regiones": ["Medellín", "Cali", "Pereira", "Manizales", "Armenia"],
                "descripcion": "Clima primaveral permanente. Lluvias en abr-may y oct-nov.",
                "productos": [
                    ("Ropa casual versátil", "muy_alto"),
                    ("Accesorios de moda", "muy_alto"),
                    ("Cosméticos y maquillaje", "alto"),
                    ("Calzado casual", "alto"),
                    ("Paraguas compacto", "medio"),
                    ("Chaqueta liviana", "medio"),
                ],
                "evitar": ["Abrigos gruesos", "Calzado de invierno"],
                "pico_mes": [1,2,3,4,5,6,7,8,9,10,11,12]
            },
            "❄️ Zona Fría (Bogotá, Tunja, Pasto, Manizales altas)": {
                "tipo": "frio", "temp": "7-18°C", "pais": "CO",
                "regiones": ["Bogotá", "Tunja", "Pasto", "Ipiales"],
                "descripcion": "Frío constante. Temporada de lluvias marcada.",
                "productos": [
                    ("Buzos y chaquetas", "muy_alto"),
                    ("Thermos y mugs térmicos", "muy_alto"),
                    ("Cremas corporales hidratantes", "muy_alto"),
                    ("Vitaminas C y D", "alto"),
                    ("Cobijas y ropa de cama", "alto"),
                    ("Calzado cerrado impermeable", "alto"),
                    ("Humidificadores", "medio"),
                ],
                "evitar": ["Ropa de playa", "Ventiladores", "Ropa liviana"],
                "pico_mes": [6,7,8,9,10,11,12,1]
            },
            "🌧️ Zona Pacífica (Chocó, Buenaventura)": {
                "tipo": "lluvia", "temp": "24-30°C", "pais": "CO",
                "regiones": ["Quibdó", "Buenaventura", "Tumaco"],
                "descripcion": "La zona más lluviosa del mundo. Humedad extrema.",
                "productos": [
                    ("Impermeables y capas de lluvia", "muy_alto"),
                    ("Calzado impermeable", "muy_alto"),
                    ("Antifrizz capilar anti-humedad", "muy_alto"),
                    ("Paraguas resistentes", "alto"),
                    ("Antihongos", "alto"),
                    ("Ropa rápido secado", "alto"),
                ],
                "evitar": ["Ropa delicada", "Suede", "Cuero sin tratar"],
                "pico_mes": [1,2,3,4,5,6,7,8,9,10,11,12]
            },
            "🌨️ Sur de Chile (Valdivia, Puerto Montt, Punta Arenas)": {
                "tipo": "frio_lluvia", "temp": "3-14°C", "pais": "CL",
                "regiones": ["Valdivia", "Puerto Montt", "Osorno", "Punta Arenas"],
                "descripcion": "Frío intenso y lluvias todo el año. Vientos fuertes.",
                "productos": [
                    ("Abrigos y parkas", "muy_alto"),
                    ("Botas impermeables", "muy_alto"),
                    ("Calefactores portátiles", "alto"),
                    ("Ropa interior térmica", "muy_alto"),
                    ("Cremas hidratantes intensivas", "alto"),
                    ("Gorros y guantes", "alto"),
                ],
                "evitar": ["Ropa de verano", "Sandalias", "Telas delgadas"],
                "pico_mes": [4,5,6,7,8,9]
            },
            "☀️ Norte de Chile (Atacama, Antofagasta, Arica)": {
                "tipo": "desierto", "temp": "15-28°C", "pais": "CL",
                "regiones": ["Arica", "Antofagasta", "Iquique", "Copiapó"],
                "descripcion": "Desierto. Días calurosos, noches frías. Radiación UV muy alta.",
                "productos": [
                    ("Protector solar SPF 70+", "muy_alto"),
                    ("Ropa UV protection", "muy_alto"),
                    ("Gafas de sol polarizadas", "muy_alto"),
                    ("Hidratación corporal intensa", "alto"),
                    ("Ropa ligera de secado rápido", "alto"),
                ],
                "evitar": ["Ropa negra", "Abrigos pesados en temporada"],
                "pico_mes": [10,11,12,1,2,3]
            },
        }

        _zona_sel = st.selectbox(
            "🌍 Selecciona la zona climática:",
            list(ZONAS_CLIMA.keys()),
            key="tend_zona_sel",
            label_visibility="collapsed"
        )

        _zona = ZONAS_CLIMA[_zona_sel]
        _mes_act = _hoy_tend.month
        _es_pico_z = _mes_act in _zona["pico_mes"]

        _TIPO_COLOR = {"calor": "#ef4444", "templado": "#10b981", "frio": "#00d4ff", "lluvia": "#5b6cfc", "frio_lluvia": "#7c3aed", "desierto": "#f59e0b"}
        _TIPO_ICO   = {"calor": "🔥", "templado": "🌤️", "frio": "❄️", "lluvia": "🌧️", "frio_lluvia": "🌨️", "desierto": "☀️"}
        _color_z = _TIPO_COLOR.get(_zona["tipo"], "#5b6cfc")
        _ico_z   = _TIPO_ICO.get(_zona["tipo"], "🌍")

        # Header zona
        st.markdown(
            f'<div style="background:{_color_z}10;border:1px solid {_color_z}33;border-radius:12px;padding:16px 18px;margin:12px 0">'
            f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">'
            f'<span style="font-size:1.8rem">{_ico_z}</span>'
            f'<div>'
            f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7">{_zona_sel}</div>'
            f'<div style="color:#a8b4d0;font-size:0.78rem">{_zona["descripcion"]} · Temp: {_zona["temp"]}</div>'
            f'</div>'
            f'<div style="margin-left:auto;background:{"#ef444420" if _es_pico_z else "#1e2337"};'
            f'color:{"#ef4444" if _es_pico_z else "#8892b0"};padding:5px 12px;border-radius:20px;font-size:0.75rem;font-weight:700">'
            f'{"⚡ Temporada activa AHORA" if _es_pico_z else "Fuera de temporada pico"}</div>'
            f'</div>'
            f'<div style="display:flex;gap:6px;flex-wrap:wrap">'
            + "".join(f'<span style="background:#1e2337;color:#a8b4d0;padding:3px 8px;border-radius:10px;font-size:0.7rem">📍 {r}</span>' for r in _zona["regiones"][:4]) +
            f'</div></div>',
            unsafe_allow_html=True
        )

        _zc1, _zc2 = st.columns([3, 2])

        with _zc1:
            st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.85rem;margin-bottom:10px">🛍️ Productos recomendados para esta zona</div>', unsafe_allow_html=True)
            _NIVEL_C = {"muy_alto": "#ef4444", "alto": "#f59e0b", "medio": "#5b6cfc"}
            for _prod_z, _niv_z in _zona["productos"]:
                _cc_z = _NIVEL_C.get(_niv_z, "#8892b0")
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;align-items:center;'
                    f'background:#1a1535;border:1px solid {_cc_z}22;border-radius:8px;padding:9px 12px;margin-bottom:5px">'
                    f'<span style="color:#c8d0e8;font-size:0.8rem">✅ {_prod_z}</span>'
                    f'<span style="background:{_cc_z}20;color:{_cc_z};padding:2px 8px;border-radius:10px;font-size:0.68rem;font-weight:700">'
                    f'{"Alta demanda" if _niv_z=="muy_alto" else "Buena demanda" if _niv_z=="alto" else "Moderada"}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        with _zc2:
            st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.85rem;margin-bottom:10px">❌ Evitar en esta zona</div>', unsafe_allow_html=True)
            for _ev in _zona["evitar"]:
                st.markdown(f'<div style="background:rgba(239,68,68,0.06);border:1px solid #ef444422;border-radius:8px;padding:8px 12px;margin-bottom:5px;color:#ef4444;font-size:0.78rem">❌ {_ev}</div>', unsafe_allow_html=True)

            # Cruce con pedidos reales por depto
            if C_DEPTO in df.columns:
                st.markdown("<br>", unsafe_allow_html=True)
                _pedidos_zona = df[df[C_DEPTO].astype(str).str.upper().isin([r.upper() for r in _zona["regiones"]])]
                if len(_pedidos_zona) > 0:
                    _ing_zona = _pedidos_zona[C_TOTAL].sum() if C_TOTAL in _pedidos_zona.columns else 0
                    st.markdown(
                        f'<div style="background:rgba(16,185,129,0.08);border:1px solid #10b981;border-radius:10px;padding:12px">'
                        f'<div style="color:#10b981;font-size:0.78rem;font-weight:700">📊 Tus datos en esta zona</div>'
                        f'<div style="color:#e8ecf7;font-size:1.1rem;font-weight:800;margin-top:4px">{len(_pedidos_zona):,} pedidos</div>'
                        f'<div style="color:#a8b4d0;font-size:0.72rem">{fmt_money(_ing_zona)} en ventas</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown('<div style="background:rgba(245,158,11,0.08);border:1px solid #f59e0b;border-radius:10px;padding:12px;color:#f59e0b;font-size:0.78rem">💡 Sin pedidos registrados en esta zona — oportunidad de expansión</div>', unsafe_allow_html=True)

    # ════════════════════════════════════════
    # TAB 3 — ANÁLISIS INTELIGENTE PRODUCTOS
    # ════════════════════════════════════════
    with _tend_tab3:
        st.markdown('<div class="seccion-titulo">📊 Análisis Inteligente de Productos</div>', unsafe_allow_html=True)

        if C_PRODUCTO not in df.columns:
            st.warning("Sube tu Excel con columna de productos para activar este análisis.")
        else:
            # Calcular métricas por producto
            _df_prod = df.copy()
            _grp_cols = {C_PRODUCTO: "Pedidos"}
            if C_TOTAL in df.columns:    _grp_cols[C_TOTAL] = "Ingresos"
            if C_GANANCIA in df.columns: _grp_cols[C_GANANCIA] = "Ganancia"

            _prod_stats = _df_prod.groupby(C_PRODUCTO).agg(
                Pedidos=(C_PRODUCTO, "count"),
                **({} if C_TOTAL not in df.columns else {"Ingresos": (C_TOTAL, "sum")}),
                **({} if C_GANANCIA not in df.columns else {"Ganancia": (C_GANANCIA, "sum")}),
            ).reset_index()

            _total_ped = _prod_stats["Pedidos"].sum()
            _prod_stats["% Participación"] = (_prod_stats["Pedidos"] / _total_ped * 100).round(1)
            _prod_stats = _prod_stats.sort_values("Pedidos", ascending=False)

            _top_n = min(10, len(_prod_stats))
            _prod_top    = _prod_stats.head(_top_n)
            _prod_bottom = _prod_stats.tail(min(5, len(_prod_stats)))

            # KPIs rápidos
            _k1, _k2, _k3, _k4 = st.columns(4)
            with _k1: st.markdown(kpi("blue", "🏷️ Productos únicos", f"{len(_prod_stats):,}"), unsafe_allow_html=True)
            with _k2: st.markdown(kpi("green", "🏆 Producto estrella", str(_prod_top.iloc[0][C_PRODUCTO])[:22]), unsafe_allow_html=True)
            with _k3:
                _prod_low = str(_prod_bottom.iloc[0][C_PRODUCTO])[:22]
                st.markdown(kpi("red", "📉 Menor rotación", _prod_low), unsafe_allow_html=True)
            with _k4:
                _conc = round(_prod_top.head(3)["% Participación"].sum(), 1)
                st.markdown(kpi("gold", "🎯 Concentración Top 3", f"{_conc}%", "del total de pedidos"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            _ai1, _ai2 = st.columns([3, 2])

            with _ai1:
                # Gráfico top productos
                if C_GANANCIA in _prod_stats.columns:
                    fig_ai = px.bar(
                        _prod_top, x="Ganancia", y=C_PRODUCTO,
                        orientation="h",
                        color="% Participación",
                        color_continuous_scale=["#12151f","#5b6cfc","#f0c060"],
                        title="Top Productos por Ganancia"
                    )
                else:
                    fig_ai = px.bar(
                        _prod_top, x="Pedidos", y=C_PRODUCTO,
                        orientation="h",
                        color="% Participación",
                        color_continuous_scale=["#12151f","#5b6cfc","#f0c060"],
                        title="Top Productos por Volumen"
                    )
                fig_ai.update_layout(**PLOT_LAYOUT, height=380, coloraxis_showscale=False, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                st.plotly_chart(fig_ai, use_container_width=True)

            with _ai2:
                st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.85rem;margin-bottom:12px">🤖 Recomendaciones IA</div>', unsafe_allow_html=True)

                # Qué escalar
                _escalar = _prod_top.head(3)[C_PRODUCTO].tolist()
                st.markdown(
                    '<div style="background:rgba(16,185,129,0.08);border:1px solid #10b981;border-radius:10px;padding:12px;margin-bottom:8px">'
                    '<div style="color:#10b981;font-size:0.78rem;font-weight:700;margin-bottom:6px">📈 Escalar (más pauta)</div>'
                    + "".join(f'<div style="color:#c8d0e8;font-size:0.76rem;margin-bottom:3px">• {p}</div>' for p in _escalar) +
                    '</div>',
                    unsafe_allow_html=True
                )

                # Qué revisar / eliminar
                _eliminar = _prod_bottom.head(3)[C_PRODUCTO].tolist()
                st.markdown(
                    '<div style="background:rgba(239,68,68,0.08);border:1px solid #ef4444;border-radius:10px;padding:12px;margin-bottom:8px">'
                    '<div style="color:#ef4444;font-size:0.78rem;font-weight:700;margin-bottom:6px">📉 Revisar / Liquidar</div>'
                    + "".join(f'<div style="color:#c8d0e8;font-size:0.76rem;margin-bottom:3px">• {p}</div>' for p in _eliminar) +
                    '</div>',
                    unsafe_allow_html=True
                )

                # Oportunidad: productos de temporada no en catálogo
                _mes_actual2 = _hoy_tend.month
                TEMP_SUGERIDOS = {
                    (12,1,2): ["Cobijas", "Thermos", "Cremas hidratantes", "Ropa abrigo"],
                    (3,4,5): ["Perfumes", "Accesorios moda", "Joyería", "Flores artificiales"],
                    (6,7,8): ["Protector solar", "Ropa ligera", "Artículos playa", "Gafas de sol"],
                    (9,10,11): ["Disfraces Halloween", "Electrónicos", "Regalos navidad", "Gadgets"]
                }
                _sugs = []
                for _meses_t, _prods_t in TEMP_SUGERIDOS.items():
                    if _mes_actual2 in _meses_t:
                        _prods_reales2 = df[C_PRODUCTO].dropna().str.lower().tolist()
                        _sugs = [p for p in _prods_t if not any(p.lower() in r for r in _prods_reales2)]
                        break

                if _sugs:
                    st.markdown(
                        '<div style="background:rgba(245,158,11,0.08);border:1px solid #f59e0b;border-radius:10px;padding:12px">'
                        '<div style="color:#f59e0b;font-size:0.78rem;font-weight:700;margin-bottom:6px">💡 Probar (temporada actual)</div>'
                        + "".join(f'<div style="color:#c8d0e8;font-size:0.76rem;margin-bottom:3px">• {p}</div>' for p in _sugs[:4]) +
                        '</div>',
                        unsafe_allow_html=True
                    )


# ═══════════════════════════════════════════════════════════
# ██████  VISTA 2: OPERACIONES
# ═══════════════════════════════════════════════════════════
elif "Operaciones" in vista_activa or "Asistente" in vista_activa or "Monitor" in vista_activa:
    op_nombre = operacion.split("  ")[1]
    op_color  = op_info["color"]
    op_pais   = op_info["pais"]
    op_moneda = op_info["moneda"]
    clp_badge2 = (f"&nbsp;&nbsp;&middot;&nbsp;&nbsp;<span style='color:#f97316;font-size:0.78rem'>"
                  f"&#x1F4B1; CLP&#8594;COP @ {trm_clp_cop}</span>") if es_clp else ""

    st.markdown(
        f'<div style="margin-bottom:28px;background:linear-gradient(135deg,#12151f,#161929);'
        f'border:1px solid #2e2558;border-radius:16px;padding:24px 28px">'
        f'<div style="display:flex;align-items:center;gap:16px">'
        f'<div style="width:4px;height:54px;background:{op_color};border-radius:4px"></div>'
        f'<div>'
        f'<div style="font-size:0.68rem;color:#7a8aaa;font-weight:700;letter-spacing:0.12em;'
        f'text-transform:uppercase;margin-bottom:5px">{op_pais} &nbsp;·&nbsp; {op_moneda}</div>'
        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-size:1.9rem;font-weight:800;'
        f'color:#e8ecf7;line-height:1;margin-bottom:6px">{op_nombre}</div>'
        f'<div style="color:#a8b4d0;font-size:0.83rem">'
        f'Operaciones &nbsp;·&nbsp; Centro de control &nbsp;·&nbsp; {total:,} pedidos{clp_badge2}'
        f'</div></div></div></div>',
        unsafe_allow_html=True
    )

    # KPIs operativos
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: st.markdown(kpi("blue","Total",f"{total:,}"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("green","✅ Entregados",f"{entregados:,}",f"{pct_ent}%"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("red","❌ Cancelados",f"{cancelados:,}"), unsafe_allow_html=True)
    with c4: st.markdown(kpi("gold","🔄 En Proceso",f"{en_proceso:,}"), unsafe_allow_html=True)
    with c5: st.markdown(kpi("purple","↩️ Devolución",f"{devolucion:,}"), unsafe_allow_html=True)
    with c6: st.markdown(kpi("cyan","⚠️ Novedades",f"{novedades:,}"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs de navegación operacional ──
    if "Monitor" in vista_activa:
        op_nav = "📊 Monitor de Estatus"
    else:
        op_nav = st.radio("", [
            "🚨 Alertas de Pedidos",
            "📦 Monitor de Pedidos",
            "📊 Monitor de Estatus",
            "📋 Monitor Financiero",
            "🗓️ Calendario Estratégico",
            "🚚 Transportadoras",
            "👥 Proveedores",
            "📦 Stock & Inventario",
            "🔁 Devoluciones",
            "📋 Novedades",
            "🏷️ Tags",
        ], horizontal=True, label_visibility="collapsed")

    # ══════════════════════════════════════════════════════
    # MONITOR DE ESTATUS — Tabla dinámica por semanas
    # ══════════════════════════════════════════════════════
    if "Alertas" in op_nav and C_ESTATUS in df.columns:

        st.markdown('<div class="seccion-titulo">🚨 Monitor de Alertas de Pedidos</div>', unsafe_allow_html=True)

        # ══ CALCULAR TODAS LAS ALERTAS ══
        # ── Configuración de umbrales por días desde despacho ──
        from datetime import date, timedelta
        hoy = date.today()

        col_umb1, col_umb2 = st.columns([3,1])
        with col_umb1:
            st.markdown(
                f'<div style="background:rgba(99,102,241,0.07);border:1px solid #2e2558;border-radius:10px;'
                f'padding:10px 16px;font-size:0.8rem;color:#a8b4d0">'
                f'<b style="color:#a5b4fc">⚙️ Umbrales activos:</b> &nbsp; '
                f'🔴 Crítico = pedidos despachados hace más de <b style="color:#ef4444">15 días</b> &nbsp;·&nbsp; '
                f'🟡 Medio = más de <b style="color:#f59e0b">5 días</b> &nbsp;·&nbsp; '
                f'🟢 Leve = más de <b style="color:#34d399">2 días</b>'
                f'</div>', unsafe_allow_html=True
            )
        with col_umb2:
            dias_critico = st.number_input("🔴 Días crítico", 1, 30, 15, key="umb_crit")
            dias_medio   = st.number_input("🟡 Días medio",   1, 20, 5, key="umb_med")
            dias_leve    = st.number_input("🟢 Días leve",    1, 10, 2, key="umb_leve")

        fecha_critico = hoy - timedelta(days=dias_critico)
        fecha_medio   = hoy - timedelta(days=dias_medio)
        fecha_leve    = hoy - timedelta(days=dias_leve)

        alertas = []

        for _, row in df.iterrows():
            est    = str(row.get(C_ESTATUS, '')).upper()
            d_m    = row.get('_d_mov')    # días desde último movimiento
            d_p    = row.get('_d_ped')    # días desde pedido
            h_m    = row.get('_h_mov')    # horas desde último movimiento
            num    = str(row.get(C_ID,  '—'))
            cli    = str(row.get(C_CLIENTE, ''))[:28] if C_CLIENTE in df.columns else ''
            guia   = str(row.get(C_GUIA, ''))         if C_GUIA    in df.columns else ''
            ciudad = str(row.get(C_CIUDAD, ''))        if C_CIUDAD  in df.columns else ''
            valor  = row.get(C_TOTAL, 0)               if C_TOTAL   in df.columns else 0
            transp = str(row.get(C_TRANSP, ''))        if C_TRANSP  in df.columns else ''

            # Fecha real de despacho/movimiento
            f_mov_raw = row.get(C_FECHA_MOV) if C_FECHA_MOV in df.columns else None
            f_ped_raw = row.get(C_FECHA)     if C_FECHA     in df.columns else None
            try:
                f_mov = pd.to_datetime(f_mov_raw).date() if f_mov_raw and not pd.isna(f_mov_raw) else None
            except: f_mov = None
            try:
                f_ped = pd.to_datetime(f_ped_raw).date() if f_ped_raw and not pd.isna(f_ped_raw) else None
            except: f_ped = None

            # Referencia de fecha: primero movimiento, si no pedido
            f_ref = f_mov or f_ped

            def nivel_por_fecha(f):
                if f is None: return None
                if f <= fecha_critico: return 1
                if f <= fecha_medio:   return 2
                if f <= fecha_leve:    return 3
                return None  # muy reciente, sin alerta

            def dias_txt(f):
                if f is None: return ''
                dias = (hoy - f).days
                return f"Despachado hace {dias} días ({f.strftime('%d/%m')})"

            def add(nivel, tipo, icono, detalle):
                alertas.append({
                    'nivel': nivel, 'tipo': tipo, 'icono': icono,
                    'id': num, 'cliente': cli, 'guia': guia,
                    'ciudad': ciudad, 'valor': valor, 'transp': transp,
                    'tiempo': detalle, 'estatus': est,
                    'fecha_ref': str(f_ref) if f_ref else ''
                })

            # ── REGLAS POR TIPO DE ESTATUS ──

            # Pedidos en Reparto sin cambio
            if 'REPARTO' in est:
                niv = nivel_por_fecha(f_ref)
                if niv:
                    tipo_txt = 'En Reparto — CRÍTICO' if niv==1 else 'En Reparto — Demorado' if niv==2 else 'En Reparto — Revisar'
                    add(niv, tipo_txt, '🔴' if niv==1 else '🟡' if niv==2 else '🟢', dias_txt(f_ref))

            # Novedades sin resolver
            elif 'NOVEDAD' in est:
                sol = str(row.get(C_NOV_SOL, '')).upper() if C_NOV_SOL in df.columns else ''
                if 'SI' not in sol and 'SÍ' not in sol:
                    nov_txt = str(row.get(C_NOVEDAD, ''))[:35] if C_NOVEDAD in df.columns else ''
                    niv = nivel_por_fecha(f_ref)
                    if niv:
                        tipo_txt = f'Novedad — {nov_txt or "Sin tipo"}'
                        add(niv, tipo_txt, '🔴' if niv==1 else '🟡' if niv==2 else '🟢', dias_txt(f_ref))

            # Reclamos en oficina — usar días desde pedido
            elif 'RECLAM' in est or 'OFICINA' in est:
                niv = nivel_por_fecha(f_ped)
                if niv:
                    add(niv, 'Reclamo en Oficina', '🔴' if niv==1 else '🟡', dias_txt(f_ped))

            # BDG Transportadora
            elif 'BDG TRANSP' in est or 'BODEGA TRANS' in est:
                niv = nivel_por_fecha(f_ref)
                if niv:
                    add(niv, 'BDG Transportadora', '🔴' if niv==1 else '🟡' if niv==2 else '🟢', dias_txt(f_ref))

            # BDG Proveedor
            elif 'BDG PROV' in est or 'BODEGA PROV' in est:
                niv = nivel_por_fecha(f_ref)
                if niv:
                    add(niv, 'BDG Proveedor', '🔴' if niv==1 else '🟡', dias_txt(f_ref))

        df_al = pd.DataFrame(alertas) if alertas else pd.DataFrame(
            columns=['nivel','tipo','icono','id','cliente','guia','ciudad','valor','transp','tiempo','estatus'])
        df_al = df_al.sort_values('nivel') if len(df_al) else df_al

        n_crit = len(df_al[df_al['nivel']==1]) if len(df_al) else 0
        n_med  = len(df_al[df_al['nivel']==2]) if len(df_al) else 0
        n_leve = len(df_al[df_al['nivel']==3]) if len(df_al) else 0

        # ══ KPIs de alertas ══
        ka1,ka2,ka3,ka4 = st.columns(4)
        with ka1: st.markdown(kpi("blue","📋 Total Alertas",f"{len(df_al):,}"), unsafe_allow_html=True)
        with ka2: st.markdown(kpi("red","🔴 Críticas",f"{n_crit:,}","Acción inmediata"), unsafe_allow_html=True)
        with ka3: st.markdown(kpi("gold","🟡 Medias",f"{n_med:,}","Revisar hoy"), unsafe_allow_html=True)
        with ka4: st.markdown(kpi("green","🟢 Leves",f"{n_leve:,}","Monitorear"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ══ FILTROS ══
        fa1, fa2, fa3, fa4 = st.columns([2,2,2,2])
        with fa1:
            filtro_nivel = st.selectbox("🎯 Nivel", ["Todos","🔴 Crítico","🟡 Medio","🟢 Leve"], key="f_nivel")
        with fa2:
            tipos_disp = ["Todos"] + sorted(df_al['tipo'].unique().tolist()) if len(df_al) else ["Todos"]
            filtro_tipo = st.selectbox("📂 Tipo", tipos_disp, key="f_tipo")
        with fa3:
            filtro_buscar = st.text_input("🔍 Buscar pedido / cliente / guía", key="f_buscar", placeholder="Ej: 66644268")
        with fa4:
            if len(df_al):
                transp_disp = ["Todas"] + sorted(df_al['transp'].replace('','Sin info').unique().tolist())
                filtro_transp = st.selectbox("🚚 Transportadora", transp_disp, key="f_transp")
            else:
                filtro_transp = "Todas"

        # Aplicar filtros
        df_fil = df_al.copy()
        if filtro_nivel != "Todos":
            nivel_map = {"🔴 Crítico":1,"🟡 Medio":2,"🟢 Leve":3}
            df_fil = df_fil[df_fil['nivel']==nivel_map[filtro_nivel]]
        if filtro_tipo != "Todos":
            df_fil = df_fil[df_fil['tipo']==filtro_tipo]
        if filtro_buscar:
            mask = (df_fil['id'].str.contains(filtro_buscar, case=False, na=False) |
                    df_fil['cliente'].str.contains(filtro_buscar, case=False, na=False) |
                    df_fil['guia'].str.contains(filtro_buscar, case=False, na=False))
            df_fil = df_fil[mask]
        if filtro_transp != "Todas":
            df_fil = df_fil[df_fil['transp'].replace('','Sin info')==filtro_transp]

        st.caption(f"Mostrando **{len(df_fil):,}** de {len(df_al):,} alertas")

        # ══ EXPORTAR ══
        if len(df_fil):
            df_export = df_fil[[c for c in ['nivel','icono','tipo','id','cliente','guia','ciudad','transp','valor','tiempo','fecha_ref','estatus'] if c in df_fil.columns]].copy()
            rename_map = {'nivel':'Prioridad','icono':'Nivel','tipo':'Tipo Alerta','id':'# Pedido','cliente':'Cliente','guia':'Guía','ciudad':'Ciudad','transp':'Transportadora','valor':'Valor Orden','tiempo':'Tiempo transcurrido','fecha_ref':'Fecha despacho','estatus':'Estatus'}
            df_export = df_export.rename(columns=rename_map)
            df_export['Prioridad'] = df_export['Prioridad'].map({1:'CRÍTICO',2:'MEDIO',3:'LEVE'})
            import io
            buf = io.BytesIO()
            df_export.to_excel(buf, index=False, engine='openpyxl')
            st.download_button("⬇️ Exportar alertas a Excel", buf.getvalue(),
                               file_name="alertas_pedidos.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        st.markdown("<br>", unsafe_allow_html=True)

        # ══ RENDERIZAR TARJETAS DE ALERTAS ══
        NIVEL_STYLE = {
            1: {"bg":"rgba(239,68,68,0.08)",  "border":"#ef4444", "badge":"#ef4444", "label":"CRÍTICO"},
            2: {"bg":"rgba(245,158,11,0.08)", "border":"#f59e0b", "badge":"#f59e0b", "label":"MEDIO"},
            3: {"bg":"rgba(52,211,153,0.08)", "border":"#34d399", "badge":"#34d399", "label":"LEVE"},
        }

        PAGE_SIZE = 50
        total_pags = max(1, -(-len(df_fil) // PAGE_SIZE))
        if total_pags > 1:
            pag = st.slider("Página", 1, total_pags, 1, key="pag_alertas")
        else:
            pag = 1
        df_pag = df_fil.iloc[(pag-1)*PAGE_SIZE : pag*PAGE_SIZE]

        if len(df_pag) == 0:
            st.markdown('<div style="text-align:center;padding:40px;color:#34d399;font-size:1.1rem">✅ Sin alertas con los filtros seleccionados</div>', unsafe_allow_html=True)
        else:
            for _, row in df_pag.iterrows():
                s = NIVEL_STYLE.get(row['nivel'], NIVEL_STYLE[3])
                valor_txt = f"$ {int(row['valor']):,}" if row['valor'] else ''
                guia_txt  = f"Guía: {row['guia']}" if row['guia'] and row['guia'] != 'nan' else ''
                transp_txt= row['transp'] if row['transp'] and row['transp'] != 'nan' else ''
                ciudad_txt= row['ciudad'] if row['ciudad'] and row['ciudad'] != 'nan' else ''

                detalles = ' · '.join(filter(None, [guia_txt, transp_txt, ciudad_txt, valor_txt]))

                valor_fmt = f"${int(row['valor']):,}" if row['valor'] else ''
                html_card = (
                    f'<div style="background:{s["bg"]};border:1px solid {s["border"]}33;'
                    f'border-left:4px solid {s["border"]};border-radius:0 12px 12px 0;'
                    f'padding:13px 18px;margin-bottom:6px;display:flex;align-items:stretch;gap:16px">'

                    # Columna izquierda — nivel badge
                    f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;'
                    f'min-width:62px;background:{s["badge"]}18;border-radius:8px;padding:6px 4px">'
                    f'<div style="font-size:1.4rem;line-height:1">{row["icono"]}</div>'
                    f'<div style="font-size:0.58rem;color:{s["badge"]};font-weight:900;'
                    f'letter-spacing:0.1em;margin-top:4px;text-transform:uppercase">{s["label"]}</div>'
                    f'</div>'

                    # Columna centro — info principal
                    f'<div style="flex:1;min-width:0">'
                    f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;'
                    f'font-size:0.87rem;margin-bottom:4px">'
                    f'{row["tipo"]}'
                    f'</div>'
                    f'<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:5px">'
                    f'<span style="background:rgba(201,168,76,0.15);color:#fcd34d;font-weight:700;'
                    f'font-size:0.78rem;padding:2px 8px;border-radius:6px">#{row["id"]}</span>'
                    f'<span style="color:#c8d0e8;font-size:0.82rem">{row["cliente"]}</span>'
                    f'</div>'
                    f'<div style="color:#7a8aaa;font-size:0.75rem;display:flex;gap:12px;flex-wrap:wrap">'
                    f'<span>&#x23F1; {row["tiempo"]}</span>'
                    f'{("<span>&#x1F6A9; " + detalles + "</span>") if detalles else ""}'
                    f'</div>'
                    f'</div>'

                    # Columna derecha — valor
                    f'<div style="display:flex;flex-direction:column;align-items:flex-end;justify-content:center;'
                    f'min-width:80px;text-align:right">'
                    f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#10b981;font-size:0.88rem">'
                    f'{valor_fmt}'
                    f'</div>'
                    f'{"<div style=\"font-size:0.7rem;color:#6b7a9e\">" + row["transp"][:14] + "</div>" if row["transp"] and row["transp"] != "nan" else ""}'
                    f'</div>'

                    f'</div>'
                )
                st.markdown(html_card, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # 📊 MONITOR DE ESTATUS — Tabla por semanas
    # ══════════════════════════════════════════════════════════════════
    elif "Estatus" in op_nav:
        st.markdown('<div class="seccion-titulo">📊 Monitor de Estatus Financiero — Resumen Semanal</div>', unsafe_allow_html=True)

        # ── Detectar columna Estatus Financiero ──
        col_ef = C_ESTATUS_FIN if C_ESTATUS_FIN in df.columns else None
        if col_ef is None:
            # Búsqueda flexible
            col_ef = next((c for c in df.columns if "FINANCIERO" in c.upper() and "ESTATUS" in c.upper()), None)

        if col_ef is None:
            st.markdown(
                '<div style="background:rgba(245,158,11,0.08);border:1px solid #f59e0b44;border-radius:14px;'
                'padding:28px;text-align:center">'
                '<div style="font-size:2rem;margin-bottom:10px">📋</div>'
                '<div style="color:#f59e0b;font-weight:800;font-family:Plus Jakarta Sans,sans-serif;font-size:1rem;margin-bottom:8px">'
                'Columna "ESTATUS FINANCIERO" no encontrada en el Excel</div>'
                '<div style="color:#a8b4d0;font-size:0.82rem;line-height:1.6">'
                'Asegúrate de que tu reporte incluya la columna <b style="color:#e8ecf7">ESTATUS FINANCIERO</b>.<br>'
                'Esta columna es la base del Monitor de Estatus — agrúpala por estado financiero de cada pedido.</div>'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            # ── Paleta de colores por Estatus Financiero ──
            COLORES_EF = {
                "PAGADO":              "#10b981",
                "COBRADO":             "#10b981",
                "ENTREGADO":           "#10b981",
                "PENDIENTE":           "#f59e0b",
                "POR COBRAR":          "#f59e0b",
                "EN PROCESO":          "#00d4ff",
                "EN CAMINO":           "#00d4ff",
                "CANCELADO":           "#ef4444",
                "CANCELADA":           "#ef4444",
                "DEVOLUCION":          "#f97316",
                "DEVOLUCIÓN":          "#f97316",
                "EN DEVOLUCIÓN":       "#f97316",
                "NOVEDAD":             "#7c3aed",
                "FRAUDE":              "#dc2626",
                "RECHAZADO":           "#dc2626",
                "PERDIDA":             "#dc2626",
                "PÉRDIDA":             "#dc2626",
                "REEMBOLSO":           "#ec4899",
                "TOTAL GENERAL":       "#f0c060",
            }

            def get_color_ef(estatus_str):
                est_up = str(estatus_str).upper()
                for k, v in COLORES_EF.items():
                    if k in est_up:
                        return v
                return "#8892b0"

            # ── Columnas de métricas ──
            C_UND_E  = C_CANTIDAD
            C_CLTS_E = C_CLIENTE
            C_PDD_E  = C_TOTAL
            C_UTIL_E = C_GANANCIA
            C_CST_E  = "PRECIO PROVEEDOR X CANTIDAD"
            C_FLT_E  = C_FLETE

            # ── Selector de mes + tabs de semanas ──
            meses_ef = sorted(df['_mes'].dropna().unique().tolist(), reverse=True) if '_mes' in df.columns else []
            col_mes, col_info = st.columns([2,3])
            with col_mes:
                mes_ef = st.selectbox("📅 Mes", ["Mes completo"] + meses_ef if meses_ef else ["Mes completo"], key="mes_ef_mon")
            with col_info:
                total_ef_vals = df[col_ef].dropna().astype(str).str.strip().unique().tolist()
                st.markdown(
                    f'<div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:6px">'
                    + ''.join([
                        f'<span style="background:{get_color_ef(v)}18;color:{get_color_ef(v)};'
                        f'border:1px solid {get_color_ef(v)}44;border-radius:20px;padding:3px 10px;'
                        f'font-size:0.7rem;font-weight:700">{v}</span>'
                        for v in sorted(total_ef_vals)[:12]
                    ])
                    + '</div>',
                    unsafe_allow_html=True
                )

            # Filtrar por mes
            df_ef = df[df['_mes'] == mes_ef].copy() if mes_ef != "Mes completo" and '_mes' in df.columns else df.copy()

            semana_tabs_ef = st.tabs(["📅 Mes Completo", "Sem 1  (1-8)", "Sem 2  (9-16)", "Sem 3  (17-24)", "Sem 4  (25-31)"])

            def semana_df_ef(df_base, sem):
                if sem == 0: return df_base
                rangos = {1:(1,8), 2:(9,16), 3:(17,24), 4:(25,31)}
                ini, fin = rangos[sem]
                try:
                    return df_base[pd.to_datetime(df_base[C_FECHA], errors='coerce').dt.day.between(ini, fin)] if C_FECHA in df_base.columns else df_base
                except:
                    return df_base

            def construir_tabla_ef(df_filtrado):
                if len(df_filtrado) == 0:
                    return pd.DataFrame()

                tiene_und  = C_UND_E  in df_filtrado.columns
                tiene_clts = C_CLTS_E in df_filtrado.columns
                tiene_pdd  = C_PDD_E  in df_filtrado.columns
                tiene_util = C_UTIL_E in df_filtrado.columns
                tiene_cst  = C_CST_E  in df_filtrado.columns
                tiene_flt  = C_FLT_E  in df_filtrado.columns

                total_pdd_g = df_filtrado[C_PDD_E].sum() if tiene_pdd else 1
                grupos = df_filtrado.groupby(col_ef)
                filas = []

                for estatus, grp in grupos:
                    fila = {"Estatus Financiero": str(estatus)}
                    fila["# PED"]  = len(grp)
                    if tiene_und:  fila["# UND"]  = int(grp[C_UND_E].sum())
                    if tiene_clts: fila["# CLTS"] = grp[C_CLTS_E].nunique()
                    if tiene_pdd:  fila["$ PDD"]  = grp[C_PDD_E].sum()
                    if tiene_util: fila["$ UTIL"] = grp[C_UTIL_E].sum()
                    if tiene_cst:  fila["$ CST"]  = grp[C_CST_E].sum()
                    if tiene_flt:  fila["$ FLT"]  = grp[C_FLT_E].sum()
                    if tiene_pdd:  fila["% PDD"]  = grp[C_PDD_E].sum() / total_pdd_g * 100
                    filas.append(fila)

                sort_col = "$ PDD" if "$ PDD" in (filas[0] if filas else {}) else "# PED"
                tabla = pd.DataFrame(filas).sort_values(sort_col, ascending=False)

                # Fila TOTAL
                total_fila = {"Estatus Financiero": "TOTAL GENERAL"}
                total_fila["# PED"]  = len(df_filtrado)
                if tiene_und:  total_fila["# UND"]  = int(df_filtrado[C_UND_E].sum())
                if tiene_clts: total_fila["# CLTS"] = df_filtrado[C_CLTS_E].nunique()
                if tiene_pdd:  total_fila["$ PDD"]  = df_filtrado[C_PDD_E].sum()
                if tiene_util: total_fila["$ UTIL"] = df_filtrado[C_UTIL_E].sum()
                if tiene_cst:  total_fila["$ CST"]  = df_filtrado[C_CST_E].sum()
                if tiene_flt:  total_fila["$ FLT"]  = df_filtrado[C_FLT_E].sum()
                if tiene_pdd:  total_fila["% PDD"]  = 100.0
                return pd.concat([tabla, pd.DataFrame([total_fila])], ignore_index=True)

            def renderizar_tabla_ef(df_filtrado, tabla):
                if len(tabla) == 0:
                    st.info("Sin datos para este período")
                    return

                n_t = len(df_filtrado)

                # ── KPIs del período ──
                ven_t  = df_filtrado[C_PDD_E].sum()  if C_PDD_E  in df_filtrado.columns else 0
                util_t = df_filtrado[C_UTIL_E].sum() if C_UTIL_E in df_filtrado.columns else 0
                flt_t  = df_filtrado[C_FLT_E].sum()  if C_FLT_E  in df_filtrado.columns else 0
                k1,k2,k3,k4 = st.columns(4)
                with k1: st.markdown(kpi("blue",  "📦 Total Pedidos",    f"{n_t:,}",       "Este período"), unsafe_allow_html=True)
                with k2: st.markdown(kpi("cyan",  "💰 Valor Total",       fmt_money(ven_t), "Todos los estatus"), unsafe_allow_html=True)
                with k3: st.markdown(kpi("green", "📈 Utilidad Total",    fmt_money(util_t),"Ganancia acumulada"), unsafe_allow_html=True)
                with k4: st.markdown(kpi("gold",  "🚚 Fletes Totales",    fmt_money(flt_t), "Costo logístico"), unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # ── Mini-cards por estatus financiero ──
                conteo_e = df_filtrado[col_ef].astype(str).str.strip().value_counts()
                mini = '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">'
                for en, ev in conteo_e.items():
                    ce    = get_color_ef(en)
                    pct_e = ev / n_t * 100 if n_t else 0
                    val_e = df_filtrado[df_filtrado[col_ef].astype(str).str.strip()==en][C_PDD_E].sum() if C_PDD_E in df_filtrado.columns else 0
                    mini += (
                        f'<div style="background:{ce}12;border:1.5px solid {ce}44;border-top:3px solid {ce};'
                        f'border-radius:12px;padding:10px 14px;min-width:130px;flex:1">'
                        f'<div style="font-size:0.67rem;color:{ce};font-weight:800;text-transform:uppercase;'
                        f'letter-spacing:0.05em;margin-bottom:6px">{en[:22]}</div>'
                        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:1.05rem">'
                        f'{ev:,} ped.</div>'
                        f'<div style="font-size:0.7rem;color:#a8b4d0;margin-top:2px">'
                        f'{pct_e:.1f}% · {fmt_money(val_e)}</div>'
                        f'<div style="background:#1e2337;border-radius:100px;height:4px;margin-top:8px;overflow:hidden">'
                        f'<div style="background:{ce};width:{min(pct_e,100):.0f}%;height:100%;border-radius:100px"></div>'
                        f'</div></div>'
                    )
                mini += '</div>'
                st.markdown(mini, unsafe_allow_html=True)

                # ── Tabla HTML ──
                cols_t = [c for c in ["Estatus Financiero","# PED","# UND","# CLTS","$ PDD","$ UTIL","$ CST","$ FLT","% PDD"] if c in tabla.columns]
                hdr_e = "".join([
                    f'<th style="padding:10px 14px;text-align:{"left" if c=="Estatus Financiero" else "right"};'
                    f'font-size:0.68rem;color:#a8b4d0;font-weight:800;text-transform:uppercase;'
                    f'letter-spacing:0.06em;border-bottom:2px solid #1e2337">{c}</th>'
                    for c in cols_t
                ])

                filas_html = ""
                for _, row in tabla.iterrows():
                    est_v   = str(row["Estatus Financiero"])
                    color   = get_color_ef(est_v) if "TOTAL" not in est_v.upper() else "#f0c060"
                    es_tot  = "TOTAL" in est_v.upper()
                    bg      = "rgba(201,168,76,0.08)" if es_tot else "rgba(255,255,255,0.02)"
                    bold    = "font-weight:700;" if es_tot else ""
                    bt      = "border-top:2px solid #1e2337;" if es_tot else ""

                    celdas = (
                        f'<td style="padding:10px 14px;{bold}{bt}">'
                        f'<span style="background:{color}18;color:{color};border-radius:20px;'
                        f'padding:3px 10px;font-size:0.78rem;font-weight:700">{est_v}</span></td>'
                    )
                    for col in cols_t[1:]:
                        if col not in row.index: continue
                        val = row[col]
                        if col in ["# PED","# UND","# CLTS"]:
                            txt = f"{int(val):,}" if pd.notna(val) else "—"
                        elif col == "% PDD":
                            txt = f"{val:.1f}%" if pd.notna(val) else "—"
                        else:
                            txt = f"${val:,.0f}" if pd.notna(val) else "—"
                            # Color verde/rojo para UTIL
                            if col == "$ UTIL" and pd.notna(val):
                                c_util = "#10b981" if val >= 0 else "#ef4444"
                                txt = f'<span style="color:{c_util}">{txt}</span>'
                        celdas += f'<td style="padding:10px 14px;text-align:right;{bold}{bt}color:#e8ecf7;font-size:0.87rem">{txt}</td>'

                    filas_html += f'<tr style="background:{bg};border-bottom:1px solid #12151f">{celdas}</tr>'

                st.markdown(
                    f'<div style="overflow-x:auto;border-radius:12px;border:1px solid #2e2558;margin-top:4px">'
                    f'<table style="width:100%;border-collapse:collapse;background:#13102a;font-family:DM Sans,sans-serif">'
                    f'<thead><tr>{hdr_e}</tr></thead><tbody>{filas_html}</tbody></table></div>',
                    unsafe_allow_html=True
                )

                # ── Gráfica: Distribución por Estatus Financiero ──
                st.markdown("<br>", unsafe_allow_html=True)
                tabla_graf = tabla[tabla["Estatus Financiero"] != "TOTAL GENERAL"]
                if "$ PDD" in tabla_graf.columns and len(tabla_graf):
                    colores_bar = [get_color_ef(e) for e in tabla_graf["Estatus Financiero"]]
                    fig_ef = go.Figure(go.Bar(
                        x=tabla_graf["Estatus Financiero"],
                        y=tabla_graf["$ PDD"],
                        marker_color=colores_bar,
                        text=[fmt_money(v) for v in tabla_graf["$ PDD"]],
                        textposition="outside",
                        textfont={"size":10,"color":"#8892b0"},
                    ))
                    fig_ef.update_layout(
                        **PLOT_LAYOUT, height=320,
                        title="Valor ($) por Estatus Financiero",
                        xaxis=AXIS_STYLE, yaxis={**AXIS_STYLE, "tickprefix":"$"}
                    )
                    st.plotly_chart(fig_ef, use_container_width=True)

            # ── Renderizar cada tab ──
            for i_ef, tab_ef in enumerate(semana_tabs_ef):
                with tab_ef:
                    df_sem_ef = semana_df_ef(df_ef, i_ef)
                    if len(df_sem_ef) == 0:
                        st.info("Sin pedidos en este período")
                        continue
                    st.caption(f"📋 {len(df_sem_ef):,} pedidos en este período")
                    tabla_ef = construir_tabla_ef(df_sem_ef)
                    renderizar_tabla_ef(df_sem_ef, tabla_ef)



    # ══════════════════════════════════════════════════════════════════
    # 📋 MONITOR FINANCIERO
    # ══════════════════════════════════════════════════════════════════
    elif "Financiero" in op_nav:
        st.markdown('<div class="seccion-titulo">📋 Monitor de Pedidos Financiero</div>', unsafe_allow_html=True)
        col_ef = next((c for c in df.columns if "FINANCIERO" in c.upper()), None)
        if col_ef is None:
            st.markdown('<div style="background:rgba(245,158,11,0.08);border:1px solid #f59e0b44;border-radius:12px;padding:24px;text-align:center"><div style="font-size:1.4rem;margin-bottom:8px">📋</div><div style="color:#f59e0b;font-weight:700;margin-bottom:6px">Columna "Estatus Financiero" no encontrada en el Excel</div><div style="color:#a8b4d0;font-size:0.8rem">Asegúrate de que tu reporte incluya la columna <b>ESTATUS FINANCIERO</b>.<br>Permite cruzar estado financiero con utilidades, márgenes y pauta.</div></div>', unsafe_allow_html=True)
        else:
            df_fin_mon = df.copy()
            ff1,ff2,ff3,ff4 = st.columns(4)
            with ff1:
                opts_ef=['Todos']+sorted(df_fin_mon[col_ef].dropna().astype(str).unique().tolist())
                fef=st.selectbox("📋 Estatus Financiero",opts_ef,key="mf_ef")
                if fef!='Todos': df_fin_mon=df_fin_mon[df_fin_mon[col_ef].astype(str)==fef]
            with ff2:
                if C_CIUDAD in df.columns:
                    opts_mfc=['Todas']+sorted(df_fin_mon[C_CIUDAD].astype(str).unique().tolist())
                    fmfc=st.selectbox("🏙️ Ciudad",opts_mfc,key="mf_ciu")
                    if fmfc!='Todas': df_fin_mon=df_fin_mon[df_fin_mon[C_CIUDAD].astype(str)==fmfc]
            with ff3:
                if C_PRODUCTO in df.columns:
                    opts_mfp=['Todos']+sorted(df_fin_mon[C_PRODUCTO].astype(str).unique().tolist())
                    fmfp=st.selectbox("📦 Producto",opts_mfp,key="mf_prod")
                    if fmfp!='Todos': df_fin_mon=df_fin_mon[df_fin_mon[C_PRODUCTO].astype(str)==fmfp]
            with ff4:
                if '_mes' in df.columns:
                    opts_mfm=['Todos']+sorted(df['_mes'].dropna().unique().tolist(),reverse=True)
                    fmfm=st.selectbox("📅 Mes",opts_mfm,key="mf_mes")
                    if fmfm!='Todos': df_fin_mon=df_fin_mon[df_fin_mon['_mes']==fmfm]
            n_mf=len(df_fin_mon)
            ing_mf=df_fin_mon[C_TOTAL].sum() if C_TOTAL in df_fin_mon.columns else 0
            gan_mf=df_fin_mon[C_GANANCIA].sum() if C_GANANCIA in df_fin_mon.columns else 0
            flt_mf=df_fin_mon[C_FLETE].sum() if C_FLETE in df_fin_mon.columns else 0
            cst_mf=df_fin_mon["PRECIO PROVEEDOR X CANTIDAD"].sum() if "PRECIO PROVEEDOR X CANTIDAD" in df_fin_mon.columns else 0
            margen_mf=gan_mf/ing_mf*100 if ing_mf else 0
            k1,k2,k3,k4,k5=st.columns(5)
            with k1: st.markdown(kpi("blue","📋 Pedidos",f"{n_mf:,}","Filtro activo"),unsafe_allow_html=True)
            with k2: st.markdown(kpi("cyan","💰 Ingresos",fmt_money(ing_mf),"Total facturado"),unsafe_allow_html=True)
            with k3: st.markdown(kpi("green","📈 Ganancia",fmt_money(gan_mf),f"{margen_mf:.1f}% margen"),unsafe_allow_html=True)
            with k4: st.markdown(kpi("red","🏭 Costo Producto",fmt_money(cst_mf),"Proveedor"),unsafe_allow_html=True)
            with k5: st.markdown(kpi("gold","🚚 Fletes",fmt_money(flt_mf),"Ent+Dev"),unsafe_allow_html=True)
            st.markdown("<br>",unsafe_allow_html=True)
            st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.85rem;margin-bottom:10px">📊 Distribución por Estatus Financiero</div>',unsafe_allow_html=True)
            resumen_ef=df_fin_mon.groupby(col_ef).agg(
                Pedidos=(C_ID,'count') if C_ID in df_fin_mon.columns else (col_ef,'count'),
                Ingresos=(C_TOTAL,'sum') if C_TOTAL in df_fin_mon.columns else (col_ef,'count'),
                Ganancia=(C_GANANCIA,'sum') if C_GANANCIA in df_fin_mon.columns else (col_ef,'count'),
                Fletes=(C_FLETE,'sum') if C_FLETE in df_fin_mon.columns else (col_ef,'count'),
            ).reset_index().sort_values('Pedidos',ascending=False)
            resumen_ef.columns=['Estatus Financiero','Pedidos','Ingresos','Ganancia','Fletes']
            total_ef=resumen_ef['Pedidos'].sum()
            hdr_ef="background:#161525;padding:10px 14px;font-size:0.67rem;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;color:#a8b4d0;border-bottom:2px solid #1e2337"
            td_ef="padding:10px 14px;font-size:0.82rem;border-bottom:1px solid #161929"
            tabla_ef=(
                f'<div style="overflow-x:auto;border-radius:12px;border:1px solid #2e2558;margin-bottom:16px">'
                f'<table style="width:100%;border-collapse:collapse;background:#13102a;font-family:DM Sans,sans-serif">'
                f'<thead><tr>'
                f'<th style="{hdr_ef};text-align:left">Estatus Financiero</th>'
                f'<th style="{hdr_ef};text-align:right">Pedidos</th>'
                f'<th style="{hdr_ef};text-align:right">% Total</th>'
                f'<th style="{hdr_ef};text-align:right">Ingresos</th>'
                f'<th style="{hdr_ef};text-align:right">Ganancia</th>'
                f'<th style="{hdr_ef};text-align:right">Margen</th>'
                f'<th style="{hdr_ef};text-align:right">Fletes</th>'
                f'</tr></thead><tbody>'
            )
            _ef_cols=['#10b981','#00d4ff','#5b6cfc','#f59e0b','#ef4444','#7c3aed','#ec4899','#f0c060']
            for _i,_r in resumen_ef.iterrows():
                _pct=_r['Pedidos']/total_ef*100 if total_ef else 0
                _mrg=_r['Ganancia']/_r['Ingresos']*100 if _r['Ingresos'] else 0
                _col=_ef_cols[int(_i)%len(_ef_cols)]
                _mc="#10b981" if _mrg>=20 else "#f59e0b" if _mrg>=10 else "#ef4444"
                tabla_ef+=(
                    f'<tr style="background:rgba(255,255,255,0.01)">'
                    f'<td style="{td_ef}"><span style="background:{_col}22;color:{_col};padding:3px 10px;border-radius:20px;font-weight:700;font-size:0.78rem">{_r["Estatus Financiero"]}</span></td>'
                    f'<td style="{td_ef};text-align:right;color:#e8ecf7;font-weight:700">{_r["Pedidos"]:,}</td>'
                    f'<td style="{td_ef};text-align:right"><div style="display:flex;align-items:center;gap:6px;justify-content:flex-end"><div style="background:#1e2337;border-radius:100px;height:5px;width:60px;overflow:hidden"><div style="background:{_col};width:{min(_pct,100):.0f}%;height:100%"></div></div><span style="color:{_col};font-weight:700">{_pct:.1f}%</span></div></td>'
                    f'<td style="{td_ef};text-align:right;color:#22d3ee">{fmt_money(_r["Ingresos"])}</td>'
                    f'<td style="{td_ef};text-align:right;color:#10b981;font-weight:700">{fmt_money(_r["Ganancia"])}</td>'
                    f'<td style="{td_ef};text-align:right;color:{_mc};font-weight:700">{_mrg:.1f}%</td>'
                    f'<td style="{td_ef};text-align:right;color:#f59e0b">{fmt_money(_r["Fletes"])}</td>'
                    f'</tr>'
                )
            tabla_ef+=(
                f'<tr style="background:rgba(201,168,76,0.07);border-top:2px solid #f0c060">'
                f'<td style="{td_ef};color:#fcd34d;font-weight:800">TOTAL</td>'
                f'<td style="{td_ef};text-align:right;color:#fcd34d;font-weight:800">{total_ef:,}</td>'
                f'<td style="{td_ef};text-align:right;color:#fcd34d;font-weight:800">100%</td>'
                f'<td style="{td_ef};text-align:right;color:#fcd34d;font-weight:800">{fmt_money(ing_mf)}</td>'
                f'<td style="{td_ef};text-align:right;color:#fcd34d;font-weight:800">{fmt_money(gan_mf)}</td>'
                f'<td style="{td_ef};text-align:right;color:#fcd34d;font-weight:800">{gan_mf/ing_mf*100:.1f}% if ing_mf else "—"</td>'
                f'<td style="{td_ef};text-align:right;color:#fcd34d;font-weight:800">{fmt_money(flt_mf)}</td>'
                f'</tr></tbody></table></div>'
            )
            st.markdown(tabla_ef,unsafe_allow_html=True)
            st.markdown('<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.85rem;margin-bottom:10px;margin-top:16px">📋 Detalle de Pedidos</div>',unsafe_allow_html=True)
            cols_fin=[c for c in [C_ID,C_FECHA,col_ef,C_ESTATUS,C_CLIENTE,C_PRODUCTO,C_CIUDAD,C_TRANSP,C_TOTAL,C_GANANCIA,C_FLETE,"PRECIO PROVEEDOR X CANTIDAD"] if c in df_fin_mon.columns]
            st.dataframe(df_fin_mon[cols_fin].head(500).reset_index(drop=True),use_container_width=True,height=400,
                column_config={C_TOTAL:st.column_config.NumberColumn("Valor",format="$%,.0f"),
                               C_GANANCIA:st.column_config.NumberColumn("Ganancia",format="$%,.0f"),
                               C_FLETE:st.column_config.NumberColumn("Flete",format="$%,.0f")})
            ce1,ce2=st.columns([3,1])
            with ce2: st.caption(f"📋 {min(n_mf,500):,} de {n_mf:,} pedidos")
            with ce1:
                if st.button("📥 Exportar Excel",key="exp_mf"):
                    import io; buf=io.BytesIO()
                    df_fin_mon[cols_fin].to_excel(buf,index=False)
                    st.download_button("⬇️ Descargar",buf.getvalue(),"monitor_financiero.xlsx","application/vnd.ms-excel",key="dl_mf")


    # ══════════════════════════════════════════════════════════════════
    # 🚚 TRANSPORTADORAS
    # ══════════════════════════════════════════════════════════════════
    elif "Transportadoras" in op_nav:
        st.markdown('<div class="seccion-titulo">🚚 Rendimiento por Transportadora</div>', unsafe_allow_html=True)
        C_TRANSP = next((c for c in df.columns if any(x in c.upper() for x in ["TRANSPORT","CARRIER","MENSAJER","OPERADOR"])), None)

        if C_TRANSP and C_ESTATUS in df.columns:
            df_t = df.copy()
            df_t['_es_ent'] = df_t[C_ESTATUS].astype(str).str.upper().str.contains('ENTREGAD', na=False)
            df_t['_es_dev'] = df_t[C_ESTATUS].astype(str).str.upper().str.contains('DEVOLUCI', na=False)
            df_t['_es_can'] = df_t[C_ESTATUS].astype(str).str.upper().str.contains('CANCELAD', na=False)
            df_t['_es_nov'] = df_t[C_ESTATUS].astype(str).str.upper().str.contains('NOVEDAD', na=False)

            grp_t = df_t.groupby(C_TRANSP).agg(
                Total=('_es_ent','count'),
                Entregados=('_es_ent','sum'),
                Devoluciones=('_es_dev','sum'),
                Cancelados=('_es_can','sum'),
                Novedades=('_es_nov','sum'),
            ).reset_index()
            grp_t['Tasa Entrega'] = (grp_t['Entregados'] / grp_t['Total'] * 100).round(1)
            grp_t['Tasa Dev']     = (grp_t['Devoluciones'] / grp_t['Total'] * 100).round(1)

            # Costo por pedido entregado
            if C_FLETE in df_t.columns:
                flete_t = df_t[df_t['_es_ent']].groupby(C_TRANSP)[C_FLETE].sum()
                grp_t['Flete Total'] = grp_t[C_TRANSP].map(flete_t).fillna(0)
                grp_t['Costo/Pedido'] = (grp_t['Flete Total'] / grp_t['Entregados'].replace(0,1)).round(0)
            else:
                grp_t['Flete Total'] = 0
                grp_t['Costo/Pedido'] = 0

            grp_t = grp_t.sort_values('Total', ascending=False)

            # Tiempo promedio si hay fechas
            if C_FECHA in df_t.columns and '_d_mov' in df_t.columns:
                tiempo_t = df_t[df_t['_es_ent']].groupby(C_TRANSP)['_d_mov'].mean().round(1)
                grp_t['Días Prom.'] = grp_t[C_TRANSP].map(tiempo_t).fillna(0)
            else:
                grp_t['Días Prom.'] = '—'

            # KPIs top transportadora
            mejor = grp_t.loc[grp_t['Tasa Entrega'].idxmax()] if len(grp_t) else None
            peor  = grp_t.loc[grp_t['Tasa Dev'].idxmax()] if len(grp_t) else None
            k1,k2,k3,k4 = st.columns(4)
            with k1: st.markdown(kpi("blue","🚚 Transportadoras",f"{len(grp_t)}"), unsafe_allow_html=True)
            with k2: st.markdown(kpi("green","⭐ Mejor Entrega",f"{mejor[C_TRANSP][:15] if mejor is not None else '—'}",f"{mejor['Tasa Entrega']}%" if mejor is not None else ""), unsafe_allow_html=True)
            with k3: st.markdown(kpi("red","⚠️ Más Devoluciones",f"{peor[C_TRANSP][:15] if peor is not None else '—'}",f"{peor['Tasa Dev']}%" if peor is not None else ""), unsafe_allow_html=True)
            with k4:
                costo_prom = int(grp_t['Costo/Pedido'].mean()) if 'Costo/Pedido' in grp_t else 0
                st.markdown(kpi("gold","💸 Costo Prom/Pedido",fmt_money(costo_prom)), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            g1, g2 = st.columns(2)

            with g1:
                fig_t = go.Figure()
                fig_t.add_trace(go.Bar(x=grp_t[C_TRANSP], y=grp_t['Tasa Entrega'], name='Tasa Entrega %',
                                       marker_color='#10b981', text=grp_t['Tasa Entrega'].astype(str)+'%',
                                       textposition='outside'))
                fig_t.add_trace(go.Bar(x=grp_t[C_TRANSP], y=grp_t['Tasa Dev'], name='Tasa Devolución %',
                                       marker_color='#ef4444', text=grp_t['Tasa Dev'].astype(str)+'%',
                                       textposition='outside'))
                fig_t.update_layout(**PLOT_LAYOUT, barmode='group', height=380, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE,
                                    title='Tasa de Entrega vs Devolución por Transportadora', yaxis_ticksuffix='%')
                st.plotly_chart(fig_t, use_container_width=True)

            with g2:
                fig_t2 = go.Figure()
                fig_t2.add_trace(go.Bar(x=grp_t[C_TRANSP], y=grp_t['Total'], name='Total', marker_color='#5b6cfc'))
                fig_t2.add_trace(go.Bar(x=grp_t[C_TRANSP], y=grp_t['Entregados'], name='Entregados', marker_color='#10b981'))
                fig_t2.add_trace(go.Bar(x=grp_t[C_TRANSP], y=grp_t['Devoluciones'], name='Devoluciones', marker_color='#f59e0b'))
                fig_t2.add_trace(go.Bar(x=grp_t[C_TRANSP], y=grp_t['Novedades'], name='Novedades', marker_color='#7c3aed'))
                fig_t2.update_layout(**PLOT_LAYOUT, barmode='group', height=380, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE,
                                     title='Volumen de Pedidos por Transportadora')
                st.plotly_chart(fig_t2, use_container_width=True)

            # Tabla detallada
            st.markdown('<div class="seccion-titulo" style="font-size:0.9rem">📊 Detalle por Transportadora</div>', unsafe_allow_html=True)
            cols_show = [C_TRANSP,'Total','Entregados','Devoluciones','Cancelados','Novedades','Tasa Entrega','Tasa Dev','Costo/Pedido','Días Prom.']
            cols_show = [c for c in cols_show if c in grp_t.columns]
            display_t = grp_t[cols_show].copy()
            if 'Costo/Pedido' in display_t.columns:
                display_t['Costo/Pedido'] = display_t['Costo/Pedido'].apply(lambda x: f"$ {int(x):,}" if x else '—')
            if 'Tasa Entrega' in display_t.columns:
                display_t['Tasa Entrega'] = display_t['Tasa Entrega'].astype(str) + '%'
            if 'Tasa Dev' in display_t.columns:
                display_t['Tasa Dev'] = display_t['Tasa Dev'].astype(str) + '%'
            st.dataframe(display_t, use_container_width=True, hide_index=True)
        else:
            st.info("No se encontró columna de Transportadora en el Excel. Verifica que exista una columna con nombre 'Transportadora', 'Carrier' o similar.")

    # ══════════════════════════════════════════════════════════════════
    # 👥 PROVEEDORES
    # ══════════════════════════════════════════════════════════════════
    elif "Proveedores" in op_nav:
        st.markdown('<div class="seccion-titulo">👥 Ranking de Proveedores</div>', unsafe_allow_html=True)
        C_PROVE = next((c for c in df.columns if any(x in c.upper() for x in ["PROVEEDOR","SUPPLIER","PROVE","VENDOR"])), None)

        if C_PROVE and C_ESTATUS in df.columns:
            df_p = df.copy()
            df_p['_ent'] = df_p[C_ESTATUS].astype(str).str.upper().str.contains('ENTREGAD', na=False)
            df_p['_can'] = df_p[C_ESTATUS].astype(str).str.upper().str.contains('CANCELAD', na=False)
            df_p['_dev'] = df_p[C_ESTATUS].astype(str).str.upper().str.contains('DEVOLUCI', na=False)

            grp_p = df_p.groupby(C_PROVE).agg(
                Pedidos=('_ent','count'),
                Entregados=('_ent','sum'),
                Cancelados=('_can','sum'),
                Devoluciones=('_dev','sum'),
            ).reset_index()
            grp_p['Tasa Entrega'] = (grp_p['Entregados']/grp_p['Pedidos']*100).round(1)
            grp_p['Tasa Cancel']  = (grp_p['Cancelados']/grp_p['Pedidos']*100).round(1)
            grp_p['Tasa Dev']     = (grp_p['Devoluciones']/grp_p['Pedidos']*100).round(1)

            if C_TOTAL in df_p.columns:
                ventas_p = df_p[df_p['_ent']].groupby(C_PROVE)[C_TOTAL].sum()
                grp_p['Ventas']       = grp_p[C_PROVE].map(ventas_p).fillna(0)
            if C_GANANCIA in df_p.columns:
                gan_p = df_p[df_p['_ent']].groupby(C_PROVE)[C_GANANCIA].sum()
                grp_p['Ganancia']     = grp_p[C_PROVE].map(gan_p).fillna(0)

            grp_p = grp_p.sort_values('Pedidos', ascending=False).head(20)

            # KPIs
            k1,k2,k3 = st.columns(3)
            with k1: st.markdown(kpi("blue","👥 Proveedores",f"{len(grp_p)}"), unsafe_allow_html=True)
            with k2:
                mejor_p = grp_p.loc[grp_p['Tasa Entrega'].idxmax()] if len(grp_p) else None
                st.markdown(kpi("green","⭐ Mejor Proveedor",f"{str(mejor_p[C_PROVE])[:18] if mejor_p is not None else '—'}",f"{mejor_p['Tasa Entrega']}%" if mejor_p is not None else ""), unsafe_allow_html=True)
            with k3:
                peor_p = grp_p.loc[grp_p['Tasa Cancel'].idxmax()] if len(grp_p) else None
                st.markdown(kpi("red","⚠️ Más Cancelaciones",f"{str(peor_p[C_PROVE])[:18] if peor_p is not None else '—'}",f"{peor_p['Tasa Cancel']}%" if peor_p is not None else ""), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            fig_p = px.bar(grp_p.head(10), x=C_PROVE, y=['Tasa Entrega','Tasa Cancel','Tasa Dev'],
                           barmode='group', color_discrete_sequence=['#10b981','#ef4444','#f59e0b'],
                           title='Top 10 Proveedores — Tasas de Entrega, Cancelación y Devolución')
            fig_p.update_layout(**PLOT_LAYOUT, height=380, xaxis=AXIS_STYLE, yaxis=dict(ticksuffix='%', **AXIS_STYLE))
            st.plotly_chart(fig_p, use_container_width=True)

            # Tabla
            disp_cols = [c for c in [C_PROVE,'Pedidos','Entregados','Cancelados','Devoluciones','Tasa Entrega','Tasa Cancel','Tasa Dev','Ventas','Ganancia'] if c in grp_p.columns]
            disp_p = grp_p[disp_cols].copy()
            for col in ['Ventas','Ganancia']:
                if col in disp_p.columns:
                    disp_p[col] = disp_p[col].apply(fmt_money)
            for col in ['Tasa Entrega','Tasa Cancel','Tasa Dev']:
                if col in disp_p.columns:
                    disp_p[col] = disp_p[col].astype(str) + '%'
            st.dataframe(disp_p, use_container_width=True, hide_index=True)
        else:
            col_prov_hint = [c for c in df.columns if 'PROV' in c.upper() or 'SUPPL' in c.upper()]
            st.info(f"No se encontró columna de Proveedor. Columnas similares encontradas: {col_prov_hint[:5] if col_prov_hint else 'Ninguna'}")

    # ══════════════════════════════════════════════════════════════════
    # 📦 INVENTARIO
    # ══════════════════════════════════════════════════════════════════
    elif "Stock" in op_nav or "Inventario" in op_nav:
        st.markdown('<div class="seccion-titulo">📦 Stock & Análisis de Devoluciones por Producto</div>', unsafe_allow_html=True)
        C_PROD = next((c for c in df.columns if any(x in c.upper() for x in ["PRODUCTO","PRODUCT","ARTICU","ITEM","SKU"])), None)

        if C_PROD and C_ESTATUS in df.columns:
            df_inv = df.copy()
            df_inv['_ent'] = df_inv[C_ESTATUS].astype(str).str.upper().str.contains('ENTREGAD', na=False)
            df_inv['_dev'] = df_inv[C_ESTATUS].astype(str).str.upper().str.contains('DEVOLUCI', na=False)
            df_inv['_can'] = df_inv[C_ESTATUS].astype(str).str.upper().str.contains('CANCELAD', na=False)
            df_inv['_und'] = df_inv[C_CANTIDAD].fillna(1) if C_CANTIDAD in df_inv.columns else 1

            grp_inv = df_inv.groupby(C_PROD).agg(
                Pedidos=('_ent','count'),
                Unids_Vendidas=('_und','sum'),
                Entregados=('_ent','sum'),
                Devoluciones=('_dev','sum'),
                Cancelados=('_can','sum'),
            ).reset_index()

            if C_TOTAL in df_inv.columns:
                v_p = df_inv.groupby(C_PROD)[C_TOTAL].sum()
                grp_inv['Ventas'] = grp_inv[C_PROD].map(v_p).fillna(0)
            if C_GANANCIA in df_inv.columns:
                g_p = df_inv.groupby(C_PROD)[C_GANANCIA].sum()
                grp_inv['Ganancia'] = grp_inv[C_PROD].map(g_p).fillna(0)

            grp_inv['Tasa Dev %'] = (grp_inv['Devoluciones']/grp_inv['Pedidos'].replace(0,1)*100).round(1)
            grp_inv['Tasa Ent %'] = (grp_inv['Entregados']/grp_inv['Pedidos'].replace(0,1)*100).round(1)
            grp_inv = grp_inv.sort_values('Pedidos', ascending=False)

            k1,k2,k3,k4 = st.columns(4)
            with k1: st.markdown(kpi("blue","📦 Productos",f"{len(grp_inv)}"), unsafe_allow_html=True)
            with k2: st.markdown(kpi("cyan","📊 Total Unidades",f"{int(grp_inv['Unids_Vendidas'].sum()):,}"), unsafe_allow_html=True)
            with k3:
                top_prod = grp_inv.iloc[0] if len(grp_inv) else None
                st.markdown(kpi("green","🏆 Más Vendido",f"{str(top_prod[C_PROD])[:18] if top_prod is not None else '—'}",f"{int(top_prod['Pedidos']):,} pedidos" if top_prod is not None else ""), unsafe_allow_html=True)
            with k4:
                alto_dev = grp_inv.loc[grp_inv['Tasa Dev %'].idxmax()] if len(grp_inv) else None
                st.markdown(kpi("red","⚠️ Más Devoluciones",f"{str(alto_dev[C_PROD])[:18] if alto_dev is not None else '—'}",f"{alto_dev['Tasa Dev %']}%" if alto_dev is not None else ""), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            g1, g2 = st.columns(2)

            with g1:
                top10 = grp_inv.head(10)
                fig_inv = go.Figure()
                fig_inv.add_trace(go.Bar(x=top10[C_PROD], y=top10['Entregados'], name='Entregados', marker_color='#10b981'))
                fig_inv.add_trace(go.Bar(x=top10[C_PROD], y=top10['Devoluciones'], name='Devoluciones', marker_color='#f59e0b'))
                fig_inv.add_trace(go.Bar(x=top10[C_PROD], y=top10['Cancelados'], name='Cancelados', marker_color='#ef4444'))
                fig_inv.update_layout(**PLOT_LAYOUT, barmode='stack', height=380, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE,
                                      title='Top 10 Productos — Entregados vs Devoluciones vs Cancelados')
                st.plotly_chart(fig_inv, use_container_width=True)

            with g2:
                if 'Ganancia' in grp_inv.columns:
                    fig_gan = px.bar(grp_inv.head(10).sort_values('Ganancia', ascending=True),
                                     x='Ganancia', y=C_PROD, orientation='h',
                                     color='Ganancia', color_continuous_scale=['#ef4444','#f59e0b','#10b981'],
                                     title='Ganancia por Producto (Top 10)')
                    fig_gan.update_layout(**PLOT_LAYOUT, height=380, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                    st.plotly_chart(fig_gan, use_container_width=True)

            # Tabla
            disp_cols = [c for c in [C_PROD,'Pedidos','Unids_Vendidas','Entregados','Devoluciones','Cancelados','Tasa Ent %','Tasa Dev %','Ventas','Ganancia'] if c in grp_inv.columns]
            disp_inv = grp_inv[disp_cols].copy()
            for col in ['Ventas','Ganancia']:
                if col in disp_inv.columns:
                    disp_inv[col] = disp_inv[col].apply(fmt_money)
            for col in ['Tasa Ent %','Tasa Dev %']:
                if col in disp_inv.columns:
                    disp_inv[col] = disp_inv[col].astype(str) + '%'
            st.dataframe(disp_inv, use_container_width=True, hide_index=True)
        else:
            st.info("No se encontró columna de Producto. Verifica que exista una columna con nombre 'Producto', 'Artículo', 'SKU' o similar.")

    # ══════════════════════════════════════════════════════════════════
    # 🔁 DEVOLUCIONES
    # ══════════════════════════════════════════════════════════════════
    elif "Devoluciones" in op_nav:
        st.markdown('<div class="seccion-titulo">🔁 Análisis de Devoluciones</div>', unsafe_allow_html=True)

        mask_dev = df[C_ESTATUS].astype(str).str.upper().str.contains('DEVOLUCI', na=False) if C_ESTATUS in df.columns else pd.Series([False]*len(df))
        df_dev = df[mask_dev].copy()

        if len(df_dev) == 0:
            st.info("No hay devoluciones registradas en el período.")
        else:
            total_dev = len(df_dev)
            pct_dev   = round(total_dev/total*100,1) if total else 0
            val_dev   = df_dev[C_TOTAL].sum() if C_TOTAL in df_dev.columns else 0
            flete_dev = df_dev[C_FLETE].sum() if C_FLETE in df_dev.columns else 0

            k1,k2,k3,k4 = st.columns(4)
            with k1: st.markdown(kpi("red","🔁 Total Devoluciones",f"{total_dev:,}",f"{pct_dev}% del total"), unsafe_allow_html=True)
            with k2: st.markdown(kpi("gold","💰 Valor Devuelto",fmt_money(val_dev)), unsafe_allow_html=True)
            with k3: st.markdown(kpi("purple","🚚 Flete Devoluciones",fmt_money(flete_dev)), unsafe_allow_html=True)
            with k4:
                costo_dev = val_dev + flete_dev
                st.markdown(kpi("red","⚠️ Costo Total Dev.",fmt_money(costo_dev)), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            g1, g2 = st.columns(2)

            with g1:
                # Devoluciones por ciudad
                C_CIUDAD = next((c for c in df.columns if any(x in c.upper() for x in ["CIUDAD","CITY","MUNICIPIO","DEPTO","DEPARTAMENTO"])), None)
                if C_CIUDAD:
                    dev_ciudad = df_dev[C_CIUDAD].value_counts().head(12).reset_index()
                    dev_ciudad.columns = ['Ciudad','Devoluciones']
                    fig_dc = px.bar(dev_ciudad.sort_values('Devoluciones'), x='Devoluciones', y='Ciudad',
                                    orientation='h', color='Devoluciones',
                                    color_continuous_scale=['#fbbf24','#f59e0b','#ef4444'],
                                    title='Top Ciudades con Más Devoluciones')
                    fig_dc.update_layout(**PLOT_LAYOUT, height=400, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                    st.plotly_chart(fig_dc, use_container_width=True)
                else:
                    st.info("Columna Ciudad no encontrada.")

            with g2:
                # Tendencia devoluciones por semana
                if C_FECHA in df_dev.columns:
                    df_dev2 = df_dev.copy()
                    df_dev2['_semana'] = df_dev2[C_FECHA].dt.isocalendar().week.astype(str)
                    tend = df_dev2.groupby('_semana').size().reset_index(name='Devoluciones')
                    fig_tend = px.line(tend, x='_semana', y='Devoluciones',
                                       title='Tendencia Semanal de Devoluciones',
                                       markers=True, color_discrete_sequence=['#f59e0b'])
                    fig_tend.update_layout(**PLOT_LAYOUT, height=400, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                    fig_tend.update_traces(line=dict(width=3), marker=dict(size=9))
                    st.plotly_chart(fig_tend, use_container_width=True)

            # Productos con más devoluciones
            C_PROD2 = next((c for c in df.columns if any(x in c.upper() for x in ["PRODUCTO","PRODUCT","ARTICU","ITEM","SKU"])), None)
            if C_PROD2:
                dev_prod = df_dev[C_PROD2].value_counts().head(10).reset_index()
                dev_prod.columns = ['Producto','Devoluciones']
                fig_dp = px.bar(dev_prod.sort_values('Devoluciones'), x='Devoluciones', y='Producto',
                                orientation='h', color='Devoluciones',
                                color_continuous_scale=['#fbbf24','#ef4444'],
                                title='Top 10 Productos con Más Devoluciones')
                fig_dp.update_layout(**PLOT_LAYOUT, height=360, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                st.plotly_chart(fig_dp, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════
    # 📋 NOVEDADES CON HISTORIAL
    # ══════════════════════════════════════════════════════════════════
    elif "Novedades" in op_nav:
        st.markdown('<div class="seccion-titulo">📋 Historial de Novedades</div>', unsafe_allow_html=True)

        mask_nov = df[C_ESTATUS].astype(str).str.upper().str.contains('NOVEDAD', na=False) if C_ESTATUS in df.columns else pd.Series([True]*len(df))
        df_nov = df[mask_nov].copy() if C_NOVEDAD in df.columns else df.copy()

        if len(df_nov) > 0:
            total_nov = len(df_nov)
            resueltas = df_nov[df_nov[C_NOV_SOL].astype(str).str.upper().str.contains('SI|SÍ', na=False)].shape[0] if C_NOV_SOL in df_nov.columns else 0
            pendientes = total_nov - resueltas
            pct_res = round(resueltas/total_nov*100,1) if total_nov else 0

            k1,k2,k3,k4 = st.columns(4)
            with k1: st.markdown(kpi("purple","⚠️ Total Novedades",f"{total_nov:,}"), unsafe_allow_html=True)
            with k2: st.markdown(kpi("green","✅ Resueltas",f"{resueltas:,}",f"{pct_res}%"), unsafe_allow_html=True)
            with k3: st.markdown(kpi("red","🔴 Pendientes",f"{pendientes:,}",f"{100-pct_res}%"), unsafe_allow_html=True)
            with k4:
                dias_prom = round(df_nov['_d_mov'].mean(),1) if '_d_mov' in df_nov.columns else 0
                st.markdown(kpi("gold","⏱️ Días Prom. Pendiente",f"{dias_prom}d"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if C_NOVEDAD in df_nov.columns:
                g1, g2 = st.columns(2)
                with g1:
                    tipo_nov = df_nov[C_NOVEDAD].value_counts().head(10).reset_index()
                    tipo_nov.columns = ['Tipo Novedad','Cantidad']
                    fig_tn = px.pie(tipo_nov, values='Cantidad', names='Tipo Novedad', hole=0.4,
                                    color_discrete_sequence=COLORES_ELEGANTES, title='Tipos de Novedad')
                    fig_tn.update_layout(**PLOT_LAYOUT, height=360)
                    fig_tn.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_tn, use_container_width=True)
                with g2:
                    if '_mes' in df_nov.columns:
                        nov_mes = df_nov.groupby('_mes').size().reset_index(name='Novedades')
                        fig_nm = px.bar(nov_mes, x='_mes', y='Novedades',
                                        color_discrete_sequence=['#7c3aed'], title='Novedades por Mes')
                        fig_nm.update_layout(**PLOT_LAYOUT, height=360, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                        st.plotly_chart(fig_nm, use_container_width=True)

            # Tabla historial
            cols_nov = [c for c in [C_ID, C_CLIENTE, C_NOVEDAD, C_NOV_SOL, '_d_mov', C_GUIA] if c in df_nov.columns]
            if cols_nov:
                st.markdown('<div style="font-size:0.8rem;color:#a8b4d0;margin-bottom:8px">Mostrando las 100 más recientes</div>', unsafe_allow_html=True)
                st.dataframe(df_nov[cols_nov].head(100), use_container_width=True, hide_index=True)


    elif "Estados" in op_nav and C_ESTATUS in df.columns:
        g1,g2 = st.columns(2)
        with g1:
            ed = df[C_ESTATUS].astype(str).value_counts().reset_index()
            ed.columns = ['Estatus','Cantidad']
            fig = px.pie(ed, values='Cantidad', names='Estatus', hole=0.4,
                        color_discrete_sequence=COLORES_ELEGANTES, title='Distribución de Estados')
            fig.update_layout(**PLOT_LAYOUT, height=380, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        with g2:
            if '_mes' in df.columns:
                em = df.groupby(['_mes', C_ESTATUS]).size().reset_index(name='Cantidad')
                fig2 = px.bar(em, x='_mes', y='Cantidad', color=C_ESTATUS, barmode='stack',
                             color_discrete_sequence=COLORES_ELEGANTES, title='Estados por Mes')
                fig2.update_layout(**PLOT_LAYOUT, height=380, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                st.plotly_chart(fig2, use_container_width=True)

    elif "Novedades" in op_nav and C_NOVEDAD in df.columns:
        nov_df = df[df[C_ESTATUS].astype(str).str.upper().str.contains('NOVEDAD', na=False)] if C_ESTATUS in df.columns else df
        total_nov = len(nov_df)
        if total_nov > 0:
            sol = sum(1 for v in nov_df[C_NOV_SOL].astype(str).str.upper() if 'SI' in v or 'SÍ' in v) if C_NOV_SOL in df.columns else 0
            no_sol = total_nov - sol
            n1,n2,n3 = st.columns(3)
            with n1: st.markdown(kpi("gold","Total Novedades",total_nov), unsafe_allow_html=True)
            with n2: st.markdown(kpi("green","✅ Solucionadas",sol,f"{round(sol/total_nov*100,1)}%"), unsafe_allow_html=True)
            with n3: st.markdown(kpi("red","❌ Pendientes",no_sol), unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            tipos = nov_df[C_NOVEDAD].astype(str).value_counts().head(12).reset_index()
            tipos.columns = ['Novedad','Cantidad']
            fig_n = px.bar(tipos, x='Cantidad', y='Novedad', orientation='h',
                          color='Cantidad', color_continuous_scale=['#12151f','#f59e0b','#ef4444'],
                          title='Top Tipos de Novedad')
            fig_n.update_layout(**PLOT_LAYOUT, height=380, coloraxis_showscale=False, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
            st.plotly_chart(fig_n, use_container_width=True)
        else:
            st.success("✅ Sin novedades registradas")

    elif "Tags" in op_nav and C_TAGS in df.columns:
        todos = []
        for tl in df['_tags_lista']: todos.extend(tl)
        if todos:
            tags_df = pd.DataFrame({'tag':todos})
            tags_df['cat'] = tags_df['tag'].apply(clasificar_tag)
            t1,t2,t3,t4 = st.tabs(["🚨 Seguimiento","❌ Cancelaciones","📊 Estratégico","📋 Todos"])
            def gtab(cat, paleta, titulo, h=320):
                d = tags_df[tags_df['cat']==cat]['tag'].value_counts().reset_index()
                d.columns = ['Tag','Cantidad']
                if len(d):
                    fig = px.bar(d, x='Cantidad', y='Tag', orientation='h', color='Cantidad',
                                color_continuous_scale=paleta, title=titulo)
                    fig.update_layout(**PLOT_LAYOUT, height=h, coloraxis_showscale=False, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                    st.plotly_chart(fig, use_container_width=True)
                else: st.info("Sin tags en esta categoría")
            with t1: gtab('seguimiento',['#12151f','#ef4444'],'Tags Seguimiento Activo')
            with t2:
                cr = tags_df[tags_df['cat']=='cancelacion_real']['tag'].value_counts().reset_index()
                cr.columns=['Tag','Cantidad']
                nc = tags_df[tags_df['cat']=='no_cancelacion']['tag'].value_counts().reset_index()
                nc.columns=['Tag','Cantidad']
                ca,cb = st.columns(2)
                with ca:
                    if len(cr):
                        fig=px.bar(cr,x='Cantidad',y='Tag',orientation='h',color='Cantidad',
                                  color_continuous_scale=['#12151f','#ef4444'],title='❌ Reales')
                        fig.update_layout(**PLOT_LAYOUT,height=300,coloraxis_showscale=False, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                        st.plotly_chart(fig,use_container_width=True)
                with cb:
                    if len(nc):
                        fig=px.bar(nc,x='Cantidad',y='Tag',orientation='h',color='Cantidad',
                                  color_continuous_scale=['#12151f','#10b981'],title='✅ No son cancelaciones')
                        fig.update_layout(**PLOT_LAYOUT,height=300,coloraxis_showscale=False, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                        st.plotly_chart(fig,use_container_width=True)
                tcr=len(tags_df[tags_df['cat']=='cancelacion_real'])
                tnc=len(tags_df[tags_df['cat']=='no_cancelacion'])
                if tcr+tnc>0:
                    st.markdown(f'<div style="background:rgba(16,185,129,0.08);border:1px solid #10b981;border-radius:10px;padding:14px;margin-top:8px">'
                                f'<b style="color:#e8ecf7">📊 Resumen:</b> '
                                f'<span class="badge-r">{tcr} cancelaciones reales</span> &nbsp; '
                                f'<span class="badge-v">{tnc} no son cancelaciones reales</span></div>', unsafe_allow_html=True)
            with t3: gtab('estrategico',['#12151f','#5b6cfc'],'Tags Estratégicos')
            with t4:
                top50=tags_df['tag'].value_counts().head(50).reset_index()
                top50.columns=['Tag','Cantidad']
                fig=px.bar(top50,x='Cantidad',y='Tag',orientation='h',color='Cantidad',
                          color_continuous_scale=['#12151f','#f0c060'],title='Top Tags')
                fig.update_layout(**PLOT_LAYOUT,height=900,coloraxis_showscale=False, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                st.plotly_chart(fig,use_container_width=True)

    elif "Monitor de Pedidos" in op_nav:
        st.markdown('<div class="seccion-titulo">📦 Monitor de Pedidos — Estatus Abiertos</div>', unsafe_allow_html=True)

        from datetime import date, timedelta

        # ── Definir paleta de colores por estatus ──
        COLORES_ESTATUS = {
            'EN CAMINO':            '#00d4ff',
            'EN PROCESO':           '#5b6cfc',
            'PENDIENTE':            '#f59e0b',
            'NOVEDAD':              '#ef4444',
            'DEVOLUCION EN CAMINO': '#f97316',
            'EN BODEGA':            '#7c3aed',
            'POR RECOGER':          '#ec4899',
            'REPROGRAMADO':         '#84cc16',
        }
        KEYWORDS_ABIERTOS = 'CAMINO|PROCESO|PENDIENTE|NOVEDAD|BODEGA|RECOGER|REPROG|GESTI'

        df_fil = df.copy()
        if C_ESTATUS in df_fil.columns:
            mask_ab = df_fil[C_ESTATUS].astype(str).str.upper().str.contains(KEYWORDS_ABIERTOS, na=False)
        else:
            mask_ab = pd.Series([True]*len(df_fil))

        # ═══════════════════════════════════════
        # FILTROS — fila 1
        # ═══════════════════════════════════════
        st.markdown('<div style="background:#161525;border:1px solid #2e2558;border-radius:12px;padding:14px 18px;margin-bottom:14px">', unsafe_allow_html=True)
        fc1,fc2,fc3,fc4,fc5,fc6 = st.columns([1,1.3,1.3,1.3,1.3,1])

        with fc1:
            mostrar_todos = st.checkbox("📋 Ver todos", value=False, key="mon_todos")
            if not mostrar_todos:
                df_fil = df_fil[mask_ab]

        with fc2:
            if C_ESTATUS in df.columns:
                opts_e = ['Todos'] + sorted(df_fil[C_ESTATUS].astype(str).unique().tolist())
                fe = st.selectbox("Estatus", opts_e, key="mon_est")
                if fe != 'Todos': df_fil = df_fil[df_fil[C_ESTATUS].astype(str) == fe]

        with fc3:
            if C_CIUDAD in df.columns:
                opts_c = ['Todas'] + sorted(df_fil[C_CIUDAD].astype(str).unique().tolist())
                fc_c = st.selectbox("🏙️ Ciudad", opts_c, key="mon_ciu")
                if fc_c != 'Todas': df_fil = df_fil[df_fil[C_CIUDAD].astype(str) == fc_c]

        with fc4:
            if C_TRANSP in df.columns:
                opts_t = ['Todas'] + sorted(df_fil[C_TRANSP].astype(str).unique().tolist())
                ft = st.selectbox("🚚 Transportadora", opts_t, key="mon_trn")
                if ft != 'Todas': df_fil = df_fil[df_fil[C_TRANSP].astype(str) == ft]

        with fc5:
            if C_TAGS in df.columns:
                opts_tg = ['Todos'] + sorted(df_fil[C_TAGS].dropna().astype(str).str.strip().unique().tolist())
                ftg = st.selectbox("🏷️ Tag", opts_tg, key="mon_tag")
                if ftg != 'Todos': df_fil = df_fil[df_fil[C_TAGS].astype(str).str.strip() == ftg]

        with fc6:
            if C_FECHA in df_fil.columns:
                try:
                    f_min = pd.to_datetime(df_fil[C_FECHA], errors='coerce').min()
                    f_max = pd.to_datetime(df_fil[C_FECHA], errors='coerce').max()
                    if pd.notna(f_min) and pd.notna(f_max):
                        rango = st.date_input("📅 Fechas", value=(f_min.date(), f_max.date()), key="mon_rango")
                        if len(rango) == 2:
                            f_desde, f_hasta = rango
                            mask_f = (pd.to_datetime(df_fil[C_FECHA], errors='coerce').dt.date >= f_desde) & \
                                     (pd.to_datetime(df_fil[C_FECHA], errors='coerce').dt.date <= f_hasta)
                            df_fil = df_fil[mask_f]
                except: pass

        st.markdown('</div>', unsafe_allow_html=True)

        # ═══════════════════════════════════════
        # KPIs RÁPIDOS
        # ═══════════════════════════════════════
        n_fil    = len(df_fil)
        ven_fil  = df_fil[C_TOTAL].sum()    if C_TOTAL    in df_fil.columns else 0
        gan_fil  = df_fil[C_GANANCIA].sum() if C_GANANCIA in df_fil.columns else 0
        nok_fil  = df_fil[C_NOVEDAD].dropna().astype(str).str.strip().ne('').sum() if C_NOVEDAD in df_fil.columns else 0
        flete_fil= df_fil[C_FLETE].sum()    if C_FLETE    in df_fil.columns else 0

        k1,k2,k3,k4,k5 = st.columns(5)
        with k1: st.markdown(kpi("blue",  "📦 Pedidos Abiertos", f"{n_fil:,}",       "Filtro actual"),            unsafe_allow_html=True)
        with k2: st.markdown(kpi("cyan",  "💰 Valor en Ruta",    fmt_money(ven_fil),  "Capital en tránsito"),      unsafe_allow_html=True)
        with k3: st.markdown(kpi("green", "📈 Ganancia Potencial",fmt_money(gan_fil), "Si todos se entregan"),     unsafe_allow_html=True)
        with k4: st.markdown(kpi("gold",  "🚚 Fletes Expuestos",  fmt_money(flete_fil),"Costo si hay problemas"),  unsafe_allow_html=True)
        with k5: st.markdown(kpi("red",   "⚠️ Con Novedad",       f"{nok_fil:,}",      "Requieren gestión urgente"),unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ═══════════════════════════════════════
        # MINI-CARDS POR TIPO DE ESTATUS
        # ═══════════════════════════════════════
        if C_ESTATUS in df_fil.columns and n_fil > 0:
            conteo_est = df_fil[C_ESTATUS].astype(str).str.upper().str.strip().value_counts()
            if len(conteo_est):
                mini_html = '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">'
                for est_n, cnt_e in conteo_est.head(8).items():
                    # Buscar color
                    color_e = '#8892b0'
                    for k_e, v_e in COLORES_ESTATUS.items():
                        if k_e in est_n:
                            color_e = v_e; break
                    pct_e = cnt_e / n_fil * 100
                    mini_html += (
                        f'<div style="background:{color_e}14;border:1px solid {color_e}44;'
                        f'border-radius:10px;padding:8px 14px;display:flex;flex-direction:column;align-items:center;'
                        f'min-width:110px">'
                        f'<div style="font-size:0.68rem;color:{color_e};font-weight:700;text-transform:uppercase;'
                        f'letter-spacing:0.04em;text-align:center;margin-bottom:4px">{est_n[:18]}</div>'
                        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:{color_e};font-size:1.1rem">{cnt_e:,}</div>'
                        f'<div style="font-size:0.68rem;color:#7a8aaa">{pct_e:.0f}% del total</div>'
                        f'</div>'
                    )
                mini_html += '</div>'
                st.markdown(mini_html, unsafe_allow_html=True)

        # ═══════════════════════════════════════
        # TABLA PRINCIPAL
        # ═══════════════════════════════════════
        cols_v = [c for c in [C_ID, C_FECHA, C_FECHA_MOV, C_ESTATUS, C_CLIENTE, C_PRODUCTO,
                               C_CIUDAD, C_DEPTO, C_TRANSP, C_GUIA, C_TOTAL, C_GANANCIA,
                               C_TAGS, C_NOVEDAD, C_NOV_SOL] if c in df_fil.columns]

        # Ordenar: más antiguo primero (más urgente)
        if C_FECHA_MOV in df_fil.columns:
            df_fil = df_fil.sort_values(C_FECHA_MOV, ascending=True, na_position='last')
        elif C_FECHA in df_fil.columns:
            df_fil = df_fil.sort_values(C_FECHA, ascending=True, na_position='last')

        # Paginación
        PAGE_SIZE = 100
        total_pags = max(1, (n_fil - 1) // PAGE_SIZE + 1)
        cp1, cp2 = st.columns([4,1])
        with cp2:
            pag_act = st.number_input("Página", min_value=1, max_value=total_pags, value=1, key="mon_pag")
        idx_ini = (pag_act - 1) * PAGE_SIZE
        idx_fin = min(idx_ini + PAGE_SIZE, n_fil)

        st.dataframe(
            df_fil[cols_v].iloc[idx_ini:idx_fin].reset_index(drop=True),
            use_container_width=True,
            height=480,
            column_config={
                C_TOTAL:    st.column_config.NumberColumn("💰 Valor",    format="$%,.0f"),
                C_GANANCIA: st.column_config.NumberColumn("📈 Ganancia", format="$%,.0f"),
                C_FLETE:    st.column_config.NumberColumn("🚚 Flete",    format="$%,.0f") if C_FLETE in df_fil.columns else None,
            }
        )

        cex1, cex2, cex3 = st.columns([2,2,1])
        with cex3:
            st.caption(f"📋 {idx_ini+1}–{idx_fin} de {n_fil:,} pedidos | Pág {pag_act}/{total_pags}")
        with cex1:
            if st.button("📥 Exportar filtro actual a Excel", key="exp_mon_ped"):
                import io
                buf = io.BytesIO()
                df_fil[cols_v].to_excel(buf, index=False)
                st.download_button("⬇️ Descargar Excel", buf.getvalue(),
                                   f"monitor_pedidos_{date.today()}.xlsx",
                                   "application/vnd.ms-excel", key="dl_mon_ped")
        with cex2:
            if st.button("📋 Exportar TODOS (sin filtro) a Excel", key="exp_mon_ped_all"):
                import io
                buf2 = io.BytesIO()
                df[cols_v].to_excel(buf2, index=False)
                st.download_button("⬇️ Descargar Completo", buf2.getvalue(),
                                   f"todos_pedidos_{date.today()}.xlsx",
                                   "application/vnd.ms-excel", key="dl_mon_ped_all")


    # ══════════════════════════════════════════════════════════════════
    # 🗓️ CALENDARIO ESTRATÉGICO ANUAL — Colombia + Chile
    # Modo importación con alertas 60 días antes
    # ══════════════════════════════════════════════════════════════════
    elif "Calendario" in op_nav:
        from datetime import date as _date_cal
        import calendar as _calendar_lib

        st.markdown('<div class="seccion-titulo">🗓️ Calendario Estratégico Anual</div>', unsafe_allow_html=True)

        # ── Base de datos de fechas estratégicas ──
        _anio = _date_cal.today().year
        _HOY_CAL = _date_cal.today()

        FECHAS_ESTRATEGICAS = {
            "Colombia": [
                # ENERO
                {"mes":1,"dia":1,  "nombre":"Año Nuevo",                    "ico":"🎆","tipo":"festivo",   "impacto":"alto",    "pais":"CO","tip":"Lanzar promociones de inicio de año. Liquida inventario navideño."},
                {"mes":1,"dia":6,  "nombre":"Día de Reyes",                 "ico":"👑","tipo":"comercial", "impacto":"alto",    "pais":"CO","tip":"Regalos infantiles, juguetes. Pauta 2 semanas antes."},
                {"mes":1,"dia":15, "nombre":"Regreso Escolar (inicio)",     "ico":"🎒","tipo":"temporada", "impacto":"muy_alto","pais":"CO","tip":"Útiles, uniformes, mochilas. Campaña desde dic."},
                # FEBRERO
                {"mes":2,"dia":14, "nombre":"San Valentín",                 "ico":"❤️","tipo":"comercial", "impacto":"alto",    "pais":"CO","tip":"Perfumes, joyería, ropa íntima, accesorios. Pauta 10 días antes."},
                {"mes":2,"dia":5,  "nombre":"Carnaval de Barranquilla",     "ico":"🎭","tipo":"regional",  "impacto":"medio",   "pais":"CO","tip":"Disfraces, artículos festivos. Mercado Atlántico."},
                # MARZO
                {"mes":3,"dia":8,  "nombre":"Día Internacional de la Mujer","ico":"🌸","tipo":"comercial", "impacto":"muy_alto","pais":"CO","tip":"Cosméticos, accesorios, moda femenina. Campaña masiva 2 sem antes."},
                {"mes":3,"dia":19, "nombre":"Día del Padre (Colombia)",     "ico":"👔","tipo":"comercial", "impacto":"alto",    "pais":"CO","tip":"Ropa, accesorios, artículos deportivos, gadgets."},
                # ABRIL
                {"mes":4,"dia":None,"nombre":"Semana Santa",                "ico":"✝️","tipo":"festivo",   "impacto":"medio",   "pais":"CO","tip":"Turismo y religiosa. Bajas ventas e-com. Prepara post-SS."},
                {"mes":4,"dia":23, "nombre":"Día del Libro (Feria Bogotá)", "ico":"📚","tipo":"cultural",  "impacto":"bajo",    "pais":"CO","tip":"Papelería, libros, artículos educativos."},
                # MAYO
                {"mes":5,"dia":12, "nombre":"Día de la Madre",              "ico":"💐","tipo":"comercial", "impacto":"muy_alto","pais":"CO","tip":"¡EVENTO MÁS GRANDE! Perfumes, flores, spa, moda. Campaña desde abril 15."},
                {"mes":5,"dia":25, "nombre":"Feria del Libro Bogotá (cierre)","ico":"📖","tipo":"cultural","impacto":"bajo",    "pais":"CO","tip":"Útiles educativos, papelería premium."},
                # JUNIO
                {"mes":6,"dia":1,  "nombre":"Inicio Vacaciones Escolares",  "ico":"🏖️","tipo":"temporada", "impacto":"alto",    "pais":"CO","tip":"Juguetes, ropa verano, viajes. Campaña familiar."},
                {"mes":6,"dia":20, "nombre":"Liquidaciones Mitad de Año",   "ico":"🏷️","tipo":"comercial", "impacto":"alto",    "pais":"CO","tip":"Rotar inventario semestre 1. Descuentos agresivos."},
                # JULIO
                {"mes":7,"dia":20, "nombre":"Día de la Independencia",      "ico":"🇨🇴","tipo":"festivo",  "impacto":"medio",   "pais":"CO","tip":"Decoración patria, eventos. Baja conversión."},
                # AGOSTO
                {"mes":8,"dia":7,  "nombre":"Batalla de Boyacá",            "ico":"⚔️","tipo":"festivo",   "impacto":"bajo",    "pais":"CO","tip":"Festivo nacional. Foco en entregas previas."},
                {"mes":8,"dia":1,  "nombre":"Feria de las Flores (Medellín)","ico":"🌺","tipo":"regional", "impacto":"alto",    "pais":"CO","tip":"Artesanías, flores, moda típica. Mercado Antioquia."},
                {"mes":8,"dia":15, "nombre":"Regreso a Clases (2do sem)",   "ico":"✏️","tipo":"temporada", "impacto":"muy_alto","pais":"CO","tip":"Útiles, uniformes, tecnología educativa."},
                # SEPTIEMBRE
                {"mes":9,"dia":20, "nombre":"Amor y Amistad",               "ico":"🤝","tipo":"comercial", "impacto":"muy_alto","pais":"CO","tip":"¡ÚNICO EN COLOMBIA! Detalles, accesorios, perfumes. Pauta desde sep 1."},
                # OCTUBRE
                {"mes":10,"dia":12,"nombre":"Día de la Raza (festivo)",     "ico":"🗓️","tipo":"festivo",   "impacto":"bajo",    "pais":"CO","tip":"Festivo. Planifica envíos evitando este día."},
                {"mes":10,"dia":31,"nombre":"Halloween",                    "ico":"🎃","tipo":"comercial", "impacto":"medio",   "pais":"CO","tip":"Disfraces, dulces, decoración. Creciendo en Col."},
                {"mes":10,"dia":20,"nombre":"Pre-Black Friday (anticipo)",  "ico":"🔥","tipo":"comercial", "impacto":"alto",    "pais":"CO","tip":"Calentar audiencia. Teaser de ofertas BF."},
                # NOVIEMBRE
                {"mes":11,"dia":None,"nombre":"Black Friday / Cyber Monday","ico":"🖤","tipo":"comercial", "impacto":"muy_alto","pais":"CO","tip":"SEMANA DE MAYOR CONVERSIÓN. Stock listo, pauta máxima desde nov 1."},
                {"mes":11,"dia":15,"nombre":"Inicio Temporada Navidad",     "ico":"🎄","tipo":"temporada", "impacto":"muy_alto","pais":"CO","tip":"Decoración, regalos, ropa festiva. La temporada más larga."},
                # DICIEMBRE
                {"mes":12,"dia":7, "nombre":"Noche de Velitas",             "ico":"🕯️","tipo":"cultural",  "impacto":"medio",   "pais":"CO","tip":"Velas, decoración, artículos navideños. Ventas pick."},
                {"mes":12,"dia":16,"nombre":"Inicio Novenas de Aguinaldo",  "ico":"⭐","tipo":"cultural",  "impacto":"alto",    "pais":"CO","tip":"Temporada pico total. Stock al máximo."},
                {"mes":12,"dia":25,"nombre":"Navidad",                      "ico":"🎁","tipo":"festivo",   "impacto":"muy_alto","pais":"CO","tip":"Máximas ventas del año. Post-Navidad: canje de regalos."},
                {"mes":12,"dia":31,"nombre":"Fin de Año",                   "ico":"🎊","tipo":"comercial", "impacto":"alto",    "pais":"CO","tip":"Ropa nueva año, accesorios. Liquidación final inventario."},
            ],
            "Chile": [
                # ENERO
                {"mes":1,"dia":1,  "nombre":"Año Nuevo",                    "ico":"🎆","tipo":"festivo",   "impacto":"alto",    "pais":"CL","tip":"Verano chileno. Alta actividad consumo."},
                {"mes":1,"dia":15, "nombre":"Temporada Verano (peak)",      "ico":"🏖️","tipo":"temporada", "impacto":"muy_alto","pais":"CL","tip":"Ropa verano, protección solar, artículos playa."},
                # FEBRERO
                {"mes":2,"dia":14, "nombre":"San Valentín",                 "ico":"❤️","tipo":"comercial", "impacto":"alto",    "pais":"CL","tip":"Regalos de pareja. Joyería, perfumes, experiencias."},
                {"mes":2,"dia":None,"nombre":"Carnaval con la Fuerza del Sol","ico":"🌞","tipo":"regional","impacto":"medio",   "pais":"CL","tip":"Arica. Artículos festivos, artesanías norteñas."},
                # MARZO
                {"mes":3,"dia":8,  "nombre":"Día de la Mujer",              "ico":"🌸","tipo":"comercial", "impacto":"muy_alto","pais":"CL","tip":"Cosméticos, moda, accesorios. Campaña 2 sem antes."},
                {"mes":3,"dia":20, "nombre":"Regreso Escolar (otoño)",      "ico":"🎒","tipo":"temporada", "impacto":"muy_alto","pais":"CL","tip":"Útiles, uniformes, tecnología educativa."},
                # ABRIL
                {"mes":4,"dia":None,"nombre":"Semana Santa",                "ico":"✝️","tipo":"festivo",   "impacto":"medio",   "pais":"CL","tip":"Festivo nacional. Turismo playa/montaña."},
                # MAYO
                {"mes":5,"dia":1,  "nombre":"Día del Trabajo",              "ico":"⚒️","tipo":"festivo",   "impacto":"bajo",    "pais":"CL","tip":"Festivo. Ropa laboral, herramientas."},
                {"mes":5,"dia":21, "nombre":"Día de las Glorias Navales",   "ico":"⚓","tipo":"festivo",   "impacto":"bajo",    "pais":"CL","tip":"Festivo. Baja actividad e-commerce."},
                {"mes":5,"dia":12, "nombre":"Día de la Madre (Chile)",      "ico":"💐","tipo":"comercial", "impacto":"muy_alto","pais":"CL","tip":"¡EVENTO CLAVE CHILE! Perfumes, flores, spa, moda."},
                # JUNIO
                {"mes":6,"dia":None,"nombre":"CyberDay Chile",              "ico":"💻","tipo":"comercial", "impacto":"muy_alto","pais":"CL","tip":"Equivalente al BF chileno. El mayor evento e-com del año."},
                {"mes":6,"dia":16, "nombre":"Día del Padre (Chile)",        "ico":"👔","tipo":"comercial", "impacto":"alto",    "pais":"CL","tip":"Ropa, electrónicos, herramientas, deportes."},
                # JULIO
                {"mes":7,"dia":16, "nombre":"Día de la Virgen del Carmen",  "ico":"⛪","tipo":"festivo",   "impacto":"bajo",    "pais":"CL","tip":"Festivo. Turismo interior."},
                {"mes":7,"dia":None,"nombre":"Vacaciones Invierno Escolar", "ico":"❄️","tipo":"temporada", "impacto":"alto",    "pais":"CL","tip":"Abrigos, calefacción, artículos hogar."},
                # AGOSTO
                {"mes":8,"dia":15, "nombre":"Asunción de la Virgen",        "ico":"🕊️","tipo":"festivo",   "impacto":"bajo",    "pais":"CL","tip":"Festivo. Evitar lanzamientos este día."},
                # SEPTIEMBRE
                {"mes":9,"dia":18, "nombre":"Fiestas Patrias Chile",        "ico":"🇨🇱","tipo":"festivo",  "impacto":"muy_alto","pais":"CL","tip":"¡EVENTO NACIONAL! Ropa típica, empanadas, chicha. Ventas masivas."},
                {"mes":9,"dia":19, "nombre":"Día de las Glorias del Ejército","ico":"🎖️","tipo":"festivo", "impacto":"medio",   "pais":"CL","tip":"Festivo ext. Patrias. Temporada alto consumo."},
                # OCTUBRE
                {"mes":10,"dia":12,"nombre":"Encuentro de Dos Mundos",      "ico":"🌍","tipo":"festivo",   "impacto":"bajo",    "pais":"CL","tip":"Festivo. Baja actividad."},
                {"mes":10,"dia":31,"nombre":"Halloween",                    "ico":"🎃","tipo":"comercial", "impacto":"alto",    "pais":"CL","tip":"Muy popular en Chile. Disfraces, decoración, dulces."},
                # NOVIEMBRE
                {"mes":11,"dia":1, "nombre":"Día de Todos los Santos",      "ico":"🕯️","tipo":"festivo",   "impacto":"bajo",    "pais":"CL","tip":"Festivo. Flores, velas."},
                {"mes":11,"dia":None,"nombre":"Black Friday Chile",         "ico":"🖤","tipo":"comercial", "impacto":"muy_alto","pais":"CL","tip":"SEMANA CLAVE. Stock preparado, pauta máxima."},
                # DICIEMBRE
                {"mes":12,"dia":8, "nombre":"Inmaculada Concepción",        "ico":"⛪","tipo":"festivo",   "impacto":"bajo",    "pais":"CL","tip":"Festivo. Inicio fuerte temporada navideña."},
                {"mes":12,"dia":25,"nombre":"Navidad",                      "ico":"🎁","tipo":"festivo",   "impacto":"muy_alto","pais":"CL","tip":"Temporada de mayor volumen de ventas."},
                {"mes":12,"dia":31,"nombre":"Fin de Año",                   "ico":"🎊","tipo":"comercial", "impacto":"alto",    "pais":"CL","tip":"Ropa nueva, accesorios. Verano chileno."},
            ]
        }

        MESES_NOMBRES = ["","Enero","Febrero","Marzo","Abril","Mayo","Junio",
                         "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

        IMPACTO_COLOR = {"muy_alto":"#ef4444","alto":"#f59e0b","medio":"#5b6cfc","bajo":"#8892b0"}
        IMPACTO_LABEL = {"muy_alto":"🔴 Muy Alto","alto":"🟡 Alto","medio":"🔵 Medio","bajo":"⚫ Bajo"}

        # ── Controles ──
        _cal_c1, _cal_c2, _cal_c3 = st.columns([1.5, 1.5, 2])
        with _cal_c1:
            _pais_cal = st.radio("País", ["🇨🇴 Colombia","🇨🇱 Chile"], horizontal=True, key="cal_pais", label_visibility="collapsed")
        with _cal_c2:
            _mes_cal_op = st.selectbox("Mes", list(range(1,13)),
                index=_HOY_CAL.month - 1,
                format_func=lambda m: MESES_NOMBRES[m], key="cal_mes_op",
                label_visibility="collapsed")
        with _cal_c3:
            _impacto_filter = st.multiselect(
                "Impacto", ["muy_alto","alto","medio","bajo"],
                default=["muy_alto","alto"],
                format_func=lambda x: IMPACTO_LABEL[x],
                key="cal_impacto_filter",
                label_visibility="collapsed"
            )

        _pais_key = "Colombia" if "Colombia" in _pais_cal else "Chile"
        _fechas_pais = FECHAS_ESTRATEGICAS[_pais_key]

        # ══════════════════════════════════════
        # 🔔 MODO IMPORTACIÓN — Próximas 60 días
        # ══════════════════════════════════════
        st.markdown("<br>", unsafe_allow_html=True)

        _proximas_imp = []
        for _fe in _fechas_pais:
            _d = _fe.get("dia") or 1
            try:
                _fecha_ev = _date_cal(_anio, _fe["mes"], _d)
            except:
                continue
            _diff = (_fecha_ev - _HOY_CAL).days
            if -5 <= _diff <= 90:  # Incluye eventos hasta 90 días
                _proximas_imp.append({**_fe, "_fecha": _fecha_ev, "_dias": _diff})

        _proximas_imp.sort(key=lambda x: x["_dias"])

        if _proximas_imp:
            st.markdown(
                '<div style="background:rgba(201,168,76,0.1);border:1px solid #f0c06044;border-radius:12px;padding:14px 18px;margin-bottom:18px">'
                '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#fcd34d;font-size:0.95rem;margin-bottom:12px">'
                '⚡ Modo Importación — Equipo de Proyecto Activado</div>',
                unsafe_allow_html=True
            )
            _imp_cols = st.columns(min(len(_proximas_imp), 3))
            for _i, _fe_p in enumerate(_proximas_imp[:3]):
                _dias_p = _fe_p["_dias"]
                if _dias_p < 0:
                    _color_p = "#8892b0"; _estado = f"Hace {abs(_dias_p)} días"
                elif _dias_p == 0:
                    _color_p = "#ef4444"; _estado = "⚡ HOY"
                elif _dias_p <= 14:
                    _color_p = "#ef4444"; _estado = f"🔴 {_dias_p} días"
                elif _dias_p <= 30:
                    _color_p = "#f59e0b"; _estado = f"🟡 {_dias_p} días"
                else:
                    _color_p = "#5b6cfc"; _estado = f"🔵 {_dias_p} días"

                with _imp_cols[_i % 3]:
                    st.markdown(
                        f'<div style="background:#13102a;border:1px solid {_color_p}44;border-radius:10px;padding:14px;text-align:center">'
                        f'<div style="font-size:1.6rem">{_fe_p["ico"]}</div>'
                        f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:{_color_p};font-size:1.4rem;margin:4px 0">{_estado}</div>'
                        f'<div style="color:#e8ecf7;font-size:0.82rem;font-weight:700">{_fe_p["nombre"]}</div>'
                        f'<div style="color:#a8b4d0;font-size:0.72rem;margin-top:4px">{_fe_p["_fecha"].strftime("%d/%m/%Y")}</div>'
                        f'<div style="background:{_color_p}15;border-radius:6px;padding:6px 8px;margin-top:8px;font-size:0.72rem;color:#c8d0e8;text-align:left">'
                        f'📌 {_fe_p["tip"]}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
            st.markdown("</div>", unsafe_allow_html=True)

            # Mostrar próximos 60 días completos como línea de tiempo
            _todos_60 = [f for f in _proximas_imp if 0 < f["_dias"] <= 60]
            if _todos_60:
                st.markdown(
                    '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:700;color:#e8ecf7;font-size:0.85rem;margin:12px 0 8px">📆 Próximos 60 días — Plan de Importación</div>',
                    unsafe_allow_html=True
                )
                for _ev60 in _todos_60:
                    _col_ev = IMPACTO_COLOR.get(_ev60["impacto"], "#8892b0")
                    _lbl_ev = IMPACTO_LABEL.get(_ev60["impacto"], "")
                    st.markdown(
                        f'<div style="display:flex;align-items:center;gap:12px;padding:10px 14px;'
                        f'margin-bottom:6px;background:#13102a;border-left:3px solid {_col_ev};border-radius:8px">'
                        f'<div style="font-size:1.3rem;min-width:30px">{_ev60["ico"]}</div>'
                        f'<div style="flex:1">'
                        f'<span style="color:#e8ecf7;font-weight:700;font-size:0.84rem">{_ev60["nombre"]}</span>'
                        f'<span style="color:#a8b4d0;font-size:0.72rem;margin-left:8px">{_ev60["_fecha"].strftime("%d/%m/%Y")}</span>'
                        f'</div>'
                        f'<div style="background:{_col_ev}20;color:{_col_ev};padding:3px 10px;border-radius:20px;font-size:0.7rem;font-weight:700;white-space:nowrap">'
                        f'Restan {_ev60["_dias"]} días</div>'
                        f'<div style="background:#1e2337;color:#a8b4d0;padding:3px 10px;border-radius:20px;font-size:0.7rem;white-space:nowrap">'
                        f'{_lbl_ev}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.95rem;margin-bottom:12px">'
            f'📅 {MESES_NOMBRES[_mes_cal_op]} {_anio} — {"🇨🇴 Colombia" if _pais_key=="Colombia" else "🇨🇱 Chile"}</div>',
            unsafe_allow_html=True
        )

        # ── Vista del mes seleccionado ──
        _fechas_mes = [f for f in _fechas_pais if f["mes"] == _mes_cal_op and f["impacto"] in _impacto_filter]

        if not _fechas_mes:
            st.info("No hay eventos estratégicos para este mes con los filtros seleccionados.")
        else:
            for _fe_m in _fechas_mes:
                _col_m = IMPACTO_COLOR.get(_fe_m["impacto"], "#8892b0")
                _dia_str = f'{_fe_m["dia"]:02d}/{_mes_cal_op:02d}/{_anio}' if _fe_m.get("dia") else f'{MESES_NOMBRES[_mes_cal_op]}'
                try:
                    _fecha_ev_m = _date_cal(_anio, _fe_m["mes"], _fe_m.get("dia") or 1)
                    _diff_m = (_fecha_ev_m - _HOY_CAL).days
                    _diff_lbl = f"Restan {_diff_m} días" if _diff_m > 0 else ("HOY 🔴" if _diff_m == 0 else f"Hace {abs(_diff_m)} días")
                except:
                    _diff_lbl = ""

                st.markdown(
                    f'<div style="border-left:4px solid {_col_m};background:{_col_m}08;border-radius:0 10px 10px 0;'
                    f'padding:14px 16px;margin-bottom:10px">'
                    f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">'
                    f'<span style="font-size:1.5rem">{_fe_m["ico"]}</span>'
                    f'<span style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.9rem">{_fe_m["nombre"]}</span>'
                    f'<span style="color:#a8b4d0;font-size:0.75rem">{_dia_str}</span>'
                    f'<span style="background:{_col_m}20;color:{_col_m};padding:2px 10px;border-radius:20px;font-size:0.7rem;font-weight:700;margin-left:auto">'
                    f'{IMPACTO_LABEL[_fe_m["impacto"]]}</span>'
                    f'<span style="background:#1e2337;color:#a8b4d0;padding:2px 10px;border-radius:20px;font-size:0.7rem">'
                    f'{_fe_m["tipo"].capitalize()}</span>'
                    f'{"<span style=background:#ef444420;color:#ef4444;padding:2px 10px;border-radius:20px;font-size:0.7rem;font-weight:700>" + _diff_lbl + "</span>" if _diff_lbl else ""}'
                    f'</div>'
                    f'<div style="background:rgba(255,255,255,0.04);border-radius:6px;padding:8px 12px;font-size:0.78rem;color:#c8d0e8">'
                    f'💡 {_fe_m["tip"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        # ── Vista anual completa (acordeón por mes) ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div style="font-family:Plus Jakarta Sans,sans-serif;font-weight:800;color:#e8ecf7;font-size:0.88rem;margin-bottom:10px">'
            f'📆 Año Completo {_anio} — {"🇨🇴 Colombia" if _pais_key=="Colombia" else "🇨🇱 Chile"}</div>',
            unsafe_allow_html=True
        )
        for _m_idx in range(1, 13):
            _fevs_m = [f for f in _fechas_pais if f["mes"] == _m_idx]
            if not _fevs_m:
                continue
            _muy_alto_m = any(f["impacto"] == "muy_alto" for f in _fevs_m)
            _ico_mes = "🔴" if _muy_alto_m else "🟡"
            with st.expander(f"{_ico_mes} {MESES_NOMBRES[_m_idx]} — {len(_fevs_m)} evento{'s' if len(_fevs_m)>1 else ''}"):
                for _fe_a in _fevs_m:
                    _col_a = IMPACTO_COLOR.get(_fe_a["impacto"], "#8892b0")
                    st.markdown(
                        f'<div style="display:flex;align-items:center;gap:8px;padding:8px 10px;margin-bottom:4px;'
                        f'background:{_col_a}08;border-left:3px solid {_col_a};border-radius:0 8px 8px 0">'
                        f'<span>{_fe_a["ico"]}</span>'
                        f'<span style="color:#e8ecf7;font-size:0.82rem;font-weight:700;flex:1">{_fe_a["nombre"]}</span>'
                        f'<span style="background:{_col_a}20;color:{_col_a};padding:2px 8px;border-radius:12px;font-size:0.68rem;font-weight:700">'
                        f'{IMPACTO_LABEL[_fe_a["impacto"]]}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown(f'<div style="color:#a8b4d0;font-size:0.73rem;padding:0 10px 8px 36px">💡 {_fe_a["tip"]}</div>', unsafe_allow_html=True)


    # Claude
    st.divider()
    CLAUDE_ACTIVO = False
    if CLAUDE_ACTIVO:
        import anthropic
        st.markdown('<div class="seccion-titulo">🤖 Asistente Claude</div>', unsafe_allow_html=True)
        resumen = f"Pedidos:{total}, Entregados:{entregados}({pct_ent}%), Cancelados:{cancelados}, Alertas críticas:{len(alertas_r)}"
        if "messages" not in st.session_state: st.session_state.messages=[]
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.write(msg["content"])
        if prompt:=st.chat_input("Pregúntame sobre tus pedidos..."):
            st.session_state.messages.append({"role":"user","content":prompt})
            with st.chat_message("user"): st.write(prompt)
            with st.chat_message("assistant"):
                client=anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
                ph=st.empty(); resp=""
                with client.messages.stream(model="claude-sonnet-4-6",max_tokens=1024,
                    system=f"Eres el asistente de VisióN360 para e-commerce en Colombia. Datos:{resumen}. Responde en español.",
                    messages=st.session_state.messages) as stream:
                    for text in stream.text_stream:
                        resp+=text; ph.write(resp+"▌")
                ph.write(resp)
            st.session_state.messages.append({"role":"assistant","content":resp})
    else:
        st.markdown('<div style="background:rgba(201,168,76,0.08);border:1px solid #f0c060;border-radius:12px;padding:14px;text-align:center;color:#fef08a;font-size:0.85rem">🤖 Claude IA se activa cuando configures tu API Key · El dashboard funciona completo sin él</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center;color:#6b7a9e;font-size:0.7rem;margin-top:30px">🚀 VisióN360 · Inteligencia Comercial</div>', unsafe_allow_html=True)
