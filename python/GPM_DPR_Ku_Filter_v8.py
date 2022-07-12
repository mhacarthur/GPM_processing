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

import netCDF4
from netCDF4 import Dataset

import warnings
warnings.filterwarnings('ignore')

year = '2019'

def create_netcdf_DPR_Ku(info,heightStormTop,zFactorMeasured,zFactorCorrected,Latitude,Longitude,
                         T_Year,T_Month,T_Day,T_Hour,T_Minute):
    
    ncfile = netCDF4.Dataset(info['file'],mode='w',format='NETCDF4_CLASSIC')

    ncfile.title = info['title']

    # [nscan,nray,nbin]

    nscan_dim, nray_dim, nbin_dim = zFactorMeasured.shape

    nscan = ncfile.createDimension('nscan',nscan_dim)
    nray = ncfile.createDimension('nray',nray_dim)
    nbin = ncfile.createDimension('nbin',nbin_dim)

    var_1 = ncfile.createVariable('NS_PRE_heightStormTop',np.float64,('nscan','nray'),zlib=True)
    var_1.standard_name = 'NS_PRE_heightStormTop'
    var_1.units = 'm'
    var_1[:,:] = heightStormTop

    var_2 = ncfile.createVariable('NS_PRE_zFactorMeasured',np.float64,('nscan','nray','nbin'),zlib=True)
    var_2.standard_name = 'NS_PRE_zFactorMeasured'
    var_2.units = 'dBZ'
    var_2[:,:,:] = zFactorMeasured

    var_3 = ncfile.createVariable('NS_SLV_zFactorCorrected',np.float64,('nscan','nray','nbin'),zlib=True)
    var_3.standard_name = 'NS_SLV_zFactorCorrected'
    var_3.units = 'dBZ'
    var_3[:,:,:] = zFactorCorrected
    
    var_4 = ncfile.createVariable('NS_Latitude',np.float64,('nscan','nray'),zlib=True)
    var_4.standard_name = 'NS_Latitude'
    var_4.units = 'decimal degrees'
    var_4[:,:] = Latitude

    var_5 = ncfile.createVariable('NS_Longitude',np.float64,('nscan','nray'),zlib=True)
    var_5.standard_name = 'NS_Longitude'
    var_5.units = 'decimal degrees'
    var_5[:,:] = Longitude

    var_6 = ncfile.createVariable('NS_ScanTime_Year',np.float64,('nscan'),zlib=True)
    var_6.standard_name = 'NS_ScanTime_Year'
    var_6.units = 'year'
    var_6[:] = T_Year

    var_7 = ncfile.createVariable('NS_ScanTime_Month',np.float64,('nscan'),zlib=True)
    var_7.standard_name = 'NS_ScanTime_Month'
    var_7.units = 'month'
    var_7[:] = T_Month

    var_8 = ncfile.createVariable('NS_ScanTime_Day',np.float64,('nscan'),zlib=True)
    var_8.standard_name = 'NS_ScanTime_Day'
    var_8.units = 'day'
    var_8[:] = T_Day

    var_9 = ncfile.createVariable('NS_ScanTime_Hour',np.float64,('nscan'),zlib=True)
    var_9.standard_name = 'NS_ScanTime_Hour'
    var_9.units = 'hour'
    var_9[:] = T_Hour

    var_10 = ncfile.createVariable('NS_ScanTime_Minute',np.float64,('nscan'),zlib=True)
    var_10.standard_name = 'NS_ScanTime_Minute'
    var_10.units = 'minutes'
    var_10[:] = T_Minute

    ncfile.close()                                                                  

dir_name = '/media/arturo/Seagate Expansion Drive/GPM/list/interception/interception_' + year + '.txt'
with open(dir_name) as f:
    lista = f.read().splitlines() 
print(f'Interception for {year} has {len(lista)} files')
n_digits = len(str(len(lista)))

for f in range(len(lista)):

    filename_split = lista[f].split("/")
    
    file_out = filename_split[7][0:-9] + '.nc'
    file_exi = '/mnt/Data/GPM/data/AS/' + str(year) + '/' + file_out
    
    if f % 100 == 0 or f == 0:
        print(f'{str(f).zfill(n_digits)} de {len(lista)}')
    elif f == len(lista) - 1:
        print(f'{str(f+1).zfill(n_digits)} de {len(lista)}')
    
    if os.path.exists(file_exi) == False:
        
        # print(lista[f])
        
        data = ca.read_netcdf(lista[f],0)

        top = data['NS_PRE_heightStormTop'].data
        zpr = data['NS_PRE_zFactorMeasured'].data
        zsl = data['NS_SLV_zFactorCorrected'].data
        
        top[top==np.min(top)] = np.nan
        zpr[zpr==np.min(zpr)] = np.nan
        zsl[zsl==np.min(zsl)] = np.nan

        mn = data['NS_ScanTime_Minute'].data
        yy = data['NS_ScanTime_Year'].data
        hh = data['NS_ScanTime_Hour'].data
        mm = data['NS_ScanTime_Month'].data
        dd = data['NS_ScanTime_DayOfMonth'].data

        lon = data['NS_Longitude'].data
        lat = data['NS_Latitude'].data
    
        x = np.where(((lon[:,24]>=-90) & (lon[:,24]<=-30) & (lat[:,24]>=-60) & (lat[:,24]<=15)))[0]
        
        top = top[x]
        zpr = zpr[x]
        zsl = zsl[x]
        
        mn = mn[x]
        yy = yy[x]
        hh = hh[x]
        mm = mm[x]
        dd = dd[x]
        
        lon = lon[x]
        lat = lat[x]
       
        info = {'file': file_exi,
                'title': 'GPM DPR Ku'}

        create_netcdf_DPR_Ku(info,top,zpr,zsl,lat,lon,yy,mm,dd,hh,mn)