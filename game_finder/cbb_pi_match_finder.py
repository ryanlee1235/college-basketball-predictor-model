import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time

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

    def checkOutliers(name):
        name = str(name)
        if name == 'UTSA':
            return 'texas-san-antonio'
        else:
            return name.lower().replace(' ', '-').replace('\'', '').replace('.', '').replace('(', '').replace(')', '').replace('&', '')
    
    df['Opponent'] = df['D_opponent'].apply(checkOutliers)

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

    def scrape_team_stats_detailed(team_name, gender='men', year='2026'):
        url = f'https://www.sports-reference.com/cbb/schools/{team_name}/{gender}/{year}.html#all_per_game_team'
        
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the per-game stats table by ID
            table = soup.find('table', {'id': 'season-total_per_game'})
            
            if table:
                # Use pandas to parse the table
                df = pd.read_html(str(table))[0]
                
                # Flatten columns if multi-level
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = ['_'.join(str(i) for i in col).strip('_') for col in df.columns.values]
                
                # Get Team row (first row)
                team_stats = df.iloc[0].to_dict()
                team_stats['team_name'] = team_name
                
                return team_stats
            else:
                print(f"Table not found for {team_name}")
                return None
                
        except Exception as e:
            print(f"Error: {e}")
            return None

    # Collect all stats
    stats_list = []
    team_list = [team] + next_6_games['Opponent'].tolist()
    for curr_team in team_list:
        # curr_team = team_row["Opponent"]
        print(f"Scraping {curr_team}...")
        stats = scrape_team_stats_detailed(curr_team)
        if stats:
            stats_list.append(stats)
        time.sleep(3)

    df = pd.DataFrame(stats_list)
    print(df)
    # df.to_csv('team_stats_for_predictions.csv', index=False)
    
except Exception as e:
        print(f"✗ Error with {team}, {year}: {e}")

