import pickle
import numpy as np
import pandas as pd

def load_models():
    with open('home_model.pkl', 'rb') as f:
        home_model = pickle.load(f)
    with open('away_model.pkl', 'rb') as f:
        away_model = pickle.load(f)
    with open('label_encoder.pkl', 'rb') as f:
        le = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    df = pd.read_csv('epl_data.csv')
    return home_model, away_model, le, scaler, df

def predict_score(home_team, away_team):
    home_model, away_model, le, scaler, df = load_models()
    try:
        home_encoded = le.transform([home_team])[0]
        away_encoded = le.transform([away_team])[0]
    except ValueError:
        return "Unknown team(s)", "Unknown team(s)"

    # Get latest stats for teams
    home_latest = df[df['HomeTeam'] == home_team].sort_values('Date').iloc[-1] if not df[df['HomeTeam'] == home_team].empty else None
    away_latest = df[df['AwayTeam'] == away_team].sort_values('Date').iloc[-1] if not df[df['AwayTeam'] == away_team].empty else None

    if home_latest is None or away_latest is None:
        # Fallback to averages
        home_stats = df[['HST', 'HC', 'HF', 'HY', 'HR']].mean()
        away_stats = df[['AST', 'AC', 'AF', 'AY', 'AR']].mean()
        home_rolling_gf = df['FTHG'].mean()
        home_rolling_ga = df['FTAG'].mean()
        home_form = 1.5
        away_rolling_gf = df['FTAG'].mean()
        away_rolling_ga = df['FTHG'].mean()
        away_form = 1.5
        home_strength = 0
        away_strength = 0
    else:
        home_stats = home_latest[['HST', 'HC', 'HF', 'HY', 'HR']]
        away_stats = away_latest[['AST', 'AC', 'AF', 'AY', 'AR']]
        home_rolling_gf = home_latest['HomeRollingGF']
        home_rolling_ga = home_latest['HomeRollingGA']
        home_form = home_latest['HomeForm']
        away_rolling_gf = away_latest['AwayRollingGF']
        away_rolling_ga = away_latest['AwayRollingGA']
        away_form = away_latest['AwayForm']
        home_strength = home_latest['HomeStrength']
        away_strength = away_latest['AwayStrength']

    form_interaction = home_form * away_form
    strength_interaction = home_strength * away_strength

    features = np.array([[home_encoded, away_encoded, home_stats['HST'], away_stats['AST'],
                          home_stats['HC'], away_stats['AC'], home_stats['HF'], away_stats['AF'],
                          home_stats['HY'], away_stats['AY'], home_stats['HR'], away_stats['AR'],
                          home_rolling_gf, home_rolling_ga, away_rolling_gf, away_rolling_ga,
                          home_form, away_form, home_strength, away_strength, form_interaction, strength_interaction]])

    features_scaled = scaler.transform(features)
    home_goals = int(home_model.predict(features_scaled)[0])
    away_goals = int(away_model.predict(features_scaled)[0])
    return home_goals, away_goals

if __name__ == "__main__":
    home, away = predict_score('Arsenal', 'Chelsea')
    print(f"Predicted score: {home} - {away}")
