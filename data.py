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
    Preprocess the data: select relevant columns, handle missing values, encode teams.
    """
    # Select relevant columns
    cols = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'Season']
    df = df[cols].dropna()

    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

    # Encode teams
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    df['HomeTeam_encoded'] = le.fit_transform(df['HomeTeam'])
    df['AwayTeam_encoded'] = le.transform(df['AwayTeam'])

    return df, le

if __name__ == "__main__":
    seasons = ['1415', '1516', '1617', '1718', '1819', '1920', '2021', '2122', '2223']
    df = download_epl_data(seasons)
    df, le = preprocess_data(df)
    df.to_csv('epl_data.csv', index=False)
    with open('label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)
    print("Data downloaded and preprocessed.")
