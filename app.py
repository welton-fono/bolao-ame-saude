import streamlit as st
import gspread
import pandas as pd
from datetime import datetime

# 1. Configuração da Página
st.set_page_config(page_title="AME SAÚDE | Bolão", layout="centered")

# --- CSS CUSTOMIZADO ESTILO AME SAÚDE ---
st.markdown("""
    <style>
    .ame-header {
        background-color: #06AA48;
        color: white;
        padding: 15px;
        font-family: 'Arial', sans-serif;
        font-size: 26px;
        font-weight: 900;
        border-radius: 8px;
        margin-bottom: 25px;
        text-align: center;
        letter-spacing: -1px;
    }
    .ame-subtitle {
        color: #06AA48;
        font-weight: bold;
        font-size: 14px;
        text-transform: uppercase;
    }
    </style>
    <div class="ame-header">AME SAÚDE | BOLÃO DA COPA 2026</div>
""", unsafe_allow_html=True)

# 2. Dicionário de Bandeiras (Imagens)
bandeiras = {
    "Brasil": "br", "Argentina": "ar", "México": "mx", "África do Sul": "za", 
    "Coreia do Sul": "kr", "Tchéquia": "cz", "Canadá": "ca", "Bósnia e Herzegovina": "ba", 
    "Catar": "qa", "Suíça": "ch", "Marrocos": "ma", "Haiti": "ht", "Escócia": "gb-sct", 
    "Estados Unidos": "us", "Paraguai": "py", "Austrália": "au", "Turquia": "tr", 
    "Alemanha": "de", "Curaçao": "cw", "Costa do Marfim": "ci", "Equador": "ec", 
    "Holanda": "nl", "Japão": "jp", "Suécia": "se", "Tunísia": "tn", "Bélgica": "be", 
    "Egito": "eg", "Irã": "ir", "Nova Zelândia": "nz", "Espanha": "es", "Cabo Verde": "cv", 
    "Arábia Saudita": "sa", "Uruguai": "uy", "França": "fr", "Senegal": "sn", 
    "Iraque": "iq", "Noruega": "no", "Argélia": "dz", "Áustria": "at", "Jordânia": "jo", 
    "Portugal": "pt", "RD Congo": "cd", "Uzbequistão": "uz", "Colômbia": "co", 
    "Inglaterra": "gb-eng", "Croácia": "hr", "Gana": "gh", "Panamá": "pa", 
    "A definir": "un"
}

def get_bandeira_img(pais):
    codigo = bandeiras.get(pais, "un")
    return f"<img src='https://flagcdn.com/24x18/{codigo}.png' width='24' style='vertical-align: middle;'>"

# 3. Conexão com o Google Sheets (USANDO SECRETS DO STREAMLIT)
try:
    credenciais = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    }
    
    conta = gspread.service_account_from_dict(credenciais)
    planilha = conta.open("PLANILHA BOLAO COPA")
    aba_jogos = planilha.worksheet("Resultados_Reais")
    aba_palpites = planilha.worksheet("Palpites")
    
    tabela = pd.DataFrame(aba_jogos.get_all_records())
except Exception as e:
    st.error(f"Erro ao conectar. Verifique as Secrets. Erro: {e}")
    st.stop()

# [O RESTANTE DO SEU CÓDIGO PERMANECE IGUAL A PARTIR DAQUI...]
# (Pode manter o seu código anterior que criava as abas, botões e ranking)
# ...
