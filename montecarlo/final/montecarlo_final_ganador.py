import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

# Cargar los datos
dataframe_completo = pd.read_csv("dataframe_completo.csv")

# Definir la lógica de Monte Carlo
def monte_carlo_simulation(team1_stats, team2_stats, num_simulations=1000):
    # Simular múltiples juegos entre los equipos basados en sus estadísticas
    team1_wins = 0
    team2_wins = 0
    draws = 0

    for _ in range(num_simulations):
        # Obtener las estadísticas relevantes de los equipos
        team1_score = team1_stats['Puntuacion_local']
        team2_score = team2_stats['Puntuacion_visitante']

        # Determinar el resultado del juego
        if team1_score > team2_score:
            team1_wins += 1
        elif team1_score < team2_score:
            team2_wins += 1
        else:
            draws += 1

    # Calcular las probabilidades de los resultados
    prob_team1_win = team1_wins / num_simulations
    prob_team2_win = team2_wins / num_simulations
    prob_draw = draws / num_simulations

    return prob_team1_win, prob_team2_win, prob_draw

# Definir los partidos de enfrentamiento
enfrentamientos = pd.DataFrame({
    'Equipo_local': ['Real Madrid'],
    'Equipo_visitante': ['Paris Saint-Germain']
})

# Inicializar las predicciones de los enfrentamientos
predicciones_enfrentamientos = [''] * len(enfrentamientos)

# Realizar predicciones sobre los enfrentamientos utilizando Monte Carlo
for index, enfrentamiento in enfrentamientos.iterrows():
    # Obtener las estadísticas de los equipos para el enfrentamiento actual
    team1_stats = dataframe_completo[dataframe_completo['Equipo_local'] == enfrentamiento['Equipo_local']].iloc[0]
    team2_stats = dataframe_completo[dataframe_completo['Equipo_local'] == enfrentamiento['Equipo_visitante']].iloc[0]

    # Realizar la simulación de Monte Carlo
    prob_team1_win, prob_team2_win, prob_draw = monte_carlo_simulation(team1_stats, team2_stats)

    # Determinar la predicción basada en las probabilidades
    if prob_team1_win > prob_team2_win:
        predicciones_enfrentamientos[index] = 'Local'
    elif prob_team1_win < prob_team2_win:
        predicciones_enfrentamientos[index] = 'Visitante'
    else:
        predicciones_enfrentamientos[index] = 'Empate'

# Presentar los resultados de los enfrentamientos
label_encoder = LabelEncoder()
label_encoder.fit(['Empate', 'Local', 'Visitante'])

for i, (equipo_local, equipo_visitante) in enumerate(zip(enfrentamientos['Equipo_local'], enfrentamientos['Equipo_visitante'])):
    print(f"Partido: {equipo_local} vs {equipo_visitante}, Predicción: {label_encoder.classes_[label_encoder.transform([predicciones_enfrentamientos[i]])[0]]}")
