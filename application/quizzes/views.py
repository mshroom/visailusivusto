from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_manager, login_required
from application.questions.models import Question, Option, UsersChoice
from application.quizzes.models import Quiz, QuizQuestion, Participation
from application.quizzes.forms import QuizForm, ModifyQuizForm, ModifyQuizCategoryForm, QuizQuestionForm

@app.route("/quizzes", methods=["GET"])
@login_required(role="USER")
def quizzes_index():
	return render_template("quizzes/list.html", quizzes = Quiz.query.filter_by(account_id=current_user.id).all())

@app.route("/quizzes/control", methods=["GET"])
@login_required(role="ADMIN")
def quizzes_control():
	return render_template("quizzes/list.html", quizzes = Quiz.query.all())

@app.route("/quizzes/new/")
@login_required(role="USER")
def quizzes_form():
	return render_template("quizzes/new.html", form = QuizForm())

@app.route("/quizzes/", methods=["POST"])
@login_required(role="USER")
def quizzes_create():
		
	form = QuizForm(request.form)
	
	if not form.validate():
		return render_template("quizzes/new.html", form = form)
	
	q = Quiz(form.name.data, form.category.data)
	q.account_id = current_user.id
	
	db.session().add(q)
	db.session().commit()
	
	return redirect(url_for("quizzes_index"))

@app.route("/quizzes/mod/<quiz_id>/", methods=["GET", "POST"])
@login_required(role="USER")
def quizzes_modify(quiz_id):
	q = Quiz.query.get(quiz_id)
	if q.account_id != current_user.id and current_user.role != "ADMIN":
		return login_manager.unauthorized()
	
	a = q.account_id
	q_form = QuizQuestionForm()
	q_form.question.choices = [(row.id, row.name) for row in Question.query.filter_by(account_id=a)]

	if request.method == "GET":
		return render_template("quizzes/modify.html", quiz = Quiz.query.get(quiz_id), questions = Quiz.findAllQuestions(quiz_id), form = ModifyQuizForm(), c_form = ModifyQuizCategoryForm(), qq_form = q_form)

	form = QuizForm(request.form)
	
	if not form.validate():
				return render_template("quizzes/modify.html", quiz = Quiz.query.get(quiz_id), questions = Quiz.findAllQuestions(quiz_id), form = ModifyQuizForm(), c_form = ModifyQuizCategoryForm(), qq_form = q_form)
	q = Quiz.query.get(quiz_id)
	q.name = form.name.data
	q.category = form.category.data
	
	db.session().commit()
	
	return redirect(url_for('quizzes_modify', quiz_id=quiz_id))

@app.route("/quizzes/mod/quiz/<quiz_id>/", methods=["POST"])
@login_required(role="USER")
def quizzes_modifyQuiz(quiz_id):
	q = Quiz.query.get(quiz_id)
	if q.account_id != current_user.id and current_user.role != "ADMIN":
		return login_manager.unauthorized()
	
	a = q.account_id
	q_form = QuizQuestionForm()
	q_form.question.choices = [(row.id, row.name) for row in Question.query.filter_by(account_id=a)]

	form = ModifyQuizForm(request.form)
	
	if not form.validate():
		return render_template("quizzes/modify.html", quiz = Quiz.query.get(quiz_id), questions = Quiz.findAllQuestions(quiz_id), form = ModifyQuizForm(), c_form = ModifyQuizCategoryForm(), qq_form = q_form)
	q = Quiz.query.get(quiz_id)
	q.name = form.name.data
	
	db.session().commit()
	
	return redirect(url_for('quizzes_modify', quiz_id=quiz_id))

@app.route("/quizzes/mod/category/<quiz_id>/", methods=["POST"])
@login_required(role="USER")
def quizzes_modifyCategory(quiz_id):
	q = Quiz.query.get(quiz_id)
	if q.account_id != current_user.id and current_user.role != "ADMIN":
		return login_manager.unauthorized()
	
	a = q.account_id
	q_form = QuizQuestionForm()
	q_form.question.choices = [(row.id, row.name) for row in Question.query.filter_by(account_id=a)]

	form = ModifyQuizCategoryForm(request.form)

	q = Quiz.query.get(quiz_id)
	q.category = form.category.data
	
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
