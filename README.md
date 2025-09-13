# EPL Score Predictor

A machine learning project to predict scores for English Premier League matches.

## How it Works

1. **Data Collection**: Downloads historical EPL match data from football-data.co.uk for seasons 2014-15 to 2022-23.

2. **Preprocessing**: Cleans the data, selects relevant columns (HomeTeam, AwayTeam, FTHG, FTAG), and encodes team names using LabelEncoder.

3. **Model Training**: Trains two Random Forest Regression models:

   - One for predicting home team goals (FTHG)
   - One for predicting away team goals (FTAG)
   - Features: Encoded home team and away team, shots on target, corners, fouls, cards, red cards.

4. **Prediction**: For given home and away teams, encodes them and uses the models to predict goals.

5. **Web Interface**: A Flask app where users can input teams and see the predicted score.

## Files

- `requirements.txt`: Python dependencies
- `data.py`: Downloads and preprocesses data, saves `epl_data.csv` and `label_encoder.pkl`
- `model.py`: Trains models, saves `home_model.pkl` and `away_model.pkl`
- `predict.py`: Prediction function
- `app.py`: Flask web app

## Prerequisites

- Python 3.7+
- Internet connection

## Setup Instructions

1. **Create Virtual Environment** (optional but recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Download Data**:

   ```bash
   python data.py
   ```

4. **Train Models**:

   ```bash
   python model.py
   ```

5. **Run Application**:

   ```bash
   python app.py
   ```

6. **Access the App**:
   - Open browser to `http://localhost:5000`
   - Enter team names and predict scores

## Notes

- Models use Random Forest Regression with additional features for improved accuracy
- Features include team encodings, shots on target, corners, fouls, cards, and red cards
- Check team name spelling if you get "Unknown team(s)" errors
