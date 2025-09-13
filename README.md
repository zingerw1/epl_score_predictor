# EPL Score Predictor

A machine learning project to predict scores for English Premier League matches.

## How it Works

1. **Data Collection**: Downloads historical EPL match data from football-data.co.uk for seasons 2014-15 to 2022-23.

2. **Preprocessing**: Cleans the data, selects relevant columns (HomeTeam, AwayTeam, FTHG, FTAG), and encodes team names using LabelEncoder.

3. **Model Training**: Trains two Linear Regression models:

   - One for predicting home team goals (FTHG)
   - One for predicting away team goals (FTAG)
   - Features: Encoded home team and away team.

4. **Prediction**: For given home and away teams, encodes them and uses the models to predict goals.

5. **Web Interface**: A Flask app where users can input teams and see the predicted score.

## Files

- `requirements.txt`: Python dependencies
- `data.py`: Downloads and preprocesses data, saves `epl_data.csv` and `label_encoder.pkl`
- `model.py`: Trains models, saves `home_model.pkl` and `away_model.pkl`
- `predict.py`: Prediction function
- `app.py`: Flask web app

## Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Download data: `python data.py`
3. Train model: `python model.py`
4. Run app: `python app.py`
5. Open browser to `http://localhost:5000`, enter teams, predict.

Note: Models are simple linear regression; predictions may not be accurate. For better accuracy, more features like team stats, form, etc., could be added.
