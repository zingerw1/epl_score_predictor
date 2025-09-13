# ⚽ EPL Score Predictor

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A sophisticated machine learning project to predict scores for English Premier League matches using Random Forest Regression. Built with Flask for an intuitive web interface. ⚽📊💻

![EPL Predictor Demo](screenshots/demo.png)

## 📋 Table of Contents

- [✨ Features](#✨-features)  
- [🔧 How it Works](#🔧-how-it-works)  
- [📋 Prerequisites](#📋-prerequisites)  
- [🚀 Installation](#🚀-installation)  
- [🎯 Usage](#🎯-usage)  
- [📁 Project Structure](#📁-project-structure)  
- [📸 Screenshots](#📸-screenshots)  
- [🤝 Contributing](#🤝-contributing)  
- [📄 License](#📄-license)  

---

## ✨ Features

- ⚡ **Accurate Predictions**: Uses Random Forest Regression trained on historical EPL data for reliable score predictions.  
- 📊 **Comprehensive Data**: Includes advanced features like shots on target, corners, fouls, yellow & red cards for better accuracy.  
- 🖥️ **User-Friendly Interface**: Clean, responsive web app built with Flask, Bootstrap, and Font Awesome.  
- 🌗 **Dark/Light Theme**: Toggle between light and dark modes for a better user experience.  
- 🏟️ **Team Crests**: Displays official team logos for visual appeal.  
- ⚠️ **Error Handling**: Provides clear messages for unknown teams or errors.  

---

## 🔧 How it Works

1. **📥 Data Collection**: Downloads historical EPL match data from football-data.co.uk for seasons 2014-15 to 2022-23.  

2. **🧹 Preprocessing**: Cleans the data, selects relevant columns (`HomeTeam`, `AwayTeam`, `FTHG`, `FTAG`), and encodes team names using LabelEncoder.  

3. **🤖 Model Training**: Trains two Random Forest Regression models:
   - One for predicting **home team goals** (FTHG)  
   - One for predicting **away team goals** (FTAG)  
   - Features: Encoded home & away teams, shots on target, corners, fouls, yellow/red cards.  

4. **🎯 Prediction**: For given home and away teams, encodes them and uses the models to predict goals.  

5. **🖥️ Web Interface**: A Flask app where users can input teams and see the predicted score with team crests.  

---

## 📋 Prerequisites

- 🐍 Python 3.7+  
- 🌐 Internet connection for data download  

---

## 🚀 Installation

1. **Clone the Repository**:

```bash
git clone https://github.com/yourusername/epl-score-predictor.git
cd epl-score-predictor
```

2. **Create Virtual Environment** (recommended):

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

3. **Install Dependencies**:

```bash
pip install -r requirements.txt
```

4. **Download Data**:

```bash
python data.py
```

5. **Train Models**:

```bash
python model.py
```

---

## 🎯 Usage

1. **Run the Application**:

```bash
python app.py
```

2. **Access the App**:
- Open your browser at `http://localhost:5000`  
- Select **home** and **away** teams from the dropdowns  
- Click **Predict Score** ⚡ to see the result with team crests 🏟️  

---

## 📁 Project Structure

```
epl-score-predictor/
├── app.py                 # Flask web application 🖥️
├── data.py                # Data download & preprocessing 📥
├── model.py               # Model training script 🤖
├── predict.py             # Prediction functions 🎯
├── requirements.txt       # Python dependencies 📦
├── epl_data.csv           # Processed dataset 🗃️
├── label_encoder.pkl      # Encoded team labels 🔢
├── home_model.pkl         # Trained home goals model 🏠
├── away_model.pkl         # Trained away goals model 🛫
├── static/
│   └── images/            # Team crest images 🏟️
└── README.md              # Project documentation 📄
```

---

## 📸 Screenshots

### Main Interface

![Main Interface](screenshots/main_interface.png)  

### Prediction Result

![Prediction Result](screenshots/prediction_result.png)  

### Dark Theme

![Dark Theme](screenshots/dark_theme.png)  

_Add your screenshots in the `screenshots/` folder._  

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository 🍴  
2. Create a feature branch: `git checkout -b feature/AmazingFeature` 🌟  
3. Commit your changes: `git commit -m 'Add some AmazingFeature'` 📝  
4. Push to the branch: `git push origin feature/AmazingFeature` 🚀  
5. Open a Pull Request 🔄  

---

## 📄 License

This project is licensed under the **MIT License** 🟢 — see the [LICENSE](LICENSE) file for details.  

---

## 📝 Notes

- Models use Random Forest Regression with additional features for improved accuracy.  
- Features include team encodings, shots on target, corners, fouls, cards, and red cards.  
- ⚠️ Check team name spelling if you get "Unknown team(s)" errors.  
- For issues, please open an issue on GitHub 🐙.