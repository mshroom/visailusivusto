from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.questions.models import Question, Option
from application.questions.forms import QuestionForm, OptionForm

@app.route("/questions", methods=["GET"])
@login_required
def questions_index():
	return render_template("questions/list.html", questions = Question.query.filter_by(account_id=current_user.id).all())

@app.route("/questions/new/")
@login_required
def questions_form():
	return render_template("questions/new.html", form = QuestionForm())

@app.route("/questions/del/<question_id>/", methods=["POST"])
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
		answer = Option.query.filter_by(quest_id=question_id, correct=1).first()
		if not answer:
			return render_template("questions/list.html", questions = Question.query.filter_by(account_id=current_user.id).all(), error = "Question has no correct answer and cannot be activated")
		q.active = True
	db.session().commit()
	
	return redirect(url_for("questions_index"))

@app.route("/questions/mod/<question_id>/", methods=["GET", "POST"])
@login_required
def questions_modify(question_id):
	if request.method == "GET":
		return render_template("questions/modify.html", question  = Question.query.get(question_id), options = Option.query.filter_by(quest_id=question_id).all(), form = QuestionForm(), opt_form = OptionForm())

	form = QuestionForm(request.form)
	
	if not form.validate():
		return render_template("questions/modify.html", question = Question.query.get(question_id), options = Option.query.filter_by(quest_id=question_id).all(), form = form, opt_form = OptionForm())
	
	q = Question.query.get(question_id)
	q.name = form.name.data
	q.category = form.category.data
	q.difficulty = form.difficulty.data
	
	db.session().commit()
	
	return redirect(url_for("questions_index"))

@app.route("/questions/mod/<question_id>/act/", methods=["POST"])
@login_required
def question_activate(question_id):
	q = Question.query.get(question_id)
	if q.active == True:
		q.active = False
	else:
		answer = Option.query.filter_by(quest_id=question_id, correct=1).first()
		if not answer:
			return render_template("questions/modify.html", question = Question.query.get(question_id), options = Option.query.filter_by(quest_id=question_id).all(), form = QuestionForm(), opt_form = OptionForm(), act_error = "Question has no correct answer and cannot be activated")
		q.active = True
	db.session().commit()
	
	return redirect(url_for('questions_modify', question_id=question_id))

@app.route("/questions/mod/<question_id>/cor/<option_id>/", methods=["POST"])
@login_required
def options_setcorrect(question_id, option_id):
	o = Option.query.get(option_id)
	if o.correct == True:
		o.correct = False
	else:
		o.correct = True
	db.session().commit()
	answer = Option.query.filter_by(quest_id=question_id, correct=True).first()
	if not answer:
		q = Question.query.get(question_id)
		q.active = False
		db.session().commit()
		return render_template("questions/modify.html", question = Question.query.get(question_id), options = Option.query.filter_by(quest_id=question_id).all(), form = QuestionForm(), opt_form = OptionForm(), act_error = "Question was deactivated because it has no correct answer")
	
	return redirect(url_for('questions_modify', question_id=question_id))

@app.route("/questions/mod/<question_id>/del/<option_id>/", methods=["POST"])
@login_required
def options_delete(question_id, option_id):
	o = Option.query.get(option_id)
	db.session().delete(o)
	db.session().commit()
	
	return redirect(url_for('questions_modify', question_id=question_id))

@app.route("/questions/mod/<question_id>/add/", methods=["POST"])
@login_required
def options_add(question_id):
	
	opt_form = OptionForm(request.form)
	
	if not opt_form.validate():
		return render_template("questions/modify.html", question = Question.query.get(question_id), options = Option.query.filter_by(quest_id=question_id).all(), form = QuestionForm(), opt_form = opt_form)
			
	o = Option(opt_form.name.data, opt_form.correct.data)
	o.quest_id = question_id
	
	db.session().add(o)
	db.session().commit()
	
	return redirect(url_for('questions_modify', question_id=question_id))
	

@app.route("/questions/", methods=["POST"])
@login_required
def questions_create():
		
	form = QuestionForm(request.form)
	
	if not form.validate():
		return render_template("questions/new.html", form = form)
	
	q = Question(form.name.data, form.category.data, form.difficulty.data)
	q.account_id = current_user.id
	
	db.session().add(q)
	db.session().commit()
	
	return redirect(url_for("questions_index"))
