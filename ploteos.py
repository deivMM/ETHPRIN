import numpy as np
import matplotlib.pyplot as plt

def plotear_temp(data,thrmcpls_to_plot=False,save=False):
    
    f, ax = plt.subplots(figsize=(10,10))
    
    if not thrmcpls_to_plot: thrmcpls_to_plot = data.columns[1:]
    
    for d in data[thrmcpls_to_plot]:
        ax.plot(data['Time'],data[d],linewidth=.5,label=d)
    
    ax.set_xlabel('Time [mins]',fontsize=12)
    ax.set_ylabel('Temperature $^\circ$C',fontsize=12)
    plt.title('Time - Temperature',fontsize=12)
    
    ax.legend()
    if save: plt.savefig('imagen.png')
    plt.show()

def plotear_displ(data,save=False):
    f, ax = plt.subplots(figsize=(10,10))
    ax.plot(data['Time'],data['Dist'],linewidth=.5,label='Dist')
    ax.set_xlabel('Time [mins]',fontsize=12)
    ax.set_ylabel('Displacement [mm]',fontsize=12)
    plt.title('Time - Displacement',fontsize=12)
    ax.legend()
    if save: plt.savefig('imagen.png')
    plt.show()

def plotear_datos_maquina(data,param,save=False):
    
    f, ax = plt.subplots(figsize=(10,10))

    for pasada in list(data.columns.get_level_values(0).unique()):
        if param == 'Power':
            ax.plot(data[pasada]['Time'],np.sqrt(3)*data[pasada]['Voltage']*data[pasada]['Current'],label=pasada)
        else:
            ax.plot(data[pasada]['Time'],data[pasada][param],label=pasada)
    
    ax.legend()
    plt.show()

def comparar_termopares(pruebas,thrmcpls_to_plot):
    for thrmcpl in thrmcpls_to_plot:
        f, ax = plt.subplots(figsize=(10,10))
        for prueba in pruebas:
            data = pruebas[prueba]
            ax.plot(data[f'Time_{thrmcpl}'],data[thrmcpl],linewidth=.5,label=f'{prueba}_{thrmcpl}')
        ax.set_xlabel('Time [mins]',fontsize=12)
        ax.set_ylabel('Temperature $^\circ$C',fontsize=12)
        plt.title('Time - Temperature',fontsize=12)
        
        ax.legend()
        plt.show()

def plotear_data_vs_data_mod(pruebas,pruebas_mod,thrmcpls):
    for thrmcpl in thrmcpls:
        f, ax = plt.subplots(figsize=(10,10))
        for p in pruebas:
            ax.plot(pruebas[p][f'Time_{thrmcpl}'],pruebas[p][thrmcpl])
            ax.plot(pruebas_mod[p][f'Time_{thrmcpl}'],pruebas_mod[p][thrmcpl])
    plt.show()
   
def plotear_orig_vs_mean(data_orig, data_mean, thrmcpls_to_plot=False):
    if not thrmcpls_to_plot: thrmcpls_to_plot = list(data_orig.values())[0].columns[1::2]
    for n, TC in enumerate(thrmcpls_to_plot):
        f, ax = plt.subplots(figsize=(10,10))
        for d in data_orig:
            ax.plot(data_orig[d][f'Time_{TC}'],data_orig[d][TC],linewidth=.3)
        ax.plot(data_mean[f'Time_mean_{TC}'],data_mean[TC],linewidth=2,color='black',linestyle='--')
    plt.show()