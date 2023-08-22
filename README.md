[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-8d59dc4de5201274e310e4c54b9627a8934c3b88527886e3b421487c677d23eb.svg)](https://classroom.github.com/a/TG-k1xUL)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-f4981d0f882b2a3f0472912d15f9806d57e124e0fc890972558857b51b24a6f9.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=10593529)


# Contenido
-   [Planteamiento](#planteamiento)
-   [Ambiente](#ambiente)
-   [Estructura](#estructura)
-   [Replicación](#replicación)
-   [Caso aplicado](#aplicación)
-   [Referencias](#referencias)

# Planteamiento
Repositorio para el proyecto final de la materia de Modelación Bayesiana de la Maestría en Ciencia de Datos del ITAM.

Este proyecto está basado en los siguientes [lineamientos](/00_planteamiento/lineamientos.pdf). Adicionalmente, se utilizará como referencia el siguiente [documento](https://mc-stan.org/users/documentation/case-studies/radon_cmdstanpy_plotnine.html) con el planteamiento original del problema.

Los datos originales se pueden extraer de la siguiente [liga](http://www.stat.columbia.edu/~gelman/arm/software/), o bien ejecutar el siguiente [comando](http://www.stat.columbia.edu/~gelman/arm/examples/ARM_Data.zip) para descargarlos directamente (Copiar y pegar la URL en el navegador si se bloqueó la ventana emergente).

# Ambiente

![Grades](https://github.com/ag-classrooms/autograding-r/actions/workflows/classroom.yml/badge.svg)

Este repositorio emula una tarea y está diseñado para garantizar la instalación de las herramientas para el curso.

El repositorio del proyecto final cuenta con el ambiente de conda "experimentacion_env" el cual contiene todas las paqueterias necesarias así como la versión de python que asegura que todo el código corra de manera correcta en cualquier computadora.

## Pasos para instalar el ambiente

1.- Asegurarse de tener instalado conda, de lo contrario se puede descargar [aquí](https://docs.conda.io/en/latest/miniconda.html)

2.- Una vez conda es instalado, se deberá crear el entorno del repo. Para esto se debe correr la siguiente linea de código.
``` bash
conda env create -f environments.yml
```
3.- Comprobar si el ambiente fue creado correctamente. Esto se puede hacercorriendo la siguiente línea de código. 
``` bash
conda info --env
```
El ambiente **experimentacion_env** debera ser parte de tus ambientes.

4.- Una vez creado el ambiente de conda éste deberá ser activado corriendo la siguiente de linea de código.
``` bash
conda activate experimentacion_env
```
5.- Tu ambiente está listo 

# Estructura

Para una navegación mas sencilla de los archivos dentro del repositorio del proyecto final, se recomienda enfocarse principalmente en los siguientes *folders*.

## datos

El *folder* datos contiene en su interior dos *subfolders*:
* bruto: Éste folder contiene los datos de mediciones de Uranio y Radón, tal cual fueron obtenidos de [Uranio](http://www.stat.columbia.edu/~gelman/arm/examples/radon/cty.dat) y [Radón](http://www.stat.columbia.edu/~gelman/arm/examples/radon/srrs2.dat') respectivamente.
* procesado: Éste folder contiene el el archivo **radon.csv** con los datos ya procesados por el *script* [preproceso.py](./src/preproceso.py). La transformación de los datos consistió en eliminar espacios en blanco, filtrar columnas calculadas, unir ambos *data frames* y descartar columnas no utilizadas.

## modelos

El *folder* modelos contiene todos los modelos de stan utilizados en el repositorio. Es de especial importancia los archivos ".stan"

## notebooks

En este *folder* se encuentran todos los notebooks usados para la replicación del modelo. 

* [00_visualizaciones.ipynb](./notebooks/00_visualizaciones.ipynb): En este notebook hacemos un primer EDA para entender mejor la forma de los datos.
* [Chequeos_predictivos_previos.ipynb](./notebooks/Chequeos_predictivos_previos.ipynb): Comprobamos la calidad de nuestras previas
* [experimentación.ipynb](./notebooks/experimentación.ipynb): En este notebook llevamos a cabo las diferentes iteraciones de los modelos presentados.

* [posterior_comparación.ipynb](./notebooks/posterior_comparación.ipynb): En este notebook se realizan las predicciones predictivas posteriores con los modelos ajustados con iniciales informativas. Ademas, se realiza comparacion de modelos con los criterios estudiados en clase.

## presentaciones
En este folder se encuentran las tres presentaciones realizadas a lo largo del curso.

* [presentacion_1](./presentaciones/presentacion_1.pdf)
* [presentacion_2](./presentaciones/presentacion_2.pdf)
* [presentacion_Final](./presentaciones/presentacion_Final.pdf)

## reporte

* [reporte](./ReporteRadon_Final.pdf)

# Replicación

Para poder replicar el código en este repo es necesario primero tener activado el ambiente de conda como se explica en la sección [Ambiente](#ambiente). Una vez el ambiente está activado, se aconseja comenzar con el *script* [preproceso.py](./src/preproceso.py) para primero analizar la limpieza a los datos originales. 

Después es oportuno analizar el *notebook* [00_visualizaciones.ipynb](./notebooks/00_visualizaciones.ipynb) para analizar los datos ya preprocesados a mayor detalle.

El siguiente paso para repetir nuestra lógica sería correr el notebook de [Experimentacion.ipynb](./notebooks/Experimentacion.ipynb) para ir paso a paso como probamos diferentes modelos.

Posteriormente se debe correr el código de [Chequeos_predictivos_previos.ipynb](./notebooks/Chequeos_predictivos_previos.ipynb) para observar si nuestros modelos estan bien especificados, y saber si la distribucion predictiva previa arroja valores que se encuentran en niveles que observariamos naturalmente.

Por último correr [posterior_comparación.ipynb](./notebooks/posterior_comparación.ipynb) para evaluar los diferentes modelos creados.

# Aplicación

El caso aplicado a *football* se encuentra en [modelo_futbol.ipynb](./src/modelo_futbol.ipynb). El ambiente "experimentacion_env" funciona para correr este *notebook*. En una Mac con procesador M1 pro, la totalidad del notebook se ejecuta en aproximadamente 50 minutos.

# Referencias

* Baath, R. (n.d.). Modeling match results in soccer using a hierarchichal model. Retrieved May 15, 2023, from https://www.sumsar.net/papers/baath_2015_modeling_match_resluts_in_soccer.pdf

* Cáncer de pulmón de células no pequeñas - Estadísticas. (n.d.). Cancer.Net. Retrieved May 15, 2023, from https://www.cancer.net/es/tipos-de-cancer/cancer-de-pulmon-de-celulas-no-pequenas/estadisticas

* Fonnesbeck, C. (n.d.). Multilevel regression modeling with CmdStanPy and plotnine. Retrieved May 15, 2023, from https://mc-stan.org/users/documentation/case-studies/radon_cmdstanpy_plotnine.html

* Gelman, A., & Hill, J. (2006). Chapter 12. In Data Analysis Using Regression and Multilevel/Hierarchical Models (p. 251). Columbia University, New York.
Health Risk of Radon | US EPA. (2023, January 5). Environmental Protection Agency. Retrieved May 15, 2023, from https://www.epa.gov/radon/health-risk-radon

* Karam, A., & Mortazavi, J. (n.d.). The Very High Background Radiation Area in Ramsar, Iran: Public Health Risk or Signal for a Regulatory Paradigm Shift? AERB. Retrieved May 15, 2023, from https://aerb.gov.in/images/PDF/image/34086353.pdf


