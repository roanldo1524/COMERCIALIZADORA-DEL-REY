import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="LUCIDBOT — Seguimiento", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #f5f0e8; }
    .block-container { padding: 1.5rem 2rem; }
    .kpi-card {
        background: white; border-radius: 14px; padding: 20px 16px;
        text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        border-top: 5px solid #c4a97d; margin-bottom: 10px;
    }
    .kpi-card.verde  { border-top-color: #059669; }
    .kpi-card.rojo   { border-top-color: #dc2626; }
    .kpi-card.amar   { border-top-color: #d97706; }
    .kpi-card.azul   { border-top-color: #2563eb; }
    .kpi-card.morado { border-top-color: #7c3aed; }
    .kpi-num   { font-size: 2rem; font-weight: 800; color: #1e1b16; margin: 8px 0 4px; }
    .kpi-label { font-size: 0.72rem; color: #6b7280; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; }
    .kpi-sub   { font-size: 0.85rem; color: #059669; font-weight: 600; margin-top: 4px; }
    .alerta-r  { background: #fef2f2; border-left: 4px solid #dc2626; border-radius: 8px; padding: 10px 14px; margin: 5px 0; font-size: 0.86rem; }
    .alerta-a  { background: #fffbeb; border-left: 4px solid #d97706; border-radius: 8px; padding: 10px 14px; margin: 5px 0; font-size: 0.86rem; }
    .badge-r   { background: #dc2626; color: white; border-radius: 20px; padding: 2px 10px; font-size: 0.75rem; font-weight: 700; }
    .badge-a   { background: #d97706; color: white; border-radius: 20px; padding: 2px 10px; font-size: 0.75rem; font-weight: 700; }
    .badge-v   { background: #059669; color: white; border-radius: 20px; padding: 2px 10px; font-size: 0.75rem; font-weight: 700; }
    .caja      { background: white; border-radius: 14px; padding: 20px 24px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#1e1b16 0%,#3d2f1a 100%);
            border-radius:16px;padding:28px 36px;margin-bottom:24px">
    <div style="display:flex;align-items:center;gap:20px">
        <div style="font-size:3rem">🚀</div>
        <div>
            <p style="color:#f5f0e8;font-size:2rem;font-weight:800;margin:0">LUCIDBOT</p>
            <p style="color:#c4a97d;font-size:0.95rem;margin:4px 0 0 0">
                Dashboard de Seguimiento de Pedidos · Dropi Colombia
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── COLUMNAS EXACTAS DE TU EXCEL ────────────────────────────
C_FECHA      = "FECHA"
C_FECHA_MOV  = "FECHA DE ÚLTIMO MOVIMIENTO"   # para calcular tiempo sin cambio
C_ID         = "ID"
C_GUIA       = "NÚMERO GUIA"
C_ESTATUS    = "ESTATUS"
C_CLIENTE    = "NOMBRE CLIENTE"
C_TELEFONO   = "TELÉFONO"
C_DEPTO      = "DEPARTAMENTO DESTINO"
C_CIUDAD     = "CIUDAD DESTINO"
C_DIRECCION  = "DIRECCION"
C_TRANSP     = "TRANSPORTADORA"
C_TOTAL      = "TOTAL DE LA ORDEN"
C_GANANCIA   = "GANANCIA"
C_FLETE      = "PRECIO FLETE"
C_PRODUCTO   = "PRODUCTO"
C_VARIACION  = "VARIACION"
C_CANTIDAD   = "CANTIDAD"
C_TAGS       = "TAGS"
C_NOVEDAD    = "NOVEDAD"
C_NOV_SOL    = "FUE SOLUCIONADA LA NOVEDAD"
C_SOLUCION   = "SOLUCIÓN"
C_OBSERV     = "OBSERVACIÓN"
C_TIENDA     = "TIENDA"
C_VENDEDOR   = "VENDEDOR"
C_INDEMN     = "CONTADOR DE INDEMNIZACIONES"
C_CONCEP_IND = "CONCEPTO ÚLTIMA INDENMIZACIÓN"
C_ULT_MOV    = "ÚLTIMO MOVIMIENTO"

# ── TAGS ────────────────────────────────────────────────────
TAGS_SEG  = ["prioridad de rastreo","en proceso indemnizacion","en proceso indemnización",
             "reclamo en oficinas","cambios de estatus","cambios de estado"]
TAGS_EST  = ["por flete elevado","cancelado por proveedor","cancelado por stock"]
TAGS_CR   = ["cancelado por el cliente","cancelado por cliente - viajes","cancelado por reseñas",
             "cancelado por precio","cancelado por datos incompletos","cancelado por alta devolucion",
             "cancelado por alta devolución","sin cobertura","no abonaron"]
TAGS_NCR  = ["se vuelve a subir","cancelado por pedido repetido","de pruebas"]
TAGS_INFO = ["duplicado entre tiendas","recompra","garantia","garantía","dinero",
             "reprogramada","confirmaciones erradas","pendiente por subir"]

def clasificar_tag(tag):
    t = tag.lower().strip()
    if any(x in t for x in TAGS_SEG):  return 'seguimiento'
    if any(x in t for x in TAGS_EST):  return 'estrategico'
    if any(x in t for x in TAGS_CR):   return 'cancelacion_real'
    if any(x in t for x in TAGS_NCR):  return 'no_cancelacion'
    if any(x in t for x in TAGS_INFO): return 'informativo'
    return 'otro'

def parse_tags(val):
    if pd.isna(val) or str(val).strip() == '': return []
    return [t.strip() for t in str(val).split(',') if t.strip()]

def horas_desde(fecha):
    try:
        if pd.isna(fecha): return None
        return (datetime.now() - pd.to_datetime(fecha)).total_seconds() / 3600
    except: return None

def kpi_html(color, label, num, sub=""):
    s = f'<div class="kpi-sub">{sub}</div>' if sub else ''
    return f'<div class="kpi-card {color}"><div class="kpi-label">{label}</div><div class="kpi-num">{num}</div>{s}</div>'

def barras(df_b, x, y, titulo, paleta, h=350):
    fig = px.bar(df_b, x=x, y=y, orientation='h', color=x,
                 color_continuous_scale=paleta, title=titulo)
    fig.update_layout(height=h, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                      showlegend=False, coloraxis_showscale=False,
                      margin=dict(l=10,r=10,t=40,b=10))
    fig.update_traces(texttemplate='%{x}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

# ── UPLOAD ──────────────────────────────────────────────────
archivo = st.file_uploader("📁 Sube tu reporte Excel de Dropi", type=["xlsx","xls"])

if archivo is None:
    st.markdown("""
    <div class="caja" style="text-align:center;padding:60px">
        <div style="font-size:4rem">📊</div>
        <h3 style="color:#1e1b16;margin:16px 0 8px">Sube tu reporte de Dropi</h3>
        <p style="color:#6b7280;font-size:0.95rem">
            El archivo debe ser el reporte de órdenes exportado desde Dropi
        </p>
        <br>
        <p style="color:#c4a97d;font-size:0.85rem">
            Columnas detectadas automáticamente: FECHA · ESTATUS · TAGS · NOVEDAD · y más
        </p>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── CARGAR ──────────────────────────────────────────────────
@st.cache_data
def cargar(f):
    df = pd.read_excel(f)
    df.columns = [str(c).strip() for c in df.columns]
    return df

with st.spinner("Analizando pedidos..."):
    df = cargar(archivo)

# Parsear fechas
for col_f in [C_FECHA, C_FECHA_MOV]:
    if col_f in df.columns:
        df[col_f] = pd.to_datetime(df[col_f], dayfirst=True, errors='coerce')

# Horas desde último movimiento (para alertas de cambio de estatus)
if C_FECHA_MOV in df.columns:
    df['_h_mov'] = df[C_FECHA_MOV].apply(horas_desde)
    df['_d_mov'] = df['_h_mov'].apply(lambda h: round(h/24,1) if h is not None else None)

# Horas desde fecha de pedido
if C_FECHA in df.columns:
    df['_h_ped'] = df[C_FECHA].apply(horas_desde)
    df['_d_ped'] = df['_h_ped'].apply(lambda h: round(h/24,1) if h is not None else None)
    df['_mes']   = df[C_FECHA].dt.to_period('M').astype(str)

# Numéricos
for col_n in [C_TOTAL, C_GANANCIA, C_FLETE, C_CANTIDAD]:
    if col_n in df.columns:
        df[col_n] = pd.to_numeric(df[col_n], errors='coerce').fillna(0)

# Tags
if C_TAGS in df.columns:
    df['_tags_lista'] = df[C_TAGS].apply(parse_tags)

total = len(df)

# ── KPIs ────────────────────────────────────────────────────
def contar(patron):
    if C_ESTATUS not in df.columns: return 0
    return len(df[df[C_ESTATUS].astype(str).str.upper().str.contains(patron, na=False)])

entregados = contar('ENTREGADO')
cancelados = contar('CANCELADO')
devolucion = contar('DEVOLUCI')
novedades  = contar('NOVEDAD')
en_reparto = contar('REPARTO')
bdg_transp = contar('BDG TRANSP|BODEGA TRANS')
bdg_prov   = contar('BDG PROV|BODEGA PROV')
reclamo    = contar('RECLAMO|OFICINA')
en_proceso = total - entregados - cancelados - devolucion

pct_ent    = round(entregados/total*100,1) if total else 0
tot_venta  = df[C_TOTAL].sum()   if C_TOTAL   in df.columns else 0
tot_gan    = df[C_GANANCIA].sum() if C_GANANCIA in df.columns else 0

st.markdown("### 📊 Resumen General")
c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
def v(n): return f"${n/1e6:.1f}M" if n>=1e6 else f"${n:,.0f}"
with c1: st.markdown(kpi_html("azul","📦 Total Pedidos",f"{total:,}"), unsafe_allow_html=True)
with c2: st.markdown(kpi_html("verde","✅ Entregados",f"{entregados:,}",f"{pct_ent}%"), unsafe_allow_html=True)
with c3: st.markdown(kpi_html("rojo","❌ Cancelados",f"{cancelados:,}"), unsafe_allow_html=True)
with c4: st.markdown(kpi_html("amar","🔄 En Proceso",f"{en_proceso:,}"), unsafe_allow_html=True)
with c5: st.markdown(kpi_html("","↩️ Devolución",f"{devolucion:,}"), unsafe_allow_html=True)
with c6: st.markdown(kpi_html("","💰 Ventas",v(tot_venta)), unsafe_allow_html=True)
with c7: st.markdown(kpi_html("verde","📈 Ganancia",v(tot_gan)), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ALERTAS ─────────────────────────────────────────────────
st.markdown("### 🚨 Centro de Alertas")

alertas_r, alertas_a = [], []

if C_ESTATUS in df.columns:
    for _, row in df.iterrows():
        est  = str(row.get(C_ESTATUS,'')).upper()
        h_m  = row.get('_h_mov')   # horas desde último movimiento
        d_m  = row.get('_d_mov')
        h_p  = row.get('_h_ped')   # horas desde pedido (para reclamo en oficina)
        d_p  = row.get('_d_ped')
        num  = str(row.get(C_ID,'—'))
        cli  = str(row.get(C_CLIENTE,''))[:25] if C_CLIENTE in df.columns else ''
        guia = str(row.get(C_GUIA,''))         if C_GUIA    in df.columns else ''

        # Reclamo en Oficina: +8 días desde fecha pedido
        if ('RECLAMO' in est or 'OFICINA' in est):
            if d_p and d_p > 8:
                alertas_r.append({'tipo':'🔴 Reclamo en Oficina','id':num,'cliente':cli,
                    'msg':f"{d_p:.0f} días sin retiro del cliente | Guía: {guia}"})

        # En Reparto: +24h sin cambio de estatus (último movimiento)
        if 'REPARTO' in est:
            if h_m and h_m > 24:
                alertas_r.append({'tipo':'🔴 En Reparto sin cambio','id':num,'cliente':cli,
                    'msg':f"{h_m:.0f}h sin cambio de estatus | Guía: {guia}"})

        # Novedad sin solucionar
        if 'NOVEDAD' in est:
            sol = str(row.get(C_NOV_SOL,'')).upper() if C_NOV_SOL in df.columns else ''
            if 'SI' not in sol and 'SÍ' not in sol:
                nov_tipo = str(row.get(C_NOVEDAD,''))[:40] if C_NOVEDAD in df.columns else ''
                alertas_r.append({'tipo':'🔴 Novedad sin resolver','id':num,'cliente':cli,
                    'msg':f"Tipo: {nov_tipo or 'No especificado'} | {d_m or '?'} días"})

        # BDG Transportadora: amarillo +24h, rojo +8 días
        if 'BDG TRANSP' in est or 'BODEGA TRANS' in est:
            if d_m and d_m > 8:
                alertas_r.append({'tipo':'🔴 BDG Transp CRÍTICO','id':num,'cliente':cli,
                    'msg':f"{d_m:.0f} días en bodega sin entrega | Guía: {guia}"})
            elif h_m and h_m > 24:
                alertas_a.append({'tipo':'🟡 BDG Transportadora','id':num,'cliente':cli,
                    'msg':f"{h_m:.0f}h sin movimiento | Guía: {guia}"})

        # BDG Proveedor: +24h
        if 'BDG PROV' in est or 'BODEGA PROV' in est:
            if h_m and h_m > 24:
                alertas_r.append({'tipo':'🔴 BDG Proveedor','id':num,'cliente':cli,
                    'msg':f"{h_m:.0f}h sin despacho desde proveedor"})

# Mostrar alertas
al, am = st.columns(2)
with al:
    st.markdown(f'<div class="caja"><b>🔴 Alertas Críticas <span class="badge-r">{len(alertas_r)}</span></b><br><br>', unsafe_allow_html=True)
    if alertas_r:
        for a in alertas_r[:30]:
            st.markdown(f'<div class="alerta-r"><b>{a["tipo"]}</b> · ID {a["id"]} · {a["cliente"]}<br><span style="color:#6b7280;font-size:0.82rem">{a["msg"]}</span></div>', unsafe_allow_html=True)
        if len(alertas_r) > 30: st.caption(f"... y {len(alertas_r)-30} alertas más")
    else:
        st.success("✅ Sin alertas críticas")
    st.markdown('</div>', unsafe_allow_html=True)

with am:
    st.markdown(f'<div class="caja"><b>🟡 Alertas de Atención <span class="badge-a">{len(alertas_a)}</span></b><br><br>', unsafe_allow_html=True)
    if alertas_a:
        for a in alertas_a[:30]:
            st.markdown(f'<div class="alerta-a"><b>{a["tipo"]}</b> · ID {a["id"]} · {a["cliente"]}<br><span style="color:#6b7280;font-size:0.82rem">{a["msg"]}</span></div>', unsafe_allow_html=True)
    else:
        st.success("✅ Sin alertas de atención")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── GRÁFICAS ESTATUS ────────────────────────────────────────
if C_ESTATUS in df.columns:
    st.markdown("### 📦 Análisis por Estatus")
    g1, g2 = st.columns(2)
    COLS = ['#1e1b16','#c4a97d','#059669','#dc2626','#2563eb','#d97706','#7c3aed','#0891b2','#65a30d','#f43f5e']
    with g1:
        ed = df[C_ESTATUS].astype(str).value_counts().reset_index()
        ed.columns = ['Estatus','Cantidad']
        fig = px.pie(ed, values='Cantidad', names='Estatus', color_discrete_sequence=COLS,
                    title='Distribución de Estados')
        fig.update_layout(height=380, paper_bgcolor='rgba(0,0,0,0)')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    with g2:
        if '_mes' in df.columns:
            em = df.groupby(['_mes', C_ESTATUS]).size().reset_index(name='Cantidad')
            fig2 = px.bar(em, x='_mes', y='Cantidad', color=C_ESTATUS, barmode='stack',
                         color_discrete_sequence=COLS, title='Estados por Mes')
            fig2.update_layout(height=380, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)

# ── NOVEDADES ───────────────────────────────────────────────
if C_ESTATUS in df.columns and C_NOVEDAD in df.columns:
    nov_df = df[df[C_ESTATUS].astype(str).str.upper().str.contains('NOVEDAD', na=False)]
    if len(nov_df) > 0:
        st.markdown("### ⚠️ Análisis de Novedades")
        total_nov = len(nov_df)
        sol = sum(1 for v in nov_df[C_NOV_SOL].astype(str).str.upper() if 'SI' in v or 'SÍ' in v) if C_NOV_SOL in df.columns else 0
        no_sol = total_nov - sol
        n1,n2,n3 = st.columns(3)
        with n1: st.markdown(kpi_html("amar","⚠️ Total Novedades",total_nov), unsafe_allow_html=True)
        with n2: st.markdown(kpi_html("verde","✅ Solucionadas",sol,f"{round(sol/total_nov*100,1)}%"), unsafe_allow_html=True)
        with n3: st.markdown(kpi_html("rojo","❌ Pendientes",no_sol), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        tipos_nov = nov_df[C_NOVEDAD].astype(str).value_counts().head(15).reset_index()
        tipos_nov.columns = ['Tipo de Novedad','Cantidad']
        barras(tipos_nov, 'Cantidad', 'Tipo de Novedad', 'Top Tipos de Novedad', 'Oranges', 350)

# ── TAGS ────────────────────────────────────────────────────
if C_TAGS in df.columns:
    st.markdown("### 🏷️ Análisis de Tags")
    todos = []
    for tl in df['_tags_lista']: todos.extend(tl)

    if todos:
        tags_df = pd.DataFrame({'tag': todos})
        tags_df['cat'] = tags_df['tag'].apply(clasificar_tag)

        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚨 Seguimiento","📊 Estratégico","❌ Cancelaciones","✅ No Cancelaciones","📋 Todos"])

        def tab_barras(cat, paleta, titulo):
            d = tags_df[tags_df['cat']==cat]['tag'].value_counts().reset_index()
            d.columns = ['Tag','Cantidad']
            if len(d): barras(d, 'Cantidad', 'Tag', titulo, paleta)
            else: st.info("Sin tags de esta categoría en los datos actuales")

        with tab1: tab_barras('seguimiento', 'Reds', 'Tags de Seguimiento Activo')
        with tab2: tab_barras('estrategico', 'Blues', 'Tags Estratégicos')
        with tab3:
            cr_d = tags_df[tags_df['cat']=='cancelacion_real']['tag'].value_counts().reset_index()
            cr_d.columns = ['Tag','Cantidad']
            nc_d = tags_df[tags_df['cat']=='no_cancelacion']['tag'].value_counts().reset_index()
            nc_d.columns = ['Tag','Cantidad']
            c_a, c_b = st.columns(2)
            with c_a:
                if len(cr_d): barras(cr_d,'Cantidad','Tag','❌ Cancelaciones Reales','Reds',300)
            with c_b:
                if len(nc_d): barras(nc_d,'Cantidad','Tag','✅ NO son Cancelaciones Reales','Greens',300)
            total_cr = len(tags_df[tags_df['cat']=='cancelacion_real'])
            total_nc = len(tags_df[tags_df['cat']=='no_cancelacion'])
            if total_cr + total_nc > 0:
                pct_real = round(total_cr/(total_cr+total_nc)*100,1)
                st.markdown(f'<div style="background:#f0fdf4;border-radius:10px;padding:16px">'
                            f'<b>📊 De los cancelados:</b> '
                            f'<span class="badge-r">{total_cr} reales ({pct_real}%)</span> &nbsp; '
                            f'<span class="badge-v">{total_nc} no son cancelaciones reales</span>'
                            f'</div>', unsafe_allow_html=True)
        with tab4: tab_barras('informativo', 'Purples', 'Tags Informativos')
        with tab5:
            top40 = tags_df['tag'].value_counts().head(40).reset_index()
            top40.columns = ['Tag','Cantidad']
            barras(top40,'Cantidad','Tag','Top 40 Tags',['#f5f0e8','#c4a97d','#1e1b16'],800)

# ── TRANSPORTADORA ──────────────────────────────────────────
if C_TRANSP in df.columns:
    st.markdown("### 🚚 Transportadoras")
    t1, t2 = st.columns(2)
    with t1:
        tr = df[C_TRANSP].astype(str).value_counts().reset_index()
        tr.columns = ['Transportadora','Pedidos']
        fig_tr = px.pie(tr, values='Pedidos', names='Transportadora',
                       color_discrete_sequence=['#1e1b16','#c4a97d','#059669','#2563eb','#d97706'],
                       title='Pedidos por Transportadora')
        fig_tr.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_tr, use_container_width=True)
    with t2:
        if C_GANANCIA in df.columns:
            tr_g = df.groupby(C_TRANSP)[C_GANANCIA].sum().reset_index()
            tr_g.columns = ['Transportadora','Ganancia']
            tr_g = tr_g.sort_values('Ganancia', ascending=False)
            barras(tr_g,'Ganancia','Transportadora','Ganancia por Transportadora',['#f5f0e8','#c4a97d','#059669'],350)

# ── GEO ─────────────────────────────────────────────────────
if C_DEPTO in df.columns or C_CIUDAD in df.columns:
    st.markdown("### 🗺️ Cobertura Geográfica")
    g3, g4 = st.columns(2)
    with g3:
        if C_DEPTO in df.columns:
            dep = df[C_DEPTO].astype(str).value_counts().head(15).reset_index()
            dep.columns = ['Departamento','Pedidos']
            barras(dep,'Pedidos','Departamento','Top Departamentos',['#f5f0e8','#c4a97d','#1e1b16'],450)
    with g4:
        if C_CIUDAD in df.columns:
            ciu = df[C_CIUDAD].astype(str).value_counts().head(15).reset_index()
            ciu.columns = ['Ciudad','Pedidos']
            barras(ciu,'Pedidos','Ciudad','Top Ciudades',['#f5f0e8','#c4a97d','#3d2f1a'],450)

# ── PRODUCTOS ───────────────────────────────────────────────
if C_PRODUCTO in df.columns:
    st.markdown("### 📦 Productos")
    p1, p2 = st.columns(2)
    with p1:
        pr = df[C_PRODUCTO].astype(str).value_counts().head(12).reset_index()
        pr.columns = ['Producto','Unidades']
        pr['Producto'] = pr['Producto'].str[:40]
        barras(pr,'Unidades','Producto','Top Productos por Unidades',['#f5f0e8','#c4a97d','#1e1b16'],450)
    with p2:
        if C_GANANCIA in df.columns:
            pg = df.groupby(C_PRODUCTO)[C_GANANCIA].sum().sort_values(ascending=False).head(12).reset_index()
            pg.columns = ['Producto','Ganancia']
            pg['Producto'] = pg['Producto'].astype(str).str[:40]
            barras(pg,'Ganancia','Producto','Top Productos por Ganancia',['#f5f0e8','#c4a97d','#059669'],450)

# ── FLETE ───────────────────────────────────────────────────
if C_FLETE in df.columns and C_CIUDAD in df.columns:
    st.markdown("### 💸 Ciudades con Flete Elevado")
    fl = df.groupby(C_CIUDAD)[C_FLETE].mean().sort_values(ascending=False).head(15).reset_index()
    fl.columns = ['Ciudad','Flete Promedio']
    barras(fl,'Flete Promedio','Ciudad','Flete Promedio por Ciudad (Top 15)',['#fffbeb','#d97706','#dc2626'],380)
    st.caption("⚠️ Ciudades con flete alto pueden no ser rentables. Considera excluirlas de pauta publicitaria.")

# ── TABLA FILTRADA ──────────────────────────────────────────
st.markdown("### 🔍 Explorar Pedidos")
f1, f2, f3 = st.columns(3)
df_fil = df.copy()

with f1:
    if C_ESTATUS in df.columns:
        opts = ['Todos'] + sorted(df[C_ESTATUS].astype(str).unique().tolist())
        filt_est = st.selectbox("Estatus", opts)
        if filt_est != 'Todos':
            df_fil = df_fil[df_fil[C_ESTATUS].astype(str) == filt_est]
with f2:
    if C_TRANSP in df.columns:
        opts_t = ['Todas'] + sorted(df[C_TRANSP].astype(str).unique().tolist())
        filt_t = st.selectbox("Transportadora", opts_t)
        if filt_t != 'Todas':
            df_fil = df_fil[df_fil[C_TRANSP].astype(str) == filt_t]
with f3:
    solo_alert = st.checkbox("🔴 Solo pedidos con alerta crítica")
    if solo_alert and alertas_r:
        ids_alerta = set(str(a['id']) for a in alertas_r)
        df_fil = df_fil[df_fil[C_ID].astype(str).isin(ids_alerta)]

cols_vis = [c for c in [C_ID, C_FECHA, C_ESTATUS, C_CLIENTE, C_PRODUCTO, C_DEPTO, C_CIUDAD,
                         C_TRANSP, C_TOTAL, C_GANANCIA, C_TAGS, C_NOVEDAD, C_NOV_SOL] if c in df.columns]
st.dataframe(df_fil[cols_vis].head(500), use_container_width=True, height=380)
st.caption(f"Mostrando {min(len(df_fil),500):,} de {len(df_fil):,} pedidos")

# ── CLAUDE ──────────────────────────────────────────────────
st.divider()
CLAUDE_ACTIVO = False
if CLAUDE_ACTIVO:
    import anthropic
    st.markdown("### 🤖 Asistente Claude")
    resumen = (f"Pedidos:{total}, Entregados:{entregados}({pct_ent}%), Cancelados:{cancelados}, "
               f"Devoluciones:{devolucion}, Ganancia:{v(tot_gan)}, "
               f"Alertas críticas:{len(alertas_r)}, Alertas atención:{len(alertas_a)}")
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])
    if prompt := st.chat_input("Pregúntame sobre tus pedidos..."):
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user"): st.write(prompt)
        with st.chat_message("assistant"):
            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
            ph = st.empty(); resp = ""
            with client.messages.stream(model="claude-sonnet-4-6", max_tokens=1024,
                system=f"Eres asistente de LUCIDBOT Colombia. Datos actuales: {resumen}. Responde en español.",
                messages=st.session_state.messages) as stream:
                for text in stream.text_stream:
                    resp += text; ph.write(resp+"▌")
            ph.write(resp)
        st.session_state.messages.append({"role":"assistant","content":resp})
else:
    st.info("🤖 Claude IA se activará cuando configures tu API Key. El dashboard funciona completo sin él.")

st.caption("🚀 LUCIDBOT · Dashboard de Seguimiento Dropi · Colombia")

