from flask import Flask, request, render_template_string
from predict import predict_score

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>EPL Score Predictor</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }
        .container { max-width: 400px; margin: auto; background: white; padding: 20px; border-radius: 8px; }
        input, button { width: 100%; padding: 10px; margin: 10px 0; }
        button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
        .result { margin-top: 20px; font-size: 1.2em; }
    </style>
</head>
<body>
    <div class="container">
        <h2>EPL Score Predictor</h2>
        <form method="post">
            <label for="home_team">Home Team:</label>
            <input type="text" id="home_team" name="home_team" required>
            <label for="away_team">Away Team:</label>
            <input type="text" id="away_team" name="away_team" required>
            <button type="submit">Predict Score</button>
        </form>
        {% if prediction %}
        <div class="result">
            Predicted Score: {{ prediction[0] }} - {{ prediction[1] }}
        </div>
        {% endif %}
        {% if error %}
        <div class="result" style="color: red;">
            {{ error }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    error = None
    if request.method == 'POST':
        home_team = request.form.get('home_team')
        away_team = request.form.get('away_team')
        home_goals, away_goals = predict_score(home_team, away_team)
        if home_goals == "Unknown team(s)":
            error = "One or both team names are unknown. Please check spelling."
        else:
            prediction = (home_goals, away_goals)
    return render_template_string(HTML_TEMPLATE, prediction=prediction, error=error)

if __name__ == '__main__':
    app.run(debug=True)
