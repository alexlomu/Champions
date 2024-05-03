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
