import joblib

model = joblib.load('usc_basketball_model.pkl')


"""['Game_num','Day_code', 'Home_away','Team_code','Op_code','Team_pts_L3','Opp_pts_L3','Team_FG%_L3',
    'Team_3P%_L3','Team_2P%_L3','Team_FT%_L3','Team_ORB_L3','Team_DRB_L3','Team_AST_L3','Team_STL_L3',
    'Team_BLK_L3','Team_TOV_L3','Team_PF','Opp_FG%_L3','Opp_3P%_L3','Opp_2P%_L3','Opp_FT%_L3',
    'Opp_ORB_L3','Opp_DRB_L3','Opp_AST_L3','Opp_STL_L3','Opp_BLK_L3','Opp_TOV_L3','Opponent_PF']"""

new_game = [[9,5,1,234,289,89.0,82.4,0.478,0.378,0.534,0.728,11.9,25.7,16.7,6.3,6.6,11.9,20,.446,.346,.496,.754,14.2,27.2,13.4,6.6,4.3,11.7,18.8]]
win_prob = model.predict_proba(new_game)[0][1]
print(f"Win probability: {win_prob:.1%}")