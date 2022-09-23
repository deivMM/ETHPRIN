import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from functools import reduce
from pathlib import Path
################################################################
### Funciones
################################################################
### replace_text(path,search_t,repl_t)
### get_TC_part_and_disp_sens_data(folder)
### get_TC_clamp_data(folder)
### get_welding_log(folder)

def replace_text(path,search_t,repl_t):
    with open(path,'r+') as f:
            file = f.read()
            file = re.sub(search_t, repl_t, file)
            f.seek(0)
            f.write(file)
            f.truncate()

def get_TC_part_and_disp_sens_data(folder):
    f_path = path/folder/'Termopares_pieza'
    csv = os.listdir(f_path)
    replace_text(f_path/csv[0],';\n|;$','\n')
    data = pd.read_csv(f_path/csv[0],sep=';')
    data.iloc[:,1:9] = data.iloc[:,1:9]+273.15 #Celsius to Kelvin conversion
    data[['Time']] = (data[['Time']]/60).round(3)
    data.loc[:,:'T8'].round(3).to_csv(f'{folder}/Part_TC_{folder}.csv',index=False)
    data['Dist'] = data['Dist']*10/15233
    data[['Time','Dist']].round(3).to_csv(f'{folder}/Disp_sensor_{folder}.csv',index=False)

def get_TC_clamp_data(folder):
    f_path = path/folder/'Termopares_mordaza'
    dfs = []
    col_names =['T9','T10','T11','T12']
    excels = sorted([f for f in os.listdir(f_path) if f.endswith('.xls')])
    for excel in excels:
        exc_data = pd.read_excel(f_path/excel)
        exc_data = exc_data.iloc[25:,4:]
        exc_data.columns = col_names

        exc_data = exc_data.astype('float')
        dfs.append(exc_data)
        
    data = pd.concat(dfs, ignore_index=True)
    time = np.arange(0,len(data)*0.01,0.01)/60
    data.insert(loc=0, column='Time', value=time)
    data.iloc[:,1:] = data.iloc[:,1:]+273.15 #Celsius to Kelvin conversion
    data.round(3).to_csv(f'{folder}/Clamp_TC_{folder}.csv',index=False)

def get_welding_log(folder):
    col_names = ['Time','Status','Mode','Options','Voltage','Current',
                 'Wire_Speed','Seam_Track','Error','M1','M2','M3','X',
                 'Y','Z','P','GasFlux','Temperature','Wire_Speed_S',
                 'Current_S','Robot_Speed','Distance','dX','dY','dZ',
                 'Gap','Mismatch','Area','Program']
    f_path = path/folder/'Welding_log'
    excels = sorted([f for f in os.listdir(f_path) if f.endswith('.xlsx')])
    
    data = {}
    for n, excel in enumerate(excels):
        exc_data = pd.read_excel(f_path/excel)
        exc_data.columns = col_names
        data[f'Pasada_{n+1}'] = exc_data
        
    data = pd.concat(data.values(), axis=1, keys=data.keys())
    
    data.to_csv(f'{folder}/welding_log_{folder}.csv',index=False)
    
def data_processing(data, wdw = 3, step = None):
    '''
    Agrupa valores en tiempo con un step dado  
    media movil con una ventana dada (wdw)
    df (time|params) -> df modificada (time|params)
    '''
    if not step:
        mod_data = data.groupby('Time').mean().reset_index()
    else:
        mod_data = data.groupby(pd.cut(data['Time'], np.arange(0, data['Time'].max()+step, step))).mean()
        mod_data = mod_data.reset_index(drop=True)
    
    mod_data = mod_data.rolling(wdw).mean()
    mod_data = mod_data.dropna()
    return mod_data 

def get_mean(pruebas,thrmcpls, dicr = 0.001):
    xs =[]
    for p in pruebas:
        xs.append(np.around(np.arange(pruebas[p]['Time'].min(),pruebas[p]['Time'].max(),dicr),3))
        xnew = reduce(np.intersect1d,xs)

    data_mean = {'Time_mean':xnew}
    
    for TC in thrmcpls:
        ys =[]
        for n, p in enumerate(pruebas):
            f = interp1d(pruebas[p]['Time'], pruebas[p][TC])
            ys.append(f(xnew))
        data_mean[f'{TC}_{p}'] = np.mean(ys,0)
    return pd.DataFrame(data_mean)
    
def get_the_diff(pruebas):
    dist = []
    for prueba in pruebas:
        data = pruebas[prueba]
        dist_TC = []
        for TC in data.columns[1::2]:
            idmax = data[data[f'Time_{TC}']<0.5][TC].idxmax()
            Time_max = data[f'Time_{TC}'][idmax]
            dist_TC.append(Time_max)
        dist.append(dist_TC)
    dist = np.array(dist)
    return (dist- dist.min(0)).T
path = Path()