from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StudyGuide(db.Model):
    __tablename__ = "study_guides"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    notes = db.Column(db.Text)
    questions = db.Column(db.ARRAY(db.String(255)))

    def __init__(self, name, notes, questions):
        self.name = name
        self.notes = notes
        self.questions = questions