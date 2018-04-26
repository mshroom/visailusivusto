from flask_wtf import FlaskForm
from wtforms import RadioField, validators
from wtforms.validators import ValidationError

class QuizGameForm(FlaskForm):
	quiz = RadioField("Quiz")

	class Meta:
		csrf = False

