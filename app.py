import os

import openai
from flask import Flask, redirect, render_template, request, url_for

from models import db, StudyGuideModel


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#===============================HELPER=FUNCTIONS==============================

# creates the prompt for when the user initally uploads notes
def generate_prompt(notes):
    return """Ask me a single practice question from the following notes: {}.
    
    Question: """.format(
        notes
    )

# generates questions for the study guide
def generate_questions(notes, num_questions):
    questions = ""
    notes = notes
    num_questions = int(num_questions)
    block_size = round(len(notes) / num_questions)
    
    while (len(notes) > 0):
        response = openai.Completion.create(
                model="text-davinci-002",
                prompt=generate_prompt(notes[:block_size]),
                temperature=0.5,
                max_tokens=2048,
            )
        questions += response.choices[0].text
        notes = notes[block_size:]

    return questions

# creates an array of questions
def format_guide(questions):
    
    if questions is None:
        return questions
    # add a newline after every question
    formatted_guide = questions.replace("?", "?\n")
    # create an array of questions
    formatted_guide = formatted_guide.split("\n")
    return formatted_guide


 #===============================ROUTES======================================

@app.before_first_request
def create_table():
    db.create_all()
 
@app.route("/")
def index():
    guides = StudyGuideModel.query.all()
    return render_template("index.html", guides=guides)

@app.route("/create-guide", methods=(["POST"]))
def create_guide():
    if request.method == "POST":
        notes = request.form["notes"]
        name = request.form["guide-name"]
        number_questions = request.form["number-questions"]
        questions = generate_questions(notes, number_questions)
        guide = StudyGuideModel(name=name, notes=notes, questions=questions)
        db.session.add(guide)
        db.session.commit()

        return redirect('/')