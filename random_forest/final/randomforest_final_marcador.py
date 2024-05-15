import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Cargar los datos
dataframe_completo = pd.read_csv("dataframe_completo.csv").fillna(0)

# Calcular la diferencia de goles
dataframe_completo['Diferencia_goles'] = dataframe_completo['Puntuacion_local'] - dataframe_completo['Puntuacion_visitante']

# Dividir los datos en conjunto de entrenamiento y prueba
X = dataframe_completo[['Equipo_local', 'Equipo_visitante']]
y = dataframe_completo['Diferencia_goles']

# Codificar variables categóricas
X_encoded = pd.get_dummies(X)

# Construir y entrenar el modelo de Random Forest para regresión
modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
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
partido_final_encoded = pd.get_dummies(partido_final, columns=['Equipo_local', 'Equipo_visitante'])

# Alinear las columnas del DataFrame de prueba con las del DataFrame de entrenamiento
partido_final_encoded = partido_final_encoded.reindex(columns = X_encoded.columns, fill_value=0)

# Realizar predicción sobre el partido final
prediccion_final = modelo_rf.predict(partido_final_encoded)

# Presentar el resultado del partido final
print(f"Resultado del partido final: {equipo_local} vs {equipo_visitante}, Predicción del marcador: {int(prediccion_final[0])} - {int(-prediccion_final[0])}")
