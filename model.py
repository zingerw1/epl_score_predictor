import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import pickle

def train_models(df):
    """
    Train Random Forest models for home and away goals with additional features.
    """
    features = ['HomeTeam_encoded', 'AwayTeam_encoded', 'HST', 'AST', 'HC', 'AC', 'HF', 'AF', 'HY', 'AY', 'HR', 'AR',
                'HomeRollingGF', 'HomeRollingGA', 'AwayRollingGF', 'AwayRollingGA', 'HomeForm', 'AwayForm',
                'HomeStrength', 'AwayStrength', 'FormInteraction', 'StrengthInteraction']
    X = df[features]
    y_home = df['FTHG']
    y_away = df['FTAG']

    X_train, X_test, y_home_train, y_home_test, y_away_train, y_away_test = train_test_split(
        X, y_home, y_away, test_size=0.2, random_state=42
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Home goals model
    home_model = RandomForestRegressor(random_state=42, n_estimators=100)
    home_model.fit(X_train_scaled, y_home_train)
    home_pred = home_model.predict(X_test_scaled)
    print(f"Home Goals MSE: {mean_squared_error(y_home_test, home_pred)}")

    # Away goals model
    away_model = RandomForestRegressor(random_state=42, n_estimators=100)
    away_model.fit(X_train_scaled, y_away_train)
    away_pred = away_model.predict(X_test_scaled)
    print(f"Away Goals MSE: {mean_squared_error(y_away_test, away_pred)}")

    # Save models and scaler
    with open('home_model.pkl', 'wb') as f:
        pickle.dump(home_model, f)
    with open('away_model.pkl', 'wb') as f:
        pickle.dump(away_model, f)
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    return home_model, away_model, scaler

if __name__ == "__main__":
    df = pd.read_csv('epl_data.csv')
    train_models(df)
    print("Models trained and saved.")
