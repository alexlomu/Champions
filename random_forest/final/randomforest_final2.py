import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer

# Cargar los datos
dataframe_completo = pd.read_csv("dataframe_completo.csv")
dataframe_completo.dropna(subset=['Puntuacion_local'], inplace=True)
# Calcular el resultado del partido (puntuación del local y visitante)
dataframe_completo['Diferencia_goles'] = dataframe_completo['Puntuacion_local'] - dataframe_completo['Puntuacion_visitante']

# Dividir los datos en conjunto de entrenamiento y prueba
X = dataframe_completo[['Equipo_local', 'Equipo_visitante', 'Diferencia_goles']]
y = dataframe_completo[['Puntuacion_local', 'Puntuacion_visitante']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Imputar valores faltantes en y_train['Puntuacion_local']
imputer = SimpleImputer(strategy='median')
y_train_imputed = imputer.fit_transform(y_train[['Puntuacion_local']])
y_train['Puntuacion_local'] = y_train_imputed

# Codificar variables categóricas
X_train_encoded = pd.get_dummies(X_train)
X_test_encoded = pd.get_dummies(X_test)

# Asegurarnos de que las columnas sean las mismas en X_train_encoded y X_test_encoded
X_train_encoded, X_test_encoded = X_train_encoded.align(X_test_encoded, join='outer', axis=1, fill_value=0)

# Construir y entrenar el modelo de Random Forest para cada equipo por separado
modelo_rf_local = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_rf_visitante = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_rf_local.fit(X_train_encoded, y_train['Puntuacion_local'])
modelo_rf_visitante.fit(X_train_encoded, y_train['Puntuacion_visitante'])

# Realizar predicciones sobre los partidos de prueba
predicciones_local = modelo_rf_local.predict(X_test_encoded)
predicciones_visitante = modelo_rf_visitante.predict(X_test_encoded)

# Calcular el error cuadrático medio (MSE) para evaluar el rendimiento del modelo
mse_local = mean_squared_error(y_test['Puntuacion_local'], predicciones_local)
mse_visitante = mean_squared_error(y_test['Puntuacion_visitante'], predicciones_visitante)
print("Error cuadrático medio (MSE) para el puntaje del equipo local:", mse_local)
print("Error cuadrático medio (MSE) para el puntaje del equipo visitante:", mse_visitante)

# Definir un partido de ejemplo
partido_ejemplo = pd.DataFrame({
    'Equipo_local': ['Paris Saint-Germain'],
    'Equipo_visitante': ['Real Madrid'],
    'Diferencia_goles': [None]  # No tenemos información sobre la diferencia de goles para este partido
})

# Codificar variables categóricas para el partido de ejemplo
partido_ejemplo_encoded = pd.get_dummies(partido_ejemplo, columns=['Equipo_local', 'Equipo_visitante'])

partido_ejemplo_encoded, _ = partido_ejemplo_encoded.align(X_train_encoded, join='outer', axis=1, fill_value=0)
# Obtener las columnas que faltan en partido_ejemplo_encoded
columnas_faltantes = set(X_train_encoded.columns) - set(partido_ejemplo_encoded.columns)

# Agregar las columnas faltantes a partido_ejemplo_encoded y establecer su valor en 0
for columna in columnas_faltantes:
    partido_ejemplo_encoded[columna] = 0

# Realizar predicciones sobre el partido de ejemplo
prediccion_local = modelo_rf_local.predict(partido_ejemplo_encoded)
prediccion_visitante = modelo_rf_visitante.predict(partido_ejemplo_encoded)

# Presentar el resultado del partido de ejemplo
resultado_final = f"{int(round(prediccion_local[0]))}-{int(round(prediccion_visitante[0]))}"
print("Resultado del partido de ejemplo:", resultado_final)
