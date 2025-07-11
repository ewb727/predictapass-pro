from flask import Flask, request, render_template
import os
import openai

app = Flask(__name__)

# Set your OpenAI API key via environment variable
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    reply = ""

    if request.method == "POST":
        message = request.form["message"]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are PredictaPass, a drag racing crew chief assistant. Ask for racer name, track, car details, etc. Offer predictions and racing advice conversationally."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"Error: {e}"

    return render_template("index.html", message=message, reply=reply)

if __name__ == "__main__":
    app.run(debug=True)

   
