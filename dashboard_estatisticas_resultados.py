import streamlit as st
import pandas as pd

# Carregar as planilhas
@st.cache_data
def load_data():
    df_dashboard = pd.read_excel('planilha_com_novos_nomes_jogadores_atualizada.xlsx')
    df_estatisticas = pd.read_excel("estatisticas_jogadores_formatado.xlsx")
    return df_dashboard, df_estatisticas

# Carregar os dados
df_dashboard, df_estatisticas = load_data()

# Configuração da página
st.set_page_config(page_title="Staking Team eSports", layout="wide")

# Menu de navegação
tab = st.sidebar.radio("Escolha a aba", ["Dashboard", "Estatísticas Gerais"])


if tab == "Dashboard":
    # Aba Dashboard
    st.title("📊 Dashboard de Jogadores")

    # ---------------- Filtros organizados ----------------
    col1, col2 = st.columns(2)

    with col1:
        filtro_mes = st.selectbox('📅 Escolha o Mês:', df_dashboard['Mês'].unique())
        filtro_semana = st.selectbox('📆 Escolha a Semana:', ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4'])
        filtro_dia = st.selectbox('🗓️ Escolha o Dia:', sorted(df_dashboard['Dia'].unique()))

    with col2:
        # Remover NaN das posições
        posicoes_validas = [p for p in df_dashboard['Posição'].dropna().unique()]
        filtro_posicao = st.selectbox('🎯 Escolha a Posição:', sorted(posicoes_validas))
        filtro_jogo = st.selectbox('🎮 Escolha o Jogo:', df_dashboard['Jogo'].unique())

    # ---------------- Aplicar filtros ----------------
    df_filtrado = df_dashboard.copy()
    df_filtrado = df_filtrado[(df_filtrado['Mês'] == filtro_mes) & (df_filtrado['Posição'] == filtro_posicao)]
    if filtro_semana in df_filtrado['Semana'].values:
        df_filtrado = df_filtrado[df_filtrado['Semana'] == filtro_semana]
    df_filtrado = df_filtrado[df_filtrado['Dia'] == filtro_dia]
    df_filtrado = df_filtrado[df_filtrado['Jogo'] == filtro_jogo]

    # ---------------- Resumo por jogador ----------------
    colunas_resumo_por_posicao = {
        'GK': ['Defesas', 'Cleansheet', 'Gols Sofridos'],
        'ZAG': ['Posses Ganhas', 'Posses Perdidas', '% Passes Certos', 'Total Passes'],
        'MC': ['Posses Ganhas', 'Posses Perdidas', '% Passes Certos', 'Total Passes'],
        'ALA': ['Posses Ganhas', 'Posses Perdidas', '% Passes Certos', 'Total Passes'],
        'ST': ['Posses Ganhas', 'Posses Perdidas', '% Passes Certos', 'Total Passes']
    }

    colunas_resumo = colunas_resumo_por_posicao.get(filtro_posicao, [])

    if not df_filtrado.empty and colunas_resumo:
        jogadores_disponiveis = df_filtrado['Jogador'].unique()
        jogador_escolhido = st.selectbox("👤 Escolha o Jogador:", jogadores_disponiveis)

        df_jogador = df_filtrado[df_filtrado['Jogador'] == jogador_escolhido]

        if not df_jogador.empty:
            st.subheader(f"📌 Resumo Rápido - {jogador_escolhido}")
            cols = st.columns(len(colunas_resumo))

            # Pegar a primeira linha do jogador dentro do filtro (igual aparece na tabela)
            linha_jogador = df_jogador.iloc[0]

            for i, campo in enumerate(colunas_resumo):
                if campo in linha_jogador.index:
                    valor = linha_jogador[campo]
                    if pd.isna(valor):
                        val_fmt = "0"
                    elif isinstance(valor, float) and "Passes Certos" in campo:
                        val_fmt = f"{valor:.0f}%"
                    else:
                        val_fmt = f"{int(valor)}" if float(valor).is_integer() else f"{valor:.1f}"
                else:
                    val_fmt = "0"

                with cols[i]:
                    st.metric(label=campo, value=val_fmt)

    # ---------------- Tabela ----------------
    st.subheader("📋 Comparação entre Jogadores")
    if not df_filtrado.empty:
        df_exibicao = df_filtrado.copy()
        for col in df_exibicao.columns:
            if "%" in col or "Passes Certos" in col:
                df_exibicao[col] = df_exibicao[col].apply(
                    lambda x: f"{'█' * int(x // 10)} {x:.0f}%" if pd.notna(x) else "-"
                )
        st.dataframe(df_exibicao, use_container_width=True)


elif tab == "Estatísticas Gerais":
    st.title("📌 Estatísticas Gerais - Jogadores")

    # Filtro de Posição
    posicoes = df_estatisticas['Posição'].dropna().unique()
    posicao_escolhida = st.selectbox("Escolha a Posição:", sorted(posicoes))

    # Filtro de Jogador
    jogadores_posicao = df_estatisticas[df_estatisticas['Posição'] == posicao_escolhida]['Jogador'].dropna().unique()
    jogador_escolhido = st.selectbox("Escolha o Jogador:", sorted(jogadores_posicao))

    # Filtrar dados
    dados_jogador = df_estatisticas[
        (df_estatisticas['Posição'] == posicao_escolhida) &
        (df_estatisticas['Jogador'] == jogador_escolhido)
    ].copy()

    destaques_por_posicao = {
        'GK': ['Defesas', 'Cleansheet', 'Gols Sofridos', '% Passes Certos'],
        'ZAG': ['Posses Ganhas', 'Posses Perdidas', 'Total Passes', '% Passes Certos'],
        'MC': ['Posses Ganhas', 'Posses Perdidas', 'Total Passes', '% Passes Certos'],
        'ALA': ['Posses Ganhas', 'Posses Perdidas', 'Total Passes', '% Passes Certos'],
        'ST': ['Posses Ganhas', 'Posses Perdidas', 'Total Passes', '% Passes Certos']
    }

    colunas = [c for c in dados_jogador.columns if c not in ['Posição','Jogador']]
    valores = dados_jogador[colunas].iloc[0].to_dict()

    st.subheader(f"📌 Estatísticas de {jogador_escolhido} ({posicao_escolhida})")

    principais = [c for c in destaques_por_posicao.get(posicao_escolhida, []) if c in valores]

    cols = st.columns(len(principais))
    for i, campo in enumerate(principais):
        val = valores[campo]
        if pd.isna(val):
            val_fmt = "0"
        elif isinstance(val, float) and "Passes Certos" in campo:
            val_fmt = f"{val:.0f}%"
        else:
            val_fmt = f"{val:.0f}" if float(val).is_integer() else f"{val:.1f}"
        with cols[i]:
            st.metric(label=campo, value=val_fmt)

    # Detalhes completos
    st.markdown("### 📋 Detalhes completos")
    extras = [c for c in colunas if c not in principais]
    if extras:
        df_detalhes = pd.DataFrame({
            "Estatística": extras,
            "Valor": [valores[c] if not pd.isna(valores[c]) else "0" for c in extras]
        })
        st.dataframe(df_detalhes, use_container_width=True)
