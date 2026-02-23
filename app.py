import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(
    page_title="LUCIDBOT — Dashboard",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
    .main { background-color: #f5f0e8; }
    .block-container { padding: 2rem 2rem; }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-top: 4px solid #2563eb;
    }
    h1 { color: #1e1b16; }
    h2 { color: #1e1b16; border-bottom: 2px solid #2563eb; padding-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🚀 LUCIDBOT — Dashboard de Ventas")
    st.caption("Sube tu Excel y analiza tus datos automáticamente")
with col2:
    st.image("https://img.icons8.com/fluency/96/combo-chart.png", width=80)

st.divider()

# ============================================================
# SUBIR ARCHIVO
# ============================================================
uploaded_file = st.file_uploader(
    "📁 Sube tu archivo Excel aquí",
    type=["xlsx", "xls"],
    help="Sube el reporte de órdenes exportado de tu plataforma"
)

if uploaded_file is None:
    st.info("👆 Sube tu archivo Excel para comenzar el análisis")
    st.stop()

# ============================================================
# CARGAR Y PROCESAR DATOS
# ============================================================
@st.cache_data
def cargar_datos(file):
    df = pd.read_excel(file)
    return df

with st.spinner("Analizando tu archivo..."):
    df = cargar_datos(uploaded_file)

# Detectar columnas automáticamente
def detectar_columna(df, posibles_nombres):
    for nombre in posibles_nombres:
        for col in df.columns:
            if nombre.lower() in col.lower():
                return col
    return None

col_fecha = detectar_columna(df, ['FECHA', 'fecha', 'date', 'FECHA DE'])
col_ventas = detectar_columna(df, ['TOTAL', 'total', 'VENTA', 'venta', 'PRECIO'])
col_estatus = detectar_columna(df, ['ESTATUS', 'estatus', 'STATUS', 'estado', 'ESTADO'])
col_producto = detectar_columna(df, ['PRODUCTO', 'producto', 'product'])
col_depto = detectar_columna(df, ['DEPARTAMENTO', 'departamento', 'DEPTO'])
col_ciudad = detectar_columna(df, ['CIUDAD', 'ciudad', 'city'])
col_utilidad = detectar_columna(df, ['GANANCIA', 'ganancia', 'UTILIDAD', 'utilidad'])
col_trans = detectar_columna(df, ['TRANSPORTADORA', 'transportadora', 'COURIER'])

# Procesar fechas
if col_fecha:
    df[col_fecha] = pd.to_datetime(df[col_fecha], dayfirst=True, errors='coerce')
    df['mes'] = df[col_fecha].dt.to_period('M').astype(str)
    df['dia_semana'] = df[col_fecha].dt.day_name()
    df['dia'] = df[col_fecha].dt.date

# Limpiar ventas
if col_ventas:
    df[col_ventas] = pd.to_numeric(df[col_ventas], errors='coerce').fillna(0)

if col_utilidad:
    df[col_utilidad] = pd.to_numeric(df[col_utilidad], errors='coerce').fillna(0)

st.success(f"✅ Archivo cargado: **{len(df):,} órdenes** | **{len(df.columns)} columnas**")

# ============================================================
# KPIs PRINCIPALES
# ============================================================
st.markdown("## 📊 Resumen General")

total_ordenes = len(df)
total_ventas = df[col_ventas].sum() if col_ventas else 0
total_utilidad = df[col_utilidad].sum() if col_utilidad else 0
entregadas = len(df[df[col_estatus].str.upper().str.contains('ENTREGADO', na=False)]) if col_estatus else 0
canceladas = len(df[df[col_estatus].str.upper().str.contains('CANCELADO', na=False)]) if col_estatus else 0
pct_entrega = round(entregadas / total_ordenes * 100, 1) if total_ordenes > 0 else 0

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("📦 Total Órdenes", f"{total_ordenes:,}")
with k2:
    st.metric("💰 Ventas Brutas", f"${total_ventas/1_000_000:.1f}M")
with k3:
    st.metric("📈 Utilidad", f"${total_utilidad/1_000_000:.1f}M")
with k4:
    st.metric("✅ % Entrega", f"{pct_entrega}%")
with k5:
    st.metric("❌ Canceladas", f"{canceladas:,}")

st.divider()

# ============================================================
# GRÁFICAS
# ============================================================

# --- VENTAS POR MES ---
if col_fecha and col_ventas:
    st.markdown("## 📅 Ventas por Mes")
    
    ventas_mes = df.groupby('mes').agg(
        Ventas=(col_ventas, 'sum'),
        Ordenes=(col_ventas, 'count'),
        Utilidad=(col_utilidad, 'sum') if col_utilidad else (col_ventas, 'count')
    ).reset_index().sort_values('mes')
    
    tab1, tab2 = st.tabs(["💰 Ventas & Utilidad", "📦 Órdenes"])
    
    with tab1:
        fig = go.Figure()
        fig.add_bar(x=ventas_mes['mes'], y=ventas_mes['Ventas']/1e6,
                   name='Ventas', marker_color='#2563eb')
        if col_utilidad:
            fig.add_bar(x=ventas_mes['mes'], y=ventas_mes['Utilidad']/1e6,
                       name='Utilidad', marker_color='#059669')
        fig.update_layout(
            barmode='group', height=400,
            yaxis_title='Millones COP',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig2 = px.bar(ventas_mes, x='mes', y='Ordenes',
                     color='Ordenes', color_continuous_scale='Blues',
                     title='Número de Órdenes por Mes')
        fig2.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)

# --- ESTADOS ---
if col_estatus:
    st.markdown("## 📊 Estado de Órdenes")
    col_a, col_b = st.columns(2)
    
    with col_a:
        estados = df[col_estatus].value_counts().reset_index()
        estados.columns = ['Estado', 'Cantidad']
        fig3 = px.pie(estados, values='Cantidad', names='Estado',
                     color_discrete_sequence=px.colors.qualitative.Bold,
                     title='Distribución de Estados')
        fig3.update_layout(height=350)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col_b:
        if col_fecha:
            estados_mes = df.groupby(['mes', col_estatus]).size().reset_index(name='Cantidad')
            fig4 = px.bar(estados_mes, x='mes', y='Cantidad', color=col_estatus,
                         title='Estados por Mes', barmode='stack',
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            fig4.update_layout(height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig4, use_container_width=True)

# --- PRODUCTOS ---
if col_producto:
    st.markdown("## 📦 Top Productos")
    col_c, col_d = st.columns(2)
    
    with col_c:
        top_productos = df[col_producto].value_counts().head(10).reset_index()
        top_productos.columns = ['Producto', 'Unidades']
        top_productos['Producto'] = top_productos['Producto'].str[:35]
        fig5 = px.bar(top_productos, x='Unidades', y='Producto', orientation='h',
                     color='Unidades', color_continuous_scale='Blues',
                     title='Top 10 Productos por Unidades')
        fig5.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig5, use_container_width=True)
    
    with col_d:
        if col_ventas:
            ventas_prod = df.groupby(col_producto)[col_ventas].sum().sort_values(ascending=False).head(10).reset_index()
            ventas_prod.columns = ['Producto', 'Ventas']
            ventas_prod['Producto'] = ventas_prod['Producto'].str[:35]
            fig6 = px.bar(ventas_prod, x='Ventas', y='Producto', orientation='h',
                         color='Ventas', color_continuous_scale='Greens',
                         title='Top 10 Productos por Ventas COP')
            fig6.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig6, use_container_width=True)

# --- DEPARTAMENTOS ---
if col_depto:
    st.markdown("## 🗺️ Ventas por Departamento")
    col_e, col_f = st.columns([2, 1])
    
    with col_e:
        top_deptos = df[col_depto].value_counts().head(20).reset_index()
        top_deptos.columns = ['Departamento', 'Órdenes']
        fig7 = px.bar(top_deptos, x='Órdenes', y='Departamento', orientation='h',
                     color='Órdenes', color_continuous_scale='Purples',
                     title='Órdenes por Departamento')
        fig7.update_layout(height=500, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig7, use_container_width=True)
    
    with col_f:
        st.markdown("### 🏆 Top 10")
        top10 = df[col_depto].value_counts().head(10)
        for i, (depto, count) in enumerate(top10.items(), 1):
            pct = round(count / total_ordenes * 100, 1)
            st.markdown(f"**{i}.** {depto} — `{count}` ({pct}%)")

# --- DIAS PICO ---
if col_fecha:
    st.markdown("## 📅 Días con Más Ventas")
    
    if col_ventas:
        ventas_dia = df.groupby('dia')[col_ventas].agg(['sum', 'count']).reset_index()
        ventas_dia.columns = ['Fecha', 'Ventas', 'Órdenes']
        ventas_dia = ventas_dia.sort_values('Ventas', ascending=False).head(15)
        ventas_dia['Fecha'] = ventas_dia['Fecha'].astype(str)
        
        fig8 = px.bar(ventas_dia, x='Fecha', y='Ventas',
                     color='Órdenes', color_continuous_scale='Oranges',
                     title='Top 15 Días por Ventas')
        fig8.update_layout(height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig8, use_container_width=True)
    
    dias_map = {'Monday':'Lunes','Tuesday':'Martes','Wednesday':'Miércoles',
                'Thursday':'Jueves','Friday':'Viernes','Saturday':'Sábado','Sunday':'Domingo'}
    df['dia_es'] = df['dia_semana'].map(dias_map)
    orden_dias = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
    
    ordenes_dow = df['dia_es'].value_counts().reindex(orden_dias).reset_index()
    ordenes_dow.columns = ['Día', 'Órdenes']
    fig9 = px.bar(ordenes_dow, x='Día', y='Órdenes',
                 color='Órdenes', color_continuous_scale='Blues',
                 title='Órdenes por Día de la Semana')
    fig9.update_layout(height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig9, use_container_width=True)

# --- TRANSPORTADORAS ---
if col_trans:
    st.markdown("## 🚚 Transportadoras")
    trans_count = df[col_trans].value_counts().reset_index()
    trans_count.columns = ['Transportadora', 'Órdenes']
    fig10 = px.pie(trans_count, values='Órdenes', names='Transportadora',
                  title='Distribución por Transportadora',
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig10.update_layout(height=350)
    st.plotly_chart(fig10, use_container_width=True)

# --- TABLA DATOS ---
st.markdown("## 🔍 Explorar Datos")
with st.expander("Ver tabla completa"):
    st.dataframe(df, use_container_width=True, height=400)

# ============================================================
# CLAUDE AI - PREPARADO (activar cuando tengas API Key)
# ============================================================
st.divider()
st.markdown("## 🤖 Asistente IA")

CLAUDE_ACTIVO = False  # Cambia a True cuando tengas créditos en Anthropic

if CLAUDE_ACTIVO:
    import anthropic
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    resumen = f"""
    Datos cargados: {total_ordenes} órdenes, ${total_ventas/1e6:.1f}M ventas, 
    ${total_utilidad/1e6:.1f}M utilidad, {pct_entrega}% tasa de entrega, 
    {canceladas} canceladas.
    """
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    if prompt := st.chat_input("Pregúntame sobre tus datos..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
            placeholder = st.empty()
            full_response = ""
            with client.messages.stream(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                system=f"Eres el asistente de LUCIDBOT. Datos actuales: {resumen}. Responde en español.",
                messages=st.session_state.messages
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    placeholder.write(full_response + "▌")
            placeholder.write(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

else:
    st.info("🤖 El asistente Claude estará disponible próximamente. Por ahora disfruta el dashboard completo arriba.")

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.caption("🚀 LUCIDBOT Dashboard · Análisis automático de ventas · Hecho con Streamlit")
