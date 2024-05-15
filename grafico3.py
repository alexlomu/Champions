import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV con el DataFrame completo
df = pd.read_csv('dataframe_completo.csv')

# Calcular el número total de victorias por equipo
victorias_por_equipo = df['Equipo_local'].value_counts() + df['Equipo_visitante'].value_counts()
victorias_por_equipo = victorias_por_equipo.fillna(0)

# Seleccionar los 10 mejores equipos
top_10_equipos = victorias_por_equipo.nlargest(10)

# Filtrar el DataFrame completo para incluir solo partidos de los 10 mejores equipos
df_top_10 = df[df['Equipo_local'].isin(top_10_equipos.index) & df['Equipo_visitante'].isin(top_10_equipos.index)]

# Calcular el número total de partidos jugados por equipo
partidos_jugados = df_top_10['Equipo_local'].value_counts() + df_top_10['Equipo_visitante'].value_counts()

# Calcular la tasa de éxito de cada equipo (victorias / partidos jugados)
tasa_exito = top_10_equipos / partidos_jugados

# Encontrar el equipo con la tasa de éxito más alta
equipo_mas_exitoso = tasa_exito.idxmax()
tasa_exito_mas_alta = tasa_exito.max()

# Crear un gráfico de barras para mostrar la tasa de éxito de cada equipo
plt.figure(figsize=(10, 6))
tasa_exito.plot(kind='bar', color='skyblue')
plt.title('Tasa de éxito de los 10 mejores equipos')
plt.xlabel('Equipo')
plt.ylabel('Tasa de éxito')
plt.xticks(rotation=45, ha='right')

# Destacar el equipo más exitoso
plt.axhline(y=tasa_exito_mas_alta, color='red', linestyle='--', label=f'Más exitoso: {equipo_mas_exitoso} ({tasa_exito_mas_alta:.2f})')
plt.legend()

# Mostrar el gráfico
plt.tight_layout()
plt.show()
