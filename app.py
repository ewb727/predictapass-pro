import os
from flask import Flask, request, render_template_string
from openai import OpenAI
import requests

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = Flask(__name__)

html = """
<!doctype html>
<title>🏁 PredictaPass - Your Crew Chief</title>
<h2>🏁 PredictaPass - Your Crew Chief</h2>
<form method=post>
  <textarea name=message rows=10 cols=50 placeholder="Type your message...">{{ message }}</textarea><br>
  <input type=submit value=Send>
</form>
<p><strong>User:</strong> {{ message }}</p>
<p><strong>PredictaPass:</strong> {{ reply }}</p>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    reply = ""
    if request.method == "POST":
        message = request.form["message"]

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are PredictaPass, a drag racing crew chief assistant. Ask for racer name, track, car details, etc. Offer predictions and racing advice conversationally."},
                    {"role": "user", "content": message}
                ]
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"Error: {e}"

    return render_template_string(html, message=message, reply=reply)

if __name__ == "__main__":
    app.run(debug=True)


   
