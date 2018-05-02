import random

from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_manager, login_required
from application.questions.models import Question, Option, UsersChoice
from application.quizzes.models import Quiz, QuizQuestion, Participation
from application.quizzes.forms import QuizForm, ModifyQuizForm, ModifyQuizCategoryForm, QuizQuestionForm, AutoQuizForm

@app.route("/quizzes", methods=["GET"])
@login_required(role="USER")
def quizzes_index():
	return render_template("quizzes/list.html", quizzes = Quiz.query.filter_by(account_id=current_user.id).all(), control = "user")

@app.route("/quizzes/control", methods=["GET"])
@login_required(role="ADMIN")
def quizzes_control():
	return render_template("quizzes/list.html", quizzes = Quiz.query.all(), control = "control")

@app.route("/quizzes/new/")
@login_required(role="USER")
def quizzes_form():
	return render_template("quizzes/new.html", form = QuizForm(), autoform = AutoQuizForm())

@app.route("/quizzes/", methods=["POST"])
@login_required(role="USER")
def quizzes_create():
		
	form = QuizForm(request.form)
	
	if not form.validate():
		return render_template("quizzes/new.html", form = form, autoform = AutoQuizForm())
	
	q = Quiz(form.name.data, form.category.data)
	q.account_id = current_user.id
	
	db.session().add(q)
	db.session().commit()
	
	return redirect(url_for("quizzes_index"))

@app.route("/quizzes/auto/", methods=["POST"])
@login_required(role="USER")
def quizzes_autocreate():
		
	autoform = AutoQuizForm(request.form)
	
	if not autoform.validate():
		return render_template("quizzes/new.html", form = QuizForm(), autoform = autoform)
	
	category = autoform.category.data
	number = autoform.number.data
	maxim = 0
	if category == "all":
		maxim = Question.query.filter_by(active=True).count()
	else:
		maxim = Question.query.filter_by(active=True, category=category).count()	
	if number > maxim:
		msg = "Please select a smaller number. Maximum for " + category + " category is " + str(maxim)
		return render_template("quizzes/new.html", form = QuizForm(), autoform = autoform, size_error = msg)
	
	q = Quiz(autoform.name.data, autoform.category.data)
	q.account_id = current_user.id
	q.automatic = True
	
	db.session().add(q)
	db.session().commit()

	questions = Question.query.filter_by(active=True).all()
	if category != "all":
		questions = Question.query.filter_by(active=True, category=q.category).all()
	
	random.shuffle(questions)
	count = 0
	while count < number:
		qq = QuizQuestion()
		qq.quiz_id = q.id
		qq.question_id = questions[count].id	
		db.session().add(qq)
		db.session().commit()
		count += 1
	
	return redirect(url_for("quizzes_index"))

@app.route("/quizzes/act/<control>/<quiz_id>/", methods=["POST"])
@login_required(role="USER")
def quizzes_activate(quiz_id, control):
	q = Quiz.query.get(quiz_id)
	if q.active == True:
		q.active = False
	else:
		questions = Quiz.findAllQuestions(quiz_id)
		if len(questions) < 2:
			a = q.account_id
			q_form = QuizQuestionForm()
			list = []
			for row in Quiz.findAllUsersUnusedQuestions(quiz_id):
				list.append((row[0], row[1]))
			q_form.question.choices = list
			if current_user.role == "ADMIN" and control == "control":
				return render_template("quizzes/list.html", quizzes = Quiz.query.all(), control = control, error = "Quiz has less than two questions and cannot be activated")
			return render_template("quizzes/list.html", quizzes = Quiz.query.filter_by(account_id=current_user.id).all(), control = control, error = "Quiz has less than two questions and cannot be activated")
		q.active = True
	db.session().commit()
	
	if current_user.role == "ADMIN" and control == "control":
		return redirect(url_for('quizzes_control'))
	return redirect(url_for('quizzes_index'))

@app.route("/quizzes/del/<control>/<quiz_id>/", methods=["POST"])
@login_required(role="USER")
def quizzes_delete(quiz_id, control):
	q = Quiz.query.get(quiz_id)
	db.session.query(QuizQuestion).filter_by(quiz_id=q.id).delete()	
	db.session().delete(q)
	db.session().commit() 

	if current_user.role == "ADMIN" and control == "control":
		return redirect(url_for('quizzes_control'))
	return redirect(url_for('quizzes_index'))


