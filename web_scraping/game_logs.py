import pandas as pd
import time
from bs4 import BeautifulSoup
import requests

teams = ['southern-california']
gender = 'men'
year = '2025'
all_games = []

for team in teams:
    url = f'https://www.sports-reference.com/cbb/schools/{team}/{gender}/{year}-gamelogs.html'
    try:

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find('table', {'id': 'team_game_log'})

        if table:
            df = pd.read_html(str(table))[0]
            
            # Get all the column names
            cols = df.columns.tolist()

            new_cols = []
            seen = {}

            for col in cols:
                if col in seen:
                    # This is a duplicate - it's opponent stats
                    seen[col] += 1
                    new_cols.append(f'Opp_{col}')
                else:
                    # First occurrence - it's team stats (or unique column)
                    seen[col] = 1
                    new_cols.append(col)

            df.columns = new_cols

            # Now rename specific columns for clarity
            df = df.rename(columns={
                'Opp': 'Opponent',           # Opponent name
                'Opp_Opp': 'Opp_pts',        # Opponent points
                'Tm': 'Team_pts',            # Team points
                'Type': 'Game_type',
                'Rslt': 'Result'
            })

            df['Team'] = team

            df['Opponent'] = df['Opponent'].str.lower().str.replace(' ', '-')

            # Add home/away indicator
            df['Home_away'] = df[''].apply(
                lambda x: 0 if '@' in str(x) else (2 if 'N' else 1) # N = neutral site, @ = away, '' = home
            )
            
            # Convert W/L to binary
            df['Won'] = df['result'].apply(lambda x: 1 if 'W' in str(x) else 0)
            print(f"✓ {team}: {len(df)} games, {len(df.columns)} columns")

            all_games.append(df)
            print(f"Downloaded {team}: {len(df)} games")

            time.sleep(4)

    except Exception as e:
        print(f"✗ Error with {team}: {e}")

# Combine all
final_df = pd.concat(all_games, ignore_index=True)
final_df.to_csv('cbb_games_usc_test_2025.csv', index=False)
print(f"\n✓ Total: {len(final_df)} games saved")