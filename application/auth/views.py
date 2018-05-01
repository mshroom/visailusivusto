from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db, login_manager, login_required
from application.auth.models import User
from application.questions.models import Question, Option, UsersChoice
from application.quizzes.models import Quiz, QuizQuestion, Participation
from application.auth.forms import LoginForm, RegisterForm, NameForm, UsernameForm, PasswordForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
	if request.method == "GET":
		return render_template("auth/loginform.html", form = LoginForm())
	
	form = LoginForm(request.form)
	
	user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
	if not user:
		return render_template("auth/loginform.html", form = form, error = "No such username or password")
	
	login_user(user)
	return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
	logout_user()
	return redirect(url_for("index"))

@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
	if request.method == "GET":
		return render_template("auth/registerform.html", form = RegisterForm())
	
	form = RegisterForm(request.form)
	
	if not form.validate():
		return render_template("auth/registerform.html", form = form)

	user = User.query.filter_by(username=form.username.data).first()
	if user:
		return render_template("auth/registerform.html", form = form, error = "Username is already in use")
	
	u = User(form.name.data, form.username.data, form.password.data)
	db.session().add(u)
	db.session().commit()
	return redirect(url_for("auth_login"))

@app.route("/auth/control", methods = ["GET"])
@login_required(role="ADMIN")
def auth_control():
	return render_template("auth/control.html", users = User.query.all())

@app.route("/auth/control/del/<user_id>", methods = ["POST"])
@login_required(role="ADMIN")
def auth_delete(user_id):
	db.session.query(UsersChoice).filter_by(account_id=user_id).delete()
	questions = Question.query.filter_by(account_id=user_id).all()
	for q in questions:
		options = Option.query.filter_by(quest_id=q.id).all()
		for o in options:
			db.session.query(UsersChoice).filter_by(option_id=o.id).delete()
		db.session.query(Option).filter_by(quest_id=q.id).delete()
	quizzes = Quiz.query.filter_by(account_id=user_id).all()
	for qz in quizzes:
		db.session.query(QuizQuestion).filter_by(quiz_id=qz.id).delete()
		db.session.query(Participation).filter_by(quiz_id=qz.id).delete()
	db.session.query(Participation).filter_by(account_id=user_id).delete()
	db.session.query(Quiz).filter_by(account_id=user_id).delete()
	db.session.query(Question).filter_by(account_id=user_id).delete()	
	u = User.query.get(user_id)
	db.session().delete(u)
	db.session().commit() 
	
	return redirect(url_for("auth_control"))

@app.route("/auth/settings/", methods = ["GET"])
@login_required(role="USER")
def auth_settings():
	return render_template("auth/settings.html", user = current_user, nameform = NameForm(), usernameform = UsernameForm(), passwordform = PasswordForm())

@app.route("/auth/settings/name/", methods = ["POST"])
@login_required(role="USER")
def auth_set_name():
	nameform = NameForm(request.form)
	
	if not nameform.validate():
		return render_template("auth/settings.html", user = current_user, nameform = nameform, usernameform = UsernameForm(), passwordform = PasswordForm())

	user = User.query.get(current_user.id)
	user.name = nameform.name.data
	db.session().commit()
	return render_template("auth/settings.html", user = current_user, nameform = NameForm(), usernameform = UsernameForm(), passwordform = PasswordForm(), error = "Name was changed")

@app.route("/auth/settings/username/", methods = ["POST"])
@login_required(role="USER")
def auth_set_username():
	usernameform = UsernameForm(request.form)
	
	if not usernameform.validate():
		return render_template("auth/settings.html", user = current_user, nameform = NameForm(), usernameform = usernameform, passwordform = PasswordForm())

	user = User.query.filter_by(username=usernameform.username.data).first()
	if user:
		return render_template("auth/settings.html",user = current_user, nameform = NameForm(), usernameform = UsernameForm(), passwordform = PasswordForm(), error = "Username is already in use")

	user = User.query.get(current_user.id)
	user.username = usernameform.username.data
	db.session().commit()
	return render_template("auth/settings.html", user = current_user, nameform = NameForm(), usernameform = UsernameForm(), passwordform = PasswordForm(), error = "Userame was changed")

@app.route("/auth/settings/password/", methods = ["POST"])
@login_required(role="USER")
def auth_set_password():
	passwordform = PasswordForm(request.form)
	
	if not passwordform.validate():
		return render_template("auth/settings.html", user = current_user, nameform = NameForm(), usernameform = UsernameForm(), passwordform = passwordform)

	user = User.query.get(current_user.id)
	user.password = passwordform.password.data
	db.session().commit()
	return render_template("auth/settings.html", user = current_user, nameform = NameForm(), usernameform = UsernameForm(), passwordform = PasswordForm(), error = "Password was changed")

@app.route("/auth/settings/delete/", methods = ["POST"])
@login_required(role="USER")
def delete_account():
	return render_template("auth/delete.html")

@app.route("/auth/settings/delete/cancel", methods = ["POST"])
@login_required(role="USER")
def delete_cancel():
	return render_template("auth/settings.html", user = current_user, nameform = NameForm(), usernameform = UsernameForm(), passwordform = PasswordForm())

@app.route("/auth/settings/delete/confirm", methods = ["POST"])
@login_required(role="USER")
def delete_confirm():
	db.session.query(UsersChoice).filter_by(account_id=current_user.id).delete()
	questions = Question.query.filter_by(account_id=current_user.id).all()
	for q in questions:
		options = Option.query.filter_by(quest_id=q.id).all()
		for o in options:
			db.session.query(UsersChoice).filter_by(option_id=o.id).delete()
		db.session.query(Option).filter_by(quest_id=q.id).delete()
	quizzes = Quiz.query.filter_by(account_id=current_user.id).all()
	for qz in quizzes:
		db.session.query(QuizQuestion).filter_by(quiz_id=qz.id).delete()
		db.session.query(Participation).filter_by(quiz_id=qz.id).delete()
	db.session.query(Participation).filter_by(account_id=current_user.id).delete()
	db.session.query(Quiz).filter_by(account_id=current_user.id).delete()
	db.session.query(Question).filter_by(account_id=current_user.id).delete()
	u = User.query.get(current_user.id)
	logout_user()
	db.session().delete(u)
	db.session().commit()	
	return redirect(url_for("auth_control"))




