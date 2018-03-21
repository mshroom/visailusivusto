from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] =  "sqlite:///quizdata.db"
app.config["SQLALCHEMY_ECHO"]=True

db = SQLAlchemy(app)

from application import views

from application.questions import models
from application.questions import views

db.create_all()
