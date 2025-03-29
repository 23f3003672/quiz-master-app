from flask_sqlalchemy import SQLAlchemy
from flask import Flask 
from datetime import datetime 
  
db= SQLAlchemy()

#User model
class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(150), unique=True, nullable=False)
    password=db.Column(db.String(255), nullable=False)
    full_name=db.Column(db.String(100),nullable=False)
    role=db.Column(db.String(10),nullable=False)#admin or user 

    scores=db.relationship('Score',backref='user',cascade="all,delete-orphan",passive_deletes=True, lazy='dynamic')

    def __init__(self,email,password,full_name,role=None):
        self.email=email
        self.password=password 
        self.full_name=full_name 
        self.role=role if role=="admin" else "user"


#Subject Model
class Subject(db.Model):
    id= db.Column(db.Integer, primary_key=True) 
    name= db.Column(db.String(50),nullable=False) 
    chapters= db.relationship('Chapter', backref='subject',cascade="all,delete",lazy=True)
    quizzes=db.relationship('Quiz',backref='subject',cascade='all,delete',lazy=True)

#Chapter model
class Chapter(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(200),nullable=False)
    subject_id= db.Column(db.Integer,db.ForeignKey('subject.id'),nullable=False)
    quizzes=db.relationship('Quiz', backref='chapter', cascade="all,delete",lazy=True)

#Quiz Model
class Quiz(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title= db.Column(db.String(200),nullable=False) 
    chapter_id=db.Column(db.Integer,db.ForeignKey('chapter.id'),nullable=False)
    subject_id=db.Column(db.Integer,db.ForeignKey('subject.id'),nullable=False)
    date=db.Column(db.Date,nullable=False)
    duration=db.Column(db.Time,nullable=False)
    
    questions=db.relationship('Question',backref='quiz', cascade="all,delete",lazy=True)
    scores=db.relationship('Score',backref='quiz',cascade="all,delete",lazy=True) 

#Question Model
class Question(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    text=db.Column(db.Text,nullable=False)
    option_a=db.Column(db.String(255),nullable=False)
    option_b=db.Column(db.String(255),nullable=False)
    option_c=db.Column(db.String(255),nullable=False)
    option_d=db.Column(db.String(255),nullable=False)
    correct_option=db.Column(db.String(1), nullable=False) #gives the correct option out of a,b,c,d

    quiz_id=db.Column(db.Integer,db.ForeignKey('quiz.id'),nullable=False)

#score Model
class Score(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    quiz_id=db.Column(db.Integer,db.ForeignKey('quiz.id'),nullable=False)
    score=db.Column(db.Integer,nullable=False)



 


