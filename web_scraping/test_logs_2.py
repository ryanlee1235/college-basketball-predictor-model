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
        df['Team'] = team
        
        df = df.rename(columns={
            'Unnamed: 0_level_0_Rk': 'Rk',
            'Unnamed: 1_level_0_Gtm': 'Game_num',
            'Unnamed: 2_level_0_Date': 'Date',
            'Unnamed: 3_level_0_Unnamed: 3_level_1': 'Home_away_raw',
            'Unnamed: 4_level_0_Opp': 'Opponent',
            'Unnamed: 5_level_0_Type': 'Game_type',
            'Score_Rslt': 'Result',
            'Score_Tm': 'Team_pts',
            'Score_Opp': 'Opp_pts',
            'Score_OT': 'OT'
        })

        # Removed the header repeats that came from other like post season stuff
        df = df[df['Date'].notna()]
        df = df[df['Date'] != 'Date']

        # Convert Win/Draw/Loss to 1/0
        df['Won'] = df['Result'].apply(lambda x: 1 if x == 'W' else 0)

        # Convert Home or Away (or neither) to a number
        df['Home_away'] = df['Home_away_raw'].apply(
            lambda x: 0 if '@' in str(x) else (2 if 'N' in str(x) else 1)
        )

        # Clean opponent names to match the url of the home team (allows me to easily categorize teams)
        # into numbers in my ML processing
        df['Opponent'] = df['Opponent'].str.lower().str.replace(' ', '-').str.replace('\'', '').str.replace('.', '').str.replace('(', '').str.replace(')', '').str.replace('&', '')

        # Define non-numeric columns
        non_numeric = ['Date', 'Team', 'Opponent', 'Home_away_raw', 'Game_type', 'Result', 'OT']

        # Convert everything else to numeric
        for col in df.columns:
            if col not in non_numeric:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # print(df.dtypes)

        feature_columns = [
            'Game_num','Date','Home_away','Team','Opponent','Game_type','Won','Team_pts','Opp_pts','Team_FG%','Team_3P%','Team_2P%','Team_eFG%',
            'Team_FT%','Team_ORB','Team_DRB','Team_TRB','Team_AST','Team_STL','Team_BLK','Team_TOV','Team_PF','Opponent_FG%','Opponent_3P%',
            'Opponent_2P%','Opponent_eFG%','Opponent_FT%','Opponent_ORB','Opponent_DRB','Opponent_TRB','Opponent_AST','Opponent_STL','Opponent_BLK',
            'Opponent_TOV','Opponent_PF'
        ]

        # Keep only columns that exist
        feature_columns = [col for col in feature_columns if col in df.columns]
        df_clean = df[feature_columns]

        # Save raw data first to inspect
        df_clean.to_csv(f'./game_logs/{team}_cleaned.csv', index=False)
        print(f"✓ {team}: {len(df_clean)} games - saved to {team}_cleaned.csv")
        
        all_games.append(df)
        time.sleep(3)
        
    except Exception as e:
        print(f"✗ Error: {e}")

# if all_games:
#     final_df = pd.concat(all_games, ignore_index=True)
#     final_df.to_csv('all_games_raw.csv', index=False)
#     print("\n✓ Check the CSV files to see column names, then update the script")