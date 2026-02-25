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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800&family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}
.stApp { background-color: #0f0e17; }
.block-container { padding: 1.5rem 2rem; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1829 0%, #0f0e17 100%);
    border-right: 1px solid #2d2b45;
}
section[data-testid="stSidebar"] * { color: #e8e6f0 !important; }

/* TÍTULOS */
h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

/* TARJETAS KPI */
.kpi {
    background: linear-gradient(135deg, #1a1829 0%, #1f1d35 100%);
    border: 1px solid #2d2b45;
    border-radius: 16px;
    padding: 22px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
}
.kpi::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.kpi.gold::before  { background: linear-gradient(90deg, #c9a84c, #f0d080); }
.kpi.green::before { background: linear-gradient(90deg, #10b981, #34d399); }
.kpi.red::before   { background: linear-gradient(90deg, #ef4444, #f87171); }
.kpi.blue::before  { background: linear-gradient(90deg, #6366f1, #818cf8); }
.kpi.purple::before{ background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
.kpi.cyan::before  { background: linear-gradient(90deg, #06b6d4, #67e8f9); }

.kpi-num {
    font-family: 'Playfair Display', serif;
    font-size: 2.1rem;
    font-weight: 800;
    color: #f0ede8;
    margin: 10px 0 4px;
    letter-spacing: -0.02em;
}
.kpi-label {
    font-size: 0.7rem;
    color: #8b8aaa;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.kpi-sub { font-size: 0.82rem; color: #10b981; font-weight: 600; margin-top: 6px; }

/* TARJETA PRODUCTO ESTRELLA */
.prod-card {
    background: linear-gradient(135deg, #1a1829 0%, #1f1d35 100%);
    border: 1px solid #2d2b45;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.prod-rank {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #c9a84c;
    min-width: 40px;
}
.prod-name { font-size: 0.9rem; font-weight: 600; color: #f0ede8; }
.prod-val  { font-size: 0.8rem; color: #8b8aaa; margin-top: 3px; }

/* ALERTAS */
.alerta-r {
    background: rgba(239,68,68,0.08);
    border-left: 3px solid #ef4444;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 5px 0;
    font-size: 0.84rem;
    color: #f0ede8;
}
.alerta-a {
    background: rgba(245,158,11,0.08);
    border-left: 3px solid #f59e0b;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 5px 0;
    font-size: 0.84rem;
    color: #f0ede8;
}

/* INSIGHT CARD */
.insight {
    background: linear-gradient(135deg, #1a1829, #1f1d35);
    border: 1px solid #2d2b45;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 12px;
}
.insight-titulo { font-family: 'Playfair Display', serif; font-size: 1rem; color: #c9a84c; font-weight: 700; margin-bottom: 8px; }
.insight-texto  { font-size: 0.86rem; color: #b0aec8; line-height: 1.6; }

/* BADGES */
.badge-r  { background: rgba(239,68,68,0.15); color:#f87171; border:1px solid #ef4444; border-radius:20px; padding:2px 10px; font-size:0.73rem; font-weight:700; }
.badge-a  { background: rgba(245,158,11,0.15); color:#fbbf24; border:1px solid #f59e0b; border-radius:20px; padding:2px 10px; font-size:0.73rem; font-weight:700; }
.badge-v  { background: rgba(16,185,129,0.15); color:#34d399; border:1px solid #10b981; border-radius:20px; padding:2px 10px; font-size:0.73rem; font-weight:700; }
.badge-g  { background: rgba(201,168,76,0.15); color:#f0d080; border:1px solid #c9a84c; border-radius:20px; padding:2px 10px; font-size:0.73rem; font-weight:700; }

/* SECCIÓN */
.seccion-titulo {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #f0ede8;
    border-bottom: 1px solid #2d2b45;
    padding-bottom: 10px;
    margin: 28px 0 18px 0;
}

/* TABLA */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* UPLOADER */
.stFileUploader {
    background: #1a1829 !important;
    border: 2px dashed #2d2b45 !important;
    border-radius: 14px !important;
}

/* Streamlit overrides */
div[data-testid="stMetricValue"] { color: #f0ede8; }
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
    font=dict(family='Space Grotesk', color='#b0aec8', size=12),
    title_font=dict(family='Syne', color='#f0ede8', size=16),
    legend=dict(font=dict(color='#b0aec8', size=11), bgcolor='rgba(0,0,0,0)'),
    margin=dict(l=10, r=10, t=50, b=10)
)
AXIS_STYLE = dict(gridcolor='#2d2b45', linecolor='#2d2b45', tickfont=dict(color='#8b8aaa'))
COLORES_ELEGANTES = ['#c9a84c','#6366f1','#10b981','#ef4444','#06b6d4','#8b5cf6','#f59e0b','#ec4899','#14b8a6','#f97316']

# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:24px 12px 16px;text-align:center">
        <div style="display:inline-flex;align-items:center;justify-content:center;
                    width:56px;height:56px;border-radius:16px;margin-bottom:14px;
                    background:linear-gradient(135deg,#6366f1 0%,#06b6d4 100%);
                    box-shadow:0 8px 24px rgba(99,102,241,0.35)">
            <span style="font-size:1.7rem;line-height:1">🌐</span>
        </div>
        <div style="font-family:'Syne',sans-serif;font-size:1.55rem;font-weight:800;
                    color:#f0ede8;letter-spacing:-0.02em;line-height:1;margin-bottom:6px">
            Visió<span style="background:linear-gradient(90deg,#6366f1,#06b6d4);
                              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                              background-clip:text">N360</span>
        </div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:0.68rem;
                    color:#5a5878;font-weight:500;letter-spacing:0.08em;
                    text-transform:uppercase;line-height:1.5">
            Todo tu negocio<br>una sola vista
        </div>
    </div>
    <div style="height:1px;background:linear-gradient(90deg,transparent,#2d2b45,transparent);
                margin:0 0 16px"></div>
    """, unsafe_allow_html=True)

    # Sección PANEL PRINCIPAL
    st.markdown('<div style="font-size:0.62rem;color:#5a5878;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;padding:0 4px;margin-bottom:6px">PANEL PRINCIPAL</div>', unsafe_allow_html=True)

    # PANEL PRINCIPAL — un solo radio unificado
    st.markdown('<div style="font-size:0.58rem;color:#3d3b55;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;padding:2px 4px;margin:4px 0 6px">ANÁLISIS</div>', unsafe_allow_html=True)
    vista = st.radio("", [
        "📊  Panel Ejecutivo",
        "📈  P&G",
        "💹  Finanzas",
        "🔮  Proyecciones",
    ], label_visibility="collapsed")

    st.markdown('<div style="font-size:0.58rem;color:#3d3b55;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;padding:2px 4px;margin:14px 0 6px">OPERACIONAL</div>', unsafe_allow_html=True)
    vista2 = st.radio("_op", [
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

    # Resaltar Monitor de Estatus visualmente cuando está activo
    if "Monitor" in vista_activa:
        st.markdown(f'''
        <div style="background:rgba(6,182,212,0.1);border:1px solid #06b6d4;border-radius:8px;
                    padding:8px 12px;margin:6px 0;font-size:0.8rem;color:#67e8f9;font-weight:600">
            🚦 Monitor activo
        </div>''', unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#2d2b45;margin:16px 0'>", unsafe_allow_html=True)

    # Sección OPERACIONES
    st.markdown('<div style="font-size:0.62rem;color:#5a5878;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;padding:0 4px;margin-bottom:8px">OPERACIÓN ACTIVA</div>', unsafe_allow_html=True)

    OPERACIONES = {
        "🤖  LUCID BOT":      {"pais": "🇨🇴 Colombia", "moneda": "COP", "color": "#6366f1",
                               "bg": "rgba(99,102,241,0.08)",  "border": "#6366f1"},
        "✨  ESSENTYA":        {"pais": "🇨🇴 Colombia", "moneda": "COP", "color": "#ec4899",
                               "bg": "rgba(236,72,153,0.08)",  "border": "#ec4899"},
        "🐂  EL TORO":         {"pais": "🇨🇴 Colombia", "moneda": "COP", "color": "#ef4444",
                               "bg": "rgba(239,68,68,0.08)",   "border": "#ef4444"},
        "🛒  Carrito Naranja": {"pais": "🇨🇱 Chile",    "moneda": "CLP", "color": "#f97316",
                               "bg": "rgba(249,115,22,0.08)",  "border": "#f97316"},
    }

    operacion = st.radio("", list(OPERACIONES.keys()), label_visibility="collapsed")
    op_info = OPERACIONES[operacion]
    es_clp   = op_info["moneda"] == "CLP"

    st.markdown(f'''<div style="background:{op_info["bg"]};border:1px solid {op_info["border"]};
        border-radius:8px;padding:8px 12px;margin:8px 0;font-size:0.8rem;
        color:{op_info["color"]};font-weight:600">
        {op_info["pais"]} · {op_info["moneda"]}
    </div>''', unsafe_allow_html=True)

    # TRM solo para Carrito Naranja
    trm_clp_cop = 4.2
    if es_clp:
        st.markdown("<hr style='border-color:#2d2b45;margin:12px 0 8px'>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.62rem;color:#5a5878;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;padding:0 4px;margin-bottom:6px">💱 CONVERSIÓN CLP → COP</div>', unsafe_allow_html=True)
        trm_clp_cop = st.number_input(
            "1 CLP = ? COP",
            min_value=1.0, max_value=20.0,
            value=4.2, step=0.1,
            help="Tasa de cambio CLP a COP. Actualiza según el valor del día. (Referencia: 1 CLP ≈ 4.2 COP)"
        )
        st.markdown(f'<div style="font-size:0.75rem;color:#8b8aaa;padding:4px">= ${trm_clp_cop:.2f} COP por cada CLP</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#2d2b45;margin:16px 0'>", unsafe_allow_html=True)

    # Sección DATOS
    st.markdown('<div style="font-size:0.62rem;color:#5a5878;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;padding:0 4px;margin-bottom:8px">IMPORTAR DATOS</div>', unsafe_allow_html=True)
    archivo = st.file_uploader(f"📁 Reporte {operacion.split('  ')[1]}", type=["xlsx","xls"],
                               help="Exporta el reporte de órdenes desde Dropi")

    if archivo:
        st.markdown(f'''<div style="background:{op_info["bg"]};border:1px solid {op_info["border"]};
            border-radius:8px;padding:10px;text-align:center;font-size:0.8rem;
            color:{op_info["color"]};margin-top:10px">
            ✅ {operacion.split("  ")[1]}<br>
            <span style="font-size:0.72rem;opacity:0.8">Archivo cargado</span>
        </div>''', unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#2d2b45;margin:16px 0'>", unsafe_allow_html=True)

    # Sección CONFIGURACIÓN
    st.markdown('<div style="font-size:0.62rem;color:#5a5878;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;padding:0 4px;margin-bottom:8px">CONFIGURACIÓN</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.82rem;color:#8b8aaa;padding:6px 4px;cursor:pointer">⚙️  Configuración</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.82rem;color:#8b8aaa;padding:6px 4px;cursor:pointer">🌐  Colombia · CO</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="position:fixed;bottom:20px;left:0;width:260px;text-align:center">
        <div style="font-size:0.7rem;color:#3d3b55">VisióN360 · v2.0 · Colombia</div>
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
        'background:linear-gradient(135deg,#6366f1 0%,#06b6d4 100%);'
        'box-shadow:0 16px 48px rgba(99,102,241,0.3)">'
        '<span style="font-size:3rem;line-height:1">&#127758;</span>'
        '</div>'

        '<div style="font-family:Syne,sans-serif;font-size:3.2rem;font-weight:800;'
        'color:#f0ede8;letter-spacing:-0.03em;line-height:1;margin-bottom:10px">'
        'Visi&#243;'
        '<span style="background:linear-gradient(90deg,#6366f1,#06b6d4);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'background-clip:text">N360</span>'
        '</div>'

        '<div style="font-family:Space Grotesk,sans-serif;font-size:1rem;color:#5a5878;'
        'font-weight:500;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:36px">'
        'Todo tu negocio &nbsp;&middot;&nbsp; Una sola vista'
        '</div>'

        '<div style="width:60px;height:2px;'
        'background:linear-gradient(90deg,#6366f1,#06b6d4);'
        'border-radius:2px;margin-bottom:36px"></div>'

        '<div style="font-size:0.95rem;color:#8b8aaa;max-width:380px;line-height:1.9;'
        'font-family:Space Grotesk,sans-serif;margin-bottom:28px">'
        'Selecciona tu operaci&#243;n y sube<br>tu reporte de Dropi para comenzar'
        '</div>'

        '<div style="background:linear-gradient(135deg,rgba(99,102,241,0.12),rgba(6,182,212,0.12));'
        'border:1px solid rgba(99,102,241,0.3);border-radius:14px;padding:16px 32px;'
        'font-family:Space Grotesk,sans-serif;color:#a5b4fc;font-size:0.88rem;font-weight:500">'
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
        f'<div style="margin-bottom:28px;background:linear-gradient(135deg,#1a1829,#1f1d35);'
        f'border:1px solid #2d2b45;border-radius:16px;padding:24px 28px">'
        f'<div style="display:flex;align-items:center;gap:16px">'
        f'<div style="width:4px;height:54px;background:{op_color};border-radius:4px"></div>'
        f'<div>'
        f'<div style="font-size:0.68rem;color:#5a5878;font-weight:700;letter-spacing:0.12em;'
        f'text-transform:uppercase;margin-bottom:5px">{op_pais} &nbsp;·&nbsp; {op_moneda}</div>'
        f'<div style="font-family:Syne,sans-serif;font-size:1.9rem;font-weight:800;'
        f'color:#f0ede8;line-height:1;margin-bottom:6px">{op_nombre}</div>'
        f'<div style="color:#8b8aaa;font-size:0.83rem">'
        f'{modulo_nombre} &nbsp;·&nbsp; {total:,} pedidos analizados{clp_badge}'
        f'</div></div></div></div>',
        unsafe_allow_html=True
    )

    # ── KPIs financieros (análisis) ──
    ticket_prom = round(tot_venta / total, 0) if total else 0
    pct_cancel  = round(cancelados/total*100,1) if total else 0
    pct_dev_g   = round(devolucion/total*100,1) if total else 0
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
    else:
        nav = st.radio("", ["📅 Evolución Mensual","🗺️ Mapa Colombia","🏆 Productos Estrella","💡 Insights"],
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
                st.markdown('<div style="font-size:0.72rem;color:#c9a84c;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px">📣 MARKETING</div>', unsafe_allow_html=True)
                pauta        = st.number_input("Pauta (Ads)",         0, 500000000, 0, 100000, key="m_pauta",      format="%d")
                lucid_bot    = st.number_input("Lucid Bot",           0, 50000000,  0, 10000,  key="m_lucidbot",   format="%d")
                open_ia      = st.number_input("Open IA",             0, 20000000,  0, 10000,  key="m_openia",     format="%d")
                luci_voice   = st.number_input("Luci Voice",          0, 20000000,  0, 10000,  key="m_lucivoz",    format="%d")
                contingencias= st.number_input("Contingencias",       0, 20000000,  0, 10000,  key="m_conting",    format="%d")
                plat_spy     = st.number_input("Plataformas Spy",     0, 10000000,  0, 10000,  key="m_platspy",    format="%d")
                dominios     = st.number_input("Dominios / GoDaddy",  0, 5000000,   0, 10000,  key="m_dominios",   format="%d")
                total_mkt    = pauta+lucid_bot+open_ia+luci_voice+contingencias+plat_spy+dominios
                st.markdown(f'<div style="background:rgba(201,168,76,0.1);border-radius:6px;padding:8px;text-align:center;color:#f0d080;font-size:0.85rem"><b>Total: {fmt_money(total_mkt)}</b></div>', unsafe_allow_html=True)

            with col_m2:
                st.markdown('<div style="font-size:0.72rem;color:#6366f1;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px">🏢 ADMINISTRATIVOS</div>', unsafe_allow_html=True)
                adm_coord    = st.number_input("Coord Leidy",             0, 20000000, 0, 100000, key="a_coord",   format="%d")
                adm_logis    = st.number_input("Samanta Logística",       0, 20000000, 0, 100000, key="a_logis",   format="%d")
                adm_sandra   = st.number_input("Sandra Confirmación",     0, 20000000, 0, 100000, key="a_sandra",  format="%d")
                adm_cont     = st.number_input("Contador",                0, 10000000, 0, 100000, key="a_contad",  format="%d")
                adm_ceo      = st.number_input("C.E.O. - Ronaldo",        0, 20000000, 0, 100000, key="a_ceo",     format="%d")
                total_adm    = adm_coord+adm_logis+adm_sandra+adm_cont+adm_ceo
                st.markdown(f'<div style="background:rgba(99,102,241,0.1);border-radius:6px;padding:8px;text-align:center;color:#a5b4fc;font-size:0.85rem"><b>Total: {fmt_money(total_adm)}</b></div>', unsafe_allow_html=True)

            with col_m3:
                st.markdown('<div style="font-size:0.72rem;color:#06b6d4;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px">📦 IMPORTACIONES</div>', unsafe_allow_html=True)
                imp_compras  = st.number_input("Importaciones & Compras", 0, 200000000, 0, 100000, key="i_comp",   format="%d")
                imp_sky      = st.number_input("Sky Carga USA-Col",       0, 50000000,  0, 100000, key="i_sky",    format="%d")
                imp_tax8     = st.number_input("Impuesto 8x1000",         0, 5000000,   0, 10000,  key="i_tax8",   format="%d")
                imp_banco    = st.number_input("Costos Bancarios",        0, 5000000,   0, 10000,  key="i_banco",  format="%d")
                imp_activ    = st.number_input("Actividades & Capac.",    0, 10000000,  0, 10000,  key="i_activ",  format="%d")
                total_imp    = imp_compras+imp_sky+imp_tax8+imp_banco+imp_activ
                st.markdown(f'<div style="background:rgba(6,182,212,0.1);border-radius:6px;padding:8px;text-align:center;color:#67e8f9;font-size:0.85rem"><b>Total: {fmt_money(total_imp)}</b></div>', unsafe_allow_html=True)

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

        def celda(val, base, invertir=False):
            p = val/base*100 if base else 0
            if invertir:
                color = "#ef4444" if p > 25 else "#fbbf24" if p > 15 else "#34d399"
            else:
                color = "#34d399" if p >= 60 else "#fbbf24" if p >= 40 else "#ef4444"
            bg = f"rgba({','.join(str(int(c,16)) for c in [color[1:3],color[3:5],color[5:7]])},0.12)" if color.startswith('#') else "transparent"
            return f'<td style="padding:8px 12px;text-align:right;color:{color};font-weight:700;font-size:0.82rem">{pct(val,base)}</td>'

        def fila_seccion(label, color="#f0ede8", bold=True, bg="transparent", colspan=11):
            fw = "800" if bold else "600"
            return f'<tr><td colspan="{colspan}" style="padding:10px 12px 4px;background:{bg};color:{color};font-family:Syne,sans-serif;font-weight:{fw};font-size:0.82rem;text-transform:uppercase;letter-spacing:0.06em">{label}</td></tr>'

        def fila(label, vals_dict, base_dict, meta=None, kpi_meta=None, invertir=False, destacar=False, color_label="#b0aec8"):
            bg = "rgba(201,168,76,0.06)" if destacar else "rgba(0,0,0,0)"
            fw = "700" if destacar else "400"
            html = f'<tr style="background:{bg};border-bottom:1px solid rgba(45,43,69,0.5)">'
            html += f'<td style="padding:8px 12px;color:{color_label};font-weight:{fw};font-size:0.82rem;white-space:nowrap">{label}</td>'
            if meta is not None:
                html += f'<td style="padding:8px 12px;text-align:right;color:#5a5878;font-size:0.78rem">{fmt_money(meta)}</td>'
                html += f'<td style="padding:8px 12px;text-align:right;color:#c9a84c;font-size:0.78rem;font-weight:700">{kpi_meta}</td>'
            else:
                html += '<td colspan="2"></td>'
            for k, v in vals_dict.items():
                base = base_dict.get(k, 1)
                p = v/base*100 if base else 0
                if invertir:
                    pc = "#ef4444" if p > 25 else "#fbbf24" if p > 15 else "#34d399"
                elif destacar:
                    pc = "#34d399" if p >= 55 else "#fbbf24" if p >= 40 else "#ef4444"
                else:
                    pc = "#f0ede8"
                bg_p = "rgba(239,68,68,0.08)" if pc=="#ef4444" else "rgba(245,158,11,0.08)" if pc=="#fbbf24" else "transparent"
                html += f'<td style="padding:8px 12px;text-align:right;color:#8b8aaa;font-size:0.8rem">{fmt_money(v)}</td>'
                html += f'<td style="padding:8px 12px;text-align:right;background:{bg_p};color:{pc};font-weight:700;font-size:0.8rem;border-radius:4px">{pct(v,base)}</td>'
            html += '</tr>'
            return html

        # Cabeceras de columnas
        cols_hdr = list(met.keys())
        shopifys = {k: met[k]["shopify"] for k in cols_hdr}
        recaudos = {k: met[k]["recaudo"] for k in cols_hdr}
        mbrutos  = {k: met[k]["margen_bruto"] for k in cols_hdr}

        marg_ops  = {k: met[k]["margen_bruto"] - manuales[k]["total_mkt"] for k in cols_hdr}
        ebitdas   = {k: marg_ops[k] - manuales[k]["total_adm"] - manuales[k]["total_imp"] for k in cols_hdr}
        imptos    = {k: met[k]["shopify"] * 0.08 for k in cols_hdr}
        netos     = {k: ebitdas[k] - imptos[k] for k in cols_hdr}

        header_cols = ""
        for c in cols_hdr:
            col_color = {"Sem I\n1-8":"#c0392b","Sem II\n9-16":"#d4ac0d","Sem III\n17-24":"#7fb3d3","Sem IV\n25-31":"#a9dfbf","Total Mes":"#27ae60"}.get(c,"#6366f1")
            label = c.replace("\n","<br>")
            header_cols += f'<th colspan="2" style="padding:10px 8px;text-align:center;background:{col_color};color:#fff;font-family:Syne,sans-serif;font-size:0.8rem;font-weight:800;letter-spacing:0.04em">{label}</th>'

        html_pg = f"""
        <div style="overflow-x:auto;border-radius:14px;border:1px solid #2d2b45;margin-top:16px">
        <table style="width:100%;border-collapse:collapse;background:#0f0e17;font-family:Space Grotesk,sans-serif">
        <thead>
          <tr style="background:#0f0e17">
            <th style="padding:12px;text-align:left;color:#8b8aaa;font-size:0.75rem;min-width:160px">Concepto</th>
            <th style="padding:12px;text-align:right;color:#8b8aaa;font-size:0.72rem">Meta</th>
            <th style="padding:12px;text-align:right;color:#8b8aaa;font-size:0.72rem">KPI</th>
            {header_cols}
          </tr>
        </thead>
        <tbody>
        """

        # BLOQUE 1 — OPERACIÓN LOGÍSTICA
        html_pg += fila_seccion("⚙️ Operación Logística", "#10b981", bg="rgba(16,185,129,0.06)")
        html_pg += fila("SHOPIFY (Total Pedidos)",   {k:met[k]["shopify"]    for k in cols_hdr}, shopifys, destacar=True, color_label="#10b981")
        html_pg += fila("  Cancelación",             {k:met[k]["cancelado"]  for k in cols_hdr}, shopifys, invertir=True)
        html_pg += fila("  Devolución",              {k:met[k]["devolucion"] for k in cols_hdr}, shopifys, invertir=True)
        html_pg += fila("  Novedades",               {k:met[k]["novedad"]    for k in cols_hdr}, shopifys, invertir=True)
        html_pg += fila("  En Reparto",              {k:met[k]["reparto"]    for k in cols_hdr}, shopifys, invertir=True)
        html_pg += fila("T. INGRESO x VENTAS",       recaudos,                                   shopifys, destacar=True, color_label="#c9a84c")

        # BLOQUE 2 — COSTO DE VENTA
        html_pg += fila_seccion("📦 Costo de Venta", "#ef4444", bg="rgba(239,68,68,0.05)")
        html_pg += fila("  V/R Producto Entregado",  {k:met[k]["c_proveedor"] for k in cols_hdr}, recaudos, invertir=True)
        html_pg += fila("  Flete de Entrega",        {k:met[k]["flete_ent"]   for k in cols_hdr}, recaudos, invertir=True)
        html_pg += fila("  Flete de Devolución",     {k:met[k]["flete_dev"]   for k in cols_hdr}, recaudos, invertir=True)
        html_pg += fila("TOTAL COSTO",               {k:met[k]["costo_total"] for k in cols_hdr}, recaudos, invertir=True, destacar=True, color_label="#ef4444")
        html_pg += fila("MARGEN BRUTO | WALLET",     mbrutos,                                     recaudos, destacar=True, color_label="#c9a84c")

        # BLOQUE 3 — MARKETING
        html_pg += fila_seccion("📣 Ret. Inv. Marketing / Ingresos", "#f59e0b", bg="rgba(245,158,11,0.05)")
        for nombre in ["Pauta","Lucid Bot","Open IA","Luci Voice","Contingencias","Plat. Spy","Dominios"]:
            key_map = {"Pauta":"Pauta","Lucid Bot":"Lucid Bot","Open IA":"Open IA","Luci Voice":"Luci Voice","Contingencias":"Contingencias","Plat. Spy":"Plat. Spy","Dominios":"Dominios"}
            html_pg += fila(f"  {nombre}", {k: manuales[k]["mkt_items"].get(key_map[nombre],0) for k in cols_hdr}, recaudos, invertir=True)
        html_pg += fila("TOTAL MARKETING",           {k:manuales[k]["total_mkt"] for k in cols_hdr}, recaudos, invertir=True, destacar=True, color_label="#f59e0b")
        html_pg += fila("MARGEN OPERACIONAL",        marg_ops, recaudos, destacar=True, color_label="#a5b4fc")

        # BLOQUE 4 — IMPORTS & ADMIN
        html_pg += fila_seccion("🌐 Importaciones & Costos Bancarios", "#06b6d4", bg="rgba(6,182,212,0.04)")
        for nombre in ["Importaciones","Sky Carga","Imp. 8x1000","C. Bancarios","Actividades"]:
            html_pg += fila(f"  {nombre}", {k: manuales[k]["imp_items"].get(nombre,0) for k in cols_hdr}, recaudos, invertir=True)
        html_pg += fila("TOTAL IMPORTS",             {k:manuales[k]["total_imp"] for k in cols_hdr}, recaudos, invertir=True, destacar=True, color_label="#67e8f9")

        html_pg += fila_seccion("🏢 Administrativos", "#8b5cf6", bg="rgba(139,92,246,0.04)")
        for nombre in ["Coord Leidy","Sam. Logística","S. Confirmación","Contador","C.E.O."]:
            html_pg += fila(f"  {nombre}", {k: manuales[k]["adm_items"].get(nombre,0) for k in cols_hdr}, recaudos, invertir=True)
        html_pg += fila("TOTAL ADMINISTRACIÓN",      {k:manuales[k]["total_adm"] for k in cols_hdr}, recaudos, invertir=True, destacar=True, color_label="#a78bfa")

        # BLOQUE 5 — EBITDA, IMPUESTOS, MARGEN NETO
        html_pg += fila_seccion("📊 Resultado Final", "#c9a84c", bg="rgba(201,168,76,0.06)")
        html_pg += fila("EBITDA",                    ebitdas, recaudos, destacar=True, color_label="#c9a84c")
        html_pg += fila("  Impuestos Estimados 8%",  imptos,  recaudos, invertir=True)
        html_pg += fila("MARGEN NETO",               netos,   recaudos, destacar=True, color_label="#f0d080")

        html_pg += "</tbody></table></div>"
        st.markdown(html_pg, unsafe_allow_html=True)

        # ── Gráfica resumen ──
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        fig_pg2 = go.Figure()
        xs = [k.replace("\n"," ") for k in cols_hdr]
        fig_pg2.add_trace(go.Bar(x=xs, y=[met[k]["shopify"]/1e6    for k in cols_hdr], name="Shopify",      marker_color="#6366f1", opacity=0.85))
        fig_pg2.add_trace(go.Bar(x=xs, y=[met[k]["recaudo"]/1e6    for k in cols_hdr], name="Recaudo",      marker_color="#06b6d4", opacity=0.85))
        fig_pg2.add_trace(go.Bar(x=xs, y=[mbrutos[k]/1e6           for k in cols_hdr], name="Margen Bruto", marker_color="#10b981", opacity=0.85))
        fig_pg2.add_trace(go.Bar(x=xs, y=[netos[k]/1e6             for k in cols_hdr], name="Margen Neto",  marker_color="#c9a84c", opacity=0.85))
        fig_pg2.add_trace(go.Scatter(x=xs, y=[netos[k]/max(met[k]["shopify"],1)*100 for k in cols_hdr],
                                     name="Margen Neto %", yaxis="y2",
                                     line=dict(color="#f0d080",width=3), marker=dict(size=9)))
        fig_pg2.update_layout(**PLOT_LAYOUT, barmode="group", height=400,
                              title="Cascada P&G por Semana",
                              xaxis=AXIS_STYLE,
                              yaxis=dict(title="Millones COP", **AXIS_STYLE),
                              yaxis2=dict(title="Margen %", overlaying="y", side="right",
                                         gridcolor="rgba(0,0,0,0)", tickfont=dict(color="#f0d080"), ticksuffix="%"))
        st.plotly_chart(fig_pg2, use_container_width=True)


    # ── PROYECCIONES ──
    elif nav == "🔮 Proyecciones":
        st.markdown('<div class="seccion-titulo">🔮 Proyecciones</div>', unsafe_allow_html=True)
        if '_mes' in df.columns and C_TOTAL in df.columns and len(df['_mes'].unique()) >= 2:
            v_mes = df.groupby('_mes')[C_TOTAL].sum().reset_index()
            v_mes.columns = ['Mes','Ventas']
            v_mes = v_mes.sort_values('Mes')

            # Promedio últimos 3 meses como base de proyección
            ult3  = v_mes['Ventas'].tail(3).mean()
            ult1  = v_mes['Ventas'].iloc[-1]
            meses_hist = list(v_mes['Mes'])

            pr1,pr2,pr3 = st.columns(3)
            with pr1:
                crecimiento = st.slider("📈 Crecimiento mensual %", -30, 100, 10, 5,
                                       help="Ajusta el crecimiento esperado mes a mes")
            with pr2:
                n_meses = st.slider("🗓️ Meses a proyectar", 1, 12, 3)
            with pr3:
                base = st.radio("Base de cálculo", ["Último mes","Promedio 3 meses"],
                               horizontal=False)

            base_val = ult1 if base == "Último mes" else ult3
            proyecciones = []
            for i in range(1, n_meses+1):
                val = base_val * ((1 + crecimiento/100) ** i)
                proyecciones.append({'Mes': f"Proyección +{i}", 'Ventas': val, 'Tipo': 'Proyección'})

            v_mes['Tipo'] = 'Histórico'
            proj_df = pd.concat([v_mes, pd.DataFrame(proyecciones)], ignore_index=True)

            fig_proj = go.Figure()
            hist = proj_df[proj_df['Tipo']=='Histórico']
            proy = proj_df[proj_df['Tipo']=='Proyección']
            fig_proj.add_trace(go.Scatter(x=hist['Mes'], y=hist['Ventas']/1e6, name='Histórico',
                                         line=dict(color=op_color, width=3), marker=dict(size=8)))
            fig_proj.add_trace(go.Scatter(x=[hist['Mes'].iloc[-1]] + list(proy['Mes']),
                                         y=[hist['Ventas'].iloc[-1]/1e6] + list(proy['Ventas']/1e6),
                                         name='Proyección', line=dict(color='#c9a84c', width=3, dash='dash'),
                                         marker=dict(size=8, symbol='diamond')))
            fig_proj.update_layout(**PLOT_LAYOUT, height=420, title='Proyección de Ventas',
                                   xaxis=AXIS_STYLE,
                                   yaxis=dict(title='Millones COP', **AXIS_STYLE))
            st.plotly_chart(fig_proj, use_container_width=True)

            # KPIs de proyección
            total_proy = sum(p['Ventas'] for p in proyecciones)
            mejor_mes_proy = max(proyecciones, key=lambda x: x['Ventas'])
            pp1, pp2, pp3 = st.columns(3)
            with pp1: st.markdown(kpi("gold","📅 Proyección Total",fmt_money(total_proy),f"{n_meses} meses"), unsafe_allow_html=True)
            with pp2: st.markdown(kpi("green","📈 Mejor mes proy.",fmt_money(mejor_mes_proy['Ventas'])), unsafe_allow_html=True)
            with pp3:
                gan_proy = total_proy * (pct_gan/100) if pct_gan else 0
                st.markdown(kpi("purple","💰 Ganancia estimada",fmt_money(gan_proy),f"{pct_gan}% margen actual"), unsafe_allow_html=True)
        else:
            st.info("Se necesitan al menos 2 meses de datos para generar proyecciones.")

    # ── EVOLUCIÓN MENSUAL ──
    elif "Evolución" in nav and '_mes' in df.columns and C_TOTAL in df.columns:
        v_mes = df.groupby('_mes').agg(
            Ventas=(C_TOTAL, 'sum'),
            Ganancia=(C_GANANCIA, 'sum') if C_GANANCIA in df.columns else (C_TOTAL,'count'),
            Ordenes=(C_TOTAL,'count')
        ).reset_index().sort_values('_mes')

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=v_mes['_mes'], y=v_mes['Ventas']/1e6,
            name='Ventas', marker=dict(color='#6366f1', opacity=0.85),
        ))
        if C_GANANCIA in df.columns:
            fig.add_trace(go.Bar(
                x=v_mes['_mes'], y=v_mes['Ganancia']/1e6,
                name='Ganancia', marker=dict(color='#10b981', opacity=0.85),
            ))
        fig.add_trace(go.Scatter(
            x=v_mes['_mes'], y=v_mes['Ordenes'],
            name='Órdenes', yaxis='y2',
            line=dict(color='#c9a84c', width=3),
            marker=dict(size=8, color='#c9a84c')
        ))
        fig.update_layout(
            **PLOT_LAYOUT,
            barmode='group', height=420,
            title='Evolución Mensual de Ventas',
            xaxis=AXIS_STYLE,
            yaxis=dict(title='Millones COP', **AXIS_STYLE),
            yaxis2=dict(title='Órdenes', overlaying='y', side='right',
                       gridcolor='rgba(0,0,0,0)', tickfont=dict(color='#c9a84c'))
        )
        st.plotly_chart(fig, use_container_width=True)

        # Días pico
        if '_dia' in df.columns:
            dias_venta = df.groupby('_dia')[C_TOTAL].sum().reset_index()
            dias_venta.columns = ['Día','Ventas']
            fig_d = px.area(dias_venta, x='Día', y='Ventas',
                           title='Ventas por Día del Mes (patrón quincenas)',
                           color_discrete_sequence=['#c9a84c'])
            fig_d.update_traces(fillcolor='rgba(201,168,76,0.15)', line=dict(color='#c9a84c',width=2))
            fig_d.update_layout(**PLOT_LAYOUT, height=280, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
            st.plotly_chart(fig_d, use_container_width=True)

    # ── MAPA COLOMBIA ──
    elif "Mapa" in nav:
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
                    color_continuous_scale=['#1a1829','#6366f1','#c9a84c'],
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
    elif "Productos" in nav and C_PRODUCTO in df.columns:

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
                    color_continuous_scale=['#1a1829','#6366f1','#c9a84c'],
                    title=f'Top 10 — {titulo}'
                )
                fig_prod.update_layout(**PLOT_LAYOUT, height=480, coloraxis_showscale=False, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                fig_prod.update_traces(texttemplate='%{x:,.0f}', textposition='outside',
                                       textfont=dict(color='#b0aec8', size=10))
                st.plotly_chart(fig_prod, use_container_width=True)



    # ── INSIGHTS ──
    elif "Insights" in nav:
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

        # ══════════════════════════════════════════════════════
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

            st.markdown('<div style="background:#1a1829;border:1px solid #2d2b45;border-radius:14px;padding:20px;margin-bottom:20px">', unsafe_allow_html=True)
            st.markdown('<div style="font-family:Syne,sans-serif;font-weight:700;color:#f0ede8;font-size:0.95rem;margin-bottom:16px">📝 Equipo de Trabajo</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # ── Encabezado columnas ──
            hc1,hc2,hc3,hc4,hc5,hc6 = st.columns([3,2,1.5,2,1.5,1])
            for lbl, col in zip(["Nombre / Cargo","Sueldo Base $","Tipo Bono","Bono / Comisión","% sobre ventas","Total Mes"],
                                 [hc1,hc2,hc3,hc4,hc5,hc6]):
                col.markdown(f'<div style="font-size:0.68rem;font-weight:800;color:#8b8aaa;text-transform:uppercase;'
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
                            st.markdown('<div style="padding-top:8px;color:#5a5878;font-size:0.8rem">—</div>', unsafe_allow_html=True)
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
                        st.markdown(f'<div style="padding-top:8px;color:#8b5cf6;font-size:0.82rem;font-weight:600">'
                                    f'{"" if tipo_bono=="Sin bono" else f"{pct_sobre_vnt:.2f}%"}</div>', unsafe_allow_html=True)
                    with c6:
                        total_emp = sueldo + bono
                        st.markdown(f'<div style="padding-top:8px;color:#c9a84c;font-weight:800;font-size:0.85rem">'
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
                f'<div style="background:rgba(201,168,76,0.07);border:1px solid #c9a84c44;border-radius:10px;'
                f'padding:10px 16px;margin:8px 0;display:flex;justify-content:space-between;align-items:center">'
                f'<span style="color:#8b8aaa;font-size:0.78rem;font-weight:700">SUBTOTALES</span>'
                f'<span style="color:#f0ede8;font-size:0.82rem">Sueldos: <b style="color:#f0ede8">{fmt_money(total_sueldos)}</b>'
                f' &nbsp;+&nbsp; Bonos/Comisiones: <b style="color:#10b981">{fmt_money(total_bonos)}</b>'
                f' &nbsp;=&nbsp; <b style="color:#c9a84c;font-size:1rem">{fmt_money(total_sueldos+total_bonos)}</b></span>'
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
            hdr_n = "background:#161525;padding:10px 14px;font-size:0.7rem;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;color:#8b8aaa;border-bottom:2px solid #2d2b45"
            td_n  = "padding:11px 14px;font-size:0.83rem;border-bottom:1px solid #1f1d35"
            tabla_nom = (
                f'<div style="overflow-x:auto;border-radius:12px;border:1px solid #2d2b45;margin-bottom:20px">'
                f'<table style="width:100%;border-collapse:collapse;background:#1a1829;font-family:Space Grotesk,sans-serif">'
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
                    f'<td style="{td_n};color:#d4d0ea;font-weight:600">{emp["nombre"]}</td>'
                    f'<td style="{td_n};text-align:right;color:#f0ede8">{fmt_money(emp["sueldo"])}</td>'
                    f'<td style="{td_n};text-align:right;color:#10b981">{fmt_money(emp["bonificacion"])}</td>'
                    f'<td style="{td_n};text-align:right;color:#c9a84c;font-weight:700">{fmt_money(total_e)}</td>'
                    f'<td style="{td_n};text-align:right;color:#8b8aaa">{pct_e:.1f}%</td>'
                    f'</tr>'
                )
            # Total
            tabla_nom += (
                f'<tr style="background:rgba(201,168,76,0.06);border-top:2px solid #c9a84c">'
                f'<td style="{td_n};color:#c9a84c;font-weight:800">TOTAL NÓMINA</td>'
                f'<td style="{td_n};text-align:right;color:#c9a84c;font-weight:800">{fmt_money(total_sueldos)}</td>'
                f'<td style="{td_n};text-align:right;color:#10b981;font-weight:800">{fmt_money(total_bonos)}</td>'
                f'<td style="{td_n};text-align:right;color:#c9a84c;font-weight:800">{fmt_money(nomina_mes)}</td>'
                f'<td style="{td_n};text-align:right;color:#c9a84c;font-weight:800">100%</td>'
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
                    f'<div style="font-family:Syne,sans-serif;font-weight:700;color:{color_dias};font-size:0.9rem">Proyección de días</div>'
                    f'<div style="color:#b0aec8;font-size:0.8rem;margin-top:3px">{msg_dias}</div>'
                    f'</div>'
                    f'<div style="margin-left:auto;text-align:right">'
                    f'<div style="font-size:1.6rem;font-weight:800;color:{color_dias};font-family:Syne,sans-serif">{dias_necesarios}d</div>'
                    f'<div style="font-size:0.7rem;color:#5a5878">necesarios</div>'
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
                    f'<div style="background:#1a1829;border:1px solid #2d2b45;border-radius:14px;padding:20px;margin-bottom:16px">'
                    f'<div style="display:flex;justify-content:space-between;margin-bottom:10px">'
                    f'<span style="font-family:Syne,sans-serif;font-weight:700;color:#f0ede8;font-size:0.9rem">'
                    f'{icono_estado} {estado_txt}</span>'
                    f'<span style="color:{color_barra};font-weight:800;font-size:1rem">{pct_avance:.1f}%</span>'
                    f'</div>'
                    f'<div style="background:#2d2b45;border-radius:100px;height:14px;overflow:hidden">'
                    f'<div style="background:linear-gradient(90deg,{color_barra},{color_barra}cc);'
                    f'width:{pct_avance:.1f}%;height:100%;border-radius:100px;'
                    f'transition:width 0.5s ease"></div>'
                    f'</div>'
                    f'<div style="display:flex;justify-content:space-between;margin-top:8px;font-size:0.75rem;color:#5a5878">'
                    f'<span>{n_ent:,} entregados</span>'
                    f'<span>Meta: {pedidos_necesarios:,} pedidos</span>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # Desglose por empleado — cuántos pedidos cubre cada uno
                if margen_unit > 0:
                    st.markdown('<div style="font-family:Syne,sans-serif;font-weight:700;color:#8b8aaa;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px">Pedidos necesarios para cubrir el sueldo de cada colaborador</div>', unsafe_allow_html=True)
                    for emp in empleados_editados:
                        total_e   = emp['sueldo'] + emp['bonificacion']
                        if total_e == 0: continue
                        peds_e    = int(total_e / margen_unit) + 1
                        pct_e_av  = min(n_ent / peds_e * 100, 100) if peds_e else 0
                        c_e       = "#10b981" if pct_e_av >= 100 else "#f59e0b" if pct_e_av >= 60 else "#ef4444"
                        check     = "✅" if pct_e_av >= 100 else "🔄"
                        st.markdown(
                            f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;'
                            f'background:#1a1829;border-radius:10px;padding:10px 14px;border:1px solid #2d2b45">'
                            f'<div style="min-width:22px">{check}</div>'
                            f'<div style="flex:1">'
                            f'<div style="font-size:0.82rem;color:#d4d0ea;font-weight:600">{emp["nombre"]}</div>'
                            f'<div style="background:#2d2b45;border-radius:100px;height:8px;margin-top:5px;overflow:hidden">'
                            f'<div style="background:{c_e};width:{pct_e_av:.0f}%;height:100%;border-radius:100px"></div>'
                            f'</div></div>'
                            f'<div style="text-align:right;min-width:90px">'
                            f'<div style="color:#c9a84c;font-weight:700;font-size:0.82rem">{fmt_money(total_e)}</div>'
                            f'<div style="color:#5a5878;font-size:0.7rem">{peds_e:,} pedidos</div>'
                            f'</div></div>',
                            unsafe_allow_html=True
                        )

                # Costos fijos adicionales
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div style="font-family:Syne,sans-serif;font-weight:700;color:#f0ede8;font-size:0.88rem;margin-bottom:10px">🏢 Costos Fijos Adicionales (mensual)</div>', unsafe_allow_html=True)
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
                    f'<td style="padding:9px 16px;color:#d4d0ea;font-size:0.83rem;{bold}">{indent}{concepto}</td>'
                    f'<td style="padding:9px 16px;text-align:right;color:{color};font-size:0.83rem;{bold}">{signo}{fmt_money(valor)}</td>'
                    f'<td style="padding:9px 16px;text-align:right;color:#5a5878;font-size:0.75rem">'
                    f'{"" if ingresos == 0 else f"{valor/ingresos*100:.1f}%"}</td>'
                    f'</tr>'
                )

            pl_html = (
                f'<div style="overflow-x:auto;border-radius:14px;border:1px solid #2d2b45">'
                f'<table style="width:100%;border-collapse:collapse;background:#1a1829;font-family:Space Grotesk,sans-serif">'
                f'<thead><tr>'
                f'<th style="padding:12px 16px;text-align:left;color:#8b8aaa;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.07em;border-bottom:2px solid #2d2b45">Concepto</th>'
                f'<th style="padding:12px 16px;text-align:right;color:#8b8aaa;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.07em;border-bottom:2px solid #2d2b45">Valor</th>'
                f'<th style="padding:12px 16px;text-align:right;color:#8b8aaa;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.07em;border-bottom:2px solid #2d2b45">% Ingreso</th>'
                f'</tr></thead><tbody>'
                + fila_pl("(+) INGRESOS — Pedidos Entregados", ingresos, destacada=True)
                + fila_pl("Costo de Productos Vendidos", costo_prod, nivel=1, es_gasto=True)
                + fila_pl("UTILIDAD BRUTA", utilidad_bruta, destacada=True)
                + '<tr><td colspan="3" style="padding:4px 16px;background:#161525"><span style="font-size:0.68rem;color:#5a5878;text-transform:uppercase;letter-spacing:0.06em">Gastos Operativos</span></td></tr>'
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
                f'<div style="background:#1a1829;border:1px solid #2d2b45;border-radius:14px;padding:24px">'
                f'<div style="font-family:Syne,sans-serif;font-weight:700;color:#f0ede8;margin-bottom:14px;font-size:0.95rem">'
                f'{"✅ Por encima del punto de equilibrio" if superavit>=0 else "🔴 Por debajo del punto de equilibrio"}</div>'
                f'<div style="background:#2d2b45;border-radius:100px;height:20px;overflow:hidden">'
                f'<div style="background:linear-gradient(90deg,{color_pe},{color_pe}bb);width:{min(pct_pe,100):.1f}%;height:100%;border-radius:100px"></div>'
                f'</div>'
                f'<div style="display:flex;justify-content:space-between;margin-top:10px;font-size:0.76rem;color:#5a5878">'
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
        elif "Costos" in fin_nav:
            st.markdown('<div class="seccion-titulo">📉 Análisis de Costos</div>', unsafe_allow_html=True)

            costo_x_ped   = (costo_prod + flete_ent) / n_ent if n_ent else 0
            costo_dev_u   = (flete_dev / n_dev) if n_dev else 0
            pauta_x_ped   = pauta_fin / n_ent if n_ent else 0
            costo_cancel  = df_fin[mask_can][C_FLETE].sum() if C_FLETE in df_fin.columns else 0

            k1,k2,k3,k4 = st.columns(4)
            with k1: st.markdown(kpi("blue","💸 Costo por Pedido Entregado",fmt_money(costo_x_ped)), unsafe_allow_html=True)
            with k2: st.markdown(kpi("red","🔁 Costo por Devolución",fmt_money(costo_dev_u)), unsafe_allow_html=True)
            with k3: st.markdown(kpi("gold","📣 Pauta por Pedido Entregado",fmt_money(pauta_x_ped)), unsafe_allow_html=True)
            with k4: st.markdown(kpi("purple","❌ Costo Total Cancelaciones",fmt_money(costo_cancel)), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            # Gráfica de torta costos
            costos_labels = ["Productos","Flete Entrega","Flete Dev.","Pauta","Nómina","Fijos"]
            costos_vals   = [costo_prod, flete_ent, flete_dev, pauta_fin, nomina_total, sum(costos_fijos.values())]
            costos_vals   = [v for v in costos_vals if v > 0]
            costos_labels = [l for l,v in zip(costos_labels,[costo_prod,flete_ent,flete_dev,pauta_fin,nomina_total,sum(costos_fijos.values())]) if v > 0]

            if costos_vals:
                fig_cos = px.pie(values=costos_vals, names=costos_labels, hole=0.45,
                                 color_discrete_sequence=COLORES_ELEGANTES,
                                 title='Distribución de Costos Totales')
                fig_cos.update_layout(**PLOT_LAYOUT, height=380)
                fig_cos.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_cos, use_container_width=True)

        # ══════════════════════════════════════════════════════
        # 🎯 KPIs FINANCIEROS
        # ══════════════════════════════════════════════════════
        elif "KPIs" in fin_nav:
            st.markdown('<div class="seccion-titulo">🎯 KPIs Financieros Clave</div>', unsafe_allow_html=True)

            tasa_conv = n_ent / n_total * 100 if n_total else 0
            ebitda    = utilidad_op
            liquidez  = ingresos / cf_total if cf_total else 0

            kpis_fin = [
                ("🎫 Ticket Promedio",           fmt_money(ticket_prom),         "Valor promedio por pedido entregado"),
                ("👤 CAC — Costo de Adquisición", fmt_money(pauta_fin/n_ent if n_ent else 0), "Pauta ÷ pedidos entregados"),
                ("💱 Tasa Conv. Financiera",      f"{tasa_conv:.1f}%",            "% pedidos que generan dinero real"),
                ("📊 EBITDA",                     fmt_money(ebitda),              "Utilidad antes de impuestos"),
                ("💧 Índice de Liquidez",          f"{liquidez:.2f}x",             "Ingresos ÷ Costos Fijos"),
                ("📈 ROI de Pauta",               f"{roi_pauta:.1f}%",            "Retorno sobre inversión publicitaria"),
                ("💵 Margen Bruto",               f"{margen_bruto_pct:.1f}%",     "Utilidad bruta sobre ingresos"),
                ("💵 Margen Neto",                f"{margen_neto_pct:.1f}%",      "Utilidad neta sobre ingresos"),
            ]

            hdr_k = "background:#161525;padding:12px 16px;font-size:0.68rem;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;color:#8b8aaa;border-bottom:2px solid #2d2b45"
            td_k  = "padding:13px 16px;border-bottom:1px solid #1f1d35;font-size:0.83rem"
            tabla_kpi = (
                f'<div style="overflow-x:auto;border-radius:14px;border:1px solid #2d2b45">'
                f'<table style="width:100%;border-collapse:collapse;background:#1a1829;font-family:Space Grotesk,sans-serif">'
                f'<thead><tr>'
                f'<th style="{hdr_k};text-align:left">Indicador</th>'
                f'<th style="{hdr_k};text-align:right">Valor</th>'
                f'<th style="{hdr_k};text-align:left">Qué mide</th>'
                f'</tr></thead><tbody>'
            )
            for nom_k, val_k, desc_k in kpis_fin:
                tabla_kpi += (
                    f'<tr style="background:rgba(255,255,255,0.01)">'
                    f'<td style="{td_k};color:#d4d0ea;font-weight:600">{nom_k}</td>'
                    f'<td style="{td_k};text-align:right;color:#c9a84c;font-weight:800;font-size:0.95rem">{val_k}</td>'
                    f'<td style="{td_k};color:#5a5878">{desc_k}</td>'
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
        st.markdown('<div style="background:#1a1829;border:1px solid #2d2b45;border-radius:14px;padding:18px;margin-bottom:20px">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:Syne,sans-serif;font-weight:700;color:#f0ede8;font-size:0.95rem;margin-bottom:12px">💾 Inversión Publicitaria por Producto (Pauta)</div>', unsafe_allow_html=True)

        col_pa, col_pb = st.columns([1,1])
        with col_pa:
            st.markdown('<div style="color:#8b8aaa;font-size:0.78rem;margin-bottom:8px">📁 Opción A — Subir Excel/CSV con columnas: <b>Producto, Pauta</b></div>', unsafe_allow_html=True)
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
            st.markdown('<div style="color:#8b8aaa;font-size:0.78rem;margin-bottom:8px">✏️ Opción B — Ingresar pauta manualmente por producto</div>', unsafe_allow_html=True)
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
                hdr_base = "background:#161525;border-bottom:2px solid #2d2b45;font-size:0.68rem;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;padding:9px 10px"
                tabla_html = (
                    f'<div style="margin-bottom:4px;font-family:Syne,sans-serif;font-size:0.75rem;'
                    f'font-weight:700;color:{color_titulo};padding:6px 0">▶ {titulo}</div>'
                    f'<div style="overflow-x:auto;border-radius:12px;border:1px solid #2d2b45;margin-bottom:16px">'
                    f'<table style="width:100%;border-collapse:collapse;background:#1a1829;font-family:Space Grotesk,sans-serif">'
                    f'<thead><tr>'
                    f'<th style="{hdr_base};text-align:left;color:#8b8aaa;min-width:160px">Producto</th>'
                    f'<th style="{hdr_base};text-align:center;color:#10b981">% ENTR</th>'
                    f'<th style="{hdr_base};text-align:center;color:#ef4444">% CNC</th>'
                    f'<th style="{hdr_base};text-align:center;color:#f59e0b">% DVL</th>'
                    f'<th style="{hdr_base};text-align:center;color:#f0ede8;background:#2d2b35">CIERRE</th>'
                    f'<th style="{hdr_base};text-align:right;color:#10b981">% VNT</th>'
                    f'<th style="{hdr_base};text-align:right;color:#f0ede8">MRGN BRT</th>'
                    f'<th style="{hdr_base};text-align:right;color:#06b6d4;background:#06b6d415">PAUTA</th>'
                    f'<th style="{hdr_base};text-align:right;color:#f0ede8">UT. BRT</th>'
                    f'<th style="{hdr_base};text-align:right;color:#c9a84c">% UT. PAUTA</th>'
                    f'<th style="{hdr_base};text-align:right;color:#8b5cf6">&#916; INV</th>'
                    f'<th style="{hdr_base};text-align:right;color:#8b5cf6">&#916; VNT</th>'
                    f'<th style="{hdr_base};text-align:right;color:#8b5cf6">&#916; UT. BRT</th>'
                    f'</tr></thead><tbody>'
                )

                for _, r in df_rows.iterrows():
                    prod_nom = str(r['PRODUCTO'])[:35]

                    # Colores semáforo
                    c_entr = "#10b981" if r['% ENTR'] >= 60 else "#f59e0b" if r['% ENTR'] >= 40 else "#ef4444"
                    c_cnc  = "#ef4444" if r['% CNC']  > 20  else "#f59e0b" if r['% CNC'] > 10  else "#10b981"
                    c_dvl  = "#ef4444" if r['% DVL']  > 20  else "#f59e0b" if r['% DVL'] > 10  else "#10b981"
                    c_vnt  = "#10b981" if r['% VNT']  > 20  else "#f0ede8"
                    c_ut   = "#10b981" if (r['% UT. PAUTA'] or 0) > 50 else "#f59e0b" if (r['% UT. PAUTA'] or 0) > 0 else "#ef4444"
                    c_dvnt = "#10b981" if r['DELTA VNT'] > 0 else "#ef4444"
                    c_dut  = "#10b981" if r['DELTA UT. BRT'] > 10 else "#f0ede8"

                    # Flecha cierre
                    flecha = "&#x25B2;" if r['CIERRE'] >= 90 else "&#x25BC;"
                    f_color = "#10b981" if r['CIERRE'] >= 90 else "#ef4444"

                    pct_ut_txt = f"{r['% UT. PAUTA']:.1f}%" if r['% UT. PAUTA'] is not None else "—"
                    pauta_txt  = fmt_money(r['PAUTA']) if r['PAUTA'] > 0 else "—"

                    td = "padding:9px 10px;font-size:0.8rem;border-bottom:1px solid #1f1d35"
                    tabla_html += (
                        f'<tr style="background:rgba(255,255,255,0.01)" '
                        f'onmouseover="this.style.background=\'rgba(99,102,241,0.07)\'" '
                        f'onmouseout="this.style.background=\'rgba(255,255,255,0.01)\'">'
                        f'<td style="{td};color:#d4d0ea;font-weight:600;text-align:left">{prod_nom}</td>'
                        f'<td style="{td};text-align:center;color:{c_entr};font-weight:700">{r["% ENTR"]:.1f}%</td>'
                        f'<td style="{td};text-align:center;color:{c_cnc};font-weight:700">{r["% CNC"]:.1f}%</td>'
                        f'<td style="{td};text-align:center;color:{c_dvl};font-weight:700">{r["% DVL"]:.1f}%</td>'
                        f'<td style="{td};text-align:center;background:#2d2b3520">'
                        f'<span style="color:{f_color}">{flecha}</span> '
                        f'<span style="color:#f0ede8;font-weight:700">{r["CIERRE"]:.1f}%</span></td>'
                        f'<td style="{td};text-align:right;color:{c_vnt};font-weight:700">{r["% VNT"]:.2f}%</td>'
                        f'<td style="{td};text-align:right;color:#f0ede8">{fmt_money(r["MRGN BRT"])}</td>'
                        f'<td style="{td};text-align:right;color:#06b6d4;font-weight:700;background:#06b6d40a">{pauta_txt}</td>'
                        f'<td style="{td};text-align:right;color:#f0ede8">{fmt_money(r["UT. BRT"])}</td>'
                        f'<td style="{td};text-align:right;color:{c_ut};font-weight:700">{pct_ut_txt}</td>'
                        f'<td style="{td};text-align:right;color:#8b5cf6">{r["DELTA INV"]:.1f}%</td>'
                        f'<td style="{td};text-align:right;color:{c_dvnt};font-weight:700">'
                        f'{"+" if r["DELTA VNT"]>0 else ""}{r["DELTA VNT"]:.1f}%</td>'
                        f'<td style="{td};text-align:right;color:{c_dut};font-weight:700">{r["DELTA UT. BRT"]:.1f}%</td>'
                        f'</tr>'
                    )

                # Fila SUBTOTAL (PARETO o NO PARETO)
                label_sub = "PARETO" if es_pareto else "NO PARETO"
                color_sub  = "#c9a84c" if es_pareto else "#6366f1"
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
                    f'<td style="{td_sub};text-align:center;color:#f0ede8">{sum_cier:.1f}%</td>'
                    f'<td style="{td_sub};text-align:right;color:#10b981">{sum_vnt:.1f}%</td>'
                    f'<td style="{td_sub};text-align:right;color:#f0ede8">{fmt_money(sum_mrgn)}</td>'
                    f'<td style="{td_sub};text-align:right;color:#06b6d4;background:#06b6d40a">{pauta_sub_txt}</td>'
                    f'<td style="{td_sub};text-align:right;color:#f0ede8">{fmt_money(sum_ut)}</td>'
                    f'<td style="{td_sub};text-align:right;color:#c9a84c">{pct_ut_sub_txt}</td>'
                    f'<td style="{td_sub};text-align:right;color:#8b5cf6">—</td>'
                    f'<td style="{td_sub};text-align:right;color:#8b5cf6">—</td>'
                    f'<td style="{td_sub};text-align:right;color:#8b5cf6">{sum_dut:.1f}%</td>'
                    f'</tr>'
                )

                tabla_html += '</tbody></table></div>'
                st.markdown(tabla_html, unsafe_allow_html=True)

            # Renderizar PARETO y NO PARETO
            render_tabla_pauta(df_pareto,    "CON PAUTA (PARETO)",    "#c9a84c", es_pareto=True)
            render_tabla_pauta(df_no_pareto, "SIN PAUTA (NO PARETO)", "#6366f1", es_pareto=False)

            # ── Fila KPI's Generales al final ──
            td_g = "padding:8px 10px;font-size:0.78rem;font-weight:700;color:#8b8aaa"
            ut_brt_tot_txt  = fmt_money(ut_brt_total)
            pauta_tot_txt   = fmt_money(pauta_total) if pauta_total else "—"
            pct_ut_tot_txt  = f"{ut_brt_total/pauta_total*100:.1f}%" if pauta_total else "—"
            kpig_html = (
                f'<div style="background:#161525;border:1px solid #2d2b45;border-radius:10px;padding:2px 0;margin-top:4px">'
                f'<table style="width:100%;border-collapse:collapse;font-family:Space Grotesk,sans-serif"><tr>'
                f'<td style="{td_g};text-align:left;min-width:160px">KPI\'s Generales</td>'
                f'<td style="{td_g};text-align:center;color:#10b981">{pct_entr_g:.1f}%</td>'
                f'<td style="{td_g};text-align:center;color:#ef4444">{pct_cnc_g:.1f}%</td>'
                f'<td style="{td_g};text-align:center;color:#f59e0b">{pct_dvl_g:.1f}%</td>'
                f'<td style="{td_g};text-align:center"></td>'
                f'<td style="{td_g};text-align:right"></td>'
                f'<td style="{td_g};text-align:right;color:#f0ede8">{fmt_money(df_prod["MRGN BRT"].sum())}</td>'
                f'<td style="{td_g};text-align:right;color:#06b6d4">{pauta_tot_txt}</td>'
                f'<td style="{td_g};text-align:right;color:#f0ede8">{ut_brt_tot_txt}</td>'
                f'<td style="{td_g};text-align:right;color:#c9a84c">{pct_ut_tot_txt}</td>'
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
                fig_dv.add_vline(x=0, line_color='#5a5878', line_width=1)
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
        f'<div style="margin-bottom:28px;background:linear-gradient(135deg,#1a1829,#1f1d35);'
        f'border:1px solid #2d2b45;border-radius:16px;padding:24px 28px">'
        f'<div style="display:flex;align-items:center;gap:16px">'
        f'<div style="width:4px;height:54px;background:{op_color};border-radius:4px"></div>'
        f'<div>'
        f'<div style="font-size:0.68rem;color:#5a5878;font-weight:700;letter-spacing:0.12em;'
        f'text-transform:uppercase;margin-bottom:5px">{op_pais} &nbsp;·&nbsp; {op_moneda}</div>'
        f'<div style="font-family:Syne,sans-serif;font-size:1.9rem;font-weight:800;'
        f'color:#f0ede8;line-height:1;margin-bottom:6px">{op_nombre}</div>'
        f'<div style="color:#8b8aaa;font-size:0.83rem">'
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
        op_nav = "🚦 Monitor"
    else:
        op_nav = st.radio("", [
            "🚦 Monitor de Estatus",
            "🚚 Transportadoras",
            "👥 Proveedores",
            "📦 Stock & Devoluciones",
            "🔁 Devoluciones",
            "📋 Novedades",
            "🏷️ Tags",
            "🔍 Pedidos",
        ], horizontal=True, label_visibility="collapsed")

    # ══════════════════════════════════════════════════════
    # MONITOR DE ESTATUS — Tabla dinámica por semanas
    # ══════════════════════════════════════════════════════
    if "Monitor" in op_nav and C_ESTATUS in df.columns:

        st.markdown('<div class="seccion-titulo">🚦 Monitor de Alertas de Pedidos</div>', unsafe_allow_html=True)

        # ══ CALCULAR TODAS LAS ALERTAS ══
        # ── Configuración de umbrales por días desde despacho ──
        from datetime import date, timedelta
        hoy = date.today()

        col_umb1, col_umb2 = st.columns([3,1])
        with col_umb1:
            st.markdown(
                f'<div style="background:rgba(99,102,241,0.07);border:1px solid #2d2b45;border-radius:10px;'
                f'padding:10px 16px;font-size:0.8rem;color:#8b8aaa">'
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
                    f'<div style="font-family:Syne,sans-serif;font-weight:700;color:#f0ede8;'
                    f'font-size:0.87rem;margin-bottom:4px">'
                    f'{row["tipo"]}'
                    f'</div>'
                    f'<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:5px">'
                    f'<span style="background:rgba(201,168,76,0.15);color:#c9a84c;font-weight:700;'
                    f'font-size:0.78rem;padding:2px 8px;border-radius:6px">#{row["id"]}</span>'
                    f'<span style="color:#d4d0ea;font-size:0.82rem">{row["cliente"]}</span>'
                    f'</div>'
                    f'<div style="color:#5a5878;font-size:0.75rem;display:flex;gap:12px;flex-wrap:wrap">'
                    f'<span>&#x23F1; {row["tiempo"]}</span>'
                    f'{("<span>&#x1F6A9; " + detalles + "</span>") if detalles else ""}'
                    f'</div>'
                    f'</div>'

                    # Columna derecha — valor
                    f'<div style="display:flex;flex-direction:column;align-items:flex-end;justify-content:center;'
                    f'min-width:80px;text-align:right">'
                    f'<div style="font-family:Syne,sans-serif;font-weight:700;color:#10b981;font-size:0.88rem">'
                    f'{valor_fmt}'
                    f'</div>'
                    f'{"<div style=\"font-size:0.7rem;color:#3d3b55\">" + row["transp"][:14] + "</div>" if row["transp"] and row["transp"] != "nan" else ""}'
                    f'</div>'

                    f'</div>'
                )
                st.markdown(html_card, unsafe_allow_html=True)

        # ══ TABLA DE MONITOREO POR SEMANAS (abajo del Monitor) ══
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="seccion-titulo" style="font-size:1rem">📊 Resumen por Estatus y Semana</div>', unsafe_allow_html=True)

        # Columnas necesarias
        C_UND  = C_CANTIDAD
        C_CLTS = C_CLIENTE
        C_PDD  = C_TOTAL
        C_UTIL = C_GANANCIA
        C_CST  = "PRECIO PROVEEDOR X CANTIDAD"
        C_FLT  = C_FLETE

        meses_disp = sorted(df['_mes'].dropna().unique().tolist(), reverse=True) if '_mes' in df.columns else []
        mes_sel = st.selectbox("📅 Mes", ["Mes completo"] + meses_disp if meses_disp else ["Mes completo"], key="mes_mon2")

        semana_tabs = st.tabs(["📅 Mes Completo", "Sem 1 (1-8)", "Sem 2 (9-16)", "Sem 3 (17-24)", "Sem 4 (25-31)"])

        def semana_df(df_base, sem):
            if sem == 0: return df_base
            rangos = {1:(1,8), 2:(9,16), 3:(17,24), 4:(25,31)}
            ini, fin = rangos[sem]
            return df_base[df_base[C_FECHA].dt.day.between(ini, fin)] if C_FECHA in df_base.columns else df_base



        def construir_tabla(df_filtrado):
            if len(df_filtrado) == 0:
                return pd.DataFrame()

            # Verificar columnas disponibles
            tiene_und  = C_UND  in df_filtrado.columns
            tiene_clts = C_CLTS in df_filtrado.columns
            tiene_pdd  = C_PDD  in df_filtrado.columns
            tiene_util = C_UTIL in df_filtrado.columns
            tiene_cst  = C_CST  in df_filtrado.columns
            tiene_flt  = C_FLT  in df_filtrado.columns

            grupos = df_filtrado.groupby(C_ESTATUS)
            filas = []
            total_pdd_global = df_filtrado[C_PDD].sum() if tiene_pdd else 1

            for estatus, grp in grupos:
                fila = {"Estatus": estatus}
                if tiene_und:  fila["# UND"]   = int(grp[C_UND].sum())
                if tiene_clts: fila["# CLTS"]  = grp[C_CLTS].nunique()
                if tiene_pdd:  fila["$ PDD"]   = grp[C_PDD].sum()
                if tiene_util: fila["$ UTIL"]  = grp[C_UTIL].sum()
                if tiene_cst:  fila["$ CST"]   = grp[C_CST].sum()
                if tiene_flt:  fila["$ FLT"]   = grp[C_FLT].sum()
                if tiene_pdd:  fila["% PDD"]   = grp[C_PDD].sum() / total_pdd_global * 100
                filas.append(fila)

            tabla = pd.DataFrame(filas).sort_values("$ PDD" if "$ PDD" in (filas[0] if filas else {}) else "Estatus", ascending=False)

            # Fila TOTAL
            total_fila = {"Estatus": "TOTAL GENERAL"}
            if tiene_und:  total_fila["# UND"]  = int(df_filtrado[C_UND].sum())
            if tiene_clts: total_fila["# CLTS"] = df_filtrado[C_CLTS].nunique()
            if tiene_pdd:  total_fila["$ PDD"]  = df_filtrado[C_PDD].sum()
            if tiene_util: total_fila["$ UTIL"] = df_filtrado[C_UTIL].sum()
            if tiene_cst:  total_fila["$ CST"]  = df_filtrado[C_CST].sum()
            if tiene_flt:  total_fila["$ FLT"]  = df_filtrado[C_FLT].sum()
            if tiene_pdd:  total_fila["% PDD"]  = 100.0
            tabla = pd.concat([tabla, pd.DataFrame([total_fila])], ignore_index=True)

            return tabla

        def renderizar_tabla(tabla):
            if len(tabla) == 0:
                st.info("Sin datos para este período")
                return

            # Colores por estatus
            COLORES_EST = {
                "PEDIDO ENTREGADO":   "#10b981",
                "ENTREGADO":          "#10b981",
                "CANCELADO":          "#ef4444",
                "PEDIDO CANCELADO":   "#ef4444",
                "DEVOLUCION":         "#f59e0b",
                "DEVOLUCIÓN":         "#f59e0b",
                "PEDIDO EN DEVOLUCIÓN":"#f59e0b",
                "NOVEDAD":            "#8b5cf6",
                "EN REPARTO":         "#06b6d4",
                "BDG TRANSP":         "#f97316",
                "BDG PROV":           "#ec4899",
                "RECLAME EN OFICINA": "#dc2626",
                "RECLAMO EN OFICINA": "#dc2626",
                "TOTAL GENERAL":      "#c9a84c",
            }

            # Header HTML
            cols_tabla = [c for c in ["Estatus","# UND","# CLTS","$ PDD","$ UTIL","$ CST","$ FLT","% PDD"] if c in tabla.columns]
            header = "".join([f'<th style="padding:10px 14px;text-align:{"left" if c=="Estatus" else "right"};font-size:0.72rem;color:#8b8aaa;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;border-bottom:2px solid #2d2b45">{c}</th>' for c in cols_tabla])

            filas_html = ""
            for _, row in tabla.iterrows():
                est_upper = str(row["Estatus"]).upper()
                color = next((v for k,v in COLORES_EST.items() if k in est_upper), "#b0aec8")
                es_total = "TOTAL" in est_upper
                bg = "rgba(201,168,76,0.08)" if es_total else "rgba(255,255,255,0.02)"
                bold = "font-weight:700;" if es_total else ""
                border_top = "border-top:2px solid #2d2b45;" if es_total else ""

                celdas = f'<td style="padding:10px 14px;{bold}{border_top}"><span style="color:{color}">{row["Estatus"]}</span></td>'
                for col in cols_tabla[1:]:
                    if col not in row.index: continue
                    val = row[col]
                    if col in ["# UND","# CLTS"]:
                        txt = f"{int(val):,}" if pd.notna(val) else "—"
                        align = "right"
                    elif col == "% PDD":
                        txt = f"{val:.1f}%" if pd.notna(val) else "—"
                        align = "right"
                    else:
                        txt = f"$ {val:,.0f}" if pd.notna(val) else "—"
                        align = "right"
                    celdas += f'<td style="padding:10px 14px;text-align:{align};{bold}{border_top}color:#f0ede8;font-size:0.88rem">{txt}</td>'

                filas_html += f'<tr style="background:{bg};border-bottom:1px solid #1a1829">{celdas}</tr>'

            html_tabla = f"""
            <div style="overflow-x:auto;border-radius:12px;border:1px solid #2d2b45;margin-top:12px">
                <table style="width:100%;border-collapse:collapse;background:#1a1829">
                    <thead><tr>{header}</tr></thead>
                    <tbody>{filas_html}</tbody>
                </table>
            </div>"""
            st.markdown(html_tabla, unsafe_allow_html=True)

        # Filtrar por mes si se seleccionó
        if mes_sel != "Mes completo" and '_mes' in df.columns:
            df_mon = df[df['_mes'] == mes_sel].copy()
        else:
            df_mon = df.copy()

        # Renderizar cada tab
        for i, tab in enumerate(semana_tabs):
            with tab:
                df_sem = semana_df(df_mon, i)
                n_peds = len(df_sem)
                if n_peds == 0:
                    st.info("Sin pedidos en este período")
                    continue
                st.caption(f"{n_peds:,} pedidos en este período")
                tabla = construir_tabla(df_sem)
                renderizar_tabla(tabla)

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
                fig_t2.add_trace(go.Bar(x=grp_t[C_TRANSP], y=grp_t['Total'], name='Total', marker_color='#6366f1'))
                fig_t2.add_trace(go.Bar(x=grp_t[C_TRANSP], y=grp_t['Entregados'], name='Entregados', marker_color='#10b981'))
                fig_t2.add_trace(go.Bar(x=grp_t[C_TRANSP], y=grp_t['Devoluciones'], name='Devoluciones', marker_color='#f59e0b'))
                fig_t2.add_trace(go.Bar(x=grp_t[C_TRANSP], y=grp_t['Novedades'], name='Novedades', marker_color='#8b5cf6'))
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
                                        color_discrete_sequence=['#8b5cf6'], title='Novedades por Mes')
                        fig_nm.update_layout(**PLOT_LAYOUT, height=360, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                        st.plotly_chart(fig_nm, use_container_width=True)

            # Tabla historial
            cols_nov = [c for c in [C_ID, C_CLIENTE, C_NOVEDAD, C_NOV_SOL, '_d_mov', C_GUIA] if c in df_nov.columns]
            if cols_nov:
                st.markdown('<div style="font-size:0.8rem;color:#8b8aaa;margin-bottom:8px">Mostrando las 100 más recientes</div>', unsafe_allow_html=True)
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
                          color='Cantidad', color_continuous_scale=['#1a1829','#f59e0b','#ef4444'],
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
            with t1: gtab('seguimiento',['#1a1829','#ef4444'],'Tags Seguimiento Activo')
            with t2:
                cr = tags_df[tags_df['cat']=='cancelacion_real']['tag'].value_counts().reset_index()
                cr.columns=['Tag','Cantidad']
                nc = tags_df[tags_df['cat']=='no_cancelacion']['tag'].value_counts().reset_index()
                nc.columns=['Tag','Cantidad']
                ca,cb = st.columns(2)
                with ca:
                    if len(cr):
                        fig=px.bar(cr,x='Cantidad',y='Tag',orientation='h',color='Cantidad',
                                  color_continuous_scale=['#1a1829','#ef4444'],title='❌ Reales')
                        fig.update_layout(**PLOT_LAYOUT,height=300,coloraxis_showscale=False, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                        st.plotly_chart(fig,use_container_width=True)
                with cb:
                    if len(nc):
                        fig=px.bar(nc,x='Cantidad',y='Tag',orientation='h',color='Cantidad',
                                  color_continuous_scale=['#1a1829','#10b981'],title='✅ No son cancelaciones')
                        fig.update_layout(**PLOT_LAYOUT,height=300,coloraxis_showscale=False, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                        st.plotly_chart(fig,use_container_width=True)
                tcr=len(tags_df[tags_df['cat']=='cancelacion_real'])
                tnc=len(tags_df[tags_df['cat']=='no_cancelacion'])
                if tcr+tnc>0:
                    st.markdown(f'<div style="background:rgba(16,185,129,0.08);border:1px solid #10b981;border-radius:10px;padding:14px;margin-top:8px">'
                                f'<b style="color:#f0ede8">📊 Resumen:</b> '
                                f'<span class="badge-r">{tcr} cancelaciones reales</span> &nbsp; '
                                f'<span class="badge-v">{tnc} no son cancelaciones reales</span></div>', unsafe_allow_html=True)
            with t3: gtab('estrategico',['#1a1829','#6366f1'],'Tags Estratégicos')
            with t4:
                top50=tags_df['tag'].value_counts().head(50).reset_index()
                top50.columns=['Tag','Cantidad']
                fig=px.bar(top50,x='Cantidad',y='Tag',orientation='h',color='Cantidad',
                          color_continuous_scale=['#1a1829','#c9a84c'],title='Top Tags')
                fig.update_layout(**PLOT_LAYOUT,height=900,coloraxis_showscale=False, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                st.plotly_chart(fig,use_container_width=True)

    elif "Pedidos" in op_nav:
        f1,f2,f3 = st.columns(3)
        df_fil = df.copy()
        with f1:
            if C_ESTATUS in df.columns:
                opts=['Todos']+sorted(df[C_ESTATUS].astype(str).unique().tolist())
                fe=st.selectbox("Estatus",opts)
                if fe!='Todos': df_fil=df_fil[df_fil[C_ESTATUS].astype(str)==fe]
        with f2:
            if C_TRANSP in df.columns:
                opts_t=['Todas']+sorted(df[C_TRANSP].astype(str).unique().tolist())
                ft=st.selectbox("Transportadora",opts_t)
                if ft!='Todas': df_fil=df_fil[df_fil[C_TRANSP].astype(str)==ft]
        with f3:
            only_alert=st.checkbox("🔴 Solo con alerta crítica")
            if only_alert and alertas_r:
                ids_a=set(str(a['id']) for a in alertas_r)
                df_fil=df_fil[df_fil[C_ID].astype(str).isin(ids_a)]

        cols_v=[c for c in [C_ID,C_FECHA,C_ESTATUS,C_CLIENTE,C_PRODUCTO,C_DEPTO,C_CIUDAD,C_TRANSP,C_TOTAL,C_GANANCIA,C_TAGS,C_NOVEDAD,C_NOV_SOL] if c in df.columns]
        st.dataframe(df_fil[cols_v].head(500), use_container_width=True, height=420)
        st.caption(f"Mostrando {min(len(df_fil),500):,} de {len(df_fil):,} pedidos")

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
        st.markdown('<div style="background:rgba(201,168,76,0.08);border:1px solid #c9a84c;border-radius:12px;padding:14px;text-align:center;color:#f0d080;font-size:0.85rem">🤖 Claude IA se activa cuando configures tu API Key · El dashboard funciona completo sin él</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center;color:#3d3b55;font-size:0.7rem;margin-top:30px">🚀 VisióN360 · Dashboard Profesional · Colombia</div>', unsafe_allow_html=True)
