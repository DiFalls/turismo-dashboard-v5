"""
╔══════════════════════════════════════════════════════════════════════╗
║   TURISMO NORDESTE · Dashboard Estratégico de Desempenho             ║
║   v5.0 — Timestamp Fixo · Sidebar Default · Sem Hint · Contraste     ║
╚══════════════════════════════════════════════════════════════════════╝

Copyright (c) 2026 Difalls ask: Pedro V. · All rights reserved.

Este trabalho está licenciado sob a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
Para ver uma cópia desta licença, visite http://creativecommons.org/licenses/by-nc-nd/4.0/ ou envie uma carta para
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

Você pode:
- Compartilhar — copiar e redistribuir o material em qualquer suporte ou formato

Sob os seguintes termos:
- Atribuição — Você deve dar crédito ao autor original.
- Não Comercial — Você não pode usar o material para fins comerciais.
- Sem Derivações — Se você remixar, transformar ou criar a partir do material, não pode distribuir o material modificado.

Aviso: Este software é fornecido "como está", sem garantias de qualquer tipo.

CORREÇÕES v5.0:
  [FIX-1] Timestamp fixado — dia + horário sempre visível no canto
  [FIX-2] Sidebar expandida por default e toggle simplificado e funcional
  [FIX-3] Removida mensagem "hover → câmera para exportar png" de todos os gráficos
  [FIX-4] Background dos gráficos com contraste claro em relação ao fundo
  [MAINT] Toda lógica de filtragem, gráficos e guias do v3.0 preservada
"""

import os
from typing import Any

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ══════════════════════════════════════════════════════════════════
# 0. PAGE CONFIG
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Turismo Nordeste · Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════
# 1. DESIGN TOKENS
# ══════════════════════════════════════════════════════════════════
PAGE_BG      = "#05080D"   # fundo da página — muito escuro
SIDEBAR_BG   = "#090E18"   # fundo da sidebar
CARD_BG      = "#0B1320"   # fundo do card/seção
CHART_CARD   = "#0F1D2E"   # fundo do card de gráfico — notavelmente mais claro que a página
PLOT_BG      = "#07111C"   # fundo interno do Plotly — levemente mais escuro que o card
PANEL        = "#182840"   # hover/panel
BORDER       = "#1E3650"
BORDER_LIGHT = "#2A4A6B"   # borda mais viva para os cards de gráfico
GRID         = "#152538"   # linhas de grade

GOLD   = "#F5A623"
TEAL   = "#20B2AA"
CORAL  = "#FF6B6B"
BLUE   = "#4A90E2"
VIOLET = "#9B59B6"
GREEN  = "#2ECC71"
AMBER  = "#FBB13C"
ROSE   = "#E91E8C"

TEXT_H = "#FFFFFF"
TEXT_P = "#CBD5E1"
TEXT_D = "#64748B"

STATE_COLORS = {"CE": GOLD, "PE": TEAL, "PI": VIOLET, "RN": CORAL}
TYPE_COLORS  = {"Hotel": BLUE, "Pousada": TEAL, "Agencia": GOLD}
PALETTE      = [GOLD, TEAL, CORAL, BLUE, VIOLET, GREEN, AMBER]

# Config Plotly para exportar imagem (câmera icon visível)
CHART_CONFIG = {
    "displayModeBar": "hover",   # aparece só ao passar o mouse — não ocupa espaço fixo
    "displaylogo": False,
    "modeBarButtonsToRemove": [
        "zoom2d", "pan2d", "select2d", "lasso2d",
        "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
        "toggleSpikelines", "hoverClosestCartesian", "hoverCompareCartesian",
    ],
    "toImageButtonOptions": {
        "format": "png",
        "filename": "turismo_nordeste_grafico",
        "height": 600,
        "width": 1100,
        "scale": 2,
    },
}

