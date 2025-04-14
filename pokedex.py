# Importações necessárias
import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.pylab import linspace
from IPython.display import display

# Classe para edição do dataset
class Dataset:
    '''Classe usada para criar as funções iniciais para o dataset'''
    def __init__(self, nome_arq=''):
        try:
            self._nome = nome_arq
            self.df = pd.read_csv(self._nome)
            self._arq = True

            for c in self.df.columns.to_list():
                print(c, end=', ')
    
        except:
            print('Arquivo, não encontrado!!!')

    def pokemons(self):
        '''Pokemons Listados por nome'''
        return self.df.Name

    def mostra(self):
        return display(self.df)


    def __str__(self):
        try:
            if self._arq == True:
                return self.df.to_string()
        except:
            return f'Arquivo não Encontrado, Dados indefinidos'

    def grafico(self, linha, coluna):
        # Criando um vetor t usando linspace
        t = linspace(0, len(self.df) - 1, len(self.df))  # Gera t de 0 até o número de linhas - 1

        # Obtenha as colunas de x e y
        x = self.df[coluna]
        y = self.df[linha]

        # Definindo o título do gráfico
        plt.title(f'{coluna} por {linha}')
        plt.grid(True)

        # Plotando x e y com estilos diferentes
        plt.plot(t, y, "bo", label=f'{linha} (azul)')  # Pontos azuis para y
        plt.plot(t, x, "ro", label=f'{coluna} (vermelho)')  # Linha vermelha para x

        # Exibindo a legenda
        plt.legend()

        # Exibindo o gráfico
        plt.show()
        


if __name__ == "__main__" :
    pk = Dataset('Pokemon.csv')
    # print(pk) Teste de Importe do dataframe
    pk.pokemons()
    pk.mostra()
    pk.grafico('HP', 'Attack') # Gráfico quantidade de Pokemons por Geração
    # pk.grafico('Attack') # Gráfico quantidade de Pokemons por Geração
    
    
    

    