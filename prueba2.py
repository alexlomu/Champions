import pandas as pd

# Ejemplo de datos
data = {'Columna1': ['Bayern München,2-1,Atletico Madrid › ESP (12)',
                     'Real Madrid CF,1-0,Manchester City FC › ENG (12)',
                     'Real Madrid CF,1-1 (*),Atletico Madrid › ESP (13)',
                     'FC Basel,1-1,PFC Ludogorets Razgrad',
                     'Paris Saint-Germain,1-1,Arsenal FC',
                     'Arsenal FC,2-0,FC Basel',
                     'PFC Ludogorets Razgrad,1-3,Paris Saint-Germain']}

df = pd.DataFrame(data)

# Eliminar la parte después del símbolo '›'
df['Columna1'] = df['Columna1'].str.split(' ›').str[0]

print(df)
