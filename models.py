import re
import uuid
import base64

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

#===============================HELPER=FUNCTIONS===============================

# Generates a random unique primary key
def uuid_url64():
    rv = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
    return re.sub(r'[\=\+\/]', lambda m: {'+': '-', '/': '_', '=': ''}[m.group(0)], rv)

#====================================MODELS====================================

class StudyGuideModel(db.Model):
    __tablename__ = "study_guides_table"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255))
    notes = db.Column(db.Text)
    questions = db.Column(db.Text)

    def __init__(self, name, notes, questions):
        self.id = str(uuid_url64())
        self.name = name
        self.notes = notes
        self.questions = questions

    def add_questions(self, questions):
        self.questions += questions
