from flask_wtf import FlaskForm
from wtforms import PasswordField, TextField, validators


class LoginForm(FlaskForm):
	username = TextField("Username")
	password = PasswordField("Password")
	
	class Meta:
		csrf = False

class RegisterForm(FlaskForm):

	name = TextField("Name", [validators.Length(min=2, max=50, message="Name must contain 2 - 50 characters")])
	username = TextField("Username", [validators.Length(min=2, max=50, message="Username must contain 2 - 50 characters")])
	password = PasswordField("Password", [validators.Length(min=4, max=50, message="Password must contain 4 - 50 characters")])
	password2 = PasswordField("Password again", [validators.Length(min=4, max=50, message="Password must contain 4 - 50 characters")])
	
	class Meta:
		csrf = False

class NameForm(FlaskForm):

	name = TextField("New name", [validators.Length(min=2, max=50, message="Name must contain 2 - 50 characters")])
	
	class Meta:
		csrf = False

class UsernameForm(FlaskForm):
	username = TextField("New username", [validators.Length(min=2, max=50, message="Username must contain 2 - 50 characters")])

	class Meta:
		csrf = False

class PasswordForm(FlaskForm):

	password = PasswordField("New password", [validators.Length(min=4, max=50, message="Password must contain 4 - 50 characters")])
	password2 = PasswordField("Password again", [validators.Length(min=4, max=50, message="Password must contain 4 - 50 characters")])
	
	class Meta:
		csrf = False
