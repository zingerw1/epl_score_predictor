from flask import Flask, request, render_template_string
from predict import predict_score, load_models

app = Flask(__name__)

# Load models and teams
_, _, le, _, _ = load_models()
teams = sorted(le.classes_)

# Map all 20 EPL teams to crest URLs
crest_urls = {
    "Arsenal": "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg",
    "Aston Villa": "https://upload.wikimedia.org/wikipedia/en/9/9f/Aston_Villa_FC_crest_%282016%29.png",
    "Bournemouth": "https://upload.wikimedia.org/wikipedia/en/6/61/AFC_Bournemouth.png",
    "Brentford": "https://upload.wikimedia.org/wikipedia/en/0/0c/Brentford_FC_crest.png",
    "Brighton": "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg",
    "Chelsea": "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg",
    "Crystal Palace": "https://upload.wikimedia.org/wikipedia/en/0/0c/Crystal_Palace_FC_logo.svg",
    "Everton": "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg",
    "Fulham": "https://upload.wikimedia.org/wikipedia/en/e/e6/Fulham_FC_%28logo%29.svg",
    "Leeds United": "https://upload.wikimedia.org/wikipedia/en/0/0c/Leeds_United_Logo.png",
    "Leicester City": "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg",
    "Liverpool": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg",
    "Manchester City": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
    "Manchester United": "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg",
    "Newcastle United": "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg",
    "Nottingham Forest": "https://upload.wikimedia.org/wikipedia/en/7/7b/Nottingham_Forest_logo.svg",
    "Southampton": "https://upload.wikimedia.org/wikipedia/en/c/c9/Southampton_FC.svg",
    "Tottenham": "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg",
    "West Ham": "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg",
    "Wolves": "https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EPL Score Predictor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Montserrat', sans-serif;
            background:
                linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                url('https://images.unsplash.com/photo-1600932710359-8df3e25a2c8f?auto=format&fit=crop&w=1600&q=80') no-repeat center center fixed;
            background-size: cover;
            min-height: 100vh;
            color: #f5f5f5;
            transition: background 0.3s ease;
        }
        body.dark {
            background:
                linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)),
                url('https://images.unsplash.com/photo-1600932710359-8df3e25a2c8f?auto=format&fit=crop&w=1600&q=80') no-repeat center center fixed;
            background-size: cover;
            color: #e0e0e0;
        }
        .card {
            border: none;
            border-radius: 20px;
            background: rgba(255,255,255,0.12);
            backdrop-filter: blur(15px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
            color: #fff;
            transition: all 0.3s ease;
        }
        body.dark .card {
            background: rgba(30,30,30,0.6);
        }
        .btn-predict {
            background: linear-gradient(45deg, #a2c2e3, #5d88bb);
            border: none;
            border-radius: 30px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #fff;
            transition: all 0.3s ease;
        }
        .btn-predict:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }
        .score-display {
            font-size: 4rem;
            font-weight: 700;
            color: #fff;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.6);
            transition: color 0.3s ease;
        }
        .team-logo {
            width: 70px;
            height: 70px;
            object-fit: contain;
            margin: 0 15px;
            filter: drop-shadow(0 2px 5px rgba(0,0,0,0.4));
        }
        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }
        .theme-toggle .btn {
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
        }
        .form-select {
            border-radius: 10px;
            border: 2px solid #ddd;
            transition: border-color 0.3s ease;
        }
        .form-select:focus {
            border-color: #5d88bb;
            box-shadow: 0 0 0 0.2rem rgba(93,136,187,0.25);
        }
        .alert {
            border-radius: 10px;
        }
        @media (max-width: 768px) {
            .score-display { font-size: 3rem; }
            .team-logo { width: 50px; height: 50px; margin: 0 10px; }
        }
    </style>
</head>
<body>
    <div class="theme-toggle">
        <button id="theme-toggle" class="btn btn-outline-light">
            <i class="fas fa-moon"></i>
        </button>
    </div>
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-md-10 col-lg-8">
                <div class="card p-5 text-center">
                    <img src="https://freebiesupply.com/logos/premier-league-logo/" alt="EPL Logo" style="width:120px; margin-bottom:20px;">
                    <h1 class="mb-4 fw-bold">EPL Score Predictor</h1>
                    <form method="post">
                        <div class="row g-3">
                            <div class="col-md-5">
                                <label for="home_team" class="form-label fw-bold"><i class="fas fa-home me-2"></i>Home Team</label>
                                <select class="form-select form-select-lg" id="home_team" name="home_team" required>
                                    <option value="">Select Home Team</option>
                                    {% for team in teams %}
                                    <option value="{{ team }}">{{ team }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="col-md-2 text-center align-self-end">
                                <span class="fs-1 fw-bold text-light">VS</span>
                            </div>
                            <div class="col-md-5">
                                <label for="away_team" class="form-label fw-bold"><i class="fas fa-plane me-2"></i>Away Team</label>
                                <select class="form-select form-select-lg" id="away_team" name="away_team" required>
                                    <option value="">Select Away Team</option>
                                    {% for team in teams %}
                                    <option value="{{ team }}">{{ team }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                        </div>
                        <div class="text-center mt-4">
                            <button type="submit" class="btn btn-predict btn-lg px-5 py-3"><i class="fas fa-magic me-2"></i>Predict Score</button>
                        </div>
                    </form>
                    {% if prediction %}
                    <div class="text-center mt-5">
                        <h3 class="mb-4 fw-bold"><i class="fas fa-chart-line me-2"></i>Predicted Score</h3>
                        <div class="d-flex justify-content-center align-items-center flex-wrap">
                            <img src="{{ crest_urls[home_team] }}" alt="{{ home_team }}" class="team-logo">
                            <div class="score-display mx-3">{{ prediction[0] }} - {{ prediction[1] }}</div>
                            <img src="{{ crest_urls[away_team] }}" alt="{{ away_team }}" class="team-logo">
                        </div>
                    </div>
                    {% endif %}
                    {% if error %}
                    <div class="alert alert-danger mt-4" role="alert"><i class="fas fa-exclamation-triangle me-2"></i>{{ error }}</div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const themeToggle = document.getElementById('theme-toggle');
        const body = document.body;
        const icon = themeToggle.querySelector('i');

        themeToggle.addEventListener('click', () => {
            body.classList.toggle('dark');
            if (body.classList.contains('dark')) {
                icon.className = 'fas fa-sun';
                localStorage.setItem('theme', 'dark');
            } else {
                icon.className = 'fas fa-moon';
                localStorage.setItem('theme', 'light');
            }
        });

        if (localStorage.getItem('theme') === 'dark') {
            body.classList.add('dark');
            icon.className = 'fas fa-sun';
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    error = None
    home_team = None
    away_team = None
    if request.method == 'POST':
        home_team = request.form.get('home_team')
        away_team = request.form.get('away_team')
        home_goals, away_goals = predict_score(home_team, away_team)
        if home_goals == "Unknown team(s)":
            error = "One or both team names are unknown. Please check spelling."
        else:
            prediction = (home_goals, away_goals)
    return render_template_string(HTML_TEMPLATE, prediction=prediction, error=error, teams=teams, home_team=home_team, away_team=away_team, crest_urls=crest_urls)

if __name__ == '__main__':
    app.run(debug=True)
