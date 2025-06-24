import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import os

# ------------------------- Configuração da Página -------------------------
st.set_page_config(page_title="Pokédex", layout="wide")

# ------------------------- Carregar Dados -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('pokemon.csv')
    df.columns = df.columns.str.strip()  # Remove espaços dos nomes das colunas
    return df

df = load_data()

# ------------------------- Sidebar - Filtros -------------------------
st.sidebar.header("🔍 Filtros")

# Filtro por Tipo 1
tipos = sorted(df['Type 1'].dropna().unique())
tipo_selecionado = st.sidebar.multiselect("Filtrar por Tipo 1", tipos, default=tipos)

# Filtro por Geração
geracoes = sorted(df['Generation'].unique())
geracao_selecionada = st.sidebar.multiselect("Filtrar por Geração", geracoes, default=geracoes)

# Filtro por Lendário
lendario_opcao = st.sidebar.selectbox("Lendário?", ["Todos", "Sim", "Não"])

# Aplicar filtros
df_filtrado = df[
    (df['Type 1'].isin(tipo_selecionado)) &
    (df['Generation'].isin(geracao_selecionada))
]

# ------------------------- Selecionar Pokémons -------------------------


if lendario_opcao == "Sim":
    df_filtrado = df_filtrado[df_filtrado['Legendary'] == True]
elif lendario_opcao == "Não":
    df_filtrado = df_filtrado[df_filtrado['Legendary'] == False]

st.sidebar.subheader("🔸 Escolha os Pokémons para comparar")
pokemon1 = st.sidebar.selectbox("Escolha o primeiro Pokémon", df_filtrado['Name'].unique())
pokemon2 = st.sidebar.selectbox("Escolha o segundo Pokémon", df_filtrado['Name'].unique())

poke1 = df[df['Name'] == pokemon1].iloc[0]
poke2 = df[df['Name'] == pokemon2].iloc[0]




# ------------------------- Titulo ---------------------------------
st.image("pokeball.png") 
st.title("Pokedex")

# ------------------------- Exibir Imagens -------------------------

def get_image_path(name, id):
    if name.startswith('Mega'):
        if name.endswith(' X'):
            path = 'pokemon_images/' + str(id) + '-mega-x.png'
        elif name.endswith(' Y'):
            path = 'pokemon_images/' + str(id) + '-mega-y.png'
        else:
            path = 'pokemon_images/' + str(id) + '-mega.png'
    elif name.endswith(' Rotom'):
        rotom_type = name.split()[0].lower()
        path = 'pokemon_images/' + str(id) + '-' + rotom_type + '.png'
    elif name.endswith(' Forme') or name.endswith(' Cloak')  or name.endswith(' Form'):
        if 'Zygarde' in name:
            path = 'pokemon_images/' + str(id) + '.png'				
        else:
            type = name.split()[1].lower()
            path = 'pokemon_images/' + str(id) + '-' + type + '.png'
    elif name.startswith('Primal '):
        type = name.split()[0].lower()
        path = 'pokemon_images/' + str(id) + '-' + type + '.png'
    elif name.startswith('Arceus'): 
        path = 'pokemon_images/' + str(id) + '-normal.png'
    else:
        path = 'pokemon_images/' + str(id) + '.png'
    return path


# 📸 Mostrar as imagens lado a lado

col_img1, col_img2 = st.columns(2)

path1 = get_image_path(poke1['Name'], poke1['#'])
if os.path.exists(path1):
    col_img1.image(path1, caption=poke1['Name'], width=200)
else:
    col_img1.warning(f"Imagem de {poke1['Name']} não encontrada.")

path2 = get_image_path(poke2['Name'], poke2['#'])
if os.path.exists(path2):
    col_img2.image(path2, caption=poke2['Name'], width=200)
else:
    col_img2.warning(f"Imagem de {poke2['Name']} não encontrada.")


# ------------------------- Exibir Informações -------------------------
col1, col2 = st.columns(2)

def show_info(col, poke):
    col.subheader(f"🔹 {poke['Name']}")
    col.write(f"**Tipo 1:** {poke['Type 1']}")
    if poke['Type 2']:
        col.write(f"**Tipo 2:** {poke['Type 2']}")
    else:
        col.write("**Tipo 2:** Nenhum")
    col.write(f"**HP:** {poke['HP']}")
    col.write(f"**Ataque:** {poke['Attack']}")
    col.write(f"**Defesa:** {poke['Defense']}")
    col.write(f"**Ataque Especial:** {poke['Sp. Atk']}")
    col.write(f"**Defesa Especial:** {poke['Sp. Def']}")
    col.write(f"**Velocidade:** {poke['Speed']}")
    col.write(f"**Geração:** {poke['Generation']}")
    col.write(f"**Lendário:** {'Sim' if poke['Legendary'] else 'Não'}")

show_info(col1, poke1)
show_info(col2, poke2)

# ------------------------ Gráfico de Barras - Comparação ------------------------
st.subheader("📊 Gráfico de Barras - Comparação de Status")

stats = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
poke1_stats = [poke1[stat] for stat in stats]
poke2_stats = [poke2[stat] for stat in stats]

fig_bar = go.Figure()

fig_bar.add_trace(go.Bar(
    x=stats,
    y=poke1_stats,
    name=pokemon1,
    marker_color='royalblue'
))

fig_bar.add_trace(go.Bar(
    x=stats,
    y=poke2_stats,
    name=pokemon2,
    marker_color='firebrick'
))

