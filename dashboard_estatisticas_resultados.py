
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Carregar as planilhas
@st.cache_data
def load_data():
    df_dashboard = pd.read_excel('planilha_com_novos_nomes_jogadores_atualizada.xlsx')
    df_resultados = pd.read_excel('modelo_resultados_dashboard_preenchido.xlsx', engine='openpyxl')
    df_estatisticas = pd.read_excel("estatisticas_jogadores_formatado.xlsx")
    return df_dashboard, df_resultados, df_estatisticas

# Carregar os dados
df_dashboard, df_resultados, df_estatisticas = load_data()

# Configuração da página
st.set_page_config(page_title="Staking Team eSports", layout="wide")

# Menu de navegação
tab = st.sidebar.radio("Escolha a aba", ["Dashboard", "Estatísticas Gerais", "Resultados"])

if tab == "Dashboard":
    # Aba Dashboard
    st.title("📊 Dashboard de Jogadores")

    # Filtros
    filtro_mes = st.selectbox('Escolha o Mês:', df_dashboard['Mês'].unique())
    filtro_posicao = st.selectbox('Escolha a Posição:', df_dashboard['Posição'].unique())

    df_filtrado = df_dashboard[(df_dashboard['Mês'] == filtro_mes) & (df_dashboard['Posição'] == filtro_posicao)]

    filtro_semana = st.selectbox('Escolha a Semana:', ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4'])
    filtro_dia = st.selectbox('Escolha o Dia:', [1, 2, 3])

    if filtro_semana in df_filtrado['Semana'].values:
        df_filtrado = df_filtrado[df_filtrado['Semana'] == filtro_semana]
    df_filtrado = df_filtrado[df_filtrado['Dia'] == filtro_dia]

    filtro_jogo = st.selectbox('Escolha o Jogo:', ['21:40:00', '22:10:00', '22:40:00', '23:10:00', '23:40:00'])
    df_filtrado = df_filtrado[df_filtrado['Jogo'] == filtro_jogo]

    colunas_por_posicao = {
        'GK': ['Defesas', 'Cleansheet', 'Gols Sofridos', '% Passe Certos', 'Total Passes'],
        'ZAG': ['Gols', 'Assistências', '% Passe Certos', 'Total Passes', 'Posses Ganhas', 'Posses Perdidas', 'Cleansheet'],
        'MC': ['Gols', 'Assistências', '% Passe Certos', 'Total Passes', 'Posses Ganhas', 'Posses Perdidas', 'Finalizações'],
        'ALA': ['Gols', 'Assistências', '% Passe Certos', 'Total Passes', 'Posses Ganhas', 'Posses Perdidas', 'Finalizações'],
        'ST': ['Gols', 'Assistências', '% Passe Certos', 'Total Passes', 'Posses Ganhas', 'Posses Perdidas', 'Finalizações']
    }

    colunas_disponiveis = [col for col in colunas_por_posicao.get(filtro_posicao, []) if col in df_filtrado.columns]

    st.write(df_filtrado)

    if not df_filtrado.empty and len(colunas_disponiveis) > 0:
        opcao = st.selectbox(f"{filtro_posicao} - Escolha um dado:", colunas_disponiveis, key=filtro_posicao)
        fig = px.bar(df_filtrado, x='Jogador', y=opcao, title=f"{opcao} por jogador")
        st.plotly_chart(fig)

elif tab == "Estatísticas Gerais":
    # Aba Estatísticas Gerais
    st.title("Estatísticas Gerais - Jogadores")
    st.header("Estatísticas por Posição e Jogador")

    # Filtro de Posição
    posicoes = df_estatisticas['Posição'].unique()
    posicao_escolhida = st.selectbox("Escolha a Posição:", posicoes)

    # Filtro de Jogador
    jogadores_posicao = df_estatisticas[df_estatisticas['Posição'] == posicao_escolhida]['Jogador']
    jogador_escolhido = st.selectbox("Escolha o Jogador:", jogadores_posicao)

    # Filtrar os dados para o jogador escolhido
    dados_jogador = df_estatisticas[(df_estatisticas['Posição'] == posicao_escolhida) & (df_estatisticas['Jogador'] == jogador_escolhido)]

    # Definir as colunas para cada posição
    if posicao_escolhida == "GK":
        colunas = ['Defesas', 'Gols Sofridos', 'Cleansheet', '% Passes Certos', 'Total Passes']
    elif posicao_escolhida == "ZAG":
        colunas = ['% Passes Certos', 'Total Passes', 'Posses Ganhas', 'Posses Perdidas', 'Cleansheet']
    elif posicao_escolhida == "MC":
        colunas = ['% Passes Certos', 'Total Passes', 'Posses Ganhas', 'Posses Perdidas', 'Gols', 'Assistências', 'Finalizações', 'Nota Média']
    elif posicao_escolhida == "ALA":
        colunas = ['Gols', 'Assistências', 'Finalizações', '% Passes Certos', 'Posses Ganhas', 'Posses Perdidas', 'Nota Média']
    elif posicao_escolhida == "ST":
        colunas = ['Gols', 'Assistências', 'Finalizações', '% Passes Certos', 'Posses Ganhas', 'Posses Perdidas', 'Nota Média']

    # Exibir as estatísticas selecionadas para o jogador escolhido
    st.write(f"Estatísticas para o jogador {jogador_escolhido}:")

    # Exibir a tabela
    st.dataframe(dados_jogador[colunas])

    # Substituir NaN por 0 para garantir que o gráfico funcione sem erros
    dados_jogador_numericos = dados_jogador[colunas].fillna(0)

    # Gráficos para algumas estatísticas
    fig, ax = plt.subplots(figsize=(8, 5))
    dados_jogador_numericos.plot(kind='bar', ax=ax)
    ax.set_title(f"Gráficos Estatísticos para {jogador_escolhido}")
    ax.set_ylabel('Valores')
    ax.set_xlabel('Estatísticas')

    # Exibir gráfico
    st.pyplot(fig)

elif tab == "Resultados":
    # Aba Resultados
    st.title('Resultado das Partidas')

    # Filtros
    st.header('Filtros')

    mes = st.selectbox('Escolha o Mês', df_resultados['Mês'].unique())
    semana = st.selectbox('Escolha a Semana', [1, 2, 3, 4])
    dia = st.selectbox('Escolha o Dia', [1, 2, 3])

    df_filtrado = df_resultados[(df_resultados['Mês'] == mes) & (df_resultados['Semana'] == semana) & (df_resultados['Dia'] == dia)]

    df_filtrado = df_filtrado.drop(columns=["Jogo"])

    st.write(f'Resultados filtrados para o mês {mes}, semana {semana} e dia {dia}:', df_filtrado)
