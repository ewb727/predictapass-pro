from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

# Setup OpenAI client
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    if request.method == "POST":
        user_message = request.form["message"]
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are PredictaPass, a drag racing crew chief assistant. Ask for racer name, track, car details, etc. Offer predictions and racing advice conversationally."},
                    {"role": "user", "content": user_message}
                ]
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"Error: {e}"
    return render_template("index.html", reply=reply)

if __name__ == "__main__":
    app.run(debug=True)
