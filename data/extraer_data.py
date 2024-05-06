import pandas as pd
import os

# Función para limpiar y procesar los datos de los CSV con el formato "MATCH_ID,SEASON,DATE_TIME,HOME_TEAM,AWAY_TEAM,STADIUM,HOME_TEAM_SCORE,AWAY_TEAM_SCORE,PENALTY_SHOOT_OUT,ATTENDANCE"
def limpiar_datos_csv_tipo_1(archivo):
    # Leer el archivo CSV en un DataFrame
    df = pd.read_csv(archivo)
    
    # Convertir la columna 'DATE_TIME' al formato de fecha adecuado
    df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], format='%d-%b-%y %I.%M.%S.%f %p', errors='coerce')
    
    # Renombrar las columnas para que sean más descriptivas
    columnas_renombradas = {
        'MATCH_ID': 'ID_partido',
        'SEASON': 'Temporada',
        'DATE_TIME': 'Fecha_hora',
        'HOME_TEAM': 'Equipo_local',
        'AWAY_TEAM': 'Equipo_visitante',
        'STADIUM': 'Estadio',
        'HOME_TEAM_SCORE': 'Puntuacion_local',
        'AWAY_TEAM_SCORE': 'Puntuacion_visitante',
        'PENALTY_SHOOT_OUT': 'Penalties',
        'ATTENDANCE': 'Asistencia'
    }
    df = df.rename(columns=columnas_renombradas)
    
    # Eliminar columnas no relevantes
    columnas_a_eliminar = ['PENALTY_SHOOT_OUT', 'ATTENDANCE']
    df = df.drop(columns=columnas_a_eliminar, errors='ignore')
    # Obtener la parte entera y decimal de cada resultado
    parte_entera_primer_tiempo = df['Puntuacion_local'].astype(int)
    parte_decimal_primer_tiempo = (df['Puntuacion_local'] * 10 % 10).astype(int)
    parte_entera_segundo_tiempo = df['Puntuacion_visitante'].astype(int)
    parte_decimal_segundo_tiempo = (df['Puntuacion_visitante'] * 10 % 10).astype(int)

    # Sumar las partes enteras y decimales correctamente
    parte_entera_resultado = parte_entera_primer_tiempo + parte_decimal_segundo_tiempo 
    parte_decimal_resultado = parte_decimal_primer_tiempo + parte_entera_segundo_tiempo

    # Concatenar las partes enteras y decimales para obtener el resultado final
    df['Resultados_temp'] = parte_entera_resultado.astype(str) + '-' + parte_decimal_resultado.astype(str)

    # Llenar las filas vacías en 'Resultado_final' con los valores de 'Resultados_temp'
    df['Resultado_final'] = df['Resultados_temp']

    return df

# Función para limpiar y procesar los datos de los CSV con el formato "Stage,Round,Group,Date,Team 1,FT,HT,Team 2,∑FT,ET,P,Comments"
def limpiar_datos_csv_tipo_2(archivo):
    # Leer el archivo CSV en un DataFrame
    df = pd.read_csv(archivo)
    
    # Eliminar columnas no relevantes para el análisis
    columnas_a_eliminar = ['Stage', 'Round', 'Group', 'ET', 'Comments']
    df = df.drop(columns=columnas_a_eliminar, errors='ignore')
    
    # Convertir la columna 'Date' al formato de fecha adecuado
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='%d-%b-%y %I.%M.%S.%f %p')
    
    # Limpiar datos en la columna 'Team 1'
    df['Team 1'] = df['Team 1'].str.split(' › ').str[0]
    df['Team 1'] = df['Team 1'].str.split(' \(').str[0]
    
    # Renombrar las columnas para que sean más descriptivas
    columnas_renombradas = {
        'Date': 'Fecha',
        'Team 1': 'Equipo_local',
        'FT': 'Resultado_final',
        'HT': 'Resultado_parcial',
        'Team 2': 'Equipo_visitante',
        'P': 'Penalties'
    }
    df = df.rename(columns=columnas_renombradas)
    return df

# Ruta a la carpeta que contiene los archivos CSV
ruta_carpeta = "data"

# Obtener la lista de archivos CSV en la carpeta especificada
archivos_csv = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith('.csv')]

# Lista para almacenar los DataFrames de cada archivo CSV
dataframes = []

# Iterar sobre cada archivo CSV
for archivo in archivos_csv:
    # Construir la ruta completa al archivo CSV
    ruta_archivo = os.path.join(ruta_carpeta, archivo)
    
    # Determinar el tipo de CSV y aplicar la limpieza de datos correspondiente
    if "MATCH_ID" in pd.read_csv(ruta_archivo, nrows=1).columns:
        df = limpiar_datos_csv_tipo_1(ruta_archivo)
    else:
        df = limpiar_datos_csv_tipo_2(ruta_archivo)
    
    # Agregar el DataFrame procesado a la lista de DataFrames
    dataframes.append(df)

# Unificar todos los DataFrames en uno solo
dataframe_completo = pd.concat(dataframes, ignore_index=True)

columnas_a_eliminar = ['ID_partido','Temporada','Fecha_hora','Estadio', 'Asistencia', 'Resultado_parcial','Fecha','Resultados_temp','∑FT','Penalties']
dataframe_completo = dataframe_completo.drop(columns=columnas_a_eliminar, errors='ignore')

dataframe_completo['Equipo_visitante'] = dataframe_completo['Equipo_visitante'].str.split(' ›').str[0]

# Mostrar una muestra de los datos limpios y procesados
print(dataframe_completo.head())

dataframe_completo.to_csv('dataframe_completo.csv', index=False)