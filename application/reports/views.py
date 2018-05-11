from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_manager, login_required
from application.reports.models import Report
from application.reports.forms import ReportForm
from application.questions.models import Question, Option
from application.quizzes.models import Quiz, QuizQuestion

@app.route("/reports", methods=["GET"])
@login_required(role="USER")
def reports_index():
	return render_template("reports/list.html", reports = Report.findAllReceivedReports(current_user.id), control = "user")

@app.route("/reports/control", methods=["GET"])
@login_required(role="ADMIN")
def reports_control():
	return render_template("reports/list.html", reports = Report.query.filter_by(checked=False).all(), control = "control")

@app.route("/reports/sort/", methods=["POST"])
@login_required(role="ADMIN")
def reports_sort():
	sorter = request.form.get("sort")
	return render_template("reports/list.html", reports = Report.query.filter_by(checked=False).order_by(sorter), control = "control")

@app.route("/reports/new/<question_id>/<quiz_id>/<turn>/", methods=["GET"])
@login_required(role="USER")
def reports_form(question_id, quiz_id, turn):
	turn = int(turn)
	return render_template("reports/new.html", question = Question.query.get(question_id), options = Option.query.filter_by(quest_id=question_id).all(), form = ReportForm(), quiz_id = quiz_id, t = turn)

@app.route("/reports/create/<question_id>/<quiz_id>/<turn>/", methods=["POST"])
@login_required(role="USER")
def reports_create(question_id, quiz_id, turn):
	question = Question.query.get(question_id)
	turn = int(turn)
	
	form = ReportForm(request.form)
	
	if not form.validate():
		return render_template("reports/new.html", question = Question.query.get(question_id), options = Option.query.filter_by(quest_id=question_id).all(), form = form, quiz_id = quiz_id, t = turn)
	
	r = Report(form.comment.data)
	r.account_id = current_user.id
	r.question_id = question.id	

	db.session().add(r)
	db.session().commit()

	q = Question.query.get(question_id)
	q.active = False
	db.session().commit()
	quizquestions = QuizQuestion.query.filter_by(question_id=q.id)
	for qq in quizquestions:
		quiz = Quiz.query.get(qq.quiz_id)
		db.session().delete(qq)
		db.session().commit()
		if quiz.active == True:
			questions = Quiz.findAllQuestions(quiz.id)
			if len(questions) < 2:
				quiz.active = False
				db.session().commit()

	if quiz_id == "-1":
		return redirect(url_for("games_play"))

	turn = turn - 1	
	return redirect(url_for('play_quiz', quiz_id=quiz_id, turn=turn, answer="-1"))

@app.route("/reports/check/<report_id>/", methods=["POST"])
@login_required(role="ADMIN")
def reports_check(report_id):
	r = Report.query.get(report_id)
	r.checked = True
	db.session().commit()

	return redirect(url_for("reports_control"))

@app.route("/reports/cancel/<question_id>/<quiz_id>/<turn>/", methods=["POST"])
@login_required(role="USER")
def reports_cancel(question_id, quiz_id, turn):
	if quiz_id == "-1":
		q = Question.query.get(question_id)
		options = Option.query.filter_by(quest_id=question_id)
		return render_template("games/answer.html", question = q, options = options)
	
	turn = int(turn)
	turn = turn - 1
	turn = str(turn)
	
	return redirect(url_for('play_quiz', quiz_id=quiz_id, turn=turn, answer="0"))

