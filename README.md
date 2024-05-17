# Champions
Este es el link del repositorio [Github](https://github.com/alexlomu/Champions)
##Introducción
Para este trabajo nos pedian hacer predicciones de la champions a través de distintos modelos, he planteado el problema haciendo una extracción de datos de distintos datasets con todo los partidos de champions desde el 2010 hasta el 2022 para obtener un dataset unico que agrupe todos los partidos y utilizar este para entrenar los distintos modelos y hacer unas gráficas.
##Extracción de datos
Con la extracción de datos se me presentó un problema, los datasets hasta el 2016 tenían una estructura distinta a los otros, para solucionar esto tuve que cambiar algunas columnas, eliminar otras y limpiarlos. Así es como quedó el código para ajustar los datos del 2010-2016:
'''
import pandas as pd
import os

# Ruta a la carpeta que contiene los archivos CSV
ruta_carpeta = "data/2010-2016"

# Obtener la lista de archivos CSV en la carpeta especificada
archivos_csv = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith('.csv')]

# Lista para almacenar los DataFrames de cada archivo CSV
dataframes = []

# Iterar sobre cada archivo CSV
for archivo in archivos_csv:
    # Construir la ruta completa al archivo CSV
    ruta_archivo = os.path.join(ruta_carpeta, archivo)
    
    # Leer el archivo CSV en un DataFrame
    df = pd.read_csv(ruta_archivo)
    
    # Eliminar columnas no relevantes para el análisis
    columnas_a_eliminar = ['Stage', 'Round', 'Group', 'ET', 'P', 'Comments']
    df = df.drop(columns=columnas_a_eliminar, errors='ignore')
    
    # Convertir la columna 'Date' al formato de fecha adecuado
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Renombrar las columnas para que sean más descriptivas
    columnas_renombradas = {
        'Date': 'Fecha',
        'Team 1': 'Equipo_local',
        'FT': 'Resultado_final',
        'HT': 'Resultado_parcial',
        'Team 2': 'Equipo_visitante'
    }
    df = df.rename(columns=columnas_renombradas)
    
    # Agregar el DataFrame procesado a la lista de DataFrames
    dataframes.append(df)

# Unificar todos los DataFrames en uno solo
dataframe_completo = pd.concat(dataframes, ignore_index=True)

# Mostrar una muestra de los datos limpios y procesados
print(dataframe_completo.head())
'''
Y el código para ajustar del 2017-2022:
'''
import pandas as pd

# Ruta al archivo de Excel
archivo_excel = "2016-2022.xlsx"

# Nombre de la hoja que deseas extraer
nombre_hoja = "matches"

# Cargar la hoja en un DataFrame de pandas
df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja)

# Ruta donde deseas guardar el archivo de Excel extraído
ruta_guardar = "partidos_2016_2022.xlsx"

# Guardar el DataFrame en un nuevo archivo de Excel
df.to_excel(ruta_guardar, index=False)

print("La hoja se ha guardado correctamente en:", ruta_guardar)

# Ruta al archivo de Excel que deseas convertir
archivo_excel = "2016-2022.xlsx"

# Nombre de la hoja que deseas convertir a CSV
nombre_hoja = "matches"

# Leer el archivo de Excel y cargar la hoja en un DataFrame de pandas
df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja)

# Ruta donde deseas guardar el archivo CSV
ruta_guardar_csv = "2016-2022.csv"

# Guardar el DataFrame como un archivo CSV
df.to_csv(ruta_guardar_csv, index=False)

print("El archivo se ha convertido a CSV y guardado en:", ruta_guardar_csv)

# Ruta al archivo CSV
archivo_csv = "2016-2022.csv"

# Leer el archivo CSV en un DataFrame de pandas
df = pd.read_csv(archivo_csv)

# Obtener las temporadas únicas
temporadas_unicas = df['SEASON'].unique()

# Iterar sobre cada temporada única
for temporada in temporadas_unicas:
    # Filtrar los datos para la temporada actual
    datos_temporada_actual = df[df['SEASON'] == temporada]
    
    # Ruta donde deseas guardar el archivo CSV para esta temporada
    ruta_guardar_csv = f"{temporada}.csv"
    
    # Guardar los datos de la temporada actual en un nuevo archivo CSV
    datos_temporada_actual.to_csv(ruta_guardar_csv, index=False)
    
    print(f"Se ha guardado la temporada {temporada} en:", ruta_guardar_csv)
'''
