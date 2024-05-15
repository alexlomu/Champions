import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost import XGBRegressor

# Cargar los datos
dataframe_completo = pd.read_csv("dataframe_completo.csv")

# Definir los enfrentamientos específicos
enfrentamientos = pd.DataFrame({
    'Equipo_local': ['Borussia Dortmund', 'Bayern München'],
    'Equipo_visitante': ['Paris Saint-Germain', 'Real Madrid']
})

# Convertir equipos a valores numéricos
label_encoder = LabelEncoder()
enfrentamientos['Equipo_local'] = label_encoder.fit_transform(enfrentamientos['Equipo_local'])
enfrentamientos['Equipo_visitante'] = label_encoder.transform(enfrentamientos['Equipo_visitante'])

# Filtrar los datos para los enfrentamientos específicos
datos_enfrentamientos = dataframe_completo[dataframe_completo['Equipo_local'].isin(enfrentamientos['Equipo_local']) & dataframe_completo['Equipo_visitante'].isin(enfrentamientos['Equipo_visitante'])]

# Dividir los datos en características (X) y objetivos (y)
X_enfrentamientos = datos_enfrentamientos[['Equipo_local', 'Equipo_visitante']]
y_local_enfrentamientos = datos_enfrentamientos['Puntuacion_local']
y_visitante_enfrentamientos = datos_enfrentamientos['Puntuacion_visitante']

# Imputar los valores perdidos con la mediana
imputer = SimpleImputer(strategy='median')
X_imputed_enfrentamientos = imputer.fit_transform(X_enfrentamientos)

# Escalar los datos
scaler = StandardScaler()
X_scaled_enfrentamientos = scaler.fit_transform(X_imputed_enfrentamientos)

# Construir y entrenar modelos XGBoost para el puntaje del equipo local y visitante
modelo_xgboost_local = XGBRegressor(objective='reg:squarederror', random_state=42)
modelo_xgboost_visitante = XGBRegressor(objective='reg:squarederror', random_state=42)

modelo_xgboost_local.fit(X_scaled_enfrentamientos, y_local_enfrentamientos)
modelo_xgboost_visitante.fit(X_scaled_enfrentamientos, y_visitante_enfrentamientos)

# Realizar predicciones sobre los enfrentamientos
predicciones_puntaje_local = modelo_xgboost_local.predict(X_scaled_enfrentamientos)
predicciones_puntaje_visitante = modelo_xgboost_visitante.predict(X_scaled_enfrentamientos)

# Presentar los resultados de los enfrentamientos
for i, (equipo_local, equipo_visitante) in enumerate(zip(enfrentamientos['Equipo_local'], enfrentamientos['Equipo_visitante'])):
    print(f"Partido: {label_encoder.classes_[equipo_local]} vs {label_encoder.classes_[equipo_visitante]}, Predicción del marcador: {int(predicciones_puntaje_local[i])} - {int(predicciones_puntaje_visitante[i])}")
