# -*- coding: utf-8 -*-

### VISUALIZAÇÃO DAS OCORRÊNCIAS DA COVID-19 POR CIDADE  ###
#
# Data de criação: 12/10/2020
# Importação dos pacotes que serão utilizados
# PANDAS: Pacote para manipulação e análise de dados
# FOLIUM: Pacote para manipulação e visualização de dados

import pandas as pd
import numpy as np

import requests

import folium
from folium import plugins


# Definição dos caminhos dos arquivos
# Arquivo CSS de coordenadas obtido no GitHub 
# Arquivo CSS dos dados atualizados da COVID-19 obtido no portal: https://brasil.io

df = pd.read_csv('C:\Covid19\caso.csv')

cidades = pd.read_csv('https://raw.githubusercontent.com/sandeco/CanalSandeco/master/covid-19/cidades_brasil.csv')

cidades = cidades.set_index('codigo_ibge')

 cities = df.loc[df.place_type =='city', :]
cities.place_type.unique()
  
array(['city'], dtype=object)

  
cities = cities.join(cidades, on='city_ibge_code')

geo_last = cities.loc[cities.is_last==True , ['city', 'latitude', 'longitude', 'state', 'confirmed', 'deaths'] ]


len(geo_last)

geo_last.state.unique()


len(geo_last.state.unique())

coordenadas = geo_last[['latitude', 'longitude', 'confirmed']]

coordenadas = coordenadas.dropna()

baseMap = folium.Map(
                 width="100%",
                 height="100%",
                 location=[-15.788497, -47.879873],
                 zoom_start=4
)


geo_last = geo_last.dropna()
geo_last


geo_last.iloc[0]['latitude']



for i in range(0, len(geo_last)):
    folium.Circle(
        location = [  geo_last.iloc[i]['latitude']   ,geo_last.iloc[i]['longitude']],
        color   = '#00FF69',
        fill    = '#00A1B3',
        tooltip = '<li><bold> CIDADE: ' + str(geo_last.iloc[i]['city']) +    "</bold></li>"+
              '<li><bold> ESTADO: ' + str(geo_last.iloc[i]['state']) +       "</bold></li>"+
              '<li><bold> CASOS : ' + str(geo_last.iloc[i]['confirmed']) +   "</bold></li>"+
              '<li><bold> MORTES: ' + str(geo_last.iloc[i]['deaths']) +      "</bold></li></ul>",
        radius  =  (geo_last.iloc[i]['confirmed'] * 0.33) 

    ).add_to(baseMap)
    
    
# Salva o mapa em um arquivo HTML
baseMap.save('mapa.html')
