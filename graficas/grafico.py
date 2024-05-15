import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('dataframe_completo.csv')
# Separar el resultado final en puntuaciones
df[['Puntuacion_local', 'Puntuacion_visitante']] = df['Resultado_final'].str.split('-', expand=True)

# Convertir las puntuaciones a números
df['Puntuacion_local'] = pd.to_numeric(df['Puntuacion_local'], errors='coerce')
df['Puntuacion_visitante'] = pd.to_numeric(df['Puntuacion_visitante'], errors='coerce')

# Crear una nueva columna para registrar al ganador
df['Ganador'] = df.apply(lambda x: x['Equipo_local'] if x['Puntuacion_local'] > x['Puntuacion_visitante'] else
                         x['Equipo_visitante'] if x['Puntuacion_visitante'] > x['Puntuacion_local'] else None, axis=1)

# Eliminar filas con empates
df = df.dropna(subset=['Ganador'])

# Contar el número de victorias por equipo
victorias = df['Ganador'].value_counts().head(15)

# Graficar los 15 equipos con más victorias
plt.figure(figsize=(10,6))
victorias.plot(kind='bar')
plt.title('Top 15 Equipos con más victorias')
plt.xlabel('Equipos')
plt.ylabel('Número de Victorias')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.savefig('graficas/top_equipos_victorias.png')
plt.show()
