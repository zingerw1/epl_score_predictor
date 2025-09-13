from flask import Flask, request, render_template_string
from predict import predict_score, load_models
import pickle

app = Flask(__name__)

# Load teams
_, _, le, _, _ = load_models()
teams = sorted(le.classes_)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EPL Score Predictor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            background-attachment: fixed;
            min-height: 100vh;
            transition: background 0.3s ease;
        }
        body.dark {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
            color: #e0e0e0;
        }
        .card {
            border: none;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            background: rgba(255,255,255,0.95);
            transition: all 0.3s ease;
        }
        body.dark .card {
            background: rgba(30,30,30,0.95);
            color: #e0e0e0;
        }
        .btn-predict {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            border: none;
            border-radius: 30px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        .btn-predict:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(255,107,107,0.4);
        }
        .score-display {
            font-size: 4rem;
            font-weight: bold;
            color: #333;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            transition: color 0.3s ease;
        }
        body.dark .score-display {
            color: #fff;
        }
        .team-badge {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(45deg, #667eea, #764ba2);
            display: inline-block;
            text-align: center;
            line-height: 60px;
            font-weight: bold;
            color: white;
            margin: 0 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
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
            border-color: #ff6b6b;
            box-shadow: 0 0 0 0.2rem rgba(255,107,107,0.25);
        }
        .alert {
            border-radius: 10px;
        }
        @media (max-width: 768px) {
            .score-display { font-size: 3rem; }
            .team-badge { width: 50px; height: 50px; line-height: 50px; margin: 0 10px; }
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
                <div class="card p-5">
                    <h1 class="text-center mb-4">
                        <i class="fas fa-futbol text-primary me-3"></i>
                        EPL Score Predictor
                        <i class="fas fa-futbol text-primary ms-3"></i>
                    </h1>
                    <form method="post">
                        <div class="row g-3">
                            <div class="col-md-5">
                                <label for="home_team" class="form-label fw-bold">
                                    <i class="fas fa-home me-2"></i>Home Team
                                </label>
                                <select class="form-select form-select-lg" id="home_team" name="home_team" required>
                                    <option value="">Select Home Team</option>
                                    {% for team in teams %}
                                    <option value="{{ team }}">{{ team }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="col-md-2 text-center align-self-end">
                                <span class="fs-1 fw-bold text-muted">VS</span>
                            </div>
                            <div class="col-md-5">
                                <label for="away_team" class="form-label fw-bold">
                                    <i class="fas fa-plane me-2"></i>Away Team
                                </label>
                                <select class="form-select form-select-lg" id="away_team" name="away_team" required>
                                    <option value="">Select Away Team</option>
                                    {% for team in teams %}
                                    <option value="{{ team }}">{{ team }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                        </div>
                        <div class="text-center mt-4">
                            <button type="submit" class="btn btn-predict btn-lg px-5 py-3">
                                <i class="fas fa-magic me-2"></i>Predict Score
                            </button>
                        </div>
                    </form>
                    {% if prediction %}
                    <div class="text-center mt-5">
                        <h3 class="mb-4">
                            <i class="fas fa-chart-line me-2"></i>Predicted Score
                        </h3>
                        <div class="d-flex justify-content-center align-items-center flex-wrap">
                            <div class="team-badge">{{ home_team[:3].upper() }}</div>
                            <div class="score-display mx-3">{{ prediction[0] }} - {{ prediction[1] }}</div>
                            <div class="team-badge">{{ away_team[:3].upper() }}</div>
                        </div>
                    </div>
                    {% endif %}
                    {% if error %}
                    <div class="alert alert-danger mt-4" role="alert">
                        <i class="fas fa-exclamation-triangle me-2"></i>{{ error }}
                    </div>
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

        // Load saved theme
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
    return render_template_string(HTML_TEMPLATE, prediction=prediction, error=error, teams=teams, home_team=home_team, away_team=away_team)

if __name__ == '__main__':
    app.run(debug=True)
