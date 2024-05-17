# Champions
Este es el link del repositorio [Github](https://github.com/alexlomu/Champions)

## Introducción
Para este trabajo nos pedian hacer predicciones de la champions a través de distintos modelos, he planteado el problema haciendo una extracción de datos de distintos datasets con todo los partidos de champions desde el 2010 hasta el 2022 para obtener un dataset unico que agrupe todos los partidos y utilizar este para entrenar los distintos modelos y hacer unas gráficas.

## Extracción de datos
Con la extracción de datos se me presentó un problema, los datasets hasta el 2016 tenían una estructura distinta a los otros, para solucionar esto tuve que cambiar algunas columnas, eliminar otras, juntar diferentes datasets y limpiarlos. Así es como quedó el código para ajustar los datos del 2010-2016:
```
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
```
Y el código para ajustar del 2017-2022:
```
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
```
Ahora en otro código juntaremos todos los datasets en un único csv además de acabar de pulir el dataset para que se ajuste a nuestras necesidades:
```
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

# Función para rellenar las puntuaciones faltantes en un DataFrame
def rellenar_puntuaciones(df):
    # Separar el resultado final en puntuaciones
    df[['Puntuacion_local', 'Puntuacion_visitante']] = df['Resultado_final'].str.split('-', expand=True)

    # Convertir las puntuaciones a números
    df['Puntuacion_local'] = pd.to_numeric(df['Puntuacion_local'], errors='coerce')
    df['Puntuacion_visitante'] = pd.to_numeric(df['Puntuacion_visitante'], errors='coerce')

    # Rellenar valores faltantes en las columnas de puntuación con el resultado final
    df['Puntuacion_local'].fillna(df['Puntuacion_local'].mean(), inplace=True)
    df['Puntuacion_visitante'].fillna(df['Puntuacion_visitante'].mean(), inplace=True)

    # Reemplazar "Real Madrid CF" por "Real Madrid" en los nombres de equipos
    df['Equipo_local'] = df['Equipo_local'].replace('Real Madrid CF', 'Real Madrid')
    df['Equipo_visitante'] = df['Equipo_visitante'].replace('Real Madrid CF', 'Real Madrid')

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

# Aplicar la función para rellenar las puntuaciones
dataframe_completo = rellenar_puntuaciones(dataframe_completo)

# Mostrar una muestra de los datos limpios y procesados
print(dataframe_completo.head())

# Guardar el DataFrame completo en un archivo CSV
dataframe_completo.to_csv('dataframe_completo.csv', index=False)
```
Ahora ya tenemos todos los datos que queríamo en un único csv con el que trabajaremos.

## Gráficas
A partir del csv hice las distintas gráficas:
1) Diagrama de barras de los 10 equipos que más porcentaje de partidos ganados en la champions league:
   ![porcentaje_victorias](https://github.com/alexlomu/Champions/assets/91721507/4960c6ce-4907-42c2-b7e8-81ef3c13c196)
2) Diagrama de barras de los 15 equipos con más partidos ganados en la champions league:
![top_equipos_victorias](https://github.com/alexlomu/Champions/assets/91721507/d1cd963c-aab9-4ac3-8d24-ca01df476790)
3) Diagrama de dispersíon de los 10 equipos con mejor ratio goles jugando de local/goles jugando de visitante:
   ![top_mejores_equipos](https://github.com/alexlomu/Champions/assets/91721507/ba950c7b-acea-4dfc-afaa-5a989b456c92)

## Modelos
He entrenado 4 modelos distintos: Gausiano, Random Forest, Montecarlo y xgboost. Para añadirle calidad al estudio y la predicción de los partidos decidí programar en cada modelo 2 códigos distintos, uno que predijese quién iba a ganar el partido o si este iba a quedar en empate y otro que predijese el marcador del encuentro. Hice las predicciones a partir de los enfrentamientos de semifinales de la champions de este año y luego en las predicciones de la final enfrente al madrid contra el PSG, es por todo que cada modelo tiene su carpeta con 4 archivos (2 para la final y 2 para semifinales).
Estos son los marcadores de las semifinales que me han predecido los distintos modelos:
### GAUSIANO
Partido: Borussia Dortmund vs Paris Saint-Germain, Predicción del Marcador: 3-0
Partido: Bayern Munchen vs Real Madrid, Predicción del Marcador: 3-0
### MONTECARLO
Partido: Paris Saint-Germain vs Borussia Dortmund, Predicción del Marcador: 4-1
Partido: Real Madrid vs Bayern Munchen, Predicción del Marcador: 2-0
### RANDOM FOREST
Partido: Paris Saint-Germain vs Borussia Dortmund, Predicción del Marcador: 2-2
Partido: Real Madrid vs Bayern Munchen, Predicción del Marcador: 4-3
### XGBOOST
Partido: Borussia Dortmund vs Paris Saint-Germain, Predicción del Marcador: 2-1
Partido: Bayern Munchen vs Real Madrid, Predicción del Marcador: 2-1

## Interfaz tkinter
Para el archivo lanzador he decidido hacer una interfaz con tkinter en la que podemos escoger que archivo ejecutar y nos devolverá el output escrito en un recuadro en medio de la interfaz. Así es como se ve:
![tkinter](https://github.com/alexlomu/Champions/assets/91721507/f26b89ee-6c1c-4792-97be-ddb4e9d555e8)



