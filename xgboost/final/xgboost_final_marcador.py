import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost import XGBRegressor
import numpy as np

# Cargar los datos
dataframe_completo = pd.read_csv("dataframe_completo.csv")

# Dividir los datos en características (X) y etiquetas (y) para goles locales y visitantes
X = dataframe_completo[['Equipo_local', 'Equipo_visitante']]
y_local = dataframe_completo['Puntuacion_local']
y_visitante = dataframe_completo['Puntuacion_visitante']

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train_local, y_test_local, y_train_visitante, y_test_visitante = train_test_split(
    X, y_local, y_visitante, test_size=0.2, random_state=42
)

# Codificar variables categóricas para los datos de entrenamiento y prueba
X_train_encoded = pd.get_dummies(X_train)
X_test_encoded = pd.get_dummies(X_test)

# Asegurarse de que las columnas de los datos de entrenamiento y prueba coincidan exactamente
common_columns = X_train_encoded.columns.intersection(X_test_encoded.columns)
X_train_encoded = X_train_encoded[common_columns]
X_test_encoded = X_test_encoded[common_columns]

# Imputar los valores perdidos con la mediana
imputer = SimpleImputer(strategy='most_frequent')
imputer.fit(X_train_encoded)

X_train_imputed = imputer.transform(X_train_encoded)
X_test_imputed = imputer.transform(X_test_encoded)

# Escalar los datos
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imputed)
X_test_scaled = scaler.transform(X_test_imputed)

# Construir los modelos XGBoost para goles locales y visitantes
modelo_xgboost_local = XGBRegressor(random_state=42)
modelo_xgboost_visitante = XGBRegressor(random_state=42)

# Entrenar los modelos
modelo_xgboost_local.fit(X_train_scaled, y_train_local)
modelo_xgboost_visitante.fit(X_train_scaled, y_train_visitante)

# Realizar predicciones sobre los partidos de prueba
predicciones_local = modelo_xgboost_local.predict(X_test_scaled)
predicciones_visitante = modelo_xgboost_visitante.predict(X_test_scaled)

# Calcular la precisión de los modelos (usando el error cuadrático medio como métrica)
mse_local = np.mean((predicciones_local - y_test_local) ** 2)
mse_visitante = np.mean((predicciones_visitante - y_test_visitante) ** 2)
print("Error cuadrático medio del modelo para goles locales:", mse_local)
print("Error cuadrático medio del modelo para goles visitantes:", mse_visitante)

# Definir los partidos de enfrentamiento
enfrentamientos = pd.DataFrame({
    'Equipo_local': ['Real Madrid'],
    'Equipo_visitante': ['Paris Saint-Germain']
})

# Codificar variables categóricas para los enfrentamientos
enfrentamientos_encoded = pd.get_dummies(enfrentamientos)

# Asegurarse de que las columnas de los enfrentamientos coincidan exactamente con las del entrenamiento
enfrentamientos_encoded = enfrentamientos_encoded.reindex(columns=X_train_encoded.columns, fill_value=0)

# Realizar predicciones sobre los enfrentamientos
predicciones_enfrentamientos_local = modelo_xgboost_local.predict(enfrentamientos_encoded)
predicciones_enfrentamientos_visitante = modelo_xgboost_visitante.predict(enfrentamientos_encoded)

# Redondear las predicciones al número entero más cercano
predicciones_enfrentamientos_local = np.round(predicciones_enfrentamientos_local).astype(int)
predicciones_enfrentamientos_visitante = np.round(predicciones_enfrentamientos_visitante).astype(int)

# Presentar los resultados de los enfrentamientos
for i, (equipo_local, equipo_visitante) in enumerate(zip(enfrentamientos['Equipo_local'], enfrentamientos['Equipo_visitante'])):
    print(f"Partido: {equipo_local} vs {equipo_visitante}, Predicción de marcador: {predicciones_enfrentamientos_local[i]} - {predicciones_enfrentamientos_visitante[i]}")
