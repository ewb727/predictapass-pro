import os
from flask import Flask, render_template_string, request
from openai import OpenAI
import requests

# Initialize GPT client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>PredictaPass Pro</title>
</head>
<body>
    <h1>PredictaPass Pro</h1>
    <form method="POST" action="/predict">
        <label>Racer Name:</label><br>
        <input type="text" name="racer_name"><br><br>

        <label>Track Name:</label><br>
        <input type="text" name="track_name"><br><br>

        <label>City:</label><br>
        <input type="text" name="city"><br><br>

        <label>State:</label><br>
        <input type="text" name="state"><br><br>

        <label>Fuel Type:</label><br>
        <input type="text" name="fuel_type"><br><br>

        <label>Trans Type:</label><br>
        <input type="text" name="trans_type"><br><br>

        <label>Stall RPM:</label><br>
        <input type="text" name="stall_rpm"><br><br>

        <label>Tire Size:</label><br>
        <input type="text" name="tire_size"><br><br>

        <input type="submit" value="Predict">
    </form>
    {% if prediction %}
        <h2>Prediction:</h2>
        <p>{{ prediction }}</p>
    {% endif %}
</body>
</html>
'''

# Helper to fetch weather
def get_weather(city, state):
    try:
        # Use Open-Meteo for free weather data
        url = f"https://api.open-meteo.com/v1/forecast?latitude=39.8&longitude=-86.1&current_weather=true"
        res = requests.get(url).json()
        weather = res.get("current_weather", {})
        return f"Temp: {weather.get('temperature')}C, Wind: {weather.get('windspeed')}kph"
    except:
        return "Weather data not available."

# Routes
@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/predict", methods=["POST"])
def predict():
    racer_name = request.form.get("racer_name")
    track_name = request.form.get("track_name")
    city = request.form.get("city")
    state = request.form.get("state")
    fuel_type = request.form.get("fuel_type")
    trans_type = request.form.get("trans_type")
    stall_rpm = request.form.get("stall_rpm")
    tire_size = request.form.get("tire_size")

    weather_info = get_weather(city, state)

    prompt = f"""
You are PredictaPass, the world’s smartest ET prediction AI. You’re helping racer {racer_name}.
Track: {track_name}, Location: {city}, {state}
Weather: {weather_info}
Setup:
- Fuel: {fuel_type}
- Transmission: {trans_type}
- Stall RPM: {stall_rpm}
- Tire Size: {tire_size}

Give your best ET prediction and one quick tuning suggestion.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a drag racing tuning assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"Error generating prediction: {e}"

    return render_template_string(HTML_TEMPLATE, prediction=answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
