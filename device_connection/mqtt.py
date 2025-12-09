#!/usr/bin/env python3
import json
import joblib
import paho.mqtt.client as mqtt
import numpy as np
import pandas as pd
from datetime import datetime

MQTT_BROKER = "192.0.0.2"  # <-- change to your broker IP (maybe localhost)
MQTT_PORT = 1883
TOPIC_FEATURES = "usc/model/features"
TOPIC_PREDICTION = "usc/model/prediction"

# Load the trained RandomForest model
model = joblib.load("../ml_model/usc_predictor_model.pkl")
print("Loaded RandomForest model from usc_predictor_model.pkl")

# Must match the order used in training
feature_cols = [
    'Game_num','Day_code', 'Home_away','Team_code','Op_code','Team_pts_L3','Opp_pts_L3','Team_FG%_L3',
    'Team_3P%_L3','Team_2P%_L3','Team_FT%_L3','Team_ORB_L3','Team_DRB_L3','Team_AST_L3','Team_STL_L3',
    'Team_BLK_L3','Team_TOV_L3','Team_PF','Opp_FG%_L3','Opp_3P%_L3','Opp_2P%_L3','Opp_FT%_L3',
    'Opp_ORB_L3','Opp_DRB_L3','Opp_AST_L3','Opp_STL_L3','Opp_BLK_L3','Opp_TOV_L3','Opponent_PF'
]

def prepare_features(data):
    """Convert MQTT data to model features"""
    features = {
        'Game_num': int(data.get("game_num", 1)),
        'Day_code': int(data.get("day_code", 0)),
        'Home_away': 1 if data.get("home") else 0,
        'Team_code': int(data.get("team_code", 0)),
        'Op_code': int(data.get("op_code", 0)),
        'Team_pts_L3': float(data.get("team_pts_l3", 0.0)),
        'Opp_pts_L3': float(data.get("opp_pts_l3", 0.0)),
        'Team_FG%_L3': float(data.get("team_fg_pct_l3", 0.0)),
        'Team_3P%_L3': float(data.get("team_3p_pct_l3", 0.0)),
        'Team_2P%_L3': float(data.get("team_2p_pct_l3", 0.0)),
        'Team_FT%_L3': float(data.get("team_ft_pct_l3", 0.0)),
        'Team_ORB_L3': float(data.get("team_orb_l3", 0.0)),
        'Team_DRB_L3': float(data.get("team_drb_l3", 0.0)),
        'Team_AST_L3': float(data.get("team_ast_l3", 0.0)),
        'Team_STL_L3': float(data.get("team_stl_l3", 0.0)),
        'Team_BLK_L3': float(data.get("team_blk_l3", 0.0)),
        'Team_TOV_L3': float(data.get("team_tov_l3", 0.0)),
        'Team_PF': float(data.get("team_pf", 0.0)),
        'Opp_FG%_L3': float(data.get("opp_fg_pct_l3", 0.0)),
        'Opp_3P%_L3': float(data.get("opp_3p_pct_l3", 0.0)),
        'Opp_2P%_L3': float(data.get("opp_2p_pct_l3", 0.0)),
        'Opp_FT%_L3': float(data.get("opp_ft_pct_l3", 0.0)),
        'Opp_ORB_L3': float(data.get("opp_orb_l3", 0.0)),
        'Opp_DRB_L3': float(data.get("opp_drb_l3", 0.0)),
        'Opp_AST_L3': float(data.get("opp_ast_l3", 0.0)),
        'Opp_STL_L3': float(data.get("opp_stl_l3", 0.0)),
        'Opp_BLK_L3': float(data.get("opp_blk_l3", 0.0)),
        'Opp_TOV_L3': float(data.get("opp_tov_l3", 0.0)),
        'Opponent_PF': float(data.get("opp_pf", 0.0))
    }
    
    X = pd.DataFrame([features])
    X = X[feature_cols]  # Ensure correct order
    return X

def on_message(client, userdata, msg):
    try:
        request = json.loads(msg.payload.decode())
        print(f"Prediction request received")
        
        # Prepare features
        X = prepare_features(request)
        
        # Predict
        win_prob = model.predict_proba(X)[0][1]
        
        # Send response
        response = {
            'win_probability': float(win_prob),
            'timestamp': datetime.now().isoformat()
        }
        client.publish(TOPIC_PREDICTION, json.dumps(response))
        print(f"Prediction: {win_prob:.1%}")
        
    except Exception as e:
        print(f"Error: {e}")

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with code", rc)
    client.subscribe(TOPIC_FEATURES)
    print("Subscribed to", TOPIC_FEATURES)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()