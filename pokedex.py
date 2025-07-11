import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
import numpy as np

# ------------------------- Configuração da Página -------------------------
st.set_page_config(page_title="Pokédex", layout="wide")

# ------------------------- Arquivos de música -------------------------
# Pasta com arquivos de música (formatos suportados: mp3, wav, etc.)
MUSIC_FOLDER = "music"
musicas = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]

# ------------------------- Inicializar o estado -------------------------
if "musica_atual" not in st.session_state:
    st.session_state.musica_atual = 0
if "tocando" not in st.session_state:
    st.session_state.tocando = False

# ------------------------- Funções dos botões -------------------------
def proxima_musica():
    st.session_state.musica_atual = (st.session_state.musica_atual + 1) % len(musicas)

def musica_anterior():
    st.session_state.musica_atual = (st.session_state.musica_atual - 1) % len(musicas)

def toggle_play():
    st.session_state.tocando = not st.session_state.tocando

# ------------------------- Interface -------------------------
st.title("🎵 PokePlayer 🎵")

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.button("⏮ Anterior", on_click=musica_anterior)
with col2:
    st.button("▶ Tocar / Pausar", on_click=toggle_play)
with col3:
    st.button("⏭ Próxima", on_click=proxima_musica)

# ------------------------- Reproduzir Música -------------------------
musica = musicas[st.session_state.musica_atual]
caminho_musica = os.path.join(MUSIC_FOLDER, musica)

st.markdown(f"**Tocando agora:** 🎶 `{musica}`")

