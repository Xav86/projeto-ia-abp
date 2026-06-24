import json
import streamlit as st
from charts.gauge import render_gauge
from charts.fuzzy import render_fuzzy
from components.fuzzy_engine import calcular_risco

st.set_page_config(
    page_title="Sistema de Previsão de Incêndios Florestais",
    page_icon="🔥",
    layout="wide",
)

# --- Carrega valores padrão do arquivo de configuração ---
with open("config/defaults.json", encoding="utf-8") as f:
    DEFAULTS = json.load(f)

# --- Estado da sessão: usa defaults enquanto a IA não retornar valores reais ---
if "risco" not in st.session_state:
    st.session_state.risco = DEFAULTS["risco"]
if "probabilidade" not in st.session_state:
    st.session_state.probabilidade = DEFAULTS["probabilidade"]
if "justificativa" not in st.session_state:
    st.session_state.justificativa = DEFAULTS["justificativa"]

# --- Título ---
st.markdown("## 🔥 Sistema Inteligente de Previsão de Incêndios Florestais")
st.caption("Avaliação de risco baseada em condições climáticas")
st.divider()

# ── Linha 1: Entradas | Indicador de Risco ──────────────────────────────────
col_esq, col_dir = st.columns([1, 2], gap="medium")

with col_esq:
    st.markdown("### Parâmetros Climáticos")

    temperatura = st.slider("Temperatura (°C)", min_value=0, max_value=50, value=25, step=1)
    umidade     = st.slider("Umidade (%)", min_value=0, max_value=100, value=50, step=1)
    vento       = st.slider("Velocidade do vento (km/h)", min_value=0, max_value=100, value=20, step=1)

    st.divider()

    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Risco", st.session_state.risco)
    col_m2.metric("Probabilidade", f"{st.session_state.probabilidade:.0f}%")

    if st.button("🔍 Calcular Risco", use_container_width=True, type="primary"):
        resultado = calcular_risco(temperatura, umidade, vento)
        # Quando a IA estiver integrada, resultado será um dict com as chaves abaixo
        if resultado is not None:
            st.session_state.risco         = resultado["risco"]
            st.session_state.probabilidade = resultado["probabilidade"]
            st.session_state.justificativa = resultado["justificativa"]
            st.rerun()

with col_dir:
    st.markdown("### Indicador de Risco")
    st.plotly_chart(render_gauge(st.session_state.probabilidade), use_container_width=True)

st.divider()

# ── Linha 2: Justificativa | Gráfico Fuzzy ──────────────────────────────────
col_esq2, col_dir2 = st.columns([1, 2], gap="medium")

with col_esq2:
    st.markdown("### Justificativa")
    st.info(st.session_state.justificativa, icon="📋")

with col_dir2:
    st.markdown("### Funções de Pertinência Fuzzy")
    st.pyplot(render_fuzzy(st.session_state.probabilidade), use_container_width=True)
