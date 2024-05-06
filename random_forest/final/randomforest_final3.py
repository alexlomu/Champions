import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Cargar los datos
dataframe_completo = pd.read_csv("dataframe_completo.csv")

# Calcular el resultado del partido (quién ganó y por cuánto)
dataframe_completo['Resultado'] = dataframe_completo.apply(
    lambda x: 'Local' if x['Puntuacion_local'] > x['Puntuacion_visitante'] else 'Visitante',
    axis=1
)
dataframe_completo['Diferencia_goles'] = dataframe_completo['Puntuacion_local'] - dataframe_completo['Puntuacion_visitante']

# Dividir los datos en conjunto de entrenamiento y prueba
X = dataframe_completo[['Equipo_local', 'Equipo_visitante', 'Diferencia_goles']]
y = dataframe_completo['Resultado']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Codificar variables categóricas
X_train_encoded = pd.get_dummies(X_train)
X_test_encoded = pd.get_dummies(X_test)

# Asegurarnos de que las columnas sean las mismas en X_train_encoded y X_test_encoded
X_train_encoded, X_test_encoded = X_train_encoded.align(X_test_encoded, join='outer', axis=1, fill_value=0)

# Construir y entrenar el modelo de Random Forest
modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
modelo_rf.fit(X_train_encoded, y_train)

# Evaluar el modelo con validación cruzada
scores = cross_val_score(modelo_rf, X_train_encoded, y_train, cv=5)
print("Precisión del modelo con validación cruzada:", scores.mean())

# Realizar predicciones sobre los partidos de prueba
predicciones = modelo_rf.predict(X_test_encoded)

# Calcular la precisión del modelo en los datos de prueba
precision = accuracy_score(y_test, predicciones)
print("Precisión del modelo en datos de prueba:", precision)

# Definir el partido final
equipo_local = 'Paris Saint-Germain'
equipo_visitante = 'Real Madrid'
diferencia_goles_final = 0  # Inicialmente sin diferencia de goles

# Preparar datos del partido final
partido_final = pd.DataFrame({
    'Equipo_local': [equipo_local],
    'Equipo_visitante': [equipo_visitante],
    'Diferencia_goles': [diferencia_goles_final]
})

# Codificar variables categóricas para el partido final
partido_final_encoded = pd.get_dummies(partido_final, columns=['Equipo_local', 'Equipo_visitante'])

# Asegurarnos de que las columnas sean las mismas en partido_final_encoded y X_train_encoded
partido_final_encoded, X_train_encoded = partido_final_encoded.align(X_train_encoded, join='outer', axis=1, fill_value=0)

# Realizar predicción sobre el partido final
prediccion_final = modelo_rf.predict(partido_final_encoded)

# Presentar el resultado del partido final
print(f"Resultado del partido final: {equipo_local} vs {equipo_visitante}, Predicción: {prediccion_final[0]}")

