from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators
from wtforms.validators import ValidationError

class ReportForm(FlaskForm):
	comment = TextAreaField("Comment", [validators.Length(min=2)])
	
	class Meta:
		csrf = False
