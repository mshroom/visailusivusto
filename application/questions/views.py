from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.questions.models import Question
from application.questions.forms import QuestionForm

@app.route("/questions", methods=["GET"])
def questions_index():
	return render_template("questions/list.html", questions = Question.query.all())

@app.route("/questions/new/")
@login_required
def questions_form():
	return render_template("questions/new.html", form = QuestionForm())

@app.route("/questions/<question_id>/", methods=["POST"])
@login_required
def questions_delete(question_id):
	q = Question.query.get(question_id)
	db.session().delete(q)
	db.session().commit()
	
	return redirect(url_for("questions_index"))

@app.route("/questions/act/<question_id>/", methods=["POST"])
@login_required
def questions_activate(question_id):
	q = Question.query.get(question_id)
	if q.active == True:
		q.active = False
	else:
		q.active = True
	db.session().commit()
	
	return redirect(url_for("questions_index"))

@app.route("/questions/", methods=["POST"])
@login_required
def questions_create():
		
	form = QuestionForm(request.form)
	
	if not form.validate():
		return render_template("questions/new.html", form = form)
	
	q = Question(form.name.data, form.category.data, form.difficulty.data, form.active.data)
	q.account_id = current_user.id
	
	db.session().add(q)
	db.session().commit()
	
	return redirect(url_for("questions_index"))
