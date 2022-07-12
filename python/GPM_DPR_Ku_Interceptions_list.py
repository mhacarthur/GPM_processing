import os
import glob
import numpy as np
import h5py
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import clima_anom as ca

import gzip as gz

import geopandas as gpd
from shapely.geometry import Polygon
import folium

year = '2019'

lista = glob.glob('/media/arturo/Seagate Expansion Drive/GPM/data/'+ year +'/*.nc4')
lista = np.sort(lista)
n_digits = len(str(len(lista)))

print()
print(f'Year {year} contains {len(lista)} files')

salida = '../list/interception/interception_' + year + '.txt'

print(f'List saved as {salida}')
print()

comm_dir0 = '/mnt/Data/shape/AS_Continent/continent.shp'
continente = gpd.read_file(comm_dir0)
continente = continente.set_crs(epsg=4326, inplace=True)

interception = []

for f in range(len(lista)):
    
    if f % 100 == 0 or f == 0:
        print(f'{str(f).zfill(n_digits)} de {len(lista)}')
    elif f == len(lista) - 1:
        print(f'{str(f+1).zfill(n_digits)} de {len(lista)}')
    
    try:
        
        data = ca.read_netcdf(lista[f],0)

        lat = data['NS_Latitude'].data
        lon = data['NS_Longitude'].data

        x = np.where(((lon[:,24]>=-90) & (lon[:,24]<=-30) & (lat[:,24]>=-60) & (lat[:,24]<=15)))[0]

        lon = lon[x]
        lat = lat[x]

        lon1 = list(lon[:,0])
        lon1.reverse()
        lon2 = list(lon[:,48])
        lon_poly = lon1 + lon2

        lat1 = list(lat[:,0])
        lat1.reverse()
        lat2 = list(lat[:,48])
        lat_poly = lat1 + lat2

        if len(lon_poly) >=3:

            passagem_ref = Polygon(zip(lon_poly,lat_poly))
            passagem = gpd.GeoDataFrame(index=[0], geometry=[passagem_ref])  
            passagem = passagem.set_crs(epsg=4326, inplace=True)

            if passagem.intersects(continente)[0] == True:

                interception.append(lista[f])
                
    except:
        
        print('Dado corrupto: ',f)


with open(salida, 'w') as f:
    for item in interception:
        f.write("%s\n" % item)
f.close()
