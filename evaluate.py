import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle
import numpy as np

def evaluate_models():
    # Load data
    df = pd.read_csv('epl_data.csv')

    # Prepare features
    features = ['HomeTeam_encoded', 'AwayTeam_encoded', 'HST', 'AST', 'HC', 'AC', 'HF', 'AF', 'HY', 'AY', 'HR', 'AR',
                'HomeRollingGF', 'HomeRollingGA', 'AwayRollingGF', 'AwayRollingGA', 'HomeForm', 'AwayForm',
                'HomeStrength', 'AwayStrength', 'FormInteraction', 'StrengthInteraction']
    X = df[features]
    y_home = df['FTHG']
    y_away = df['FTAG']

    # Split data (same as in model.py)
    X_train, X_test, y_home_train, y_home_test, y_away_train, y_away_test = train_test_split(
        X, y_home, y_away, test_size=0.2, random_state=42
    )

    # Load models and scaler
    with open('home_model.pkl', 'rb') as f:
        home_model = pickle.load(f)
    with open('away_model.pkl', 'rb') as f:
        away_model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    # Scale test features
    X_test_scaled = scaler.transform(X_test)

    # Predict on test set
    home_pred = home_model.predict(X_test_scaled)
    away_pred = away_model.predict(X_test_scaled)

    # Calculate metrics for home goals
    print("Home Goals Evaluation:")
    print(f"MSE: {mean_squared_error(y_home_test, home_pred):.4f}")
    print(f"MAE: {mean_absolute_error(y_home_test, home_pred):.4f}")
    print(f"R²: {r2_score(y_home_test, home_pred):.4f}")

    print("\nAway Goals Evaluation:")
    print(f"MSE: {mean_squared_error(y_away_test, away_pred):.4f}")
    print(f"MAE: {mean_absolute_error(y_away_test, away_pred):.4f}")
    print(f"R²: {r2_score(y_away_test, away_pred):.4f}")

    # Overall accuracy (exact score prediction)
    exact_matches = 0
    total = len(y_home_test)
    for i in range(total):
        pred_home = round(home_pred[i])
        pred_away = round(away_pred[i])
        actual_home = y_home_test.iloc[i]
        actual_away = y_away_test.iloc[i]
        if pred_home == actual_home and pred_away == actual_away:
            exact_matches += 1

    print(f"\nExact Score Accuracy: {exact_matches}/{total} ({exact_matches/total*100:.2f}%)")

    # Goal difference accuracy
    gd_matches = 0
    for i in range(total):
        pred_gd = round(home_pred[i]) - round(away_pred[i])
        actual_gd = y_home_test.iloc[i] - y_away_test.iloc[i]
        if pred_gd == actual_gd:
            gd_matches += 1

    print(f"Goal Difference Accuracy: {gd_matches}/{total} ({gd_matches/total*100:.2f}%)")

if __name__ == "__main__":
    evaluate_models()
