import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# CONFIGURAÇÃO DA PÁGINA (Tema Escuro e Layout Amplo)
st.set_page_config(page_title="Dashboard de Investimentos", layout="wide")

# ESTILIZAÇÃO CUSTOMIZADA (Preto e Amarelo Premium)
st.markdown("""
    <style>
        .stApp { background-color: #121212; color: #e0e0e0; }
        h1 { color: #ffd700 !important; font-family: 'Segoe UI', sans-serif; text-transform: uppercase; letter-spacing: 2px; text-align: center; margin-bottom: 30px; }
        h2, h3 { color: #ffd700 !important; border-bottom: 2px solid #ffd700; padding-bottom: 5px; margin-top: 20px; }
        div[data-testid="stMetric"] { background-color: #1e1e1e; border: 1px solid #333; border-top: 5px solid #ffd700; border-radius: 8px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        div[data-testid="stMetricLabel"] { color: #a6a6a6 !important; font-weight: bold; }
        div[data-testid="stMetricValue"] { color: #ffffff !important; }
        .stSelectbox label { color: #ffd700 !important; font-weight: bold; font-size: 1.1rem; }
        /* Estilização do botão de download */
        div.stDownloadButton > button { background-color: #ffd700 !important; color: #121212 !important; font-weight: bold !important; border: none !important; border-radius: 6px !important; width: 100%; padding: 10px !important; }
        div.stDownloadButton > button:hover { background-color: #f5b041 !important; color: #121212 !important; }
    </style>
""", unsafe_allow_html=True)

# 1. CARREGAR E TRATAR OS DADOS DA PLANILHA
@st.cache_data
def carregar_dados():
    df = pd.read_csv('dados.csv')
    df['pl'] = pd.to_numeric(df['pl'], errors='coerce')
    df['valorCotaFundo'] = pd.to_numeric(df['valorCotaFundo'], errors='coerce')
    df['dataPosicao'] = pd.to_datetime(df['dataPosicao'], format='%d/%m/%Y', errors='coerce')
    return df.sort_values('dataPosicao')

df = carregar_dados()

# Mapeamento manual dos dados fixos de cadastro
dados_fundos_cadastro = {
    "22691 - XP SELECTION FII": {
        "cnpj": "30.983.020/0001-90",
        "tipo": "FII",
        "condominio": "FECHADO",
        "publico": "GERAL",
        "gestor": "XP VISTA ASSET MANAGEMENT LTDA.",
        "custodiante": "OLIVEIRA TRUST DTVM S.A.",
        "pl_exibicao": "R$ 365.918.672,24",
        "exercicio": "31 de Dezembro"
    },
    "32781 - TG REAL ESTATE FII": {
        "cnpj": "44.625.562/0001-04",
        "tipo": "FII",
        "condominio": "FECHADO",
        "publico": "QUALIFICADO",
        "gestor": "TG CORE ASSET LTDA",
        "custodiante": "OLIVEIRA TRUST DTVM S.A.",
        "pl_exibicao": "R$ 1.374.569.162,60",
        "exercicio": "31 de Dezembro"
    }
}

# TÍTULO PRINCIPAL
st.markdown("<h1>📊 Dashboard de Investimentos Premium</h1>", unsafe_allow_html=True)

# --- FILTRO SELETOR DE FUNDO ---
opcoes_fundos = list(dados_fundos_cadastro.keys())
fundo_selecionado = st.selectbox("🔍 Selecione o Fundo para Análise:", opcoes_fundos)

info = dados_fundos_cadastro[fundo_selecionado]

st.write("---")

# --- SEÇÃO 1: FICHA TÉCNICA E DADOS CADASTRAIS ---
st.markdown(f"<h3>📋 Ficha Técnica: {fundo_selecionado}</h3>", unsafe_allow_html=True)

linha1_col1, linha1_col2, linha1_col3 = st.columns(3)
with linha1_col1:
    st.metric(label="CNPJ do Fundo", value=info["cnpj"])
with linha1_col2:
    st.metric(label="Tipo de Fundo", value=info["tipo"])
with linha1_col3:
    st.metric(label="Condomínio", value=info["condominio"])

linha2_col1, linha2_col2, linha2_col3 = st.columns(3)
with linha2_col1:
    st.metric(label="Público-Alvo", value=info["publico"])
with linha2_col2:
    st.metric(label="Gestor do Fundo", value=info["gestor"])
with linha2_col3:
    st.metric(label="Custodiante", value=info["custodiante"])

linha3_col1, linha3_col2, linha3_col3 = st.columns(3)
with linha3_col1:
    st.metric(label="Patrimônio Líquido (PL de Referência)", value=info["pl_exibicao"])
with linha3_col2:
    st.metric(label="Fim do Exercício Social", value=info["exercicio"])

# Filtragem dos dados para os cálculos dinâmicos
dados_filtrados = df[df['nomeFundo'] == fundo_selecionado].copy()

# --- EXPORTAÇÃO PARA EXCEL ---
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    dados_exportacao = dados_filtrados.copy()
    if 'dataPosicao' in dados_exportacao.columns:
        dados_exportacao['dataPosicao'] = dados_exportacao['dataPosicao'].dt.strftime('%d/%m/%Y')
    dados_exportacao.to_excel(writer, index=False, sheet_name='Dados Filtrados')

st.write("")
st.download_button(
    label=f"📥 Baixar Relatório de Ativos em Excel (.xlsx)",
    data=buffer.getvalue(),
    file_name=f"relatorio_{fundo_selecionado.replace(' ', '_')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.write("---")

# --- NOVO UPGRADE: SEÇÃO DE RESUMO ESTATÍSTICO DINÂMICO ---
st.markdown("<h3>📊 Resumo Estatístico do Período</h3>", unsafe_allow_html=True)

if not dados_filtrados.empty:
    # Realizando os cálculos matemáticos na hora
    media_cota = dados_filtrados['valorCotaFundo'].mean()
    min_cota = dados_filtrados['valorCotaFundo'].min()
    max_cota = dados_filtrados['valorCotaFundo'].max()
    total_registros = len(dados_filtrados)
    
    # Exibindo os resultados calculados em 4 colunas elegantes
    est1, est2, est3, est4 = st.columns(4)
    with est1:
        st.metric(label="Média do Valor da Cota", value=f"R$ {media_cota:,.2f}")
    with est2:
        st.metric(label="Menor Cota Registrada", value=f"R$ {min_cota:,.2f}")
    with est3:
        st.metric(label="Maior Cota Registrada", value=f"R$ {max_cota:,.2f}")
    with est4:
        st.metric(label="Total de Ativos/Registros", value=f"{total_registros}")
else:
    st.warning("Sem dados estatísticos disponíveis para este fundo.")

st.write("---")

# --- SEÇÃO 3: GRÁFICO TEMPORAL DE COTAS ---
st.markdown("<h3>📈 Gráfico de Evolução do Valor da Cota</h3>", unsafe_allow_html=True)

if not dados_filtrados.empty:
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#1e1e1e')
    
    datas_texto = dados_filtrados['dataPosicao'].dt.strftime('%d/%m/%Y')
    
    ax.plot(datas_texto, dados_filtrados['valorCotaFundo'], 
            marker='o', color='#ffd700', linewidth=2, label="Valor da Cota")
    
    plt.xlabel('Data da Posição', color='#a6a6a6', labelpad=10)
    plt.ylabel('Valor da Cota (R$)', color='#a6a6a6', labelpad=10)
    plt.grid(True, color='#333333', linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    st.pyplot(fig)
