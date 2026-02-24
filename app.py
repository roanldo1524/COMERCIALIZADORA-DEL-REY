import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="LUCIDBOT Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
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
h1, h2, h3 { font-family: 'Playfair Display', serif !important; }

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
    font=dict(family='Inter', color='#b0aec8', size=12),
    title_font=dict(family='Playfair Display', color='#f0ede8', size=16),
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
    <div style="text-align:center;padding:20px 0 10px">
        <div style="font-size:2.5rem">🚀</div>
        <div style="font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:800;color:#f0ede8">LUCIDBOT</div>
        <div style="font-size:0.72rem;color:#8b8aaa;letter-spacing:0.1em;text-transform:uppercase">Analytics Dashboard</div>
    </div>
    <hr style="border-color:#2d2b45;margin:10px 0 20px">
    """, unsafe_allow_html=True)

    # Sección PANEL PRINCIPAL
    st.markdown('<div style="font-size:0.62rem;color:#5a5878;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;padding:0 4px;margin-bottom:6px">PANEL PRINCIPAL</div>', unsafe_allow_html=True)

    # Grupo 1: Análisis
    st.markdown('<div style="font-size:0.58rem;color:#3d3b55;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;padding:2px 4px;margin:4px 0 4px">ANÁLISIS</div>', unsafe_allow_html=True)
    vista = st.radio("", [
        "📊  Panel Ejecutivo",
        "📈  P&G",
        "💹  Finanzas",
        "🔮  Proyecciones",
    ], label_visibility="collapsed")

    # Grupo 2: Operacional
    st.markdown('<div style="font-size:0.58rem;color:#3d3b55;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;padding:2px 4px;margin:12px 0 4px">OPERACIONAL</div>', unsafe_allow_html=True)
    vista2 = st.radio("_op", [
        "📦  Operaciones",
        "🚦  Monitor de Estatus",
        "📣  Marketing",
        "🛍️  Catálogo",
        "🤖  Asistente IA",
    ], label_visibility="collapsed")

    # Unificar en una sola variable activa
    # Si el usuario toca el grupo operacional, vista queda en su última selección
    # Usamos session_state para saber cuál fue el último tocado
    if "last_group" not in st.session_state:
        st.session_state.last_group = "analisis"
    
    # Detectar cuál grupo está activo comparando con session_state
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
        <div style="font-size:0.7rem;color:#3d3b55">LUCIDBOT · v2.0 · Colombia</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# SIN ARCHIVO
# ═══════════════════════════════════════════════════════════
if archivo is None:
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                min-height:70vh;text-align:center">
        <div style="font-size:5rem;margin-bottom:20px">📊</div>
        <div style="font-family:'Playfair Display',serif;font-size:2.5rem;font-weight:800;
                    color:#f0ede8;margin-bottom:12px">
            LUCIDBOT Analytics
        </div>
        <div style="font-size:1rem;color:#8b8aaa;max-width:400px;line-height:1.7">
            Sube tu reporte de Dropi desde el panel izquierdo para comenzar el análisis completo
        </div>
        <div style="margin-top:30px;background:rgba(201,168,76,0.1);border:1px solid #c9a84c;
                    border-radius:12px;padding:16px 28px;color:#f0d080;font-size:0.85rem">
            📁 Arrastra tu Excel en el panel izquierdo
        </div>
    </div>
    """, unsafe_allow_html=True)
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

    st.markdown(f"""
    <div style="margin-bottom:28px;background:linear-gradient(135deg,#1a1829,#1f1d35);
                border:1px solid #2d2b45;border-radius:16px;padding:24px 28px">
        <div style="display:flex;align-items:center;gap:16px">
            <div style="width:4px;height:48px;background:{op_color};border-radius:4px"></div>
            <div>
                <div style="font-size:0.7rem;color:#5a5878;font-weight:700;letter-spacing:0.12em;
                            text-transform:uppercase;margin-bottom:4px">{op_pais} · {op_moneda}</div>
                <div style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:800;
                            color:#f0ede8;line-height:1">{op_nombre}</div>
                <div style="color:#8b8aaa;font-size:0.85rem;margin-top:6px">
                    {vista_activa.split('  ')[1]} · {total:,} pedidos analizados
                    {"&nbsp;&nbsp;·&nbsp;&nbsp;<span style='color:#f97316;font-size:0.78rem'>💱 CLP→COP @ " + str(trm_clp_cop) + "</span>" if es_clp else ""}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ──
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: st.markdown(kpi("blue","Total Pedidos",f"{total:,}"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("green","Entregados",f"{entregados:,}",f"✓ {pct_ent}%"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("red","Cancelados",f"{cancelados:,}"), unsafe_allow_html=True)
    with c4: st.markdown(kpi("gold","En Proceso",f"{en_proceso:,}"), unsafe_allow_html=True)
    with c5: st.markdown(kpi("cyan","Ventas",fmt_money(tot_venta)), unsafe_allow_html=True)
    with c6: st.markdown(kpi("purple","Ganancia",fmt_money(tot_gan),f"{pct_gan}% margen"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── NAVEGACIÓN INTERACTIVA ──
    st.markdown('<div class="seccion-titulo">Explorar datos</div>', unsafe_allow_html=True)

    # Sub-navegación según módulo activo
    if "P&G" in vista_activa:
        nav = "💰 P&G"
    elif "Proyecciones" in vista_activa:
        nav = "🔮 Proyecciones"
    elif "Finanzas" in vista_activa:
        nav = "📅 Evolución Mensual"
    else:
        nav = st.radio("", ["📅 Evolución Mensual","🗺️ Mapa Colombia","🏆 Productos Estrella","🚚 Transportadoras","💡 Insights"],
                       horizontal=True, label_visibility="collapsed")

    # ── P&G ──
    if nav == "💰 P&G":
        st.markdown('<div class="seccion-titulo">📈 Estado de Pérdidas y Ganancias</div>', unsafe_allow_html=True)
        if C_TOTAL in df.columns and C_GANANCIA in df.columns:
            tot_flete   = df[C_FLETE].sum()    if C_FLETE    in df.columns else 0
            tot_proveedor = df["PRECIO PROVEEDOR X CANTIDAD"].sum() if "PRECIO PROVEEDOR X CANTIDAD" in df.columns else 0
            tot_comision  = df["COMISION"].sum()   if "COMISION"  in df.columns else 0
            margen = round(tot_gan/tot_venta*100,1) if tot_venta else 0

            p1,p2,p3,p4 = st.columns(4)
            with p1: st.markdown(kpi("cyan",  "💰 Ingresos Brutos",  fmt_money(tot_venta)), unsafe_allow_html=True)
            with p2: st.markdown(kpi("red",   "📦 Costo Proveedor",  fmt_money(tot_proveedor)), unsafe_allow_html=True)
            with p3: st.markdown(kpi("gold",  "🚚 Fletes",           fmt_money(tot_flete)), unsafe_allow_html=True)
            with p4: st.markdown(kpi("green", "✅ Ganancia Neta",    fmt_money(tot_gan), f"{margen}% margen"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if '_mes' in df.columns:
                pg_mes = df.groupby('_mes').agg(
                    Ingresos=(C_TOTAL,'sum'),
                    Ganancia=(C_GANANCIA,'sum'),
                    Flete=(C_FLETE,'sum') if C_FLETE in df.columns else (C_TOTAL,'count')
                ).reset_index()
                pg_mes['Costo'] = pg_mes['Ingresos'] - pg_mes['Ganancia']
                pg_mes['Margen_%'] = (pg_mes['Ganancia'] / pg_mes['Ingresos'] * 100).round(1)

                fig_pg = go.Figure()
                fig_pg.add_trace(go.Bar(x=pg_mes['_mes'], y=pg_mes['Ingresos']/1e6, name='Ingresos',
                                       marker_color='#6366f1', opacity=0.85))
                fig_pg.add_trace(go.Bar(x=pg_mes['_mes'], y=pg_mes['Costo']/1e6, name='Costos',
                                       marker_color='#ef4444', opacity=0.85))
                fig_pg.add_trace(go.Bar(x=pg_mes['_mes'], y=pg_mes['Ganancia']/1e6, name='Ganancia',
                                       marker_color='#10b981', opacity=0.85))
                fig_pg.add_trace(go.Scatter(x=pg_mes['_mes'], y=pg_mes['Margen_%'], name='Margen %',
                                           yaxis='y2', line=dict(color='#c9a84c', width=3),
                                           marker=dict(size=8, color='#c9a84c')))
                fig_pg.update_layout(**PLOT_LAYOUT, barmode='group', height=420,
                                     title='P&G Mensual — Ingresos vs Costos vs Ganancia',
                                     xaxis=AXIS_STYLE,
                                     yaxis=dict(title='Millones COP', **AXIS_STYLE),
                                     yaxis2=dict(title='Margen %', overlaying='y', side='right',
                                                gridcolor='rgba(0,0,0,0)', tickfont=dict(color='#c9a84c'),
                                                ticksuffix='%'))
                st.plotly_chart(fig_pg, use_container_width=True)

                # Tabla P&G por mes
                pg_mes['Ingresos']  = pg_mes['Ingresos'].apply(fmt_money)
                pg_mes['Ganancia']  = pg_mes['Ganancia'].apply(fmt_money)
                pg_mes['Costo']     = pg_mes['Costo'].apply(fmt_money)
                pg_mes['Margen_%']  = pg_mes['Margen_%'].astype(str) + '%'
                pg_mes = pg_mes.rename(columns={'_mes':'Mes','Margen_%':'Margen'})
                st.dataframe(pg_mes[['Mes','Ingresos','Costo','Ganancia','Margen']], use_container_width=True)
        else:
            st.info("Se necesitan las columnas TOTAL DE LA ORDEN y GANANCIA para el P&G")

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
                                      mapbox=dict(center=dict(lat=4.5, lon=-74.3, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)))
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

    # ── TRANSPORTADORAS ──
    elif "Transportadora" in nav and C_TRANSP in df.columns:

        tr_count = df[C_TRANSP].astype(str).value_counts().reset_index()
        tr_count.columns = ['Transportadora','Pedidos']

        t1, t2 = st.columns(2)
        with t1:
            fig_tr = px.pie(tr_count, values='Pedidos', names='Transportadora',
                           color_discrete_sequence=COLORES_ELEGANTES,
                           title='Pedidos por Transportadora', hole=0.45)
            fig_tr.update_layout(**PLOT_LAYOUT, height=380, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
            fig_tr.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_tr, use_container_width=True)

        with t2:
            if C_GANANCIA in df.columns:
                tr_g = df.groupby(C_TRANSP)[C_GANANCIA].sum().sort_values(ascending=False).reset_index()
                tr_g.columns = ['Transportadora','Ganancia']
                fig_trg = px.bar(tr_g, x='Ganancia', y='Transportadora', orientation='h',
                                color='Ganancia', color_continuous_scale=['#1a1829','#10b981'],
                                title='Ganancia por Transportadora')
                fig_trg.update_layout(**PLOT_LAYOUT, height=380, coloraxis_showscale=False, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
                st.plotly_chart(fig_trg, use_container_width=True)

        if C_FLETE in df.columns and C_CIUDAD in df.columns:
            st.markdown("#### 💸 Ciudades con Flete Elevado")
            fl = df.groupby(C_CIUDAD)[C_FLETE].mean().sort_values(ascending=False).head(15).reset_index()
            fl.columns = ['Ciudad','Flete Promedio']
            fig_fl = px.bar(fl, x='Flete Promedio', y='Ciudad', orientation='h',
                           color='Flete Promedio', color_continuous_scale=['#1a1829','#f59e0b','#ef4444'],
                           title='Flete Promedio por Ciudad')
            fig_fl.update_layout(**PLOT_LAYOUT, height=420, coloraxis_showscale=False, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
            st.plotly_chart(fig_fl, use_container_width=True)
            st.caption("⚠️ Considera excluir ciudades de flete alto de tu pauta publicitaria")

    # ── INSIGHTS ──
    elif "Insights" in nav:
        st.markdown("#### 💡 Insights Estratégicos Automáticos")

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


# ═══════════════════════════════════════════════════════════
# ██████  VISTA 2: OPERACIONES
# ═══════════════════════════════════════════════════════════
elif "Operaciones" in vista_activa or "Asistente" in vista_activa or "Monitor" in vista_activa:
    op_nombre = operacion.split("  ")[1]
    op_color  = op_info["color"]
    op_pais   = op_info["pais"]
    op_moneda = op_info["moneda"]

    st.markdown(f"""
    <div style="margin-bottom:28px;background:linear-gradient(135deg,#1a1829,#1f1d35);
                border:1px solid #2d2b45;border-radius:16px;padding:24px 28px">
        <div style="display:flex;align-items:center;gap:16px">
            <div style="width:4px;height:48px;background:{op_color};border-radius:4px"></div>
            <div>
                <div style="font-size:0.7rem;color:#5a5878;font-weight:700;letter-spacing:0.12em;
                            text-transform:uppercase;margin-bottom:4px">{op_pais} · {op_moneda}</div>
                <div style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:800;
                            color:#f0ede8;line-height:1">{op_nombre}</div>
                <div style="color:#8b8aaa;font-size:0.85rem;margin-top:6px">
                    Operaciones · Centro de control · {total:,} pedidos activos
                    {"&nbsp;&nbsp;·&nbsp;&nbsp;<span style='color:#f97316;font-size:0.78rem'>💱 CLP→COP @ " + str(trm_clp_cop) + "</span>" if es_clp else ""}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs operativos
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: st.markdown(kpi("blue","Total",f"{total:,}"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("green","✅ Entregados",f"{entregados:,}",f"{pct_ent}%"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("red","❌ Cancelados",f"{cancelados:,}"), unsafe_allow_html=True)
    with c4: st.markdown(kpi("gold","🔄 En Proceso",f"{en_proceso:,}"), unsafe_allow_html=True)
    with c5: st.markdown(kpi("purple","↩️ Devolución",f"{devolucion:,}"), unsafe_allow_html=True)
    with c6: st.markdown(kpi("cyan","⚠️ Novedades",f"{novedades:,}"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Calcular alertas
    alertas_r, alertas_a = [], []
    if C_ESTATUS in df.columns:
        for _, row in df.iterrows():
            est  = str(row.get(C_ESTATUS,'')).upper()
            h_m  = row.get('_h_mov')
            d_m  = row.get('_d_mov')
            h_p  = row.get('_h_ped')
            d_p  = row.get('_d_ped')
            num  = str(row.get(C_ID,'—'))
            cli  = str(row.get(C_CLIENTE,''))[:22] if C_CLIENTE in df.columns else ''
            guia = str(row.get(C_GUIA,''))         if C_GUIA    in df.columns else ''

            if ('RECLAMO' in est or 'OFICINA' in est) and d_p and d_p > 8:
                alertas_r.append({'tipo':'Reclamo en Oficina','id':num,'cliente':cli,
                    'msg':f"{d_p:.0f} días sin retiro | Guía: {guia}"})

            if 'REPARTO' in est and h_m and h_m > 24:
                alertas_r.append({'tipo':'En Reparto sin cambio','id':num,'cliente':cli,
                    'msg':f"{h_m:.0f}h sin cambio de estatus | Guía: {guia}"})

            if 'NOVEDAD' in est:
                sol = str(row.get(C_NOV_SOL,'')).upper() if C_NOV_SOL in df.columns else ''
                if 'SI' not in sol and 'SÍ' not in sol:
                    nov = str(row.get(C_NOVEDAD,''))[:35] if C_NOVEDAD in df.columns else ''
                    alertas_r.append({'tipo':'Novedad sin resolver','id':num,'cliente':cli,
                        'msg':f"{nov or 'Sin tipo'} | {d_m or '?'} días"})

            if ('BDG TRANSP' in est or 'BODEGA TRANS' in est):
                if d_m and d_m > 8:
                    alertas_r.append({'tipo':'BDG Transp CRÍTICO','id':num,'cliente':cli,
                        'msg':f"{d_m:.0f} días sin entrega | Guía: {guia}"})
                elif h_m and h_m > 24:
                    alertas_a.append({'tipo':'BDG Transportadora','id':num,'cliente':cli,
                        'msg':f"{h_m:.0f}h sin movimiento | Guía: {guia}"})

            if ('BDG PROV' in est or 'BODEGA PROV' in est) and h_m and h_m > 24:
                alertas_r.append({'tipo':'BDG Proveedor','id':num,'cliente':cli,
                    'msg':f"{h_m:.0f}h sin despacho"})

    # Mostrar alertas
    al, am = st.columns(2)
    with al:
        st.markdown(f'<div style="background:#1a1829;border:1px solid #2d2b45;border-radius:14px;padding:20px">'
                    f'<div style="font-family:Playfair Display,serif;font-size:1.1rem;color:#f0ede8;font-weight:700;margin-bottom:14px">'
                    f'🔴 Alertas Críticas <span class="badge-r">{len(alertas_r)}</span></div>', unsafe_allow_html=True)
        if alertas_r:
            for a in alertas_r[:25]:
                st.markdown(f'<div class="alerta-r"><b>{a["tipo"]}</b> · #{a["id"]} · {a["cliente"]}<br>'
                            f'<span style="color:#8b8aaa;font-size:0.8rem">{a["msg"]}</span></div>', unsafe_allow_html=True)
            if len(alertas_r)>25: st.caption(f"... y {len(alertas_r)-25} más")
        else:
            st.markdown('<div style="color:#34d399;text-align:center;padding:20px">✅ Sin alertas críticas</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with am:
        st.markdown(f'<div style="background:#1a1829;border:1px solid #2d2b45;border-radius:14px;padding:20px">'
                    f'<div style="font-family:Playfair Display,serif;font-size:1.1rem;color:#f0ede8;font-weight:700;margin-bottom:14px">'
                    f'🟡 Alertas de Atención <span class="badge-a">{len(alertas_a)}</span></div>', unsafe_allow_html=True)
        if alertas_a:
            for a in alertas_a[:25]:
                st.markdown(f'<div class="alerta-a"><b>{a["tipo"]}</b> · #{a["id"]} · {a["cliente"]}<br>'
                            f'<span style="color:#8b8aaa;font-size:0.8rem">{a["msg"]}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#34d399;text-align:center;padding:20px">✅ Sin alertas de atención</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs de análisis operativo
    op_nav = st.radio("", ["📦 Estados","⚠️ Novedades","🏷️ Tags","🔍 Pedidos"],
                     horizontal=True, label_visibility="collapsed")

    if "Estados" in op_nav and C_ESTATUS in df.columns:
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
                    system=f"Eres asistente LUCIDBOT Colombia. Datos:{resumen}. Responde en español.",
                    messages=st.session_state.messages) as stream:
                    for text in stream.text_stream:
                        resp+=text; ph.write(resp+"▌")
                ph.write(resp)
            st.session_state.messages.append({"role":"assistant","content":resp})
    else:
        st.markdown('<div style="background:rgba(201,168,76,0.08);border:1px solid #c9a84c;border-radius:12px;padding:14px;text-align:center;color:#f0d080;font-size:0.85rem">🤖 Claude IA se activa cuando configures tu API Key · El dashboard funciona completo sin él</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center;color:#3d3b55;font-size:0.7rem;margin-top:30px">🚀 LUCIDBOT Analytics · Dashboard Profesional · Colombia</div>', unsafe_allow_html=True)
