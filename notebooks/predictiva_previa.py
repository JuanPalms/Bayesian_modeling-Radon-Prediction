"""
Este modulo de python ajusta la predictiva previa y genera N=978 * 1000 simulaciones y establece una funcion para graficar la previa
"""
import os
import pandas as pd
import numpy as np
from cmdstanpy import CmdStanModel
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from outils import load_config

# Load config file calling load_config function
config_f = load_config("config.yaml")

def ajuste_previa_predictiva(archivo, modelstring, data):
    """
    Genera simulaciones de la predictiva previa
    Args: 
    archivo (string): nombre del archivo stan en el que se guardara el modelo
    modelstring (strin): string del modelo en codigo de stan
    data(dictionary): dictionnary containing data to fit stan model
    Returns:
    summary(pandas dataframe): dataframe con resultados de diagnostico de las simulaciones
    y_sim_df(pandas dataframe): dataframe con las 900 y pico simulaciones generadas
    y_sim_original(numpy array): array con las simulaciones en su escala orignal (picuries)
    column_means(array): promedio de cada una de la simulaciones de las 900 observaciones
    column_max: observaciones maximas de cada una de las simulaciones de las 900 observaciones
    column_min: observaciones minimas de cada una de las simulaciones de las 900 observaciones
    pct_95: percentil 95 de cada una de las simulaciones de las 900 observaciones
    pct_99: percentil 99 de cada una de las simulaciones de las 900 observaciones
    """
    # Creo el archivo de Stan
    modelo = os.path.join(config_f["models_directory"], archivo)
    with open(modelo, 'w') as f:
        f.write(modelstring)
    # Compilo el modelo
    compilacion=CmdStanModel(stan_file=os.path.join(config_f["models_directory"], archivo))
    # Hago el ajuste, corro las cadenas
    ajuste = compilacion.sample(
    data=data, 
    show_progress=False, 
    chains=1,
    iter_warmup= 1000,
    iter_sampling=10000)
    #Saco el resumen de la cadena
    summary=ajuste.summary().round(2)
    # Extraigo las simulaciones
    y_sim = ajuste.stan_variable("y_sim")
    # Convierto mis simulaciones a la unidad original
    y_sim_original=np.exp(y_sim)
    #Hago un dataframe
    y_sim_df = pd.DataFrame(y_sim_original)
    # Asignar nombres de columna basados en los índices de 'x'
    column_names = [f"y_sim[{i+1}]" for i in range(y_sim.shape[1])]
    y_sim_df.columns = column_names
    # Calculo los promedios de las simulaciones
    column_means = y_sim_df.mean(axis=0)
    # Column max 
    column_max = y_sim_df.max(axis=0)
    # Column min
    column_min = y_sim_df.min(axis=0)
    # Percentil 95
    pct_95 = y_sim_df.apply(lambda x: x.quantile(0.95), axis=0)
    # Percentil 99
    pct_99 = y_sim_df.apply(lambda x: x.quantile(0.99), axis=0)
    

    
    return summary, y_sim_df, y_sim_original, column_means, column_max, column_min, pct_95, pct_99


def plot_histogram(data, title, ylog_scale=False, xlog_scale=False, data_lim=False):
    """
    Graficas las estadisticas requeridas de la predictiva previa
    Args:
    data(array): estadistica de las simulaciones de la previa
    title(string): titulo de la grafica
    log_scale(boolean): indicador para graficar el y en escala logaritmica
    """
    if data_lim:
        data = data[data < 100]
    # Crear el histograma
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(data, alpha=0.75, color="teal", edgecolor="white")
    # Personalizar el gráfico
    ax.set_title(title, fontsize=15)
    ax.set_xlabel("Valor",fontsize=15)
    ax.set_ylabel("Frecuencia", fontsize=15)
    
    # Establecer la escala de los ejes
    if ylog_scale:
        ax.set_yscale('log')
    
    # Establecer la escala de los ejes
    if xlog_scale:
        ax.set_xscale('log')