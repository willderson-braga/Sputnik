# -*- coding: utf-8 -*-


### VISUALIZAÇÃO DAS OCORRÊNCIAS DA COVID-19 POR CIDADE EM MAPA DE CALOR ###
#
#
# Data de criação: 22/04/2020

# Importação dos pacotes que serão utilizados
# PANDAS: Pacote para manipulação e análise de dados
# FOLIUM: Pacote para manipulação e visualização de dados

import folium
from folium import plugins

import pandas as pd


# Definição dos caminhos dos arquivos
# Arquivo CSS de coordenadas obtido no GitHub do Sandeco
# Arquivo CSS dos dados atualizados da COVID-19 obtido no portal: https://brasil.io
COORDENADAS = 'https://raw.githubusercontent.com/sandeco/CanalSandeco/master/covid-19/cidades_brasil.csv'
DADOS = 'https://brasil.io/dataset/covid19/caso/?format=csv'

# Criação dos DataFrames dos arquivos e renomeação de suas colunas
df_coordenadas = pd.read_csv(COORDENADAS, usecols = (0, 2, 3))
df_coordenadas.rename(columns = {'codigo_ibge': 'id_ibge'}, inplace = True)

df_dados = pd.read_csv(DADOS, usecols = (1, 2, 3, 4, 5, 6, 8))
df_dados.columns = ['estado', 'cidade', 'tipo', 'confirmado', 'mortes', 'final', 'id_ibge']

# Definindo os códigos do IBGE como índice do DataFrame de coordenadas
coordenadas = df_coordenadas.copy()
coordenadas = coordenadas.set_index('id_ibge')

# Filtrando somente as cidades do arquivo do COVID
status_cidades = df_dados.loc[df_dados.tipo == 'city', : ]

# União dos dados de coordenadas e os dados do COVID
status_cidades_coordenada = status_cidades.join(coordenadas, on = 'id_ibge')

# Filtrando somente os dados de status e os campos de interesse
status = status_cidades_coordenada.loc[
	
	status_cidades_coordenada.final == True,
	 
	 [
		'estado',
		'cidade',
		'confirmado',
		'mortes',
		'latitude',
		'longitude'
	]
]

# Filtra somente os dados para plotar os casos confirmados e remove as ocorrência de dados faltantes
confirmados = status[['latitude', 'longitude', 'confirmado']]
confirmados = confirmados.dropna()

# Cria o mapa com localização inicial no Brasil
brasil = [-15.788497, -47.879873]

mapa = folium.Map(

	width = '100%',
	height = '100%',
	zoom_start = 4,
	location = brasil

	)

# ESTILOS DE VISUALIZAÇÃO DO MAPA
# Defina a visualização alterando o índice da variável (estilos)
estilos = ['stamenterrain', 'stamentoner', 'cartodbdark_matter', 'Mapbox Control Room', 'Mapbox Bright']
folium.TileLayer(estilos[3]).add_to(mapa)

# Adiciona ao mapa os pontos de calor
mapa = mapa.add_child(plugins.HeatMap(confirmados))

# Remove as ocorrências que possuem dados faltantes
status = status.dropna()

# Adiciona ao mapa pontos com informações
for i in range(0, len(status)):
	folium.Circle(

		location = [status.iloc[i]['latitude'], status.iloc[i]['longitude']],
		color = '#00FF69',
		fill = '#00A1B3',
		tooltip = '<ul><li><bold> CIDADE: ' + str(status.iloc[i]['cidade']) + '</bold></li> ' +
				  '<li><bold> ESTADO: ' + str(status.iloc[i]['estado']) + '</bold></li> ' +
				  '<li><bold> CASOS HOJE: ' + str(status.iloc[i]['confirmado']) + '</bold></li> ' +
				  '<li><bold> MORTES HOJE: ' + str(status.iloc[i]['mortes']) + '</bold></li></ul>',
		radius = (status.iloc[i]['confirmado'] * 1.1)

	).add_to(mapa)

# Salva o mapa em um arquivo HTML
mapa.save('mapa.html')
