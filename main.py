# pip install streamlit pandas matplotlib seaborn
import pandas as pd
import streamlit as st
import altair as alt

# importar dados e fazer limpeza
df = pd.read_csv('https://raw.githubusercontent.com/luisctorrens/amazon_prime_superdata/main/amazon_prime_titles.csv')
df.columns = ['id', 'tipo', 'titulo',
              'diretor', 'elenco',
              'pais','data', 'ano',
              'classificacao','duration',
              'categoria', 'descricao']
df.drop(columns=['id', 'data'], inplace=True)
df['ano'] = df['ano']
# listar paises únicos
paises = pd.unique(df['pais'])
paises_unicos = set()
for pais in paises:
    try:
        nomes = pais.split(', ')
        for nome in nomes:
            paises_unicos.add(nome)
    except:
        continue

# listar tipos
tipos = pd.unique(df['tipo'])

tab_df, tab_dash = st.tabs(['Dados', 'Dashboard'])

with tab_df:
    # adicionar filtros
    tipos_selecionados = st.multiselect('Tipos', tipos)
    paises_selecionados = st.multiselect('País', paises_unicos)

    # filtrar tipo
    if len(tipos_selecionados) == 1:
        df = df.query(f'tipo == "{tipos_selecionados[0]}"')
    # filtrar pais
    if len(paises_selecionados) > 0:
        df = df.query("pais in @paises_selecionados")

    st.dataframe(df, hide_index=True, column_config={'ano': st.column_config.NumberColumn(format='%d')})
with tab_dash:
    df_agrupado_ano = pd.DataFrame(df.groupby(['ano']).size())
    df_agrupado_ano.columns = ['quantidade']
    st.subheader('Títulos por ano')
    transparencia = st.slider('Transparencia',min_value=0.2, max_value=1.0, value=0.5, step=0.01)
    st.area_chart(df_agrupado_ano, use_container_width=True, color=(255, 255, 255, transparencia))

    df_agrupado_tipo = pd.DataFrame(df.groupby(['tipo']).size())
    df_agrupado_tipo.columns = ['quantidade']
    st.bar_chart(df_agrupado_tipo, use_container_width=True, color=(255, 255, 255, 0.9))

    st.divider()

    # categoria
    categorias = pd.unique(df['categoria'])
    lista_categorias = set()
    for linha in categorias:
        itens = linha.split(', ')
        for item in itens:
            lista_categorias.add(item)

    contagem_categorias = {}
    for categoria in lista_categorias:
        contagem_categorias[categoria] = df['categoria'].str.contains(categoria).sum()

    contagem_categorias['Culture'] = contagem_categorias['and Culture']
    contagem_categorias.pop('Culture')
    st.write(contagem_categorias)
