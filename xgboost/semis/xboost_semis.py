import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost import XGBClassifier
import numpy as np

# Cargar los datos
dataframe_completo = pd.read_csv("dataframe_completo.csv")

# Calcular el resultado del partido (quién ganó y por cuánto)
dataframe_completo['Resultado'] = dataframe_completo.apply(
    lambda x: 'Empate' if x['Puntuacion_local'] == x['Puntuacion_visitante'] else 'Local' if x['Puntuacion_local'] > x['Puntuacion_visitante'] else 'Visitante',
    axis=1
)
dataframe_completo['Diferencia_goles'] = dataframe_completo['Puntuacion_local'] - dataframe_completo['Puntuacion_visitante']

# Dividir los datos en conjunto de entrenamiento y prueba
X = dataframe_completo[['Equipo_local', 'Equipo_visitante', 'Diferencia_goles']]
y = dataframe_completo['Resultado']

# Convertir clases categóricas a valores numéricos
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Codificar variables categóricas para los datos de entrenamiento y prueba
X_train_encoded = pd.get_dummies(X_train)
X_test_encoded = pd.get_dummies(X_test)

# Asegurarse de que las columnas de los datos de entrenamiento y prueba coincidan exactamente
# Esto es importante para garantizar que las columnas se codifiquen de la misma manera
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

# Construir el modelo XGBoost
modelo_xgboost = XGBClassifier(random_state=42)

# Entrenar el modelo
modelo_xgboost.fit(X_train_scaled, y_train)

# Realizar predicciones sobre los partidos de prueba
predicciones_proba = modelo_xgboost.predict_proba(X_test_scaled)

# Tomar la clase con la probabilidad más alta como la predicción
predicciones = np.argmax(predicciones_proba, axis=1)

# Calcular la precisión del modelo en los datos de prueba
precision = accuracy_score(y_test, predicciones)
print("Precisión del modelo en datos de prueba:", precision)

# Definir los partidos de enfrentamiento
enfrentamientos = pd.DataFrame({
    'Equipo_local': ['Borussia Dortmund', 'Bayern München'],
    'Equipo_visitante': ['Paris Saint-Germain', 'Real Madrid'],
    'Diferencia_goles': [None, None]  # No tenemos información sobre la diferencia de goles para estos partidos
})

# Codificar variables categóricas para los enfrentamientos
enfrentamientos_encoded = pd.get_dummies(enfrentamientos)

# Asegurarse de que las columnas de los enfrentamientos coincidan exactamente con las del entrenamiento
enfrentamientos_encoded = enfrentamientos_encoded.reindex(columns=X_train_encoded.columns, fill_value=0)

# Realizar predicciones sobre los enfrentamientos
predicciones_enfrentamientos_proba = modelo_xgboost.predict_proba(enfrentamientos_encoded)

# Tomar la clase con la probabilidad más alta como la predicción para los enfrentamientos
predicciones_enfrentamientos = np.argmax(predicciones_enfrentamientos_proba, axis=1)

# Presentar los resultados de los enfrentamientos
for i, (equipo_local, equipo_visitante) in enumerate(zip(enfrentamientos['Equipo_local'], enfrentamientos['Equipo_visitante'])):
    print(f"Partido: {equipo_local} vs {equipo_visitante}, Predicción: {label_encoder.classes_[predicciones_enfrentamientos[i]]}")
