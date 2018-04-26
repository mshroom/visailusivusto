import random

from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_manager, login_required
from application.questions.models import Question, Option
from application.questions.forms import QuestionForm, OptionForm, ModifyQuestionForm, ModifyCategoryForm, ModifyDifficultyForm

@app.route("/questions", methods=["GET"])
@login_required(role="USER")
def questions_index():
	return render_template("questions/list.html", questions = Question.query.filter_by(account_id=current_user.id).all(), control = "user")

@app.route("/questions/control", methods=["GET"])
@login_required(role="ADMIN")
def questions_control():
	return render_template("questions/list.html", questions = Question.query.all(), control = "control")

@app.route("/questions/new/")
@login_required(role="USER")
def questions_form():
	return render_template("questions/new.html", form = QuestionForm())

@app.route("/questions/del/<control>/<question_id>/", methods=["POST"])
@login_required(role="USER")
def questions_delete(question_id, control):
	q = Question.query.get(question_id)
	db.session.query(QuizQuestion).filter_by(question_id=q.id).delete()
 
	options = Option.query.filter_by(quest_id=question_id).all()
	for o in options:
		db.session.query(UsersChoice).filter_by(option_id=o.id).delete()
	db.session.query(Option).filter_by(quest_id=question_id).delete()	
	db.session().delete(q)
	db.session().commit() 
	
	if current_user.role == "ADMIN" and control == "control":
		return redirect(url_for('questions_control'))
	return redirect(url_for('questions_index'))


@app.route("/questions/act/<control>/<question_id>/", methods=["POST"])
@login_required(role="USER")
def questions_activate(question_id, control):
	q = Question.query.get(question_id)
	if q.active == True:
		q.active = False
	else:
		answer = Option.query.filter_by(quest_id=question_id, correct=True).first()
		if not answer:
			if current_user.role == "ADMIN" and control == "control":
				return render_template("questions/list.html", questions = Question.query.all(), control = control, error = "Question has no correct answer and cannot be activated")
			return render_template("questions/list.html", questions = Question.query.filter_by(account_id=current_user.id).all(), control = control, error = "Question has no correct answer and cannot be activated")
		q.active = True
	db.session().commit()
	
	if current_user.role == "ADMIN" and control == "control":
		return redirect(url_for('questions_control'))
	return redirect(url_for('questions_index'))

@app.route("/questions/mod/<question_id>/", methods=["GET", "POST"])
@login_required(role="USER")
def questions_modify(question_id):
	q = Question.query.get(question_id)
	if q.account_id != current_user.id and current_user.role != "ADMIN":
		return login_manager.unauthorized()

	if request.method == "GET":
		return render_template("questions/modify.html", question  = Question.query.get(question_id), options = Option.query.filter_by(quest_id=question_id).all(), opt_form = OptionForm(), q_form = ModifyQuestionForm(), c_form = ModifyCategoryForm(), d_form = ModifyDifficultyForm())

	form = QuestionForm(request.form)
	
	if not form.validate():
		return render_template("questions/modify.html", question  = Question.query.get(question_id), options = Option.query.filter_by(quest_id=question_id).all(), opt_form = OptionForm(), q_form = ModifyQuestionForm(), c_form = ModifyCategoryForm(), d_form = ModifyDifficultyForm())
	
	q = Question.query.get(question_id)
	q.name = form.name.data
	q.category = form.category.data
	q.difficulty = form.difficulty.data
	
	db.session().commit()
	
	return redirect(url_for('questions_modify', question_id=question_id))

@app.route("/questions/mod/question/<question_id>/", methods=["POST"])
@login_required(role="USER")
def questions_modifyQuestion(question_id):
	q_form = ModifyQuestionForm(request.form)
	if not q_form.validate():
		return render_template("questions/modify.html", question  = Question.query.get(question_id), options = Option.query.filter_by(quest_id=question_id).all(), opt_form = OptionForm(), q_form = ModifyQuestionForm(), c_form = ModifyCategoryForm(), d_form = ModifyDifficultyForm())

	q = Question.query.get(question_id)
	q.name = q_form.name.data

	db.session().commit()

	return redirect(url_for('questions_modify', question_id=question_id))

