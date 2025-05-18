"""
Developer: Andrianov Matvey
Task: Pandas Data Analysis
Version: 1.0
"""

import pandas as pd

df = pd.read_csv('./players_22.csv')

max_aggression = df['mentality_aggression'].max()
min_aggression = df['mentality_aggression'].min()

max_agg_players = df[df['mentality_aggression'] == max_aggression]
min_agg_players = df[df['mentality_aggression'] == min_aggression]

mean_shot_power_max = max_agg_players['power_shot_power'].mean()
mean_shot_power_min = min_agg_players['power_shot_power'].mean()

ratio = mean_shot_power_max / mean_shot_power_min
ratio_rounded = round(ratio, 2)

average_wage = df['wage_eur'].mean()
low_wage_players = df[df['wage_eur'] < average_wage]
mean_speed = low_wage_players['movement_sprint_speed'].mean()
mean_speed_rounded = round(mean_speed, 2)

print(f"Отношение силы удара: {ratio_rounded} раз")
print(f"Средняя скорость: {mean_speed_rounded}")