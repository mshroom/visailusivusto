from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, SelectField, validators
from wtforms.validators import ValidationError

class QuestionForm(FlaskForm):
	name = TextField("Question", [validators.Length(min=2)])
	active = BooleanField("Active")
	category = SelectField("Category", choices=[('history', 'History'), ('geography', 'Geography'), ('literature', 'Literature'), ('music', 'Music'), ('art', 'Art'), ('movies', 'Movies'), ('sports', 'Sports'), ('nature', 'Nature'), ('science', 'Science'), ('other', 'Other')])
	difficulty = SelectField("Difficulty", choices=[('easy', 'Easy'), ('medium', 'Medium'), ('difficult', 'Difficult')])
	
	def validate_name(self, field):
		if len(field.data) > 0:
			if field.data.endswith('?') == False and field.data[0].isupper() == False:
				raise ValidationError('Question must start with a big letter and end with a "?"')
			elif field.data[0].isupper() == False:
				raise ValidationError('Question must start with a big letter')
			elif field.data.endswith('?') == False:
				raise ValidationError('Question must end with a "?"')
	
	class Meta:
		csrf = False
