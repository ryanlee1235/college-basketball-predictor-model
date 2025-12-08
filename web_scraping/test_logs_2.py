import pandas as pd
import time

teams = ['southern-california']
year = '2025'
all_games = []

for team in teams:
    url = f'https://www.sports-reference.com/cbb/schools/{team}/men/{year}-gamelogs.html'
    
    try:
        # Read table with header parameter to handle multi-level
        df = pd.read_html(url, header=[0, 1])[0]
        
        # Flatten columns
        df.columns = ['_'.join(str(i) for i in col).strip('_') for col in df.columns.values]
        
        # Add team
        df['team'] = team
        
        # Save raw data first to inspect
        df.to_csv(f'{team}_raw.csv', index=False)
        print(f"✓ {team}: {len(df)} games - saved to {team}_raw.csv")
        
        all_games.append(df)
        time.sleep(3)
        
    except Exception as e:
        print(f"✗ Error: {e}")

if all_games:
    final_df = pd.concat(all_games, ignore_index=True)
    final_df.to_csv('all_games_raw.csv', index=False)
    print("\n✓ Check the CSV files to see column names, then update the script")