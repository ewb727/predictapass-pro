import os
from flask import Flask, render_template, request
import openai

app = Flask(__name__)

import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]


@app.route("/", methods=["GET", "POST"])
def chat():
    conversation = []

    if request.method == "POST":
        user_input = request.form["user_input"]

        # Append the user's message to the conversation
        conversation.append({"role": "user", "content": user_input})

        # Include the system prompt (PredictaPass personality)
        messages = [
            {"role": "system", "content": "You are PredictaPass, a friendly and smart drag racing crew chief who helps racers set up their car and dial in ETs. Start by asking their name and car info, then guide them like a conversation."}
        ] + conversation

        try:
            

                response = openai.chat.completions.create(
    model="gpt-4",
    messages=messages,
    temperature=0.7
)

            

            assistant_reply = response.choices[0].message.content.strip()
            conversation.append({"role": "assistant", "content": assistant_reply})

            return render_template("chat.html", conversation=conversation)

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            return render_template("chat.html", conversation=conversation, error=error_msg)

    return render_template("chat.html", conversation=conversation)