@app.route("/quizzes/mod/<quiz_id>/", methods=["GET", "POST"])
@login_required(role="USER")
def quizzes_modify(quiz_id):
	q = Quiz.query.get(quiz_id)
	if (q.account_id != current_user.id or q.automatic==True) and current_user.role != "ADMIN":
		return login_manager.unauthorized()
	
	a = q.account_id
	q_form = QuizQuestionForm()
	list = []
	for row in Quiz.findAllUsersUnusedQuestions(quiz_id):
		list.append((row[0], row[1]))
	q_form.question.choices = list

	return render_template("quizzes/modify.html", quiz = Quiz.query.get(quiz_id), questions = Quiz.findAllQuestions(quiz_id), form = ModifyQuizForm(), c_form = ModifyQuizCategoryForm(), qq_form = q_form)

@app.route("/quizzes/mod/quiz/<quiz_id>/", methods=["POST"])
@login_required(role="USER")
def quizzes_modifyQuiz(quiz_id):
	q = Quiz.query.get(quiz_id)
	if (q.account_id != current_user.id or q.automatic == True) and current_user.role != "ADMIN":
		return login_manager.unauthorized()
	
	a = q.account_id
	q_form = QuizQuestionForm()
	list = []
	for row in Quiz.findAllUsersUnusedQuestions(quiz_id):
		list.append((row[0], row[1]))
	q_form.question.choices = list

	form = ModifyQuizForm(request.form)
	
	if not form.validate():
		return render_template("quizzes/modify.html", quiz = Quiz.query.get(quiz_id), questions = Quiz.findAllQuestions(quiz_id), form = form, c_form = ModifyQuizCategoryForm(), qq_form = q_form)
	q = Quiz.query.get(quiz_id)
	q.name = form.name.data
	
	db.session().commit()
	
	return redirect(url_for('quizzes_modify', quiz_id=quiz_id))

@app.route("/quizzes/mod/category/<quiz_id>/", methods=["POST"])
@login_required(role="USER")
def quizzes_modifyCategory(quiz_id):
	q = Quiz.query.get(quiz_id)
	
	a = q.account_id
	q_form = QuizQuestionForm()
	list = []
	for row in Quiz.findAllUsersUnusedQuestions(quiz_id):
		list.append((row[0], row[1]))
	q_form.question.choices = list

	form = ModifyQuizCategoryForm(request.form)

	q = Quiz.query.get(quiz_id)
	q.category = form.category.data
	
	db.session().commit()
	
	return redirect(url_for('quizzes_modify', quiz_id=quiz_id))

@app.route("/quizzes/mod/act/<quiz_id>/", methods=["POST"])
@login_required(role="USER")
def quiz_activate(quiz_id):
	q = Quiz.query.get(quiz_id)
	if q.active == True:
		q.active = False
	else:
		questions = Quiz.findAllQuestions(quiz_id)
		if len(questions) < 2:
			a = q.account_id
			q_form = QuizQuestionForm()
			list = []
			for row in Quiz.findAllUsersUnusedQuestions(quiz_id):
				list.append((row[0], row[1]))
			q_form.question.choices = list
			return render_template("quizzes/modify.html", quiz = Quiz.query.get(quiz_id), questions = Quiz.findAllQuestions(quiz_id), form = ModifyQuizForm(), c_form = ModifyQuizCategoryForm(), qq_form = q_form, act_error = "Quiz has less than two questions and cannot be activated")
		q.active = True
	db.session().commit()

	return redirect(url_for('quizzes_modify', quiz_id=quiz_id))


@app.route("/quizzes/mod/<quiz_id>/add/", methods=["POST"])
@login_required(role="USER")
def quizQuestions_add(quiz_id):
	qq_form = QuizQuestionForm(request.form)
		
	qn = Question.query.get(qq_form.question.data)
	
	qq = QuizQuestion()
	qq.quiz_id = quiz_id
	qq.question_id = qn.id
	
	db.session().add(qq)
	db.session().commit()
	
	return redirect(url_for('quizzes_modify', quiz_id=quiz_id))

@app.route("/quizzes/mod/<qz_id>/del/<qn_id>/", methods=["POST"])
@login_required(role="USER")
def quizQuestions_delete(qz_id, qn_id):
	db.session.query(QuizQuestion).filter_by(quiz_id=qz_id, question_id=qn_id).delete()
	db.session().commit()
	q = Quiz.query.get(qz_id)
	if q.active == True:
		questions = Quiz.findAllQuestions(qz_id)
		if len(questions) < 2:
			q.active = False
			db.session().commit()
			a = q.account_id
			q_form = QuizQuestionForm()
			list = []
			for row in Quiz.findAllUsersUnusedQuestions(qz_id):
				list.append((row[0], row[1]))
			q_form.question.choices = list
			return render_template("quizzes/modify.html", quiz = Quiz.query.get(qz_id), questions = Quiz.findAllQuestions(qz_id), form = ModifyQuizForm(), c_form = ModifyQuizCategoryForm(), qq_form = q_form, act_error = "Quiz was deactivated beacause it has less than two questions")
	return redirect(url_for('quizzes_modify', quiz_id=qz_id))
