import pandas as pd
from datetime import datetime

team = 'southern-california'
display_team = "USC"
gender = 'men'
year = '2026'

url = f'https://www.sports-reference.com/cbb/schools/{team}/{gender}/{year}-gamelogs.html'

try:
    df = pd.read_html(url, header=[0, 1])[0]
    # Flatten columns
    df.columns = ['_'.join(str(i) for i in col).strip('_') for col in df.columns.values]

    df = df.rename(columns={
            'Unnamed: 0_level_0_Rk': 'Rk',
            'Unnamed: 1_level_0_Gtm': 'Game_num',
            'Unnamed: 2_level_0_Date': 'Date',
            'Unnamed: 3_level_0_Unnamed: 3_level_1': 'Home_away_raw',
            'Unnamed: 4_level_0_Opp': 'D_opponent',
            'Unnamed: 5_level_0_Type': 'Game_type'
        })
    # Add team
    df['D_team'] = display_team
    df['Team'] = team

    df['Opponent'] = df['D_opponent'].str.lower().str.replace(' ', '-').str.replace('\'', '').str.replace('.', '').str.replace('(', '').str.replace(')', '').str.replace('&', '')

    # Convert date column
    df['Date'] = pd.to_datetime(df['Date'])

    # Convert Home or Away (or neither) to a number
    df['Home_away'] = df['Home_away_raw'].apply(
        lambda x: 0 if '@' in str(x) else (2 if 'N' in str(x) else 1)
    )

    # Get current date
    today = datetime.now()

    # Filter for future games
    upcoming = df[df['Date'] >= today].sort_values('Date')

    # Get next 6
    next_6_games = upcoming.head(6)[['Rk', 'Date', 'Home_away', 'Team', 'D_team', 'Opponent', 'D_opponent']]

    print(next_6_games)

except Exception as e:
        print(f"✗ Error with {team}, {year}: {e}")