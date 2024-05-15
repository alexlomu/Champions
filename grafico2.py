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

# Calcular el promedio de puntuaciones locales y visitantes por equipo
promedio_puntuaciones = df_top_10.groupby('Equipo_local')[['Puntuacion_local', 'Puntuacion_visitante']].mean()

# Graficar el gráfico de dispersión
plt.figure(figsize=(10, 6))
plt.scatter(promedio_puntuaciones['Puntuacion_local'], promedio_puntuaciones['Puntuacion_visitante'], s=top_10_equipos*20, alpha=0.5)

# Añadir etiquetas a los puntos
for equipo, puntuacion_local, puntuacion_visitante in zip(promedio_puntuaciones.index, promedio_puntuaciones['Puntuacion_local'], promedio_puntuaciones['Puntuacion_visitante']):
    plt.text(puntuacion_local, puntuacion_visitante, equipo, fontsize=9, ha='center', va='center')

# Configurar etiquetas y título del gráfico
plt.xlabel('Puntuación local promedio')
plt.ylabel('Puntuación visitante promedio')
plt.title('Gráfico de dispersión de los 10 mejores equipos')

# Mostrar el gráfico
plt.grid(True)
plt.tight_layout()
plt.show()