@app.route("/questions/mod/category/<question_id>/", methods=["POST"])
@login_required(role="USER")
def questions_modifyCategory(question_id):
	c_form = ModifyCategoryForm(request.form)

	q = Question.query.get(question_id)
	q.category = c_form.category.data

	db.session().commit()

	return redirect(url_for('questions_modify', question_id=question_id))

@app.route("/questions/mod/difficulty/<question_id>/", methods=["POST"])
@login_required(role="USER")
def questions_modifyDifficulty(question_id):
	d_form = ModifyDifficultyForm(request.form)

	q = Question.query.get(question_id)
	q.difficulty = d_form.difficulty.data

	db.session().commit()

	return redirect(url_for('questions_modify', question_id=question_id))

@app.route("/questions/mod/<question_id>/act/", methods=["POST"])
@login_required(role="USER")
def question_activate(question_id):
	q = Question.query.get(question_id)
	if q.active == True:
		q.active = False
	else:
		answer = Option.query.filter_by(quest_id=question_id, correct=True).first()
		if not answer:
			return render_template("questions/modify.html", question  = Question.query.get(question_id), options = Option.query.filter_by(quest_id=question_id).all(), opt_form = OptionForm(), q_form = ModifyQuestionForm(), c_form = ModifyCategoryForm(), d_form = ModifyDifficultyForm(), act_error = "Question has no correct answer and cannot be activated")
		q.active = True
	db.session().commit()
	
	return redirect(url_for('questions_modify', question_id=question_id))

@app.route("/questions/mod/<question_id>/cor/<option_id>/", methods=["POST"])
@login_required(role="USER")
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
		return render_template("questions/modify.html", question  = Question.query.get(question_id), options = Option.query.filter_by(quest_id=question_id).all(), opt_form = OptionForm(), q_form = ModifyQuestionForm(), c_form = ModifyCategoryForm(), d_form = ModifyDifficultyForm(), act_error = "Question was deactivated because it has no correct answer")
	
	return redirect(url_for('questions_modify', question_id=question_id))

@app.route("/questions/mod/<question_id>/del/<option_id>/", methods=["POST"])
@login_required(role="USER")
def options_delete(question_id, option_id):
	o = Option.query.get(option_id)
	db.session.query(UsersChoice).filter_by(option_id=o.id).delete()
	db.session().delete(o)
	db.session().commit()
	answer = Option.query.filter_by(quest_id=question_id, correct=True).first()
	if not answer:
		q = Question.query.get(question_id)
		q.active = False
		db.session().commit()
		return render_template("questions/modify.html", question  = Question.query.get(question_id), options = Option.query.filter_by(quest_id=question_id).all(), opt_form = OptionForm(), q_form = ModifyQuestionForm(), c_form = ModifyCategoryForm(), d_form = ModifyDifficultyForm(), act_error = "Question was deactivated because it has no correct answer")
	
	return redirect(url_for('questions_modify', question_id=question_id))

@app.route("/questions/mod/<question_id>/add/", methods=["POST"])
@login_required(role="USER")
def options_add(question_id):
	opt_form = OptionForm(request.form)
	
	if not opt_form.validate():
		return render_template("questions/modify.html", question  = Question.query.get(question_id), options = Option.query.filter_by(quest_id=question_id).all(), opt_form = OptionForm(), q_form = ModifyQuestionForm(), c_form = ModifyCategoryForm(), d_form = ModifyDifficultyForm())
			
	o = Option(opt_form.name.data, opt_form.correct.data)
	o.quest_id = question_id
	
	db.session().add(o)
	db.session().commit()
	
	return redirect(url_for('questions_modify', question_id=question_id))
	

@app.route("/questions/", methods=["POST"])
@login_required(role="USER")
def questions_create():
		
	form = QuestionForm(request.form)
	
	if not form.validate():
		return render_template("questions/new.html", form = form)
	
	q = Question(form.name.data, form.category.data, form.difficulty.data)
	q.account_id = current_user.id
	
	db.session().add(q)
	db.session().commit()
	
	return redirect(url_for("questions_index"))

