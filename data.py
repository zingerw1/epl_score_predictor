import pandas as pd
import requests
from io import StringIO
import pickle
from sklearn.preprocessing import LabelEncoder
import os
import gc

# Relevant columns to keep
COLUMNS = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'HST', 'AST', 'HC', 'AC',
           'HF', 'AF', 'HY', 'AY', 'HR', 'AR']

def download_epl_data(season):
    """
    Download EPL match data for a single season from football-data.co.uk.
    Handles malformed CSVs safely.
    """
    url = f"https://www.football-data.co.uk/mmz4281/{season}/E0.csv"
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text), usecols=lambda c: c in COLUMNS, on_bad_lines='skip')
        df['Season'] = season
        return df
    except Exception as e:
        print(f"Failed to download {season}: {e}")
        return pd.DataFrame()

def preprocess_data(df):
    """
    Preprocess a single season DataFrame.
    """
    df = df.copy().dropna()
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
    df = df.sort_values('Date').reset_index(drop=True)

    # Encode teams
    le = LabelEncoder()
    df['HomeTeam_encoded'] = le.fit_transform(df['HomeTeam'])
    df['AwayTeam_encoded'] = le.transform(df['AwayTeam'])

    # Add features
    df = add_team_features(df)

    # Downcast numeric columns to save memory
    numeric_cols = ['FTHG','FTAG','HST','AST','HC','AC','HF','AF','HY','AY','HR','AR',
                    'HomeRollingGF','HomeRollingGA','AwayRollingGF','AwayRollingGA',
                    'HomeForm','AwayForm','HomeStrength','AwayStrength','FormInteraction','StrengthInteraction']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], downcast='float')

    return df, le

def add_team_features(df):
    """
    Add rolling averages, form, strength, and interaction features using transform for memory efficiency.
    """
    # Points
    df['HomePoints'] = df.apply(lambda x: 3 if x['FTHG'] > x['FTAG'] else 1 if x['FTHG'] == x['FTAG'] else 0, axis=1)
    df['AwayPoints'] = df.apply(lambda x: 3 if x['FTAG'] > x['FTHG'] else 1 if x['FTAG'] == x['FTHG'] else 0, axis=1)

    # Rolling stats per team using transform
    df['HomeRollingGF'] = df.groupby('HomeTeam')['FTHG'].transform(lambda x: x.rolling(5, min_periods=1).mean())
    df['HomeRollingGA'] = df.groupby('HomeTeam')['FTAG'].transform(lambda x: x.rolling(5, min_periods=1).mean())
    df['HomeForm'] = df.groupby('HomeTeam')['HomePoints'].transform(lambda x: x.rolling(5, min_periods=1).mean())

    df['AwayRollingGF'] = df.groupby('AwayTeam')['FTAG'].transform(lambda x: x.rolling(5, min_periods=1).mean())
    df['AwayRollingGA'] = df.groupby('AwayTeam')['FTHG'].transform(lambda x: x.rolling(5, min_periods=1).mean())
    df['AwayForm'] = df.groupby('AwayTeam')['AwayPoints'].transform(lambda x: x.rolling(5, min_periods=1).mean())

    # Fill missing values
    df['HomeRollingGF'] = df['HomeRollingGF'].fillna(df['FTHG'].mean())
    df['HomeRollingGA'] = df['HomeRollingGA'].fillna(df['FTAG'].mean())
    df['HomeForm'] = df['HomeForm'].fillna(1.5)
    df['AwayRollingGF'] = df['AwayRollingGF'].fillna(df['FTAG'].mean())
    df['AwayRollingGA'] = df['AwayRollingGA'].fillna(df['FTHG'].mean())
    df['AwayForm'] = df['AwayForm'].fillna(1.5)

    # Strengths
    home_strength = df.groupby('HomeTeam')['FTHG'].mean() - df.groupby('HomeTeam')['FTAG'].mean()
    away_strength = df.groupby('AwayTeam')['FTAG'].mean() - df.groupby('AwayTeam')['FTHG'].mean()
    df['HomeStrength'] = df['HomeTeam'].map(home_strength).fillna(0)
    df['AwayStrength'] = df['AwayTeam'].map(away_strength).fillna(0)

    # Interactions
    df['FormInteraction'] = df['HomeForm'] * df['AwayForm']
    df['StrengthInteraction'] = df['HomeStrength'] * df['AwayStrength']

    return df

if __name__ == "__main__":
    seasons = [f"{str(y)[-2:]}{str(y+1)[-2:]}" for y in range(2000, 2025)]
    csv_file = 'epl_data.csv'
    label_file = 'label_encoder.pkl'

    # Remove old files to start fresh
    if os.path.exists(csv_file):
        os.remove(csv_file)

    for season in seasons:
        print(f"Processing season {season}...")
        df_season = download_epl_data(season)
        if df_season.empty:
            continue
        df_season, le = preprocess_data(df_season)

        # Append season to CSV
        df_season.to_csv(csv_file, mode='a', index=False, header=not os.path.exists(csv_file))

        # Save LabelEncoder (overwrite each time is fine)
        with open(label_file, 'wb') as f:
            pickle.dump(le, f)

        # Clean up memory
        del df_season
        gc.collect()

    print("All seasons processed successfully. Dataset is ready!")

    # Fit label encoder on all teams from the dataset
    df_all = pd.read_csv(csv_file)
    all_teams = pd.concat([df_all['HomeTeam'], df_all['AwayTeam']]).unique()
    le = LabelEncoder()
    le.fit(all_teams)
    with open(label_file, 'wb') as f:
        pickle.dump(le, f)
    print(f"Label encoder updated with {len(le.classes_)} teams.")
