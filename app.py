from flask import Flask, request, render_template_string
from predict import predict_score, load_models

app = Flask(__name__)

# Load models and teams
_, _, le, _, _ = load_models()

# Map all 20 EPL teams to crest URLs
crest_urls = {
    "Arsenal": "/static/images/Arsenal_FC.svg",
    "Aston Villa": "/static/images/aston-villa-logo.svg",
    "Bournemouth": "/static/images/afc-bournemouth.svg",
    "Brentford": "/static/images/brentford-fc-logo.svg",
    "Brighton": "/static/images/brighton-hove-albion-logo.svg",
    "Burnley": "/static/images/Burnley_FC.svg",
    "Cardiff": "/static/images/cardiff-city-fc-logo.svg",
    "Chelsea": "/static/images/chelsea-fc.svg",
    "Crystal Palace": "/static/images/crystal-palace-fc.svg",
    "Everton": "/static/images/everton-fc-2000-2013.svg",
    "Fulham": "/static/images/fulham-fc-logo.svg",
    "Hull": "/static/images/hull-city-afc-2014-2019.svg",
    "Ipswich": "/static/images/Ipswich_Town_FC.svg",
    "Leeds": "/static/images/leeds-united-fc.svg",
    "Leicester": "/static/images/leicester-city-fc.svg",
    "Liverpool": "/static/images/Liverpool_FC.svg",
    "Luton": "/static/images/luton-town-fc.zip",
    "Man City": "/static/images/manchester-city-fc.svg",
    "Man United": "/static/images/manchester-united-f.c.-.svg",
    "Middlesbrough": "/static/images/middlesbrough-fc-logo.svg",
    "Newcastle": "/static/images/newcastle-united-fc.svg",
    "Norwich": "/static/images/norwich-logo-vector.png",
    "Nott'm Forest": "/static/images/Nottingham_Forest.svg",
    "QPR": "/static/images/Queens_Park_Rangers_FC.svg",
    "Sheffield United": "/static/images/sheffield-united-logo.svg",
    "Southampton": "/static/images/southampton-fc.svg",
    "Stoke": "/static/images/stoke-city-fc-logo.svg",
    "Sunderland": "/static/images/sunderland-afc-logo.svg",
    "Swansea": "/static/images/Swansea_City.svg",
    "Tottenham": "/static/images/tottenham-hotspur-fc-logo.png",
    "Watford": "/static/images/watford-fc-logo.svg",
    "West Brom": "/static/images/west-bromwich.svg",
    "West Ham": "/static/images/west-ham-united-fc.svg",
    "Wolves": "/static/images/Wolverhampton_Wanderers_FC.svg"
}

# Use all teams that have crest images, not just those in the current data
teams = sorted(crest_urls.keys())


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
                linear-gradient(rgba(200,200,200,0.6), rgba(200,200,200,0.6)),
                url('/static/images/epl_background.jpg') no-repeat center center fixed;
            background-size: cover;
            min-height: 100vh;
            color: #333;
            transition: all 0.3s ease;
        }
        body.dark {
            background:
                linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)),
                url('/static/images/epl_background.jpg') no-repeat center center fixed;
            background-size: cover;
            color: #e0e0e0;
        }
        .card {
            border: none;
            border-radius: 20px;
            background: rgba(200,200,200,0.12);
            backdrop-filter: blur(15px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
            color: #333;
            transition: all 0.3s ease;
        }
        body.dark .card {
            background: rgba(30,30,30,0.6);
            color: #f5f5f5;
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
        body.dark .btn-predict {
            background: linear-gradient(45deg, #5d88bb, #3b5f8c);
            color: #fff;
        }
        .score-display {
            font-size: 4rem;
            font-weight: 700;
            color: #333;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
            transition: color 0.3s ease;
        }
        body.dark .score-display {
            color: #fff;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.6);
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
            border-color: #333;
            color: #333;
        }
        body.dark .theme-toggle .btn {
            border-color: #fff;
            color: #fff;
        }
        .form-select {
            border-radius: 10px;
            border: 2px solid #ddd;
            transition: all 0.3s ease;
            background-color: #fff;
            color: #333;
        }
        body.dark .form-select {
            border-color: #555;
            background-color: #222;
            color: #eee;
        }
        .form-select:focus {
            border-color: #5d88bb;
            box-shadow: 0 0 0 0.2rem rgba(93,136,187,0.25);
        }
        .alert {
            border-radius: 10px;
        }
        body.dark footer { color: #fff; }
        body.dark footer a { color: #fff; }
        body.dark .text-dark { color: #fff !important; }
        .epl-logo {
            filter: invert(0);
            transition: filter 0.3s ease;
        }
        body.dark .epl-logo {
            filter: invert(1);
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
                    <img src="/static/images/Premier_League_Logo.svg" alt="EPL Logo" style="width:120px; margin-bottom:20px;" class="epl-logo">
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
                                <span class="fs-1 fw-bold text-dark">VS</span>
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

        // Apply saved theme
        if (localStorage.getItem('theme') === 'dark') {
            body.classList.add('dark');
            icon.className = 'fas fa-sun';
        } else {
            body.classList.remove('dark');
            icon.className = 'fas fa-moon';
        }
    </script>
    <footer class="text-center mt-5" style="color: #666; font-size: 0.9rem;">
        Made by Kagiso Setwaba |
        <a href="https://github.com/zingerw1" target="_blank" style="color: #666;"><i class="fab fa-github"></i> GitHub</a> |
        <a href="https://www.linkedin.com/in/kagiso-setwaba-ab465b261/" target="_blank" style="color: #666;"><i class="fab fa-linkedin"></i> LinkedIn</a>
    </footer>
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
