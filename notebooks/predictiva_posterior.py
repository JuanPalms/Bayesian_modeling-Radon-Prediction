"""
Este modulo de python ajusta la predictiva posterior y genera N=978 * 1000 simulaciones y establece una funcion para graficar elementos de comparacion relevantes para los diagnosticos posteriores
predictive checks
"""
import os
import pandas as pd
import numpy as np
from cmdstanpy import CmdStanModel
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from outils import load_config
import matplotlib.patches as patches
import arviz as az
import xarray as xr

# Load config file calling load_config function
config_f = load_config("config.yaml")



def ajuste_posterior_predictiva(archivo, modelstring, data, datos_originales, parametros, n_samples, n_chains):
    """
    Genera simulaciones de la predictiva posterior
    Args: 
    archivo (string): nombre del archivo stan en el que se guardara el modelo
    modelstring (strin): string del modelo en codigo de stan
    data(dictionary): dictionnary containing data to fit stan model
    datos_originales(pandas dataframe): dataframe de pandas con los datos
    parametros(list): Lista de parametros sobre los cuales hace inferencia el modelo (acepta regex).
    Returns:
    parametros(pandas dataframe): dataframe con las simulaciones de los parametros del modelo.
    predicciones_natural (pandas dataframe): dataframe con las 900 y pico simulaciones generadas 
    en escala natural (pico-curies por litro)
    estadisticas_replicaciones(pandas dataframe): dataframe con una columna de medias de 
    predicciones y de desviaciones estandar. 
    summary_modelo(pandas dataframe): dataframe con estadisticas de salida del summary.
    muestras_aleatorias(pandas dataframe): subset de simulaciones para graficar
    
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
    chains=n_chains,
    iter_warmup= 1000,
    iter_sampling=n_samples)
    parametros = ajuste.draws_pd(vars=parametros)
    predicciones = ajuste.draws_pd(vars=['y_rep'])
    predicciones_natural= predicciones.applymap(np.exp)
    muestras_aleatorias = predicciones_natural\
               .sample(n=15, random_state=34)\
               .transpose()\
               .set_index(datos_originales.index)
    muestras_aleatorias.insert(0, "datos_originales", datos_originales['radon_natural'])
    media=predicciones_natural.transpose().mean()
    desviacion_estandar = predicciones_natural.transpose().std()
    # Crear un nuevo DataFrame con las columnas 'Media' y 'Desviación Estándar'
    estadisticas_replicaciones = pd.DataFrame({'Media': media, 'Desviación Estándar': desviacion_estandar})
    #summary_modelo=ajuste.summary().round(2)
    return parametros, predicciones_natural, estadisticas_replicaciones, muestras_aleatorias, ajuste


def grafica_hist_replicaciones_observados(muestras_aleatorias):
    """
    Grafica los datos observados del problema contra 14 muestras aleatorias de las replicaciones realizadas
    """
    # Crear un panel único para los histogramas
    fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(12, 12))

    # Establecer el rango común para los ejes x e y
    x_min = muestras_aleatorias.min().min()
    x_max = muestras_aleatorias.max().min()

    # Iterar sobre cada columna y crear un histograma en el panel
    for i, column in enumerate(muestras_aleatorias.columns):
        ax = axes[i // 4, i % 4]

        # Graficar el primer histograma con un color diferente
        if i == 0:
            ax.hist(muestras_aleatorias[column], bins=50, alpha=0.70, color="red", edgecolor="white")
        else:
            ax.hist(muestras_aleatorias[column], bins=50, alpha=0.40, color="teal", edgecolor="white")

        # Establecer los rangos en los ejes x e y
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(0, 250)

        # Ajustar las etiquetas del eje x
        if i >= 12:
            ax.set_xlabel("Nivel de radon")
        else:
            ax.set_xticklabels([])

        # Mostrar la leyenda solo en el primer histograma
        if i == 0:
            ax.set_title("Datos observados", color="red")

    fig.suptitle("Histogramas de datos observados\n y replicaciones", fontsize=15)
    plt.tight_layout();


def grafica_media_std_replicaciones(estadisticas_replicaciones, datos_originales):
    mn_radon=datos_originales
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(10, 5))
    fig.suptitle('Media y desviación estándar de replicaciones\n y datos observados', fontsize=15)
    plt.subplots_adjust(top=0.80)
    ax1.hist(estadisticas_replicaciones["Media"], bins=40, alpha=0.50, color="teal", edgecolor="white")
    ax1.set_title("Medias")
    ax1.axvline(mn_radon["radon_natural"].mean(), color="red")
    ax1.legend([f"Media de datos\n observados"], loc='upper right', frameon=False, framealpha=1, fontsize=9)
    ax1.text(0.70, 0.80, "Replicaciones", transform=ax1.transAxes, color="black",fontsize=9)
    rect1 = patches.Rectangle((0.60, 0.78), 0.07, 0.07, alpha=0.50, 
                              facecolor="teal", edgecolor="none", transform=ax1.transAxes)
    ax1.add_patch(rect1)
    ax2.hist(estadisticas_replicaciones["Desviación Estándar"],bins=40, alpha=0.50, color="teal", edgecolor="white")
    ax2.set_title("Desviación estándar")
    ax2.axvline(mn_radon["radon_natural"].std(), color="red")
    ax2.legend([f"Desviación estándar\n de datos observados"], loc='upper right', 
               frameon=False, framealpha=1,fontsize=9)
    ax2.text(0.57, 0.80, "Replicaciones", transform=ax2.transAxes, color="black",fontsize=9)
    rect2 = patches.Rectangle((0.48, 0.78), 0.07, 0.07, alpha=0.50,
                              facecolor="teal", edgecolor="none", transform=ax2.transAxes)
    ax2.add_patch(rect2);
    
def grafica_scatter_estadisticas(estadisticas_replicaciones, datos_originales):
    mn_radon=datos_originales
    plt.scatter(estadisticas_replicaciones["Media"], estadisticas_replicaciones["Desviación Estándar"], 
                alpha=0.1, edgecolors="white", s=30, color="teal")

    # Señalar la primera entrada con una flecha y texto
    plt.annotate("Datos observados", xy=(mn_radon["radon_natural"].mean(), 
                                         mn_radon["radon_natural"].std()), xytext=(10, -20),
                 textcoords="offset points", arrowprops=dict(arrowstyle="->",
                 connectionstyle="arc3,rad=0.5"), fontsize=10, color="red")
    plt.scatter(mn_radon["radon_natural"].mean(), mn_radon["radon_natural"].std(), color="red")
    plt.xlabel("Media")
    plt.ylabel("Desviación Estándar")
    plt.title("Distribución de estadísticas:\n replicaciones de las observaciones")

def calcula_metricas(ajuste, parametros, n_chains, n_draws_per_chain):
    # Extraer la log-verosimilitud
    log_lik = ajuste.draws_pd(vars=['log_lik'])
    log_lik_np = log_lik.to_numpy()
    log_lik_np = log_lik_np.reshape((n_chains, n_draws_per_chain, -1))  
    log_lik_xr = xr.DataArray(log_lik_np, dims=["chain", "draw", "log_lik_dim"])
    
    # Extraer parámetros
    posterior_dict = {}
    for param in parametros:
        param_values = ajuste.stan_variable(param)
        param_dim = len(param_values.shape)  # Obtener la dimensión del parámetro
        if param_dim > 1:
            # Si el parámetro tiene más de una dimensión (es un vector o matriz)
            param_np = param_values.reshape((n_chains, n_draws_per_chain, -1))
            param_xr = xr.DataArray(param_np, dims=["chain", "draw", f"{param}_dim"])
        else:
            param_np = param_values.reshape((n_chains, n_draws_per_chain))
            param_xr = xr.DataArray(param_np, dims=["chain", "draw"])
        posterior_dict[param] = param_xr

    # Crear objeto InferenceData
    idata = az.from_dict(posterior=posterior_dict, log_likelihood={"y": log_lik_xr})

    # Calcular WAIC y LOO
    waic = az.waic(idata)
    loo = az.loo(idata)
    
    return waic, loo



def loglik_posterior_predictiva(archivo, modelstring, data, datos_originales, parametros, n_samples, n_chains):
    """
    Genera simulaciones de la predictiva posterior
    Args: 
    archivo (string): nombre del archivo stan en el que se guardara el modelo
    modelstring (strin): string del modelo en codigo de stan
    data(dictionary): dictionnary containing data to fit stan model
    datos_originales(pandas dataframe): dataframe de pandas con los datos
    parametros(list): Lista de parametros sobre los cuales hace inferencia el modelo (acepta regex).
    Returns:
    parametros(pandas dataframe): dataframe con las simulaciones de los parametros del modelo.
    predicciones_natural (pandas dataframe): dataframe con las 900 y pico simulaciones generadas 
    en escala natural (pico-curies por litro)
    estadisticas_replicaciones(pandas dataframe): dataframe con una columna de medias de 
    predicciones y de desviaciones estandar. 
    summary_modelo(pandas dataframe): dataframe con estadisticas de salida del summary.
    muestras_aleatorias(pandas dataframe): subset de simulaciones para graficar
    
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
    chains=n_chains,
    iter_warmup= 1000,
    iter_sampling=n_samples)
    parametros = ajuste.draws_pd(vars=parametros)

    return parametros, ajuste