# ══════════════════════════════════════════════════════════════════
# 2. CSS GLOBAL
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Syne:wght@400;600;700;800&display=swap');

    /* RESTAURA O BOTÃO DE TOGGLE DA SIDEBAR */
  button[kind="header"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: rgba(245, 166, 35, 0.15) !important;
    border-radius: 8px !important;
    z-index: 9999 !important;
    width: 32px !important;
    height: 32px !important;
    align-items: center !important;
    justify-content: center !important;
  }

  button[kind="header"]:hover {
    background: rgba(245, 166, 35, 0.4) !important;
  }

  /* RESTAURA A BARRA SUPERIOR (DEPLOY) */
  header[data-testid="stHeader"] {
    background: transparent !important;
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
  }

  /* GARANTE QUE O CONTEÚDO NÃO FIQUE SOBREPOSTO */
  .main .block-container {
    padding-top: 3rem !important;
  }
            
  /* ── Página ── */
  .stApp {
    background: #05080D !important;
  }
  .main .block-container {
    padding: 0.75rem 1.75rem 2rem 1.75rem !important;
    max-width: 100% !important;
  }

  /* ── Sidebar ── */
  
  section[data-testid="stSidebar"] .stSelectbox > div[data-baseweb="select"] > div,
  section[data-testid="stSidebar"] .stMultiSelect > div[data-baseweb="select"] > div {
    background: #1A2436 !important;
    border: 1px solid #2A4A6B !important;
    border-radius: 8px !important;
    color: #CBD5E1 !important;
  }

  /* ── Animações ── */
  @keyframes fadeUp {
    from { opacity:0; transform:translateY(10px); }
    to   { opacity:1; transform:translateY(0); }
  }
  @keyframes shine {
    0%   { background-position: 0% center; }
    100% { background-position: 200% center; }
  }
  @keyframes ts-blink {
    0%,100% { opacity:1; }
    50%      { opacity:0.5; }
  }

              /* ══════════════════════════════════════════════════════
     TIMESTAMP FIXADO - POSICIONADO CORRETAMENTE
  ══════════════════════════════════════════════════════ */
  #ts-badge {
    position: fixed;
    top: 60px;  /* Aumentado para ficar abaixo do botão de deploy */
    right: 16px;
    z-index: 99999;
    background: linear-gradient(135deg, rgba(9,14,24,0.96), rgba(15,29,46,0.96));
    border: 1px solid #2A4A6B;
    border-left: 3px solid #F5A623;
    border-radius: 10px;
    padding: 6px 14px 6px 12px;
    display: flex;
    align-items: center;
    gap: 9px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    backdrop-filter: blur(8px);
    font-family: 'JetBrains Mono', monospace;
    pointer-events: none;
    animation: fadeUp 0.5s ease both;
  }

  #ts-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #2ECC71;
    animation: ts-blink 2s ease infinite;
    flex-shrink: 0;
  }
  #ts-label {
    font-size: 9px;
    color: #64748B;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 1px;
  }
  #ts-time {
    font-size: 13px;
    font-weight: 600;
    color: #F5A623;
    letter-spacing: 0.5px;
  }
  #ts-date {
    font-size: 10px;
    color: #CBD5E1;
    letter-spacing: 0.3px;
  }

  /* ── Top bar ── */
  .top-bar {
    background: linear-gradient(135deg, #0B1320 0%, #0C1520 100%);
    border: 1px solid #2A4A6B;
    border-bottom: 2px solid #F5A623;
    border-radius: 16px;
    padding: 14px 24px;
    margin-bottom: 18px;
    animation: fadeUp 0.4s ease both;
  }
  .top-bar-title {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(90deg, #F5A623, #FBB13C, #F5A623, #E69500, #F5A623);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shine 3s linear infinite;
    letter-spacing: -0.02em;
    margin: 0;
  }
  .top-bar-sub {
    font-size: 11px;
    color: #64748B;
    letter-spacing: 0.08em;
    margin-top: 2px;
    font-family: 'Inter', sans-serif;
  }
  .stats-info {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #CBD5E1;
  }
  .stats-highlight {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 600;
    color: #F5A623;
    background: rgba(245,166,35,0.10);
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid rgba(245,166,35,0.25);
  }

  /* ── Section header ── */
  .section-header {
    display: flex;
    align-items: baseline;
    gap: 14px;
    margin: 24px 0 12px;
    padding-bottom: 10px;
    border-bottom: 2px solid #F5A623;
    animation: fadeUp 0.4s ease both;
  }
  .section-title {
    font-family: 'Syne', sans-serif;
    font-size: 19px;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0;
  }
  .section-pill {
    background: rgba(245,166,35,0.10);
    border: 1px solid rgba(245,166,35,0.35);
    color: #F5A623;
    font-size: 10px;
    padding: 3px 14px;
    border-radius: 30px;
    font-weight: 700;
    letter-spacing: 0.09em;
    white-space: nowrap;
  }

  /* ── KPI Cards ── */
  .kpi-card {
    background: linear-gradient(135deg, #0F1D2E 0%, #111E30 100%);
    border: 1px solid #2A4A6B;
    border-top: 3px solid var(--card-color, #F5A623);
    border-radius: 16px;
    padding: 16px 14px 12px;
    width: 100%;
    min-height: 160px;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s;
    animation: fadeUp 0.5s ease both;
    box-shadow: 0 4px 16px rgba(0,0,0,0.35);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-sizing: border-box;
  }
  .kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.5);
  }
  .kpi-icon { font-size: 26px; text-align: center; display: block; }
  .kpi-label {
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #64748B;
    font-weight: 600;
    text-align: center;
    margin: 3px 0 2px;
  }
  .kpi-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 21px;
    font-weight: 700;
    text-align: center;
    word-break: break-word;
    margin: 3px 0;
  }
  .kpi-sub { font-size: 10px; color: #64748B; text-align: center; font-family: 'Inter', sans-serif; }
  .kpi-delta-up { color: #2ECC71; font-weight: 600; font-size: 11px; text-align: center; }
  .kpi-delta-down { color: #FF6B6B; font-weight: 600; font-size: 11px; text-align: center; }
  .kpi-delta-neutral { color: #FBB13C; font-weight: 600; font-size: 11px; text-align: center; }

  /* ── Chart Cards ── */
  .chart-card {
    background: #0F1D2E;
    border: 1.5px solid #2A4A6B;
    border-radius: 16px;
    padding: 16px 16px 6px;
    margin-bottom: 12px;
    box-shadow: 0 0 0 1px rgba(42,74,107,0.25), 0 6px 24px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.03);
    animation: fadeUp 0.5s ease both;
    position: relative;
  }
  .chart-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #F5A623 0%, #20B2AA 50%, transparent 100%);
    border-radius: 16px 16px 0 0;
    opacity: 0.55;
  }
  .chart-title { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; color: #FFFFFF; margin: 0 0 2px; }
  .chart-subtitle { font-family: 'Inter', sans-serif; font-size: 10.5px; color: #64748B; margin: 0 0 8px; }

  /* ── Insights ── */
  .insight-box {
    background: linear-gradient(135deg, #0F1D2E 0%, #111E30 100%);
    border-left: 3px solid #F5A623;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.25);
    animation: fadeUp 0.6s ease both;
    display: flex;
    align-items: flex-start;
    gap: 12px;
  }
  .insight-icon { font-size: 18px; flex-shrink: 0; margin-top: 1px; }
  .insight-text { font-family: 'Inter', sans-serif; color: #CBD5E1; font-size: 13px; line-height: 1.55; }
  .insight-text strong { color: #FFFFFF; }

  /* ── Filter titles sidebar ── */
  .filter-title {
    font-family: 'Syne', sans-serif;
    font-size: 12px;
    font-weight: 700;
    color: #F5A623;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid rgba(245,166,35,0.25);
    display: block;
  }

  /* ── Resumo filtros ── */
  .resumo-text {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    color: #CBD5E1;
    line-height: 1.9;
    background: rgba(0,0,0,0.3);
    padding: 10px 14px;
    border-radius: 10px;
    border: 1px solid #1E3650;
  }

  /* ── Botões tipo na sidebar ── */
  div[data-testid="stSidebar"] .stButton > button {
    background: #1A2A3A;
    border: 1px solid #1E3650;
    border-radius: 10px;
    color: #64748B;
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 600;
    padding: 12px 6px;
    width: 100%;
    transition: all 0.2s ease;
    white-space: pre-line;
    line-height: 1.3;
  }
  div[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(245,166,35,0.14);
    border-color: #F5A623;
    color: #F5A623;
  }
  .active-badge {
    background: linear-gradient(135deg,#f4c475,#E69500);
    border-radius: 0 0 10px 10px;
    padding: 2px 0;
    text-align: center;
    font-size: 10px;
    font-weight: 800;
    color: #0D1117;
    letter-spacing: 1px;
  }
  .inactive-ph { height: 16px; }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 5px; height: 5px; }
  ::-webkit-scrollbar-track { background: #05080D; }
  ::-webkit-scrollbar-thumb { background: #2A4A6B; border-radius: 4px; }
  ::-webkit-scrollbar-thumb:hover { background: #F5A623; }

  /* ── Streamlit overrides ── */
  #MainMenu { visibility: hidden; }
  footer    { visibility: hidden; }
  header    { visibility: hidden; }

  /* ── HR ── */
  hr {
    margin: 8px 0;
    border: none;
    height: 1px;
    background: linear-gradient(90deg, #F5A623, transparent, #20B2AA);
    opacity: 0.3;
  }
            
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# FIX-1 · TIMESTAMP FIXADO — atualiza via JS a cada segundo
# ══════════════════════════════════════════════════════════════════
from datetime import datetime as _dt
_now = _dt.now()
st.markdown(f"""
<div id="ts-badge">
  <div id="ts-dot"></div>
  <div>
    <div id="ts-label">GERADO EM</div>
    <div id="ts-time">{_now.strftime('%H:%M:%S')}</div>
    <div id="ts-date">{_now.strftime('%d/%m/%Y')}</div>
  </div>
</div>
<script>
(function() {{
  function pad(n) {{ return n < 10 ? '0' + n : n; }}
  function tick() {{
    var d = new Date();
    var el_t = document.getElementById('ts-time');
    var el_d = document.getElementById('ts-date');
    if (el_t) el_t.textContent = pad(d.getHours())+':'+pad(d.getMinutes())+':'+pad(d.getSeconds());
    if (el_d) el_d.textContent = pad(d.getDate())+'/'+(pad(d.getMonth()+1))+'/'+d.getFullYear();
  }}
  tick();
  setInterval(tick, 1000);
}})();
</script>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# 3. LOAD & PREPARE DATA
# ══════════════════════════════════════════════════════════════════
def _find_excel() -> pd.DataFrame:
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "base_case_turismo.xlsx"),
        "/mnt/user-data/uploads/base_case_turismo.xlsx",
        "base_case_turismo.xlsx",
    ]
    for p in candidates:
        if os.path.exists(p):
            return pd.read_excel(p)
    raise FileNotFoundError("base_case_turismo.xlsx não encontrado.")

@st.cache_data
def load_data() -> pd.DataFrame:
    try:
        df = _find_excel()
    except (FileNotFoundError, RuntimeError) as exc:
        st.error(f"❌ {exc}")
        st.stop()
        raise
    df.columns = ["Mes","Estado","Cidade","Tipo","Receita","Clientes","Ocupacao","Avaliacao"]
    MESES_ORDER = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    MESES_PT    = {"January":"Jan","February":"Fev","March":"Mar","April":"Abr",
                   "May":"Mai","June":"Jun","July":"Jul","August":"Ago",
                   "September":"Set","October":"Out","November":"Nov","December":"Dez"}
    ESTADOS_FULL = {"CE":"Ceará","PE":"Pernambuco","PI":"Piauí","RN":"Rio Grande do Norte"}
    df["Mes_Ordem"]       = df["Mes"].map({m:i for i,m in enumerate(MESES_ORDER)})
    df["Mes_PT"]          = df["Mes"].map(MESES_PT)
    df["Estado_Full"]     = df["Estado"].map(ESTADOS_FULL)
    df["Rev_por_Cliente"] = df["Receita"] / df["Clientes"].replace(0, np.nan)
    return df

df_raw: pd.DataFrame = load_data()
if df_raw.empty:
    st.error("❌ Sem dados.")
    st.stop()

MESES_PT_LIST  = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
MESES_EN_LIST  = ["January","February","March","April","May","June",
                  "July","August","September","October","November","December"]
MESES_FULL_MAP = {"January":"Janeiro","February":"Fevereiro","March":"Março","April":"Abril",
                  "May":"Maio","June":"Junho","July":"Julho","August":"Agosto",
                  "September":"Setembro","October":"Outubro","November":"Novembro","December":"Dezembro"}
ESTADOS_FULL   = {"CE":"Ceará","PE":"Pernambuco","PI":"Piauí","RN":"Rio Grande do Norte"}

# ══════════════════════════════════════════════════════════════════
# 4. HELPERS
# ══════════════════════════════════════════════════════════════════
def fmt_brl(v, decimals=0):
    if pd.isna(v): return "R$ 0"
    if v >= 1_000_000: return f"R$ {v/1_000_000:.{decimals}f}M"
    if v >= 1_000:     return f"R$ {v/1_000:.0f}K"
    return f"R$ {v:,.{decimals}f}"

def hex2rgba(h, a=0.15):
    h = h.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{a})"

def base_layout(**kw: Any) -> dict[str, Any]:
    layout: dict[str, Any] = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=PLOT_BG,          # ← área do gráfico tem fundo próprio
        font=dict(family="Inter, sans-serif", color=TEXT_P, size=11),
        margin=dict(l=14, r=14, t=46, b=14),
        legend=dict(
            bgcolor=f"rgba(13,26,40,0.85)", bordercolor=BORDER, borderwidth=1,
            font=dict(color=TEXT_P, size=10),
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
        ),
        hoverlabel=dict(bgcolor=PANEL, font_color=TEXT_H, bordercolor=BORDER, font_size=12),
        xaxis=dict(showgrid=False, zeroline=False, color=TEXT_P,
                   tickfont=dict(color=TEXT_P, size=10), linecolor=BORDER),
        yaxis=dict(showgrid=True, gridcolor=GRID, gridwidth=1, zeroline=False,
                   color=TEXT_P, tickfont=dict(color=TEXT_P, size=10)),
        modebar=dict(remove=[], bgcolor="rgba(13,26,40,0.9)",
                     color=TEXT_D, activecolor=GOLD),
    )
    layout.update(kw)
    return layout

def kpi_html(icon, label, value, sub, color, delta_txt="", delta_type="neutral"):
    cls = {"up":"kpi-delta-up","down":"kpi-delta-down","neutral":"kpi-delta-neutral"}.get(delta_type,"kpi-delta-neutral")
    delta_html = f'<div class="{cls}">{delta_txt}</div>' if delta_txt else ""
    return f"""
    <div class="kpi-card" style="--card-color:{color}; border-top:3px solid {color};">
      <span class="kpi-icon">{icon}</span>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value" style="color:{color};">{value}</div>
      <div class="kpi-sub">{sub}</div>
      {delta_html}
    </div>"""

def section(title, pill=""):
    pill_html = f'<span class="section-pill">{pill}</span>' if pill else ""
    st.markdown(f"""
    <div class="section-header">
      <p class="section-title">{title}</p>
      {pill_html}
    </div>""", unsafe_allow_html=True)

def insight(icon, html_text):
    st.markdown(f"""
    <div class="insight-box">
      <span class="insight-icon">{icon}</span>
      <span class="insight-text">{html_text}</span>
    </div>""", unsafe_allow_html=True)

def chart_wrap(title, subtitle):
    """Abre um card de gráfico com header limpo (sem hint de exportação)."""
    st.markdown(f"""
    <div class="chart-card">
      <div class="chart-title">{title}</div>
      <div class="chart-subtitle">{subtitle}</div>
    </div>""", unsafe_allow_html=True)

def render_chart_with_validation(df, required, func, title, msg, min_records=1):
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.info(f"📊 **{title}** — colunas ausentes: {', '.join(missing)}\n\n{msg}")
        return False
    if len(df) < min_records:
        st.info(f"📊 **{title}** — registros insuficientes ({len(df)}/{min_records}).\n\n{msg}")
        return False
    func()
    return True

# ── Semáforos ──────────────────────────────────────────────────
def semaforo_ocupacao(v):
    if v >= 75: return GREEN, "▲ Excelente", "up"
    if v >= 60: return AMBER, "● Atenção",   "neutral"
    return CORAL, "▼ Crítico", "down"

def semaforo_avaliacao(v):
    if v >= 4.5: return GREEN, "▲ Excelente",     "up"
    if v >= 3.5: return AMBER, "● Satisfatório",  "neutral"
    return CORAL, "▼ Insatisfatório", "down"

def semaforo_ticket(v):
    if v >= 250: return GREEN, "▲ Premium", "up"
    if v >= 150: return AMBER, "● Padrão",  "neutral"
    return CORAL, "▼ Baixo", "down"

def semaforo_variacao(pct):
    if pct > 5:  return GREEN, f"▲ +{pct:.1f}%", "up"
    if pct < -5: return CORAL, f"▼ {pct:.1f}%",  "down"
    return AMBER, f"● {pct:+.1f}%", "neutral"

def render_footer(df):
    """Renderiza o footer padrão do dashboard"""
    st.markdown(f"""
    <div style="margin-top: 36px; padding: 16px 24px; border-top: 1px solid {BORDER};
         text-align: center; color: {TEXT_D}; font-size: 11px; letter-spacing: 0.06em;">
      🌊 <strong style="color: {TEXT_P}">Turismo Nordeste · Dashboard Estratégico</strong>
      &nbsp;·&nbsp; Streamlit + Plotly
      &nbsp;·&nbsp; <strong style="color: {GOLD}">{len(df):,}</strong> registros analisados
      &nbsp;·&nbsp; v5.0
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# 5. SIDEBAR  — FILTROS (expandida por default, toggle nativo)
# ══════════════════════════════════════════════════════════════════
# FIX-2: sidebar usa o colapso nativo do Streamlit (seta ◀►).
# O initial_sidebar_state="expanded" já garante abertura por default.
# Removida a lógica de session_state que causava o bug de não aparecer.

with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding:14px 0 16px;">
      <span style="font-size:42px;">🌊</span>
      <div style="font-family:'Syne',sans-serif; font-size:20px; font-weight:800;
           background:linear-gradient(90deg,#F0F4FF,#E9A320);
           -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:5px 0 2px;">
        Turismo Nordeste
      </div>
      <div style="font-size:10px; color:#65a4e6; letter-spacing:0.14em; font-family:'Inter',sans-serif;">
        PAINEL DE FILTROS
      </div>
    </div>
    <hr/>
    """, unsafe_allow_html=True)

    # ── Tipo de Empreendimento ──────────────────────────────────
    st.markdown('<span class="filter-title">🏨 Tipo de Empreendimento</span>', unsafe_allow_html=True)
    todos_tipos = sorted(df_raw["Tipo"].unique())
    if "tipos_selecionados" not in st.session_state:
        st.session_state.tipos_selecionados = todos_tipos.copy()

    def toggle_tipo(tipo):
        sel = st.session_state.tipos_selecionados
        if tipo in sel:
            if len(sel) > 1:
                sel.remove(tipo)
        else:
            sel.append(tipo)
        st.rerun()

    tipo_info = {"Hotel":"🏨\nHotel","Pousada":"🏡\nPousada","Agencia":"✈️\nAgência"}
    col_t1, col_t2, col_t3 = st.columns(3)
    for col, tipo in zip([col_t1, col_t2, col_t3], ["Hotel","Pousada","Agencia"]):
        ativo = tipo in st.session_state.tipos_selecionados
        with col:
            if st.button(tipo_info.get(tipo, tipo), key=f"btn_{tipo}", use_container_width=True):
                toggle_tipo(tipo)
            if ativo:
                st.markdown('<div class="active-badge">✓ ATIVO</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="inactive-ph"></div>', unsafe_allow_html=True)

    # Destaca botões ativos via CSS dinâmico
    btn_css = ""
    for tipo in ["Hotel","Pousada","Agencia"]:
        if tipo in st.session_state.tipos_selecionados:
            btn_css += f"""
            div[data-testid="stSidebar"] button[kind="secondary"][data-testid="baseButton-secondary"]:has(> p:contains("{tipo_info.get(tipo,'').split(chr(10))[1]}")) {{
                background: linear-gradient(135deg,{GOLD},{AMBER}) !important;
                color: #0D1117 !important; border-color: {GOLD} !important;
            }}"""
    if btn_css:
        st.markdown(f"<style>{btn_css}</style>", unsafe_allow_html=True)

    sel_tipos = st.session_state.tipos_selecionados
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── Período de Análise ───────────────────────────────────────
    st.markdown('<span class="filter-title">📅 Período de Análise</span>', unsafe_allow_html=True)
    meses_dict = {pt: en for pt, en in zip(MESES_PT_LIST, MESES_EN_LIST)}

    if "tamanho_janela" not in st.session_state: st.session_state.tamanho_janela = 3
    if "posicao_janela" not in st.session_state: st.session_state.posicao_janela = 0

    cl, cr = st.columns([0.38, 0.62])
    with cl:
        st.markdown("**📏 Janela**")
        opcoes = list(range(1, 13))
        idx = opcoes.index(st.session_state.tamanho_janela) if st.session_state.tamanho_janela in opcoes else 2
        tam = st.selectbox("", options=opcoes, index=idx, label_visibility="collapsed")
        if tam != st.session_state.tamanho_janela:
            st.session_state.tamanho_janela = tam
            max_pos = 12 - tam
            if st.session_state.posicao_janela > max_pos:
                st.session_state.posicao_janela = max_pos
            st.rerun()
    with cr:
        st.markdown("**📍 Início**")
        max_pos = 12 - st.session_state.tamanho_janela
        st.session_state.posicao_janela = max(0, min(st.session_state.posicao_janela, max_pos))
        pos = st.slider("", 0, max_pos, st.session_state.posicao_janela,
                        label_visibility="collapsed", key="slider_pos")
        if pos != st.session_state.posicao_janela:
            st.session_state.posicao_janela = pos
            st.rerun()

    idx_ini = st.session_state.posicao_janela
    idx_fim = idx_ini + st.session_state.tamanho_janela - 1
    sel_meses = [meses_dict[MESES_PT_LIST[i]] for i in range(idx_ini, idx_fim + 1)]
    periodo_desc = f"{MESES_PT_LIST[idx_ini]} → {MESES_PT_LIST[idx_fim]} ({st.session_state.tamanho_janela} mês{'es' if st.session_state.tamanho_janela>1 else ''})"

    html_m = '<div style="display:flex; gap:3px; margin:8px 0 3px; flex-wrap:wrap;">'
    for i, m in enumerate(MESES_PT_LIST):
        ativo = idx_ini <= i <= idx_fim
        bg    = f"linear-gradient(180deg,{GOLD},{AMBER})" if ativo else BORDER
        cor   = "#1A1A1A" if ativo else TEXT_D
        fw    = "800" if ativo else "500"
        html_m += f'<div style="flex:1;min-width:26px;text-align:center;padding:5px 1px;background:{bg};border-radius:6px;color:{cor};font-size:10px;font-weight:{fw};">{m}</div>'
    html_m += "</div>"
    st.markdown(html_m, unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center;font-size:11px;color:{TEXT_D};margin-bottom:4px;">{periodo_desc}</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── Localização ─────────────────────────────────────────────
    st.markdown('<span class="filter-title">📍 Localização</span>', unsafe_allow_html=True)
    cidades_por_estado = {e: sorted(df_raw[df_raw["Estado"]==e]["Cidade"].unique())
                          for e in df_raw["Estado"].unique()}

    if "estados_sel" not in st.session_state:
        st.session_state.estados_sel = {e: True for e in cidades_por_estado}
    if "cidades_sel" not in st.session_state:
        st.session_state.cidades_sel = {e: {c: True for c in cs}
                                        for e, cs in cidades_por_estado.items()}

    estados_lista = list(cidades_por_estado.keys())

    def render_estado(col, estado, cidades):
        with col:
            chk, txt = st.columns([0.13, 0.87], gap="small")
            with chk:
                val = st.checkbox("", value=st.session_state.estados_sel.get(estado, True),
                                  key=f"est_{estado}", label_visibility="collapsed")
            with txt:
                st.markdown(f"""
                <div style="margin-top:2px;">
                  <span style="font-size:11px;font-weight:700;color:{GOLD};">
                    🏛️ {estado} · {ESTADOS_FULL.get(estado,'')}
                  </span><br>
                  <span style="font-size:10px;color:{TEXT_D};">{len(cidades)} cidade(s)</span>
                </div>""", unsafe_allow_html=True)
            if val != st.session_state.estados_sel.get(estado, True):
                st.session_state.estados_sel[estado] = val
                for c in cidades:
                    st.session_state.cidades_sel[estado][c] = val
                st.rerun()
            if val:
                with st.expander(f"🗺️ {len(cidades)} cidades", expanded=False):
                    for cidade in cidades:
                        cv = st.checkbox(cidade,
                                         value=st.session_state.cidades_sel[estado].get(cidade, True),
                                         key=f"cid_{estado}_{cidade}")
                        if cv != st.session_state.cidades_sel[estado].get(cidade, True):
                            st.session_state.cidades_sel[estado][cidade] = cv
                            st.session_state.estados_sel[estado] = all(
                                st.session_state.cidades_sel[estado].values())
                            st.rerun()
            st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

    pairs = [(estados_lista[i], estados_lista[i+1] if i+1 < len(estados_lista) else None)
             for i in range(0, len(estados_lista), 2)]
    for e1, e2 in pairs:
        ca, cb = st.columns(2)
        render_estado(ca, e1, cidades_por_estado[e1])
        if e2:
            render_estado(cb, e2, cidades_por_estado[e2])

    sel_estados = [e for e, v in st.session_state.estados_sel.items() if v]
    sel_cidades = [c for e, cs in st.session_state.cidades_sel.items()
                   for c, v in cs.items() if v]

    # ── Resumo ───────────────────────────────────────────────────
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown('<span class="filter-title">🔍 Filtros Ativos</span>', unsafe_allow_html=True)
    total_cidades_raw = sum(len(v) for v in cidades_por_estado.values())
    st.markdown(f"""
    <div class="resumo-text">
      📅 Período: <strong>{periodo_desc}</strong><br>
      🏨 Tipos: <strong>{len(sel_tipos)}</strong>/{len(todos_tipos)}<br>
      📍 Estados: <strong>{len(sel_estados)}</strong>/{len(cidades_por_estado)}<br>
      🏙️ Cidades: <strong>{len(sel_cidades)}</strong>/{total_cidades_raw}
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# 6. FILTRAGEM
# ══════════════════════════════════════════════════════════════════
df = df_raw.copy()
if sel_meses:   df = df[df["Mes"].isin(sel_meses)]
if sel_tipos:   df = df[df["Tipo"].isin(sel_tipos)]
if sel_estados: df = df[df["Estado"].isin(sel_estados)]
if sel_cidades: df = df[df["Cidade"].isin(sel_cidades)]

if df.empty:
    st.warning("⚠️ Nenhum dado para os filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

# ══════════════════════════════════════════════════════════════════
# 7. ABAS PRINCIPAIS
# ══════════════════════════════════════════════════════════════════

tab_dash, tab_graficos, tab_filtros = st.tabs([
    "📊  Dashboard",
    "📖  Como Interpretar os Gráficos",
    "🔍  Como Usar os Filtros",
])

# ══════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════════
with tab_dash:

        # Botão imprimir / PDF
    n_meses    = df["Mes"].nunique()
    n_estados  = df["Estado"].nunique()
    n_cidades  = df["Cidade"].nunique()
    n_registros = len(df)

    col_header, col_print = st.columns([0.85, 0.15])
    with col_header:
        st.markdown(f"""
        <div class="top-bar">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;">
            <div style="display:flex;align-items:center;gap:14px;">
              <span style="font-size:38px;">🌊</span>
              <div>
                <div class="top-bar-title">Turismo Nordeste</div>
                <div class="top-bar-sub">DASHBOARD ESTRATÉGICO · SETOR DE HOSPITALIDADE · NORDESTE</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div class="stats-info">
                <span style="color:#F5A623;font-weight:700;">{n_meses}</span> meses ·
                <span style="color:#F5A623;font-weight:700;">{n_estados}</span> estado(s) ·
                <span style="color:#F5A623;font-weight:700;">{n_cidades}</span> cidade(s)
              </div>
              <div style="margin-top:5px;">
                <span class="stats-highlight">📈 {n_registros:,} registros filtrados</span>
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_print:
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        
        # Botão de impressão usando HTML/JavaScript diretamente
        st.markdown("""
        <div style="text-align: right;">
            <button id="print-btn" style="
                background: linear-gradient(135deg, #F5A623, #E69500);
                border: none;
                border-radius: 10px;
                padding: 8px 16px;
                color: #0D1117;
                font-weight: 700;
                font-size: 14px;
                cursor: pointer;
                transition: all 0.2s ease;
                font-family: 'Inter', sans-serif;
            ">
                🖨️ Imprimir / PDF
            </button>
        </div>
        <script>
            document.getElementById('print-btn').addEventListener('click', function() {
                window.print();
            });
        </script>
        """, unsafe_allow_html=True)

    # ── KPIs ─────────────────────────────────────────────────────
    section("Visão Executiva", "KPIs ESTRATÉGICOS")

    receita_tot  = df["Receita"].sum()
    clientes_tot = df["Clientes"].sum()
    ocup_med     = df["Ocupacao"].mean()
    aval_med     = df["Avaliacao"].mean()
    ticket_med   = df["Rev_por_Cliente"].mean()

    df_base = df_raw.copy()
    if sel_tipos: df_base = df_base[df_base["Tipo"].isin(sel_tipos)]
    ocup_base   = df_base["Ocupacao"].mean()
    aval_base   = df_base["Avaliacao"].mean()
    ticket_base = df_base["Rev_por_Cliente"].mean()

    receita_med_fil  = df.groupby("Mes")["Receita"].sum().mean()
    receita_med_base = df_base[df_base["Mes"].isin(sel_meses)].groupby("Mes")["Receita"].sum().mean()
    if pd.isna(receita_med_base) or receita_med_base == 0:
        receita_med_base = df_base.groupby("Mes")["Receita"].sum().mean()

    pct_receita  = receita_tot / df_raw["Receita"].sum() * 100
    delta_ocup   = ocup_med  - ocup_base
    delta_aval   = aval_med  - aval_base
    delta_ticket = (ticket_med - ticket_base) / ticket_base * 100 if ticket_base else 0

    ocup_color,   _, ocup_dt   = semaforo_ocupacao(ocup_med)
    aval_color,   _, aval_dt   = semaforo_avaliacao(aval_med)
    ticket_color, _, ticket_dt = semaforo_ticket(ticket_med)
    rec_color,    _, rec_dt    = semaforo_variacao(
        (receita_med_fil - receita_med_base) / receita_med_base * 100
        if receita_med_base and not pd.isna(receita_med_base) else 0)

    ocup_delta_txt   = f"{'▲' if delta_ocup>=0 else '▼'} {abs(delta_ocup):.1f}pp vs geral"
    aval_delta_txt   = f"{'▲' if delta_aval>=0 else '▼'} {abs(delta_aval):.2f} vs meta 4.0"
    ticket_delta_txt = f"{'▲' if delta_ticket>=0 else '▼'} {abs(delta_ticket):.1f}% vs geral"
    rec_med_msg      = f"{'▲' if (receita_med_fil-receita_med_base)>=0 else '▼'} vs baseline"

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1:
        st.markdown(kpi_html("💰","Receita Total",fmt_brl(receita_tot,2),
                             f"{n_meses} meses filtrados",GOLD,
                             f"{pct_receita:.0f}% do total geral","up" if pct_receita>50 else "neutral"),
                    unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_html("👥","Clientes",f"{clientes_tot:,}",
                             f"ticket R$ {ticket_med:,.0f}",TEAL,"","neutral"),
                    unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_html("🏨","Ocupação Média",f"{ocup_med:.1f}%",
                             f"geral: {ocup_base:.1f}%",ocup_color,
                             ocup_delta_txt,"up" if delta_ocup>=0 else "down"),
                    unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_html("⭐","Avaliação",f"{aval_med:.2f}/5",
                             "meta: 4.0",aval_color,
                             aval_delta_txt,"up" if delta_aval>=0 else "down"),
                    unsafe_allow_html=True)
    with c5:
        st.markdown(kpi_html("📈","Ticket Médio",fmt_brl(ticket_med),
                             f"geral: {fmt_brl(ticket_base)}",ticket_color,
                             ticket_delta_txt,"up" if delta_ticket>=0 else "down"),
                    unsafe_allow_html=True)
    with c6:
        st.markdown(kpi_html("📅","Receita Média/Mês",fmt_brl(receita_med_fil,1),
                             f"{n_meses} meses no filtro",rec_color,
                             rec_med_msg,rec_dt),
                    unsafe_allow_html=True)

    # ── Tendências & Composição ───────────────────────────────────
    section("Tendências & Composição", "ANÁLISE TEMPORAL")
    col_a, col_b = st.columns([3,1])

    with col_a:
        def render_linhas():
            st.markdown("""<div class="chart-card">
              <div class="chart-title">📈 Evolução da Receita Mensal</div>
              <div class="chart-subtitle">Por tipo de empreendimento + total combinado</div>
            </div>""", unsafe_allow_html=True)
            g = df.groupby(["Mes_Ordem","Mes_PT","Tipo"])["Receita"].sum().reset_index().sort_values("Mes_Ordem")
            tot = df.groupby(["Mes_Ordem","Mes_PT"])["Receita"].sum().reset_index().sort_values("Mes_Ordem")
            fig = go.Figure()
            for tipo in sorted(g["Tipo"].unique()):
                t = g[g["Tipo"]==tipo]
                c = TYPE_COLORS.get(tipo, GOLD)
                fig.add_trace(go.Scatter(
                    x=t["Mes_PT"], y=t["Receita"], name=tipo, mode="lines+markers",
                    line=dict(color=c, width=2.5), marker=dict(size=6,color=c),
                    fill="tozeroy", fillcolor=hex2rgba(c, 0.08),
                    hovertemplate=f"<b>{tipo}</b><br>%{{x}}: R$ %{{y:,.0f}}<extra></extra>",
                ))
            fig.add_trace(go.Scatter(
                x=tot["Mes_PT"], y=tot["Receita"], name="Total",
                mode="lines", line=dict(color=TEXT_H, width=1.5, dash="dot"),
                hovertemplate="<b>Total</b><br>%{x}: R$ %{y:,.0f}<extra></extra>",
            ))
            fig.update_layout(base_layout(height=320))
            st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)

        render_chart_with_validation(df, ["Mes_Ordem","Mes_PT","Tipo","Receita"],
                                      render_linhas, "Evolução da Receita",
                                      "Selecione ao menos 1 mês e 1 tipo.")

    with col_b:
        def render_donut():
            st.markdown("""<div class="chart-card">
              <div class="chart-title">🍩 Mix por Tipo</div>
              <div class="chart-subtitle">Participação na receita total</div>
            </div>""", unsafe_allow_html=True)
            mix = df.groupby("Tipo")["Receita"].sum().reset_index()
            fig = go.Figure(go.Pie(
                labels=mix["Tipo"], values=mix["Receita"], hole=0.6,
                marker=dict(colors=[TYPE_COLORS.get(t, GOLD) for t in mix["Tipo"]],
                            line=dict(color=PAGE_BG, width=2)),
                textinfo="label+percent", 
                textfont=dict(color=TEXT_H, size=10),
                textposition="auto",
                hovertemplate="<b>%{label}</b><br>R$ %{value:,.0f}<br>%{percent}<extra></extra>",
                showlegend=True
            ))
            fig.add_annotation(
                text=f"<b>{fmt_brl(mix['Receita'].sum(),1)}</b>",
                x=0.5, y=0.5, showarrow=False, align="center",
                font=dict(color=TEXT_H, size=14),
            )
            fig.update_layout(
                base_layout(),
                height=380,
                margin=dict(l=10, r=10, t=30, b=60),
                legend=dict(
                orientation="h",
                y=-0.15,
                x=0.5,
                xanchor="center",
                yanchor="top",
                bgcolor="rgba(0,0,0,0)",
                font=dict(color=TEXT_P, size=11)
                ),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)

        render_chart_with_validation(df, ["Tipo", "Receita"], render_donut,
                                      "Mix por Tipo", "Selecione ao menos 1 tipo.")

    # ── Desempenho Regional ───────────────────────────────────────
    section("Desempenho Regional", "ESTADOS & SAZONALIDADE")
    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("""<div class="chart-card">
          <div class="chart-title">🗺️ Desempenho por Estado</div>
          <div class="chart-subtitle">Receita (barra) · Clientes (◆)</div>
        </div>""", unsafe_allow_html=True)
        est = df.groupby("Estado").agg(Receita=("Receita","sum"),Clientes=("Clientes","sum")).reset_index()
        est = est.sort_values("Receita", ascending=True)
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            y=est["Estado"], x=est["Receita"], orientation="h", name="Receita",
            marker=dict(color=[STATE_COLORS.get(e,GOLD) for e in est["Estado"]],
                        line=dict(color="rgba(0,0,0,0)")),
            hovertemplate="<b>%{y}</b><br>Receita: R$ %{x:,.0f}<extra></extra>",
            text=[fmt_brl(v) for v in est["Receita"]], textposition="inside",
            textfont=dict(color=TEXT_H, size=10),
        ))
        fig3.add_trace(go.Scatter(
            y=est["Estado"], x=est["Clientes"], mode="markers", name="Clientes",
            marker=dict(color=TEXT_H, size=11, symbol="diamond"),
            xaxis="x2",
            hovertemplate="<b>%{y}</b><br>Clientes: %{x:,}<extra></extra>",
        ))
        fig3.update_layout(base_layout(
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            xaxis2=dict(overlaying="x", side="top", showgrid=False, zeroline=False,
                        tickfont=dict(color=TEXT_D, size=9)),
            yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=11, color=TEXT_H)),
            height=320,
        ))
        st.plotly_chart(fig3, use_container_width=True, config=CHART_CONFIG)

    with col_d:
        st.markdown("""<div class="chart-card">
          <div class="chart-title">🌡️ Sazonalidade · Estado × Mês</div>
          <div class="chart-subtitle">Intensidade de receita por período e localidade</div>
        </div>""", unsafe_allow_html=True)
        heat = df.groupby(["Estado","Mes_PT"])["Receita"].sum().reset_index()
        ordem_full = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
        meses_pres = [m for m in ordem_full if m in heat["Mes_PT"].values]
        heat["Mes_Ord"] = heat["Mes_PT"].map({m:i for i,m in enumerate(ordem_full)})
        heat = heat.sort_values("Mes_Ord")
        pivot = heat.pivot(index="Estado", columns="Mes_PT", values="Receita")
        pivot = pivot.reindex(columns=meses_pres)
        colorscale = [[0.0,"rgba(10,22,40,0.9)"],[0.5,"rgba(0,177,170,0.6)"],[1.0,GOLD]]
        fig4 = go.Figure(go.Heatmap(
            z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
            colorscale=colorscale,
            hovertemplate="<b>%{y} · %{x}</b><br>R$ %{z:,.0f}<extra></extra>",
            showscale=True,
            colorbar=dict(thickness=10, len=0.85, tickfont=dict(color=TEXT_P, size=9),
                          bgcolor="rgba(0,0,0,0)", outlinecolor="rgba(0,0,0,0)"),
        ))
        fig4.update_layout(base_layout(
            xaxis=dict(showgrid=False, tickfont=dict(size=10, color=TEXT_P)),
            yaxis=dict(showgrid=False, tickfont=dict(size=11, color=TEXT_H)),
            plot_bgcolor="rgba(0,0,0,0)",
            height=320,
        ))
        st.plotly_chart(fig4, use_container_width=True, config=CHART_CONFIG)

    # ── Posicionamento Estratégico ─────────────────────────────────
    section("Posicionamento Estratégico", "MATRIZ & RANKING")
    col_e, col_f = st.columns([1,1])

    with col_e:
        def render_scatter():
            st.markdown("""<div class="chart-card">
              <div class="chart-title">🎯 Matriz Estratégica</div>
              <div class="chart-subtitle">Ocupação × Satisfação · tamanho = receita</div>
            </div>""", unsafe_allow_html=True)
            sc = df.groupby(["Cidade","Estado"]).agg(
                Ocupacao=("Ocupacao","mean"), Avaliacao=("Avaliacao","mean"),
                Receita=("Receita","sum"), Clientes=("Clientes","sum"),
            ).reset_index()
            fig5 = go.Figure()
            for estado in sc["Estado"].unique():
                s  = sc[sc["Estado"]==estado]
                c  = STATE_COLORS.get(estado, GOLD)
                mx = s["Receita"].max()
                fig5.add_trace(go.Scatter(
                    x=s["Ocupacao"], y=s["Avaliacao"],
                    mode="markers", name=estado,
                    marker=dict(color=c, size=[max(10,r/mx*40) for r in s["Receita"]],
                                opacity=0.85, line=dict(color=PAGE_BG, width=1.5)),
                    customdata=np.stack([s["Cidade"],s["Receita"],s["Clientes"]], axis=-1),
                    hovertemplate=(
                        "<b>%{customdata[0]}</b> · "+estado+"<br>"
                        "Ocupação: %{x:.1f}% · Avaliação: %{y:.2f}/5<br>"
                        "Receita: R$ %{customdata[1]:,.0f}<br>"
                        "Clientes: %{customdata[2]:,}<extra></extra>"
                    ),
                ))
            occ_med = sc["Ocupacao"].mean()
            aval_m  = sc["Avaliacao"].mean()
            fig5.add_hline(y=aval_m, line_dash="dot", line_color=BORDER_LIGHT, line_width=1.2)
            fig5.add_vline(x=occ_med, line_dash="dot", line_color=BORDER_LIGHT, line_width=1.2)
            x_lo,x_hi = sc["Ocupacao"].min(), sc["Ocupacao"].max()
            y_lo,y_hi = sc["Avaliacao"].min(), sc["Avaliacao"].max()
            quad_anns = [
                (x_lo+(occ_med-x_lo)*0.5, aval_m+(y_hi-aval_m)*0.6, "★ Alto Potencial", GREEN),
                (occ_med+(x_hi-occ_med)*0.5, aval_m+(y_hi-aval_m)*0.6, "🏆 Destaque Total", GOLD),
                (x_lo+(occ_med-x_lo)*0.5, y_lo+(aval_m-y_lo)*0.35, "⚠ Atenção", CORAL),
                (occ_med+(x_hi-occ_med)*0.5, y_lo+(aval_m-y_lo)*0.35, "📊 Operacional", BLUE),
            ]
            annotations = [
                dict(x=qx,y=qy,text=qt,showarrow=False,
                     font=dict(color=qc,size=9,family="Inter"),
                     bgcolor=hex2rgba(qc,0.08),bordercolor=qc,borderwidth=1,borderpad=4)
                for qx,qy,qt,qc in quad_anns
            ]
            fig5.update_layout(base_layout(
                xaxis=dict(title="Taxa de Ocupação (%)", showgrid=True, gridcolor=GRID),
                yaxis=dict(title="Avaliação Média (1-5)", showgrid=True, gridcolor=GRID),
                annotations=annotations, height=360,
            ))
            st.plotly_chart(fig5, use_container_width=True, config=CHART_CONFIG)

        render_chart_with_validation(df, ["Cidade","Estado","Ocupacao","Avaliacao","Receita"],
                                      render_scatter, "Matriz Estratégica",
                                      "Selecione ao menos 1 cidade.", min_records=2)

    with col_f:
        def render_ranking():
            st.markdown("""<div class="chart-card">
              <div class="chart-title">🏅 Ranking de Cidades</div>
              <div class="chart-subtitle">Top 12 por receita acumulada</div>
            </div>""", unsafe_allow_html=True)
            rank = df.groupby("Cidade").agg(Receita=("Receita","sum")).reset_index()
            rank = rank.sort_values("Receita",ascending=False).head(12).sort_values("Receita",ascending=True)
            n    = len(rank)
            clrs = [GOLD if i==n-1 else (TEAL if i>=n-4 else BLUE) for i in range(n)]
            fig6 = go.Figure(go.Bar(
                y=rank["Cidade"], x=rank["Receita"], orientation="h",
                marker=dict(color=clrs, line=dict(color="rgba(0,0,0,0)")),
                text=[fmt_brl(v) for v in rank["Receita"]],
                textposition="inside", textfont=dict(color=TEXT_H, size=10),
                hovertemplate="<b>%{y}</b><br>R$ %{x:,.0f}<extra></extra>",
            ))
            fig6.update_layout(base_layout(
                xaxis=dict(showgrid=False, zeroline=False, visible=False),
                yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=10, color=TEXT_P)),
                height=360,
            ))
            st.plotly_chart(fig6, use_container_width=True, config=CHART_CONFIG)

        render_chart_with_validation(df, ["Cidade","Receita"], render_ranking,
                                      "Ranking de Cidades", "Selecione ao menos 1 cidade.", min_records=2)

    # ── Qualidade & Experiência ───────────────────────────────────
    section("Qualidade & Experiência", "SATISFAÇÃO · TICKET · PERFIL")
    col_g, col_h, col_i = st.columns(3)

    with col_g:
        st.markdown("""<div class="chart-card">
          <div class="chart-title">⭐ Satisfação por Estado & Tipo</div>
          <div class="chart-subtitle">Avaliação média · meta 4.0</div>
        </div>""", unsafe_allow_html=True)
        sat = df.groupby(["Estado","Tipo"])["Avaliacao"].mean().reset_index()
        fig7 = go.Figure()
        for tipo in sorted(sat["Tipo"].unique()):
            t = sat[sat["Tipo"]==tipo]
            fig7.add_trace(go.Bar(
                x=t["Estado"], y=t["Avaliacao"], name=tipo,
                marker_color=TYPE_COLORS.get(tipo,GOLD),
                hovertemplate=f"<b>{tipo}</b><br>%{{x}}: %{{y:.2f}}/5.0<extra></extra>",
            ))
        fig7.add_hline(y=4.0, line_dash="dash", line_color=GREEN, line_width=1.5,
                       annotation_text="  meta 4.0",
                       annotation_font=dict(color=GREEN, size=10))
        fig7.update_layout(base_layout(
            barmode="group", bargap=0.25, bargroupgap=0.08,
            yaxis=dict(range=[0,5.4], showgrid=True, gridcolor=GRID, title="Avaliação (1-5)"),
            height=300,
        ))
        st.plotly_chart(fig7, use_container_width=True, config=CHART_CONFIG)

    with col_h:
        st.markdown("""<div class="chart-card">
          <div class="chart-title">💳 Ticket Médio (Boxplot)</div>
          <div class="chart-subtitle">Distribuição R$/cliente por tipo</div>
        </div>""", unsafe_allow_html=True)
        fig8 = go.Figure()
        for tipo in sorted(df["Tipo"].unique()):
            t = df[df["Tipo"]==tipo]["Rev_por_Cliente"].dropna()
            c = TYPE_COLORS.get(tipo, GOLD)
            fig8.add_trace(go.Box(
                y=t, name=tipo,
                marker_color=c, line=dict(color=c, width=1.5),
                fillcolor=hex2rgba(c, 0.12), boxmean="sd",
                hovertemplate=f"<b>{tipo}</b><br>R$ %{{y:,.2f}}<extra></extra>",
            ))
        fig8.update_layout(base_layout(
            yaxis=dict(title="R$ por cliente", showgrid=True, gridcolor=GRID),
            xaxis=dict(showgrid=False),
            height=300,
        ))
        st.plotly_chart(fig8, use_container_width=True, config=CHART_CONFIG)

    with col_i:
        st.markdown("""<div class="chart-card">
          <div class="chart-title">🕸️ Perfil Competitivo por Estado</div>
          <div class="chart-subtitle">Índice normalizado por dimensão</div>
        </div>""", unsafe_allow_html=True)
        metrics  = ["Receita","Clientes","Ocupacao","Avaliacao","Rev_por_Cliente"]
        cats     = ["Receita","Clientes","Ocupação","Avaliação","Ticket"]
        radar_df = df.groupby("Estado")[metrics].mean().reset_index()
        norm = radar_df.copy()
        for m in metrics:
            mn,mx = norm[m].min(), norm[m].max()
            norm[m] = (norm[m]-mn)/(mx-mn+1e-9)*100
        fig9 = go.Figure()
        for _, row in norm.iterrows():
            estado = row["Estado"]
            vals   = [row[m] for m in metrics]
            c      = STATE_COLORS.get(estado, GOLD)
            fig9.add_trace(go.Scatterpolar(
                r=vals+[vals[0]], theta=cats+[cats[0]], name=estado,
                fill="toself", fillcolor=hex2rgba(c, 0.12),
                line=dict(color=c, width=2),
                hovertemplate=f"<b>{estado}</b><br>%{{theta}}: %{{r:.1f}}<extra></extra>",
            ))
        fig9.update_layout(base_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0,100], gridcolor=GRID,
                                tickfont=dict(color=TEXT_D, size=7), linecolor=BORDER),
                angularaxis=dict(tickfont=dict(color=TEXT_H, size=10),
                                 linecolor=BORDER, gridcolor=GRID),
            ),
            legend=dict(orientation="h", y=-0.15),
            height=300, plot_bgcolor="rgba(0,0,0,0)",
        ))
        st.plotly_chart(fig9, use_container_width=True, config=CHART_CONFIG)

    # ── Composição Temporal ───────────────────────────────────────
    section("Composição Temporal", "ÁREA · KPIs MENSAIS")
    col_j, col_k = st.columns([2,1])

    with col_j:
        st.markdown("""<div class="chart-card">
          <div class="chart-title">📊 Composição de Receita por Estado</div>
          <div class="chart-subtitle">Área empilhada · participação mensal</div>
        </div>""", unsafe_allow_html=True)
        area = df.groupby(["Mes_Ordem","Mes_PT","Estado"])["Receita"].sum().reset_index().sort_values("Mes_Ordem")
        fig10 = go.Figure()
        for estado in sorted(area["Estado"].unique()):
            a = area[area["Estado"]==estado]
            c = STATE_COLORS.get(estado, GOLD)
            fig10.add_trace(go.Scatter(
                x=a["Mes_PT"], y=a["Receita"], name=estado,
                mode="lines", stackgroup="one",
                line=dict(color=c, width=1.5),
                fillcolor=hex2rgba(c, 0.45),
                hovertemplate=f"<b>{estado}</b><br>%{{x}}: R$ %{{y:,.0f}}<extra></extra>",
            ))
        fig10.update_layout(base_layout(height=300))
        st.plotly_chart(fig10, use_container_width=True, config=CHART_CONFIG)

    with col_k:
        st.markdown("""<div class="chart-card">
          <div class="chart-title">📉 KPIs Mensais</div>
          <div class="chart-subtitle">Receita · Ocupação · Avaliação</div>
        </div>""", unsafe_allow_html=True)
        mes_kpi = df.groupby(["Mes_Ordem","Mes_PT"]).agg(
            Receita=("Receita","sum"), Ocupacao=("Ocupacao","mean"), Avaliacao=("Avaliacao","mean"),
        ).reset_index().sort_values("Mes_Ordem")
        fig11 = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.07,
                              subplot_titles=["Receita","Ocupação %","Avaliação"])
        for col_n, metric, color, row in [
            ("Receita","Receita",GOLD,1),("Ocupacao","Ocupação",TEAL,2),("Avaliacao","Avaliação",VIOLET,3)
        ]:
            fig11.add_trace(go.Scatter(
                x=mes_kpi["Mes_PT"], y=mes_kpi[col_n], mode="lines+markers", name=metric,
                line=dict(color=color, width=2), marker=dict(size=5, color=color),
                fill="tozeroy", fillcolor=hex2rgba(color, 0.1),
                hovertemplate=f"<b>{metric}</b><br>%{{x}}: %{{y:,.1f}}<extra></extra>",
            ), row=row, col=1)
        fig11.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=PLOT_BG,
            font=dict(family="Inter", color=TEXT_P, size=9),
            margin=dict(l=10,r=10,t=44,b=10), showlegend=False, height=300,
            modebar=dict(remove=[]),
        )
        for i in [1,2,3]:
            fig11.update_xaxes(showgrid=False, zeroline=False, tickfont=dict(color=TEXT_P,size=8), row=i, col=1)
            fig11.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=TEXT_P,size=8), row=i, col=1)
        fig11.update_annotations(font=dict(color=TEXT_D, size=10))
        st.plotly_chart(fig11, use_container_width=True, config=CHART_CONFIG)

    # ── Insights ─────────────────────────────────────────────────
    section("Insights Estratégicos", "ANÁLISE AUTOMÁTICA")

    mes_top_en  = str(df.groupby("Mes")["Receita"].sum().idxmax())
    mes_bot_en  = str(df.groupby("Mes")["Receita"].sum().idxmin())
    mes_top_pt  = MESES_FULL_MAP.get(mes_top_en, mes_top_en)
    mes_bot_pt  = MESES_FULL_MAP.get(mes_bot_en, mes_bot_en)
    tipo_top      = str(df.groupby("Tipo")["Receita"].sum().idxmax())
    rec_tipo      = df.groupby("Tipo")["Receita"].sum()
    pct_top_ins   = rec_tipo[tipo_top] / rec_tipo.sum() * 100
    cidade_top    = str(df.groupby("Cidade")["Receita"].sum().idxmax())
    estado_ocup   = str(df.groupby("Estado")["Ocupacao"].mean().idxmax())
    ocup_max_v    = df.groupby("Estado")["Ocupacao"].mean().max()
    tipo_aval_ins = str(df.groupby("Tipo")["Avaliacao"].mean().idxmax())
    aval_max_v    = df.groupby("Tipo")["Avaliacao"].mean().max()
    abaixo_meta   = int((df.groupby(["Estado","Tipo"])["Avaliacao"].mean() < 4.0).sum())
    est_ticket_top = str(df.groupby("Estado")["Rev_por_Cliente"].mean().idxmax())
    ticket_top_v   = df.groupby("Estado")["Rev_por_Cliente"].mean().max()

    col_ins1, col_ins2 = st.columns(2)
    with col_ins1:
        insight("📅", f"<strong>{mes_top_pt}</strong> é o mês de maior receita — oportunidade de maximizar preços e ocupação. <strong>{mes_bot_pt}</strong> é o mais fraco: ideal para campanhas de marketing off-season.")
        insight("🏆", f"<strong>{tipo_top}</strong> lidera com <strong>{pct_top_ins:.1f}%</strong> do total filtrado. Concentração alta sugere dependência — diversificar pode reduzir risco operacional.")
        insight("📍", f"<strong>{cidade_top}</strong> é a cidade de maior receita no período. Priorize ações de expansão de capacidade e retenção de clientes nesta praça.")
    with col_ins2:
        insight("🏨", f"<strong>{estado_ocup}</strong> lidera em ocupação média: <strong>{ocup_max_v:.1f}%</strong>. Alta ocupação pode indicar necessidade de revisão tarifária (pricing dinâmico).")
        insight("⭐", f"<strong>{tipo_aval_ins}</strong> tem a melhor avaliação: <strong>{aval_max_v:.2f}/5.0</strong>. Há <strong>{abaixo_meta}</strong> combinação(ões) Estado/Tipo abaixo da meta 4.0 — pontos críticos de melhoria.")
        insight("💡", f"<strong>{est_ticket_top}</strong> possui o maior ticket médio: <strong>{fmt_brl(ticket_top_v)}/cliente</strong>. Use a Matriz Estratégica para identificar destinos com alta avaliação e baixa ocupação — candidatos a precificação premium.")

    # ── Tabela Gerencial ──────────────────────────────────────────
    section("Sumário por Estado × Tipo", "TABELA GERENCIAL")
    summary = df.groupby(["Estado","Tipo"]).agg(
        Receita=("Receita","sum"), Clientes=("Clientes","sum"),
        Ocupacao=("Ocupacao","mean"), Avaliacao=("Avaliacao","mean"),
        Ticket=("Rev_por_Cliente","mean"),
    ).reset_index().sort_values(["Estado","Tipo"])
    summary["Receita_fmt"]  = summary["Receita"].apply(fmt_brl)
    summary["Clientes_fmt"] = summary["Clientes"].apply(lambda x: f"{x:,}")
    summary["Ocup_fmt"]     = summary["Ocupacao"].apply(lambda x: f"{x:.1f}%")
    summary["Aval_fmt"]     = summary["Avaliacao"].apply(lambda x: f"{x:.2f}")
    summary["Tick_fmt"]     = summary["Ticket"].apply(fmt_brl)
    table = summary[["Estado","Tipo","Receita_fmt","Clientes_fmt","Ocup_fmt","Aval_fmt","Tick_fmt"]].copy()
    table.columns = ["Estado","Tipo","Receita Total","Clientes","Ocupação %","Avaliação","Ticket Médio"]
    st.dataframe(table, use_container_width=True, hide_index=True)

    # Footer
    render_footer(df)


# ══════════════════════════════════════════════════════════════════
# TAB 2 — GUIA DE GRÁFICOS (DESIGN MELHORADO)
# ══════════════════════════════════════════════════════════════════
with tab_graficos:
    # Cabeçalho estilizado
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0F1D2E 0%, #0B1320 100%); 
                border: 1px solid #2A4A6B; 
                border-bottom: 3px solid #F5A623; 
                border-radius: 20px; 
                padding: 24px 28px; 
                margin-bottom: 28px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.3);">
        <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap;">
            <span style="font-size: 48px;">📖</span>
            <div>
                <div style="font-family: 'Syne', sans-serif; font-size: 24px; font-weight: 800; color: #FFFFFF; margin-bottom: 8px;">
                    Como Interpretar Cada Gráfico
                </div>
                <div style="color: #CBD5E1; font-size: 14px; line-height: 1.6;">
                    Esta página explica a <strong style="color: #F5A623;">lógica de leitura</strong>, o <strong style="color: #F5A623;">que cada elemento visual representa</strong>
                    e <strong style="color: #F5A623;">quais perguntas estratégicas</strong> cada gráfico foi desenhado para responder.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    def guide_card_enhanced(icon, title, subtitle, body_html, questions):
        q_items = "".join(f'<li><span class="q-marker">❓</span> {q}</li>' for q in questions)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0F1D2E 0%, #0D1828 100%);
                    border: 1px solid #2A4A6B;
                    border-radius: 20px;
                    padding: 0;
                    margin-bottom: 20px;
                    transition: all 0.3s ease;
                    overflow: hidden;">
            <div style="background: linear-gradient(90deg, #F5A623 0%, #E69500 100%);
                        padding: 12px 20px;
                        display: flex;
                        align-items: center;
                        gap: 12px;">
                <span style="font-size: 28px;">{icon}</span>
                <div>
                    <div style="font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 800; color: #0D1117;">
                        {title}
                    </div>
                    <div style="font-size: 11px; color: #0D1117; opacity: 0.8; margin-top: 2px;">
                        {subtitle}
                    </div>
                </div>
            </div>
            <div style="padding: 20px;">
                <div style="font-family: 'Inter', sans-serif; font-size: 13px; color: #CBD5E1; line-height: 1.7; margin-bottom: 20px;">
                    {body_html}
                </div>
                <div style="background: rgba(245,166,35,0.08); border-left: 3px solid #F5A623; border-radius: 12px; padding: 14px 18px; margin-top: 8px;">
                    <div style="font-family: 'Syne', sans-serif; font-size: 11px; font-weight: 700; color: #F5A623; letter-spacing: 0.08em; margin-bottom: 10px;">
                        📌 PERGUNTAS QUE ESTE GRÁFICO RESPONDE
                    </div>
                    <ul style="margin: 0; padding-left: 0; list-style: none;">
                        {q_items}
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Layout em grid para os cards de gráficos
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 20px;">
    """, unsafe_allow_html=True)
    
    # KPIs
    guide_card_enhanced(
        "💰", "Cards de KPI", "VISÃO EXECUTIVA",
        """Os KPIs (Indicadores-chave de desempenho) mostram os números mais importantes do negócio em tempo real.
        <br><br>
        <span class="label" style="background: rgba(245,166,35,0.15);">SEMÁFORO</span>
        <span style="color:#2ECC71;">🟢 Verde</span> = Excelente · 
        <span style="color:#FBB13C;">🟡 Amarelo</span> = Atenção · 
        <span style="color:#FF6B6B;">🔴 Vermelho</span> = Crítico
        <br><br>
        <strong>💡 Dica:</strong> Passe o mouse sobre cada card para ver mais detalhes.""",
        [
            "O desempenho atual está acima ou abaixo da meta?",
            "Qual indicador precisa de atenção imediata?",
            "Há variação significativa em relação ao período anterior?"
        ]
    )
    
    # Evolução da Receita
    guide_card_enhanced(
        "📈", "Evolução da Receita Mensal", "SÉRIE TEMPORAL",
        """Cada linha colorida representa um <strong>tipo de empreendimento</strong>. A linha pontilhada mostra o <strong>total</strong>.
        <br><br>
        <strong>🔍 Padrões a observar:</strong><br>
        • Picos simultâneos → sazonalidade estrutural<br>
        • Divergência entre tipos → sensibilidade diferente à sazonalidade<br>
        • Áreas preenchidas → magnitude relativa entre segmentos""",
        [
            "Qual tipo de empreendimento lidera o crescimento?",
            "Há meses de queda generalizada ou específica?",
            "Como o padrão muda ao filtrar por estado?"
        ]
    )
    
    # Mix por Tipo
    guide_card_enhanced(
        "🍩", "Mix por Tipo (Donut)", "COMPOSIÇÃO DA RECEITA",
        """O gráfico de rosca mostra a <strong>participação percentual</strong> de cada tipo na receita total.
        <br><br>
        <strong>⚖️ Interpretação:</strong><br>
        • Mix equilibrado (~33% cada) → resiliência e diversificação<br>
        • Domínio de um segmento (>50%) → risco de concentração<br>
        • O centro exibe o valor total da receita no período.""",
        [
            "A receita está concentrada em um único tipo?",
            "Como o mix muda em alta vs. baixa temporada?",
            "Há um tipo ganhando participação ao longo do tempo?"
        ]
    )
    
    # Matriz Estratégica
    guide_card_enhanced(
        "🎯", "Matriz Estratégica", "OCUPAÇÃO × SATISFAÇÃO",
        """Cada ponto é uma <strong>cidade</strong>. O tamanho da bolha = receita. A cor = estado.
        <br><br>
        <strong>🎨 Quadrantes:</strong><br>
        • <span style="color:#2ECC71;">★ Alto Potencial</span> → espaço para crescer sem perder qualidade<br>
        • <span style="color:#F5A623;">🏆 Destaque Total</span> → melhor cenário, pode pressionar preços<br>
        • <span style="color:#FF6B6B;">⚠ Atenção</span> → risco operacional, ação urgente<br>
        • <span style="color:#4A90E2;">📊 Operacional</span> → sobrecarga, qualidade comprometida""",
        [
            "Quais cidades têm maior potencial de crescimento?",
            "Há cidades sobrecarregadas (alta ocupação, baixa satisfação)?",
            "Qual estado concentra mais cidades no quadrante de risco?"
        ]
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Segunda linha do grid
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 20px;">
    """, unsafe_allow_html=True)
    
    # Heatmap
    guide_card_enhanced(
        "🌡️", "Sazonalidade (Heatmap)", "ESTADO × MÊS",
        """Cada célula representa a <strong>receita de um par Estado × Mês</strong>.
        <br><br>
        <strong>🎨 Cores:</strong><br>
        • Dourado → alta receita (pico de temporada)<br>
        • Azul escuro → baixa receita (off-season)<br>
        • Transição suave → sazonalidade gradual""",
        [
            "Qual estado tem receita mais distribuída ao longo do ano?",
            "Em quais meses a concorrência é mais acirrada?",
            "Há estados com receita concentrada em apenas 1-2 meses?"
        ]
    )
    
    # Radar
    guide_card_enhanced(
        "🕸️", "Perfil Competitivo (Radar)", "DIMENSÕES MÚLTIPLAS",
        """O radar compara estados em 5 dimensões normalizadas (0-100).
        <br><br>
        <strong>📊 Como ler:</strong><br>
        • Área maior → desempenho geral superior<br>
        • Forma equilibrada → consistência em todas as frentes<br>
        • Picos isolados → excelência em poucos aspectos""",
        [
            "Qual estado tem o perfil mais equilibrado?",
            "Há um estado que domina em receita mas tem avaliação baixa?",
            "Qual estado é mais forte em satisfação do cliente?"
        ]
    )
    
    # Boxplot
    guide_card_enhanced(
        "📦", "Ticket Médio (Boxplot)", "DISTRIBUIÇÃO ESTATÍSTICA",
        """O boxplot mostra a <strong>distribuição completa</strong> do ticket médio por tipo.
        <br><br>
        <strong>🔧 Elementos:</strong><br>
        • Linha central → mediana (valor do meio)<br>
        • Caixa → 50% dos dados (intervalo interquartil)<br>
        • Bigodes → amplitude sem outliers<br>
        • Pontos → valores atípicos (outliers)""",
        [
            "Qual tipo tem o ticket mais consistente?",
            "Há valores atípicos muito acima da média?",
            "A mediana do Hotel é realmente maior que da Pousada?"
        ]
    )
    
    # Ranking
    guide_card_enhanced(
        "🏅", "Ranking de Cidades", "TOP PERFORMERS",
        """Barras horizontais ordenadas da maior para a menor receita.
        <br><br>
        <strong>🎨 Código de cores:</strong><br>
        • <span style="color:#F5A623;">Dourado</span> → 1º lugar<br>
        • <span style="color:#20B2AA;">Teal</span> → 2º ao 4º lugar<br>
        • <span style="color:#4A90E2;">Azul</span> → demais posições""",
        [
            "Qual cidade lidera a receita no estado selecionado?",
            "Há grande concentração (1 cidade >40% da receita)?",
            "Como o ranking muda em diferentes períodos?"
        ]
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Seção de dicas rápidas
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0F1D2E 0%, #0B1320 100%);
                border: 1px solid #2A4A6B;
                border-radius: 20px;
                padding: 20px 24px;
                margin-top: 20px;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
            <span style="font-size: 24px;">⚡</span>
            <span style="font-family: 'Syne', sans-serif; font-size: 16px; font-weight: 700; color: #F5A623;">
                Dicas Rápidas
            </span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">
            <div style="background: rgba(0,0,0,0.2); border-radius: 12px; padding: 12px;">
                <div style="color: #F5A623; font-size: 20px; margin-bottom: 8px;">📷</div>
                <div style="color: #CBD5E1; font-size: 12px;">Clique na <strong>câmera</strong> no canto superior do gráfico para exportar como PNG</div>
            </div>
            <div style="background: rgba(0,0,0,0.2); border-radius: 12px; padding: 12px;">
                <div style="color: #F5A623; font-size: 20px; margin-bottom: 8px;">🖱️</div>
                <div style="color: #CBD5E1; font-size: 12px;">Passe o mouse sobre qualquer elemento para ver <strong>detalhes interativos</strong></div>
            </div>
            <div style="background: rgba(0,0,0,0.2); border-radius: 12px; padding: 12px;">
                <div style="color: #F5A623; font-size: 20px; margin-bottom: 8px;">🔄</div>
                <div style="color: #CBD5E1; font-size: 12px;">Os filtros na sidebar <strong>atualizam todos os gráficos</strong> simultaneamente</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    render_footer(df)



# ══════════════════════════════════════════════════════════════════
# TAB 3 — GUIA DE FILTROS (MESMO ESTILO DA TAB 2)
# ══════════════════════════════════════════════════════════════════
with tab_filtros:
    # Cabeçalho estilizado (mesmo padrão da Tab 2)
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0F1D2E 0%, #0B1320 100%); 
                border: 1px solid #2A4A6B; 
                border-bottom: 3px solid #F5A623; 
                border-radius: 20px; 
                padding: 24px 28px; 
                margin-bottom: 28px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.3);">
        <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap;">
            <span style="font-size: 48px;">🔍</span>
            <div>
                <div style="font-family: 'Syne', sans-serif; font-size: 24px; font-weight: 800; color: #FFFFFF; margin-bottom: 8px;">
                    Como Usar os Filtros da Sidebar
                </div>
                <div style="color: #CBD5E1; font-size: 14px; line-height: 1.6;">
                    Os filtros são <strong style="color: #F5A623;">combinados</strong> — cada seleção refina simultaneamente todos os gráficos e KPIs do Dashboard.
                    <strong style="color: #F5A623;">Nenhum filtro é obrigatório</strong> — deixar em branco significa <em style="color: #F5A623;">todos</em>.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    def filter_card_same_style(icon, title, subtitle, body_html, questions):
        """Mesmo estilo da função guide_card_enhanced da Tab 2"""
        q_items = "".join(f'<li><span class="q-marker">❓</span> {q}</li>' for q in questions)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0F1D2E 0%, #0D1828 100%);
                    border: 1px solid #2A4A6B;
                    border-radius: 20px;
                    padding: 0;
                    margin-bottom: 20px;
                    transition: all 0.3s ease;
                    overflow: hidden;">
            <div style="background: linear-gradient(90deg, #F5A623 0%, #E69500 100%);
                        padding: 12px 20px;
                        display: flex;
                        align-items: center;
                        gap: 12px;">
                <span style="font-size: 28px;">{icon}</span>
                <div>
                    <div style="font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 800; color: #0D1117;">
                        {title}
                    </div>
                    <div style="font-size: 11px; color: #0D1117; opacity: 0.8; margin-top: 2px;">
                        {subtitle}
                    </div>
                </div>
            </div>
            <div style="padding: 20px;">
                <div style="font-family: 'Inter', sans-serif; font-size: 13px; color: #CBD5E1; line-height: 1.7; margin-bottom: 20px;">
                    {body_html}
                </div>
                <div style="background: rgba(245,166,35,0.08); border-left: 3px solid #F5A623; border-radius: 12px; padding: 14px 18px; margin-top: 8px;">
                    <div style="font-family: 'Syne', sans-serif; font-size: 11px; font-weight: 700; color: #F5A623; letter-spacing: 0.08em; margin-bottom: 10px;">
                        📌 PERGUNTAS QUE ESTE FILTRO RESPONDE
                    </div>
                    <ul style="margin: 0; padding-left: 0; list-style: none;">
                        {q_items}
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Layout em grid para os cards de filtros (mesmo da Tab 2)
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 20px;">
    """, unsafe_allow_html=True)
    
    # Filtro de Tipo
    filter_card_same_style(
        "🏨", "Tipo de Empreendimento", "SEGMENTAÇÃO POR CATEGORIA",
        """Três botões toggle: <strong>Hotel</strong> · <strong>Pousada</strong> · <strong>Agência</strong>.
        <br><br>
        • Botão <span style="color:#F5A623;">ativo (laranja)</span> = incluído no filtro<br>
        • Botão <span style="color:#64748B;">inativo (cinza)</span> = excluído<br>
        • Ao menos 1 tipo sempre estará ativo
        <br><br>
        <strong>💡 Dica:</strong> Compare os KPIs ao ativar apenas um tipo por vez. Anote os valores de receita e ocupação de cada tipo isolado.""",
        [
            "Hotéis têm ticket médio maior que Pousadas?",
            "Agências têm avaliação mais alta que hospedagens?",
            "Qual estado tem mais força em Pousadas?"
        ]
    )
    
    # Filtro de Período
    filter_card_same_style(
        "📅", "Período de Análise", "JANELA DESLIZANTE",
        """Dois controles combinados:
        <br><br>
        • <strong>📏 Janela (1–12)</strong> — quantos meses consecutivos analisar<br>
        • <strong>📍 Início (slider 0–11)</strong> — posição inicial na linha do tempo<br><br>
        Os meses selecionados aparecem destacados em <span style="color:#F5A623;">dourado</span>.
        <br><br>
        <strong>💡 Dica:</strong> Mova o slider de Início mantendo Janela=1 para 'varrer' o ano mês a mês como um vídeo.""",
        [
            "Qual trimestre tem a maior receita média?",
            "O desempenho do 1º semestre é superior ao 2º semestre?",
            "Em qual mês específico a ocupação atinge o pico?"
        ]
    )
    
    # Filtro de Estado
    filter_card_same_style(
        "🏛️", "Filtro de Estado", "SELEÇÃO HIERÁRQUICA",
        """Cada estado possui um checkbox principal.
        <br><br>
        • <strong>Marcar/desmarcar o estado</strong> ativa/desativa todas as suas cidades automaticamente<br>
        • Estados disponíveis: <span style="color:#F5A623;">CE</span> (Ceará), <span style="color:#F5A623;">PE</span> (Pernambuco), 
          <span style="color:#F5A623;">PI</span> (Piauí), <span style="color:#F5A623;">RN</span> (Rio Grande do Norte)
        <br><br>
        <strong>💡 Dica:</strong> Ative 2 estados por vez e compare o radar para ver quem é superior em cada dimensão.""",
        [
            "Como CE se compara a PE em receita, ocupação e avaliação?",
            "Qual estado tem a maior homogeneidade entre suas cidades?",
            "Há estados onde Pousadas superam Hotéis em receita?"
        ]
    )
    
    # Filtro de Cidade
    filter_card_same_style(
        "🗺️", "Filtro de Cidade", "MICROANÁLISE LOCAL",
        """Após ativar um estado, clique no expander <strong>🗺️ N cidades</strong> para ver e selecionar cidades individualmente.
        <br><br>
        <strong>Cidades disponíveis por estado:</strong><br>
        • CE: Fortaleza, Jericoacoara, Canoa Quebrada<br>
        • PE: Recife, Olinda, Porto de Galinhas<br>
        • PI: Teresina, Parnaíba, Luís Correia<br>
        • RN: Natal, Pipa, Genipabu
        <br><br>
        <strong>💡 Dica:</strong> Para análise de cidade individual, desative o estado e reative apenas a cidade desejada.""",
        [
            "Fortaleza concentra mais de 50% da receita do Ceará?",
            "Porto de Galinhas tem avaliação acima da média de PE?",
            "Qual cidade litorânea tem a maior taxa de ocupação no verão?"
        ]
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Seção de combinações estratégicas (mesmo estilo da Tab 2)
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0F1D2E 0%, #0B1320 100%);
                border: 1px solid #2A4A6B;
                border-radius: 20px;
                padding: 24px;
                margin-top: 20px;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
            <span style="font-size: 28px;">🎯</span>
            <span style="font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 800; color: #F5A623;">
                Combinações Estratégicas Recomendadas
            </span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">
            <div style="background: rgba(245,166,35,0.08); border-radius: 16px; padding: 16px; border-top: 3px solid #F5A623;">
                <div style="font-size: 24px; margin-bottom: 8px;">🏆</div>
                <div style="font-weight: 700; color: #F5A623; margin-bottom: 8px;">Alta Temporada Premium</div>
                <div style="font-size: 11px; color: #CBD5E1;">Tipo: Hotel | Período: Janela 3 (pico)</div>
            </div>
            <div style="background: rgba(245,166,35,0.08); border-radius: 16px; padding: 16px; border-top: 3px solid #F5A623;">
                <div style="font-size: 24px; margin-bottom: 8px;">📊</div>
                <div style="font-weight: 700; color: #F5A623; margin-bottom: 8px;">Benchmark Regional</div>
                <div style="font-size: 11px; color: #CBD5E1;">Tipo: Todos | Comparar 2 estados</div>
            </div>
            <div style="background: rgba(245,166,35,0.08); border-radius: 16px; padding: 16px; border-top: 3px solid #F5A623;">
                <div style="font-size: 24px; margin-bottom: 8px;">⚠️</div>
                <div style="font-weight: 700; color: #F5A623; margin-bottom: 8px;">Diagnóstico de Risco</div>
                <div style="font-size: 11px; color: #CBD5E1;">Janela: 1 | Varrer meses críticos</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    render_footer(df)