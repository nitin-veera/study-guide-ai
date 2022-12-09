import os

import openai
from flask import Flask, redirect, render_template, request, url_for

from models import db, StudyGuideModel


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#===============================HELPER=FUNCTIONS==============================

# creates the prompt for when the user initally uploads notes
def generate_prompt(notes):
    return """Create practice questions from the following notes: {}.
    
    Questions: """.format(
        notes
    )

# generates questions for the study guide
def generate_questions(notes):
    questions = ""
    notes = notes
    
    while (len(notes) > 500):
        response = openai.Completion.create(
                model="text-davinci-002",
                prompt=generate_prompt(notes[:500]),
                temperature=0.5,
                max_tokens=2048,
            )
        questions += response.choices[0].text
        notes = notes[500:]
        
    return questions


# def generate_add_prompt(notes,)

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
        questions = generate_questions(notes)
        guide = StudyGuideModel(name=name, notes=notes, questions=questions)
        db.session.add(guide)
        db.session.commit()

        return redirect('/')

# @app.route("/add-questions/<string:id>", methods=(["POST"]))
# def add_questions(id):
#     guide = StudyGuideModel.query.filter_by(id=id).first()
#     if request.method == "POST":
#         # response = openai.Completion.create(
#         #     model="text-davinci-002",
#         #     prompt=generate_prompt(),
#         #     temperature=0.5,
#         #     max_tokens=2048,
#         # )

#         return redirect('/')
