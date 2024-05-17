import pandas as pd
import numpy as np

# Cargar los datos
dataframe_completo = pd.read_csv("dataframe_completo.csv")

# Definir la lógica de Monte Carlo para predecir el marcador
def monte_carlo_score_simulation(team1_stats, team2_stats, num_simulations=1000):
    team1_scores = []
    team2_scores = []

    for _ in range(num_simulations):
        # Obtener las estadísticas relevantes de los equipos
        team1_mean_score = team1_stats['Puntuacion_local']
        team2_mean_score = team2_stats['Puntuacion_visitante']

        # Simular los goles anotados utilizando una distribución Poisson
        team1_score = np.random.poisson(team1_mean_score)
        team2_score = np.random.poisson(team2_mean_score)

        team1_scores.append(team1_score)
        team2_scores.append(team2_score)

    # Calcular las medias de los goles anotados por cada equipo
    mean_team1_score = np.mean(team1_scores)
    mean_team2_score = np.mean(team2_scores)

    # Redondear las medias al número entero más cercano
    predicted_team1_score = int(round(mean_team1_score))
    predicted_team2_score = int(round(mean_team2_score))

    return predicted_team1_score, predicted_team2_score

# Definir los partidos de enfrentamiento
enfrentamientos = pd.DataFrame({
    'Equipo_local': ['Paris Saint-Germain', 'Real Madrid'],
    'Equipo_visitante': ['Borussia Dortmund', 'Bayern München']
})

# Inicializar las predicciones de los enfrentamientos
predicciones_enfrentamientos = []

# Realizar predicciones sobre los enfrentamientos utilizando Monte Carlo
for index, enfrentamiento in enfrentamientos.iterrows():
    # Obtener las estadísticas de los equipos para el enfrentamiento actual
    team1_stats = dataframe_completo[dataframe_completo['Equipo_local'] == enfrentamiento['Equipo_local']].iloc[0]
    team2_stats = dataframe_completo[dataframe_completo['Equipo_local'] == enfrentamiento['Equipo_visitante']].iloc[0]

    # Realizar la simulación de Monte Carlo para el marcador
    predicted_team1_score, predicted_team2_score = monte_carlo_score_simulation(team1_stats, team2_stats)

    # Guardar la predicción
    predicciones_enfrentamientos.append((predicted_team1_score, predicted_team2_score))

# Presentar los resultados de los enfrentamientos
for i, (equipo_local, equipo_visitante) in enumerate(zip(enfrentamientos['Equipo_local'], enfrentamientos['Equipo_visitante'])):
    print(f"Partido: {equipo_local} vs {equipo_visitante}, Predicción de marcador: {predicciones_enfrentamientos[i][0]} - {predicciones_enfrentamientos[i][1]}")
