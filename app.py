from flask import Flask, request, render_template, jsonify
import openai
import os

app = Flask(__name__)

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

PROMPT_TEMPLATE = """
You are PredictaPass, a bracket racing AI crew chief assistant.
Begin by greeting the racer by name. Based on the setup and weather data, provide a smart ET prediction and one paragraph of tuning advice.

Setup:
- Racer: {racer}
- Car: {car}
- Track: {track}
- Engine: {engine}
- Transmission: {trans}
- Converter stall: {stall}
- Tire size: {tires}
- Launch RPM: {launch}
- Shift RPM: {shift}
- Fuel: {fuel}

Weather:
- Temp: {temp} °F
- Humidity: {humidity} %
- Barometric Pressure: {baro} inHg
- Elevation: {elevation} ft

Act like a friendly, helpful bracket racing crew chief who knows the racer well. Speak directly to the racer by name. Provide one clean, confident ET prediction followed by a short tuning tip or suggestion.
"""

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prompt = PROMPT_TEMPLATE.format(**data)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        reply = response.choices[0].message.content
        return jsonify({'response': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
