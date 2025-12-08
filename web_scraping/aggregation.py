import pandas as pd
import glob

csv_files = glob.glob('game_logs/*.csv')

dataframes = []

for i in range(2023, 2027):
    df = pd.read_csv('./game_logs/cbb_games_' + str(i) + '.csv')
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)
combined_df.to_csv('./game_logs/cbb_games_23-26.csv', index=False)