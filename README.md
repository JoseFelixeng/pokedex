
# Pokédex 

Uma Pokédex interativa desenvolvida em **Python** utilizando **Streamlit**, **Plotly** e **Pandas**, que permite explorar, visualizar e comparar Pokémons de forma interativa com gráficos e filtros dinâmicos.

---

## 🚀 Funcionalidades

- 🔍 Filtro por:
  - **Tipo 1**
  - **Geração**
  - **Pokémons Lendários ou Não**

- ⚔️ **Comparação entre dois Pokémons**:
  - Imagens lado a lado
  - Informações detalhadas
  - Gráficos de barras
  - Gráficos radar
  - Tabela comparativa de atributos

- 📊 Análises:
  - Quantidade de Pokémons por geração
  - Quantidade de Pokémons por tipo (Type 1 e Type 2)
  - Heatmap de geração vs tipo
  - Quantidade de lendários vs não lendários (barra e pizza)

---

## 📂 Estrutura de Pastas

```
├── pokemon.csv                  # Base de dados com informações dos Pokémons
├── pokemon_images/              # Pasta com as imagens dos Pokémons
├── pokedex.py                   # Código principal do Streamlit
├── README.md                    # Este arquivo
├── requirements.txt             # Dependências do projeto
└── pokeball.png                 # Logo exibido no topo
```

---

## 🔧 Instalação Local

1. **Clone este repositório**

```bash

cd pokedex
```

2. **Crie um ambiente virtual (opcional)**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**

```bash
streamlit run pokedex.py
```

---

## 🧠 Como usar

- Use a barra lateral para filtrar Pokémons por **tipo**, **geração** e se são **lendários**.
- Compare dois Pokémons escolhendo seus nomes.
- Visualize gráficos comparativos, heatmaps e distribuições.
- As imagens dos Pokémons devem estar na pasta `/pokemon_images/` e o arquivo de dados `pokemon.csv` na raiz.

---



## 🔗 Créditos

- Dataset: https://www.kaggle.com/datasets/abcsds/pokemon
- Imagens: Coletadas da internet para fins educacionais.

---

## 🚀 Desenvolvido por
  - José Felix 
  - Flavio José