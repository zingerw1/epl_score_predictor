import pandas as pd
import requests
from io import StringIO
import pickle

def download_epl_data(seasons):
    """
    Download EPL match data for given seasons from football-data.co.uk
    Seasons format: '1415' for 2014-15, etc.
    """
    base_url = "https://www.football-data.co.uk/mmz4281/{}/E0.csv"
    dfs = []
    for season in seasons:
        url = base_url.format(season)
        try:
            response = requests.get(url)
            response.raise_for_status()
            df = pd.read_csv(StringIO(response.text))
            df['Season'] = season
            dfs.append(df)
        except Exception as e:
            print(f"Failed to download {season}: {e}")
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def preprocess_data(df):
    """
    Preprocess the data: select relevant columns, handle missing values, encode teams, add feature engineering.
    """
    # Select relevant columns including additional features
    cols = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'HST', 'AST', 'HC', 'AC', 'HF', 'AF', 'HY', 'AY', 'HR', 'AR', 'Season']
    df = df[cols].dropna()

    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    df = df.sort_values('Date').reset_index(drop=True)

    # Encode teams
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    df['HomeTeam_encoded'] = le.fit_transform(df['HomeTeam'])
    df['AwayTeam_encoded'] = le.transform(df['AwayTeam'])

    # Feature engineering: rolling averages and form
    df = add_team_features(df)

    return df, le

def add_team_features(df):
    """
    Add rolling averages, form, and interaction features.
    """
    # Calculate points for each match
    df['HomePoints'] = df.apply(lambda x: 3 if x['FTHG'] > x['FTAG'] else 1 if x['FTHG'] == x['FTAG'] else 0, axis=1)
    df['AwayPoints'] = df.apply(lambda x: 3 if x['FTAG'] > x['FTHG'] else 1 if x['FTAG'] == x['FTHG'] else 0, axis=1)

    # Home team stats
    home_stats = df.groupby('HomeTeam').apply(lambda x: x.assign(
        HomeRollingGF=x['FTHG'].rolling(5, min_periods=1).mean(),
        HomeRollingGA=x['FTAG'].rolling(5, min_periods=1).mean(),
        HomeForm=x['HomePoints'].rolling(5, min_periods=1).mean()
    )).reset_index(drop=True)

    # Away team stats
    away_stats = df.groupby('AwayTeam').apply(lambda x: x.assign(
        AwayRollingGF=x['FTAG'].rolling(5, min_periods=1).mean(),
        AwayRollingGA=x['FTHG'].rolling(5, min_periods=1).mean(),
        AwayForm=x['AwayPoints'].rolling(5, min_periods=1).mean()
    )).reset_index(drop=True)

    # Merge back
    df = df.merge(home_stats[['Date', 'HomeTeam', 'HomeRollingGF', 'HomeRollingGA', 'HomeForm']], on=['Date', 'HomeTeam'], how='left')
    df = df.merge(away_stats[['Date', 'AwayTeam', 'AwayRollingGF', 'AwayRollingGA', 'AwayForm']], on=['Date', 'AwayTeam'], how='left')

    # Fill NaN with overall averages
    df['HomeRollingGF'].fillna(df['FTHG'].mean(), inplace=True)
    df['HomeRollingGA'].fillna(df['FTAG'].mean(), inplace=True)
    df['HomeForm'].fillna(1.5, inplace=True)  # Average points
    df['AwayRollingGF'].fillna(df['FTAG'].mean(), inplace=True)
    df['AwayRollingGA'].fillna(df['FTHG'].mean(), inplace=True)
    df['AwayForm'].fillna(1.5, inplace=True)

    # Home/away strength
    home_strength = df.groupby('HomeTeam')['FTHG'].mean() - df.groupby('HomeTeam')['FTAG'].mean()
    away_strength = df.groupby('AwayTeam')['FTAG'].mean() - df.groupby('AwayTeam')['FTHG'].mean()
    df['HomeStrength'] = df['HomeTeam'].map(home_strength).fillna(0)
    df['AwayStrength'] = df['AwayTeam'].map(away_strength).fillna(0)

    # Interaction features
    df['FormInteraction'] = df['HomeForm'] * df['AwayForm']
    df['StrengthInteraction'] = df['HomeStrength'] * df['AwayStrength']

    return df

if __name__ == "__main__":
    seasons = ['1415', '1516', '1617', '1718', '1819', '1920', '2021', '2122', '2223']
    df = download_epl_data(seasons)
    df, le = preprocess_data(df)
    df.to_csv('epl_data.csv', index=False)
    with open('label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)
    print("Data downloaded and preprocessed.")
