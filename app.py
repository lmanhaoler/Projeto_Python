import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CONFIGURAÇÃO DA PÁGINA (Tema Escuro e Layout Amplo)
st.set_page_config(page_title="Dashboard de Investimentos", layout="wide")

# ESTILIZAÇÃO CUSTOMIZADA (Preto e Amarelo Premium)
st.markdown("""
    <style>
        /* Fundo principal do app */
        .stApp { background-color: #121212; color: #e0e0e0; }
        /* Título principal */
        h1 { color: #ffd700 !important; font-family: 'Segoe UI', sans-serif; text-transform: uppercase; letter-spacing: 2px; text-align: center; margin-bottom: 30px; }
        /* Subtítulos dos blocos */
        h2, h3 { color: #ffd700 !important; border-bottom: 2px solid #ffd700; padding-bottom: 5px; margin-top: 20px; }
        /* Estilização dos cards/métricas do Streamlit */
        div[data-testid="stMetric"] { background-color: #1e1e1e; border: 1px solid #333; border-top: 5px solid #ffd700; border-radius: 8px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        div[data-testid="stMetricLabel"] { color: #a6a6a6 !important; font-weight: bold; }
        div[data-testid="stMetricValue"] { color: #ffffff !important; }
        /* Estilização da caixa de seleção */
        .stSelectbox label { color: #ffd700 !important; font-weight: bold; font-size: 1.1rem; }
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

# Mapeamento manual dos dados fixos de cadastro que você pediu do Dashboard
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

# Carrega os metadados do fundo escolhido no seletor
info = dados_fundos_cadastro[fundo_selecionado]

st.write("---")

# --- SEÇÃO 1: FICHA TÉCNICA E DADOS CADASTRAIS (NO TOPO) ---
st.markdown(f"<h3>📋 Ficha Técnica: {fundo_selecionado}</h3>", unsafe_allow_html=True)

# Organizando as métricas em colunas (3 por linha para ficar elegante)
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

st.write("---")

# --- SEÇÃO 2: GRÁFICO TEMPORAL DE COTAS (ABAIXO DOS DADOS) ---
st.markdown("<h3>📈 Gráfico de Evolução do Valor da Cota</h3>", unsafe_allow_html=True)

# Filtra a tabela de dados dinamicamente com base na escolha do seletor
dados_filtrados = df[df['nomeFundo'] == fundo_selecionado]

if not dados_filtrados.empty:
    # Configurações do gráfico em Modo Escuro
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#1e1e1e')
    
    # Transforma datas para texto formatado para o gráfico
    datas_texto = dados_filtrados['dataPosicao'].dt.strftime('%d/%m/%Y')
    
    # Desenha a linha dourada do fundo selecionado
    ax.plot(datas_texto, dados_filtrados['valorCotaFundo'], 
            marker='o', color='#ffd700', linewidth=2, label="Valor da Cota")
    
    plt.xlabel('Data da Posição', color='#a6a6a6', labelpad=10)
    plt.ylabel('Valor da Cota (R$)', color='#a6a6a6', labelpad=10)
    plt.grid(True, color='#333333', linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Renderiza o gráfico na tela
    st.pyplot(fig)
else:
    st.warning("Nenhum dado histórico de cotas foi encontrado para este fundo na planilha.")
