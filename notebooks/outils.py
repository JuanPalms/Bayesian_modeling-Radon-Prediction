"""
This python module defines some useful functions
"""
import os
import yaml
from IPython.core.magic import register_cell_magic
import time

# folder to load config file
CONFIG_PATH = "../"

# Function to load yaml configuration file
def load_config(config_name):
    """
    Sets the configuration file path
    Args:
    config_name: Name of the configuration file in the directory
    Returns:
    Configuration file
    """
    with open(os.path.join(CONFIG_PATH, config_name), encoding="utf-8") as conf:
        config = yaml.safe_load(conf)
    return config

def prior_predictive_check(model):
    """
    Returns histogram of means of prior distribution
    Args:
    Model(fitted stan model)
    Returns:
    y_sim: prior distribution simulations
    fig: histogram 
    """
    complete_pooling_model_previa_fit.stan_variable("y_sim")
    

config_f = load_config("config.yaml")
LOGFILE = config_f["log_file"]

@register_cell_magic
def log_run(line, cell):
    """
    Esta funcion ayuda a loggear el tiempo de ejecucion de las celdas indicadas en un archivo 
    de texto plano.
    Args:
    line (texto) Descripcion en texto del output sobre el cual se loggea el tiempo de ejecucion 
    ! No es necesario agregarlo en forma de strings, solo poner texto. 
    cell (celda de jupyter con el codigo a hacer el loggeo)
    returns:
    Tiempo de ejecucion y descripcion.
    """

    # Start the timer
    start = time.time()

    # Execute the cell
    result = get_ipython().run_cell(cell)

    # End the timer
    end = time.time()

    # Compute the execution time
    exec_time = end - start

    # Open the log file and append the execution time
    with open(LOGFILE, 'a') as f:
        f.write(f'Execution time: {exec_time:.6f} seconds, \nDescription: {line}\n, \n-------------------------------------------------------------------------------------------')

    return result