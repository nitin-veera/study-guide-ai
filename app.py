import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        notes = request.form["notes"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(notes),
            temperature=0.5,
            max_tokens=2048,
        )
        return redirect(url_for("index", questions=response.choices[0].text))

    questions = request.args.get("questions")
    return render_template("index.html", questions=format_guide(questions))


def generate_prompt(notes):
    return """Create practice questions from the following notes: {}.
    
    Questions: """.format(
        notes
    )


def format_guide(questions):
    
    if questions is None:
        return questions
    # add a newline after every question
    formatted_guide = questions.replace("?", "?\n")
    # create an array of questions
    formatted_guide = formatted_guide.split("\n")

    return formatted_guide
