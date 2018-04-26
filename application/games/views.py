import random

from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_manager, login_required
from application.questions.models import Question, Option, UsersChoice
from application.quizzes.models import QuizQuestion, Quiz
from application.games.forms import QuizGameForm

@app.route("/play/", methods=["GET"])
def games_play():
	return render_template("games/play.html", categories = Question.findAllCategoriesInUse(), quizzes = Quiz.query.all())

@app.route("/play/random/", methods=["GET"])
def play_random():
	questions = Question.query.filter_by(active=True).all()
	random.shuffle(questions)
	q = questions[0]
	options = Option.query.filter_by(quest_id=q.id).all()
	random.shuffle(options)
	return render_template("games/answer.html", question = q, options = options)

@app.route("/play/categories/<cat>", methods=["GET"])
def play_category(cat):
	questions = Question.query.filter_by(active=True, category=cat).all()	
	random.shuffle(questions)
	q = questions[0]
	options = Option.query.filter_by(quest_id=q.id).all()
	random.shuffle(options)
	return render_template("games/answer.html", question = q, options = options)

@app.route("/play/<question_id>/<option_id>", methods=["POST"])
def options_choose(question_id, option_id):
	if current_user.is_authenticated:
		c = UsersChoice()
		c.account_id = current_user.id
		c.option_id = option_id

		db.session().add(c)
		db.session().commit()

	o = Option.query.get(option_id)
	if o.correct:
		return render_template("games/result.html", option = o, question = Question.query.get(question_id),result = "Correct answer!")

	return render_template("games/result.html", option = o, question = Question.query.get(question_id),result = "Wrong answer!")

@app.route("/play/quizzes/<quiz_id>/<turn>/<answer>", methods=["GET"])
def play_quiz(quiz_id, turn, answer):
	quiz = Quiz.query.get(quiz_id)
	questions = Quiz.findAllQuestions(quiz_id)
	turn = int(turn)
	result = "Correct answer!"
	if answer == "False":
		result = "Wrong answer!"
	if turn == 0:
		result = ""
	if turn < len(questions):
		q = questions[turn]
		options = Option.query.filter_by(quest_id=q["id"]).all()
		random.shuffle(options)
		turn += 1
		return render_template("games/quiz.html", quiz = quiz, question = q, options = options, turn = turn, result = result)
	return redirect(url_for('quiz_results', quiz_id=quiz_id))

@app.route("/play/quizzes/<quiz_id>/<turn>/<question_id>/<option_id>", methods=["POST"])
def quiz_choose(quiz_id, turn, question_id, option_id):
	q = Quiz.query.get(quiz_id)
	qn = Question.query.get(question_id)
	options = Option.query.filter_by(quest_id=qn.id).all()
	o = Option.query.get(option_id)
	if o.correct:
		return redirect(url_for('play_quiz', quiz_id=quiz_id, turn=turn, answer="True"))

	return redirect(url_for('play_quiz', quiz_id=quiz_id, turn=turn, answer="False"))

@app.route("/play/quizzes/<quiz_id>/results", methods=["GET"])
def quiz_results(quiz_id):
	q = Quiz.query.get(quiz_id)
	return render_template("games/quizresult.html", quiz = q)





