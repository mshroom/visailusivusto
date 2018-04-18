from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db, login_manager, login_required
from application.auth.models import User
from application.questions.models import Question, Option, UsersChoice
from application.auth.forms import LoginForm, RegisterForm

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
	questions = Question.query.filter_by(account_id=user_id).all()
	for q in questions:
		options = Option.query.filter_by(quest_id=q.id).all()
		for o in options:
			db.session.query(UsersChoice).filter_by(option_id=o.id).delete()
		db.session.query(Option).filter_by(quest_id=q.id).delete()
	db.session.query(Question).filter_by(account_id=user_id).delete()	
	u = User.query.get(user_id)
	db.session().delete(u)
	db.session().commit() 
	
	return redirect(url_for("auth_control"))	




