import pandas as pd
import numpy as np

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
    'Equipo_local': ['Borussia Dortmund', 'Bayern München'],
    'Equipo_visitante': ['Paris Saint-Germain', 'Real Madrid']
})

# Realizar predicciones sobre los enfrentamientos utilizando Monte Carlo
for index, enfrentamiento in enfrentamientos.iterrows():
    # Obtener las estadísticas de los equipos para el enfrentamiento actual
    team1_stats = dataframe_completo[dataframe_completo['Equipo_local'] == enfrentamiento['Equipo_local']].iloc[0]
    team2_stats = dataframe_completo[dataframe_completo['Equipo_local'] == enfrentamiento['Equipo_visitante']].iloc[0]

    # Realizar la simulación de Monte Carlo
    prob_team1_win, prob_team2_win, prob_draw = monte_carlo_simulation(team1_stats, team2_stats)

    # Presentar los resultados
    print(f"Partido: {enfrentamiento['Equipo_local']} vs {enfrentamiento['Equipo_visitante']}")
    print(f"Probabilidad de victoria de {enfrentamiento['Equipo_local']}: {prob_team1_win}")
    print(f"Probabilidad de victoria de {enfrentamiento['Equipo_visitante']}: {prob_team2_win}")
    print(f"Probabilidad de empate: {prob_draw}")
 