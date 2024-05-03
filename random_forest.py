import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

dataframe_completo = pd.read_csv("dataframe_completo.csv")
# Calcular el resultado del partido (quién ganó y por cuánto)
dataframe_completo['Resultado'] = dataframe_completo.apply(
    lambda x: 'Empate' if x['Puntuacion_local'] == x['Puntuacion_visitante'] else 'Local' if x['Puntuacion_local'] > x['Puntuacion_visitante'] else 'Visitante',
    axis=1
)
dataframe_completo['Diferencia_goles'] = dataframe_completo['Puntuacion_local'] - dataframe_completo['Puntuacion_visitante']

# Preparar los datos para el modelo
X = dataframe_completo[['Equipo_local', 'Equipo_visitante', 'Diferencia_goles']]
y = dataframe_completo['Resultado']

X_train = dataframe_completo[['Equipo_local', 'Equipo_visitante', 'Diferencia_goles']]
y_train = dataframe_completo['Resultado']

# Codificar variables categóricas
X_train_encoded = pd.get_dummies(X_train)

# Construir y entrenar el modelo de Random Forest
modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
modelo_rf.fit(X_train_encoded, y_train)

# Definir los partidos de semifinales de este año
partidos_semifinales = pd.DataFrame({
    'Equipo_local': ['Paris Saint-Germain', 'Bayern München'],
    'Equipo_visitante': ['Borussia Dortmund', 'Real Madrid'],
    'Diferencia_goles': [None, None]  # No tenemos información sobre la diferencia de goles para estos partidos
})

# Codificar variables categóricas para los partidos de semifinales
partidos_semifinales_encoded = pd.get_dummies(partidos_semifinales)

# Reindexar el DataFrame para que coincida con las columnas del DataFrame de entrenamiento
partidos_semifinales_encoded = partidos_semifinales_encoded.reindex(columns=X_train_encoded.columns, fill_value=0)

# Realizar predicciones sobre los partidos de semifinales
predicciones = modelo_rf.predict(partidos_semifinales_encoded)

# Mostrar las predicciones
for i, prediccion in enumerate(predicciones):
    print(f"El partido entre {partidos_semifinales.iloc[i]['Equipo_local']} y {partidos_semifinales.iloc[i]['Equipo_visitante']} es probable que termine con una victoria para: {prediccion}")