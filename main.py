import os
import re
import pandas as pd
from pathlib import Path
import data_processing as dproc
import ploteos as plo

path = Path()
################################################################
########## Obtener datos
################################################################

# folders = next(os.walk('.'))[1]
# for folder in folders:
#     dproc.get_TC_part_and_disp_sens_data(folder)
#     dproc.get_TC_clamp_data(folder)
# #     dproc.get_welding_log(folder)
#     print(f'Realizada la carpeta: {folder}')

################################################################
########## plotear termopares
################################################################

# folders = next(os.walk('.'))[1]
# folder = 2
# zona = 'Part' #Part | Clamp
# data = pd.read_csv(path/folders[folder]/f'{zona}_TC_{folders[folder]}.csv')
# plo.plotear_temp(data)

################################################################
########## plotear sensores despl
################################################################

# folders = next(os.walk('.'))[1]
# folder = 6
# data = pd.read_csv(path/folders[folder]/f'Disp_sensor_{folders[folder]}.csv')
# plo.plotear_displ(data)

################################################################
########## comparacion entre termopares
################################################################

# folders = next(os.walk('.'))[1]
# folders = [dr for dr in folders if re.search('6082_0[1-3]_H',dr)] #6082_0[1-3]_H | 2219_0[2-4]_H
# pruebas = {}
# zona = 'Part' #Part | Clamp

# for folder in folders:
#     pruebas[folder] = pd.read_csv(path/folder/f'{zona}_TC_{folder}.csv')

# plo.comparar_termopares(pruebas,['T3'])

################################################################
########## plotear datos maquina
################################################################

# data = pd.read_csv('2219_01_C/welding_log_2219_01_C.csv', header=[0, 1])
# data = pd.read_csv('2219_02_H/welding_log_2219_02_H.csv', header=[0, 1])
# data = pd.read_csv('2219_03_H/welding_log_2219_03_H.csv', header=[0, 1])

# plo.plotear_datos_maquina(data,'X')
# plo.plotear_datos_maquina(data,'Y')
# plo.plotear_datos_maquina(data,'Z')
# plo.plotear_datos_maquina(data,'Power')

################################################################
########## comparar pruebas vs pruebas modificadas
################################################################

folders = next(os.walk('.'))[1]
zona = 'Part' #Part | Clamp
pruebas = {}
pruebas_mod = {}

filtro = '2219_0[2-4]_H'
folders = [dr for dr in folders if re.search(filtro,dr)] #6082_0[1-3]_H | 2219_0[2-4]_H

for folder in folders:
    data = pd.read_csv(path/folder/f'{zona}_TC_{folder}.csv')
    data_mod = dproc.data_processing(data,8)
    for i in range(2,16,2):
        data.insert(i,f'Time_T{int(i/2+1)}',data['Time'])
        data_mod.insert(i,f'Time_T{int(i/2+1)}',data_mod['Time'])
    data.rename(columns = {'Time':'Time_T1'}, inplace = True)
    data_mod.rename(columns = {'Time':'Time_T1'}, inplace = True) 
    pruebas[folder] = data
    pruebas_mod[folder] = data_mod

diff = dproc.get_the_diff(pruebas_mod)

plo.comparar_termopares(pruebas_mod,['T8'])

for npr, p in enumerate(pruebas_mod):
    for nTC, TC in enumerate(data.columns[0::2]):
        pruebas_mod[p][TC] = pruebas_mod[p][TC] - diff[nTC,npr]
plo.comparar_termopares(pruebas_mod,['T8'])

# plo.plotear_data_vs_data_mod(pruebas,pruebas_mod,['T1'])

################################################################
########## obtener medias
################################################################

# data_mean = dproc.get_mean(pruebas_mod,['T1','T2'], dicr = 0.001)
# plo.plotear_orig_vs_mean(pruebas_mod, data_mean, ['T1','T2'])

####### data_mean.to_csv('T1_T8_Mean.csv',index=False)

################################################################
########## voy por aqui 
################################################################


# plo.comparar_termopares(pruebas_mod,['T1'])    
# plo.comparar_termopares(pruebas,['T1','T2'])

# from scipy.interpolate import interp1d
# from functools import reduce
# import numpy as np

# def get_mean(pruebas, dicr = 0.001):
#     data_mean = {}
#     for TC in list(list(pruebas.values())[0].columns)[1::2]:
#         xs =[]
#         ys =[]
#         for  n, p in enumerate(pruebas):
#             xs.append(np.around(np.arange(pruebas[p][f'Time_{TC}'].min(),pruebas[p][f'Time_{TC}'].max(),dicr),3))
#         xnew = reduce(np.intersect1d,xs)
#         data_mean[f'Time_mean_{TC}'] = xnew
#         for  n, p in enumerate(pruebas):
#             f = interp1d(pruebas[p][f'Time_{TC}'], pruebas[p][TC])
#             ys.append(f(xnew))
#         data_mean[TC] = np.mean(ys,0)
#     return pd.DataFrame(dict([(k,pd.Series(v)) for k,v in data_mean.items()]))

# data_mean = get_mean(pruebas_mod)

# plo.plotear_orig_vs_mean(pruebas_mod, data_mean)
# data_mean.to_csv('T1_T8_Mean.csv',index=False)