if st.session_state.tocando:
    audio_file = open(caminho_musica, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')
else:
    st.info("▶ Pressione Tocar para ouvir a música.")


# ------------------------- Carregar Dados -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('pokemon.csv')
    df.columns = df.columns.str.strip()  # Remove espaços dos nomes das colunas
    return df

df = load_data()

# ------------------------- Machine Learning (K-means) -------------------------
# Pré-processamento dos dados
features = df[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Aplicar K-means
kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
clusters = kmeans.fit_predict(scaled_features)
df['Cluster'] = clusters

# ------------------------- Treinar modelo de classificação (Lendário) -------------------------
@st.cache_data
def train_model():
    X = df[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']]
    y = df['Legendary']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

model = train_model()

# ------------------------- Sidebar - Filtros -------------------------

st.sidebar.header("🔍 Filtros")

# Filtro por Tipo 1

tipos = sorted(df['Type 1'].dropna().unique())
tipo_selecionado = st.sidebar.multiselect("Filtrar por Tipo 1", tipos, default=tipos)

# Filtro por Geração
geracoes = sorted(df['Generation'].unique())
geracao_selecionada = st.sidebar.multiselect("Filtrar por Geração", geracoes, default=geracoes)


# Filtro por Lendário
lendario_opcao = st.sidebar.selectbox("Lendário?", ["Sim", "Não"])

# Aplicar filtros
df_filtrado = df[
    (df['Type 1'].isin(tipo_selecionado)) &
    (df['Generation'].isin(geracao_selecionada))
]

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

# Mostrar as imagens lado a lado
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
    col.write(f"**Grupo (Cluster):** {poke['Cluster']}")

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
df_geracao = df['Generation'].value_counts().reset_index()
df_geracao.columns = ['Generation', 'Count']
df_geracao = df_geracao.sort_values('Generation')

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

# -------------------- Tabela cruzada --------------------
st.subheader("📊 Pokémons por Geração e Tipo 1")
cross_tab = pd.crosstab(df['Generation'], df['Type 1'])
fig = px.imshow(
    cross_tab,
    text_auto=True,
    labels=dict(x="Tipo", y="Geração", color="Quantidade"),
    color_continuous_scale="Blues"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Pokémons por Geração e Tipo 2")
cross_tab = pd.crosstab(df['Generation'], df['Type 2'])
fig = px.imshow(
    cross_tab,
    text_auto=True,
    labels=dict(x="Tipo", y="Geração", color="Quantidade"),
    color_continuous_scale="Blues"
)
st.plotly_chart(fig, use_container_width=True)

# -------------------- Pokémons Lendários --------------------
df_lendario = df['Legendary'].value_counts().reset_index()
df_lendario.columns = ['Lendário', 'Quantidade']
df_lendario['Lendário'] = df_lendario['Lendário'].map({True: 'Lendário', False: 'Não Lendário'})

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
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

fig = px.pie(
    df_lendario,
    names='Lendário',
    values='Quantidade',
    hole=0.4,
    color='Lendário',
    template='plotly_dark'
)
st.plotly_chart(fig, use_container_width=True)

# ------------------------- Agrupamento de Pokémons (K-means) -------------------------
st.header("🤖 Agrupamento de Pokémons por Similaridade")
st.write("""
Os Pokémons foram agrupados em 6 categorias usando o algoritmo K-means com base em seus atributos:
- **HP, Ataque, Defesa, Ataque Especial, Defesa Especial e Velocidade**
""")

# Seletor para escolher um cluster
cluster_selecionado = st.selectbox("Selecione um grupo para visualizar:", sorted(df['Cluster'].unique()))

# Filtrar Pokémons do cluster selecionado
cluster_df = df[df['Cluster'] == cluster_selecionado]

# Mostrar estatísticas do cluster
st.subheader(f"📊 Estatísticas do Grupo {cluster_selecionado}")
cluster_stats = cluster_df[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].mean().reset_index()
cluster_stats.columns = ['Atributo', 'Valor Médio']

fig = px.bar(
    cluster_stats,
    x='Atributo',
    y='Valor Médio',
    text='Valor Médio',
    title=f'Atributos Médios do Grupo {cluster_selecionado}',
    template='plotly_dark'
)
fig.update_traces(texttemplate='%{y:.1f}', textposition='outside')
st.plotly_chart(fig, use_container_width=True)

# Mostrar Pokémons do cluster
st.subheader(f"🧩 Pokémons do Grupo {cluster_selecionado}")
st.dataframe(cluster_df[['Name', 'Type 1', 'Type 2', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']])

# Visualização dos clusters (PCA para redução de dimensionalidade)
st.subheader("🌌 Visualização dos Grupos (2D)")

# Reduzir para 2 dimensões usando PCA
pca = PCA(n_components=2)
reduced_features = pca.fit_transform(scaled_features)
df['PCA1'] = reduced_features[:, 0]
df['PCA2'] = reduced_features[:, 1]

# Plot
fig = px.scatter(
    df,
    x='PCA1',
    y='PCA2',
    color='Cluster',
    hover_name='Name',
    title='Visualização dos Grupos de Pokémons',
    template='plotly_dark',
    labels={'PCA1': 'Componente Principal 1', 'PCA2': 'Componente Principal 2'}
)
st.plotly_chart(fig, use_container_width=True)

# ------------------------ Descrição dos Clusters ------------------------
st.subheader("📝 Características dos Grupos")
cluster_descriptions = {
    0: "Pokémons equilibrados - Atributos médios em todas as categorias",
    1: "Especialistas em Defesa - Alta defesa e HP, ataque moderado",
    2: "Ataque Puro - Alto ataque físico, baixa defesa especial",
    3: "Velocistas - Alta velocidade, atributos moderados",
    4: "Tanques - Alta defesa e HP, baixa velocidade",
    5: "Poderosos - Altos valores em todos os atributos (Lendários)"
}

selected_cluster_desc = cluster_descriptions.get(cluster_selecionado, "Descrição não disponível")
st.info(f"**Grupo {cluster_selecionado}:** {selected_cluster_desc}")

# ------------------------- Previsão de Lendário -------------------------
st.header("🔮 Prever se um Pokémon é Lendário")
st.write("Insira os atributos de um Pokémon para prever se ele é lendário:")

col1, col2, col3 = st.columns(3)
with col1:
    hp = st.number_input("HP", min_value=1, max_value=255, value=50)
    attack = st.number_input("Ataque", min_value=1, max_value=255, value=50)
with col2:
    defense = st.number_input("Defesa", min_value=1, max_value=255, value=50)
    sp_atk = st.number_input("Ataque Especial", min_value=1, max_value=255, value=50)
with col3:
    sp_def = st.number_input("Defesa Especial", min_value=1, max_value=255, value=50)
    speed = st.number_input("Velocidade", min_value=1, max_value=255, value=50)

if st.button("Prever"):
    input_data = [[hp, attack, defense, sp_atk, sp_def, speed]]
    prediction = model.predict(input_data)[0]
    prediction_proba = model.predict_proba(input_data)[0]
    
    if prediction:
        st.success("Este Pokémon é classificado como **Lendário**!")
    else:
        st.info("Este Pokémon é classificado como **Não Lendário**.")
    
    st.write(f"Probabilidade: {prediction_proba[1]*100:.2f}% de ser lendário, {prediction_proba[0]*100:.2f}% de não ser lendário.")

# ------------------------ Ocultar Menu e Footer do Streamlit ------------------------
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)