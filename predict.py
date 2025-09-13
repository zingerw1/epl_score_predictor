import pickle
import numpy as np

def load_models():
    with open('home_model.pkl', 'rb') as f:
        home_model = pickle.load(f)
    with open('away_model.pkl', 'rb') as f:
        away_model = pickle.load(f)
    with open('label_encoder.pkl', 'rb') as f:
        le = pickle.load(f)
    return home_model, away_model, le

def predict_score(home_team, away_team):
    home_model, away_model, le = load_models()
    try:
        home_encoded = le.transform([home_team])[0]
        away_encoded = le.transform([away_team])[0]
    except ValueError:
        return "Unknown team(s)", "Unknown team(s)"

    features = np.array([[home_encoded, away_encoded]])
    home_goals = round(home_model.predict(features)[0])
    away_goals = round(away_model.predict(features)[0])
    return home_goals, away_goals

if __name__ == "__main__":
    home, away = predict_score('Arsenal', 'Chelsea')
    print(f"Predicted score: {home} - {away}")