fig_bar.update_layout(
    title='Comparação dos Status dos Pokémons',
    xaxis_title='Atributos',
    yaxis_title='Valor dos Status',
    barmode='group',
    template='plotly_dark',
    height=500
)

st.plotly_chart(fig_bar, use_container_width=True)


# ------------------------ Radar Chart - Comparação ------------------------
st.subheader("🕸️ Radar Chart - Comparação de Status")

fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=poke1_stats,
    theta=stats,
    fill='toself',
    name=pokemon1
))

fig_radar.add_trace(go.Scatterpolar(
    r=poke2_stats,
    theta=stats,
    fill='toself',
    name=pokemon2
))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, max(max(poke1_stats), max(poke2_stats)) + 20]
        )),
    showlegend=True,
    template='plotly_dark'
)

st.plotly_chart(fig_radar, use_container_width=True)

# ------------------------ Tabela Comparativa ------------------------
st.subheader("📋 Tabela Comparativa dos Status")

df_compare = pd.DataFrame({
    pokemon1: poke1_stats,
    pokemon2: poke2_stats
}, index=stats)

st.table(df_compare)


# ------------------- Quantidade de pokemons por geração ---------------------------------


# Contar quantos Pokémons existem por geração
df_geracao = df['Generation'].value_counts().reset_index()
df_geracao.columns = ['Generation', 'Count']
df_geracao = df_geracao.sort_values('Generation')

# Criar gráfico de barras
fig = px.bar(
    df_geracao,
    x='Generation',
    y='Count',
    text='Count',
    title='Quantidade de Pokémons por Geração',
    labels={'Generation': 'Geração', 'Count': 'Quantidade'},
    template='plotly_dark'
)

fig.update_traces(textposition='outside')
fig.update_layout(
    xaxis=dict(type='category'),
    yaxis_title="Quantidade de Pokémons"
)

st.subheader("📊 Quantidade de Pokémons por Geração")
st.plotly_chart(fig, use_container_width=True)


# -------------------- Sidebar para escolher Type 1 ou Type 2 --------------------
st.sidebar.subheader("⚙️ Selecione o tipo")
tipo_escolhido = st.sidebar.selectbox("Tipo Base", ["Type 1", "Type 2"])

# Filtrar pokémons que possuem valor no tipo escolhido
df_filtrado = df[df[tipo_escolhido].notna()]

# -------------------- Agrupar dados --------------------
df_tipo = df_filtrado[tipo_escolhido].value_counts().reset_index()
df_tipo.columns = ['Tipo', 'Quantidade']
df_tipo = df_tipo.sort_values('Quantidade', ascending=False)

# -------------------- Plotar gráfico --------------------
fig = px.bar(
    df_tipo,
    x='Tipo',
    y='Quantidade',
    text='Quantidade',
    title=f'📊 Quantidade de Pokémons por {tipo_escolhido}',
    labels={'Quantidade': 'Quantidade de Pokémons', 'Tipo': 'Tipo'},
    template='plotly_dark'
)

fig.update_traces(textposition='outside')
fig.update_layout(
    xaxis=dict(type='category'),
    yaxis_title="Quantidade de Pokémons"
)

st.subheader(f"📊 Quantidade de Pokémons por {tipo_escolhido}")
st.plotly_chart(fig, use_container_width=True)

# Tabela cruzada entre Geração e Tipo 1
cross_tab = pd.crosstab(df['Generation'], df['Type 1'])

fig = px.imshow(
    cross_tab,
    text_auto=True,
    labels=dict(x="Tipo", y="Geração", color="Quantidade"),
    title="📊 Quantidade de Pokémons por Geração e Tipo (Type 1)",
    color_continuous_scale="Blues"
)

st.subheader("📊 Pokémons por Geração e Tipo 1")
st.plotly_chart(fig, use_container_width=True)


cross_tab = pd.crosstab(df['Generation'], df['Type 1'])

fig = px.imshow(
    cross_tab,
    text_auto=True,
    labels=dict(x="Tipo", y="Geração", color="Quantidade"),
    title="📊 Quantidade de Pokémons por Geração e Tipo (Type 2)",
    color_continuous_scale="Blues"
)

st.subheader("📊 Pokémons por Geração e Tipo 2")
st.plotly_chart(fig, use_container_width=True)


import plotly.express as px
import pandas as pd
import streamlit as st


df_lendario = df['Legendary'].value_counts().reset_index()
df_lendario.columns = ['Lendário', 'Quantidade']
df_lendario['Lendário'] = df_lendario['Lendário'].map({True: 'Lendário', False: 'Não Lendário'})

# -------------------- Gráfico de Barras --------------------
fig = px.bar(
    df_lendario,
    x='Lendário',
    y='Quantidade',
    text='Quantidade',
    title="📊 Quantidade de Pokémons Lendários vs Não Lendários",
    color='Lendário',
    template='plotly_dark'
)

fig.update_traces(textposition='outside')
fig.update_layout(
    yaxis_title="Quantidade de Pokémons",
    xaxis_title="Categoria",
    showlegend=False
)

st.subheader("📊 Pokémons Lendários vs Não Lendários")
st.plotly_chart(fig, use_container_width=True)

fig = px.pie(
    df_lendario,
    names='Lendário',
    values='Quantidade',
    hole=0.4,
    color='Lendário',
    template='plotly_dark'
)

st.subheader("🥧 Pokémons Lendários vs Não Lendários")
st.plotly_chart(fig, use_container_width=True)



# ------------------------ Ocultar Menu e Footer do Streamlit ------------------------
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)