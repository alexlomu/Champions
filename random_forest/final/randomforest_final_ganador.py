import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Cargar los datos
dataframe_completo = pd.read_csv("dataframe_completo.csv").fillna(0)

# Calcular el resultado del partido (quién ganó y por cuánto)
dataframe_completo['Resultado_final'] = dataframe_completo.apply(
    lambda x: 'Empate' if x['Puntuacion_local'] == x['Puntuacion_visitante'] else 'Local' if x['Puntuacion_local'] > x['Puntuacion_visitante'] else 'Visitante',
    axis=1
)
dataframe_completo['Diferencia_goles'] = dataframe_completo['Puntuacion_local'] - dataframe_completo['Puntuacion_visitante']

# Dividir los datos en conjunto de entrenamiento y prueba
X = dataframe_completo[['Equipo_local', 'Equipo_visitante', 'Diferencia_goles']]
y = dataframe_completo['Resultado_final']

# Codificar variables categóricas
X_encoded = pd.get_dummies(X)

# Construir y entrenar el modelo de Random Forest
modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
modelo_rf.fit(X_encoded, y)

# Definir los equipos finalistas
equipo_local = 'Paris Saint-Germain'
equipo_visitante = 'Real Madrid'

# Preparar datos del partido final
partido_final = pd.DataFrame({
    'Equipo_local': [equipo_local],
    'Equipo_visitante': [equipo_visitante],
})

# Codificar variables categóricas para el partido final
# Aquí estamos asegurando que las columnas de los equipos estén presentes
# y que coincidan con las columnas utilizadas durante el entrenamiento
X_train_teams = X['Equipo_local'].append(X['Equipo_visitante']).unique()
partido_final_encoded = pd.get_dummies(partido_final, columns=['Equipo_local', 'Equipo_visitante'])
missing_cols = set(X_train_teams) - set(partido_final_encoded.columns)
for col in missing_cols:
    partido_final_encoded[col] = 0

# Realizar predicción sobre el partido final
prediccion_final = modelo_rf.predict(partido_final_encoded)

# Presentar el resultado del partido final
resultado_final = "Empate" if prediccion_final[0] == "Empate" else equipo_local if prediccion_final[0] == "Local" else equipo_visitante
print(f"Resultado del partido final: {equipo_local} vs {equipo_visitante}, Predicción: {resultado_final}")
