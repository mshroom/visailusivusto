from flask_wtf import FlaskForm
from wtforms import TextField, SelectField, validators
from wtforms.validators import ValidationError

class QuizForm(FlaskForm):
	name = TextField("Quiz name", [validators.Length(min=2)])
	category = SelectField("Category", choices=[('history', 'History'), ('geography', 'Geography'), ('literature', 'Literature'), ('music', 'Music'), ('art', 'Art'), ('movies', 'Movies'), ('sports', 'Sports'), ('nature', 'Nature'), ('science', 'Science'), ('other', 'Other')])
	
	class Meta:
		csrf = False

class ModifyQuizForm(FlaskForm):
	name = TextField("Quiz name", [validators.Length(min=2)])

	class Meta:
		csrf = False

class ModifyQuizCategoryForm(FlaskForm):
	category = SelectField("Category", choices=[('history', 'History'), ('geography', 'Geography'), ('literature', 'Literature'), ('music', 'Music'), ('art', 'Art'), ('movies', 'Movies'), ('sports', 'Sports'), ('nature', 'Nature'), ('science', 'Science'), ('other', 'Other')])
	
	class Meta:
		csrf = False


class QuizQuestionForm(FlaskForm):
	question = SelectField("Question")

	class Meta:
		csrf = False

