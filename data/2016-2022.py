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