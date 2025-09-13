import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle

def train_models(df):
    """
    Train linear regression models for home and away goals.
    """
    features = ['HomeTeam_encoded', 'AwayTeam_encoded']
    X = df[features]
    y_home = df['FTHG']
    y_away = df['FTAG']

    X_train, X_test, y_home_train, y_home_test, y_away_train, y_away_test = train_test_split(
        X, y_home, y_away, test_size=0.2, random_state=42
    )

    # Home goals model
    home_model = LinearRegression()
    home_model.fit(X_train, y_home_train)
    home_pred = home_model.predict(X_test)
    print(f"Home Goals MSE: {mean_squared_error(y_home_test, home_pred)}")

    # Away goals model
    away_model = LinearRegression()
    away_model.fit(X_train, y_away_train)
    away_pred = away_model.predict(X_test)
    print(f"Away Goals MSE: {mean_squared_error(y_away_test, away_pred)}")

    # Save models
    with open('home_model.pkl', 'wb') as f:
        pickle.dump(home_model, f)
    with open('away_model.pkl', 'wb') as f:
        pickle.dump(away_model, f)

    return home_model, away_model

if __name__ == "__main__":
    df = pd.read_csv('epl_data.csv')
    train_models(df)
    print("Models trained and saved.")
