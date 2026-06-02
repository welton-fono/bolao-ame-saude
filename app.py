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

# 3. Conexão com o Google Sheets
try:
    conta = gspread.service_account(filename="credenciais.json")
    planilha = conta.open("PLANILHA BOLAO COPA")
    aba_jogos = planilha.worksheet("Resultados_Reais")
    aba_palpites = planilha.worksheet("Palpites")
    
    tabela = pd.DataFrame(aba_jogos.get_all_records())
except Exception as e:
    st.error(f"Erro ao conectar com a planilha. Erro: {e}")
    st.stop()

# Menus de navegação
aba1, aba2, aba3 = st.tabs(["⚽ Jogos", "🏆 Classificação", "📜 Regulamento"])

# ==========================================
# ABA 1: TELA DE PALPITES
# ==========================================
with aba1:
    st.markdown("<p class='ame-subtitle'>Deixe seus palpites</p>", unsafe_allow_html=True)
    nome_usuario = st.text_input("Identifique-se pelo nome:")
    st.divider()

    palpites_temp_A = {}
    palpites_temp_B = {}

    if not tabela.empty:
        fases = tabela['Fase'].unique()
        for fase in fases:
            if str(fase) == 'Fase' or str(fase) == '': continue
            
            with st.expander(fase, expanded=False):
                jogos_fase = tabela[tabela['Fase'] == fase]
                for index, jogo in jogos_fase.iterrows():
                    id_jogo = jogo['ID_Jogo']
                    
                    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 3])
                    with col1:
                        img_a = get_bandeira_img(jogo['Time_A'])
                        st.markdown(f"<div style='text-align: right; padding-top: 8px; font-weight: bold;'>{jogo['Time_A']} {img_a}</div>", unsafe_allow_html=True)
                    with col2:
                        palpites_temp_A[id_jogo] = st.number_input("", min_value=0, step=1, key=f"gol_a_{id_jogo}")
                    with col3:
                        st.markdown("<div style='text-align: center; padding-top: 8px; color: gray;'><b>X</b></div>", unsafe_allow_html=True)
                    with col4:
                        palpites_temp_B[id_jogo] = st.number_input("", min_value=0, step=1, key=f"gol_b_{id_jogo}")
                    with col5:
                        img_b = get_bandeira_img(jogo['Time_B'])
                        st.markdown(f"<div style='text-align: left; padding-top: 8px; font-weight: bold;'>{img_b} {jogo['Time_B']}</div>", unsafe_allow_html=True)
                    st.divider()

    st.write("")
    if st.button("SALVAR PALPITES", use_container_width=True, type="primary"):
        if nome_usuario.strip() == "":
            st.error("⚠️ Digite seu nome antes de salvar!")
        else:
            with st.spinner('Registrando...'):
                data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                novas_linhas = []
                for id_jogo in palpites_temp_A.keys():
                    gols_a = palpites_temp_A[id_jogo]
                    gols_b = palpites_temp_B[id_jogo]
                    novas_linhas.append([data_hora_atual, nome_usuario.strip().upper(), id_jogo, gols_a, gols_b])
                
                aba_palpites.append_rows(novas_linhas)
                st.success(f"Pronto, {nome_usuario}! Palpites salvos na base de dados.")

# ==========================================
# ABA 2: RANKING (O CÉREBRO DO BOLÃO)
# ==========================================
with aba2:
    st.markdown("<p class='ame-subtitle'>Classificação do Bolão</p>", unsafe_allow_html=True)
    
    try:
        dados_palpites = aba_palpites.get_all_records()
        df_palpites = pd.DataFrame(dados_palpites)
    except:
        df_palpites = pd.DataFrame()

    if df_palpites.empty:
        st.info("Ainda não há participantes no bolão.")
    else:
        # Filtra apenas os jogos que você marcou como "Finalizado" na planilha
        df_finalizados = tabela[tabela['Status'].astype(str).str.upper() == 'FINALIZADO']
        
        if df_finalizados.empty:
            st.info("Nenhum jogo foi finalizado ainda. O ranking aparecerá após o primeiro resultado oficial!")
        else:
            pontuacao = {}
            
            # Percorre todos os palpites dados
            for index, palpite in df_palpites.iterrows():
                nome = str(palpite['Nome']).strip()
                id_jogo = palpite['ID_Jogo']
                palpite_a = int(palpite['Palpite_Gols_A'])
                palpite_b = int(palpite['Palpite_Gols_B'])
                
                if nome not in pontuacao:
                    pontuacao[nome] = 0
                
                # Procura se esse jogo já acabou
                jogo_real = df_finalizados[df_finalizados['ID_Jogo'] == id_jogo]
                
                if not jogo_real.empty:
                    real_a = int(jogo_real.iloc[0]['Gols_A'])
                    real_b = int(jogo_real.iloc[0]['Gols_B'])
                    
                    # REGRA 1: Placar Exato = 5 Pontos
                    if palpite_a == real_a and palpite_b == real_b:
                        pontuacao[nome] += 5
                    # REGRA 2: Acertou Vencedor/Empate = 3 Pontos
                    else:
                        vencedor_real = "A" if real_a > real_b else ("B" if real_b > real_a else "Empate")
                        vencedor_palpite = "A" if palpite_a > palpite_b else ("B" if palpite_b > palpite_a else "Empate")
                        
                        if vencedor_real == vencedor_palpite:
                            pontuacao[nome] += 3
            
            # Monta a tabela final
            df_ranking = pd.DataFrame(list(pontuacao.items()), columns=['Participante', 'Pontos'])
            df_ranking = df_ranking.sort_values(by='Pontos', ascending=False).reset_index(drop=True)
            df_ranking.index = df_ranking.index + 1 # Posição 1, 2, 3...
            df_ranking.index.name = 'Posição'
            
            # Pódio Especial para 1º e 2º lugar!
            if len(df_ranking) > 0:
                st.success(f"🥇 **1º LUGAR:** {df_ranking.iloc[0]['Participante']} ({df_ranking.iloc[0]['Pontos']} pts)")
            if len(df_ranking) > 1:
                st.info(f"🥈 **2º LUGAR:** {df_ranking.iloc[1]['Participante']} ({df_ranking.iloc[1]['Pontos']} pts)")
                
            st.divider()
            st.dataframe(df_ranking, use_container_width=True)

# ==========================================
# ABA 3: REGRAS
# ==========================================
with aba3:
    st.markdown("<p class='ame-subtitle'>Critérios de Pontuação</p>", unsafe_allow_html=True)
    st.write("Acertar o placar exato do jogo: **5 pontos**")
    st.write("Acertar apenas a seleção vencedora: **3 pontos**")
