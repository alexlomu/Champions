import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Cargar los datos
dataframe_completo = pd.read_csv("dataframe_completo.csv")

# Calcular la diferencia de goles
dataframe_completo['Diferencia_goles'] = dataframe_completo['Puntuacion_local'] - dataframe_completo['Puntuacion_visitante']

# Dividir los datos en conjunto de entrenamiento y prueba
X = dataframe_completo[['Equipo_local', 'Equipo_visitante', 'Diferencia_goles']]
y = dataframe_completo['Resultado_final']
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

# Definir los partidos de semifinales de este año (ida y vuelta)
partidos_semifinales_ida = pd.DataFrame({
    'Equipo_local': ['Borussia Dortmund', 'Bayern München'],
    'Equipo_visitante': ['Paris Saint-Germain', 'Real Madrid'],
})

partidos_semifinales_vuelta = pd.DataFrame({
    'Equipo_local': ['Paris Saint-Germain', 'Real Madrid'],
    'Equipo_visitante': ['Borussia Dortmund', 'Bayern München'],
})

# Codificar variables categóricas para los partidos de semifinales (ida y vuelta)
partidos_semifinales_ida_encoded = pd.get_dummies(partidos_semifinales_ida)
partidos_semifinales_vuelta_encoded = pd.get_dummies(partidos_semifinales_vuelta)

# Reindexar los DataFrames de los partidos de semifinales para que coincidan con las columnas del DataFrame de entrenamiento
partidos_semifinales_ida_encoded, _ = partidos_semifinales_ida_encoded.align(X_train_encoded, join='outer', axis=1, fill_value=0)
partidos_semifinales_vuelta_encoded, _ = partidos_semifinales_vuelta_encoded.align(X_train_encoded, join='outer', axis=1, fill_value=0)

# Realizar predicciones sobre los partidos de ida y vuelta
predicciones_ida = modelo_rf.predict(partidos_semifinales_ida_encoded)
predicciones_vuelta = modelo_rf.predict(partidos_semifinales_vuelta_encoded)

# Presentar los resultados de los partidos de ida y vuelta
print("\nResultados de los partidos de ida:")
for i, (equipo_local, equipo_visitante) in enumerate(zip(partidos_semifinales_ida['Equipo_local'], partidos_semifinales_ida['Equipo_visitante'])):
    print(f"Partido de ida: {equipo_local} vs {equipo_visitante}, Predicción del marcador: {predicciones_ida[i]}")

print("\nResultados de los partidos de vuelta:")
for i, (equipo_local, equipo_visitante) in enumerate(zip(partidos_semifinales_vuelta['Equipo_local'], partidos_semifinales_vuelta['Equipo_visitante'])):
    print(f"Partido de vuelta: {equipo_local} vs {equipo_visitante}, Predicción del marcador: {predicciones_vuelta[i]}")
