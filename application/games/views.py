import random

from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_manager, login_required
from application.auth.models import User
from application.questions.models import Question, Option, UsersChoice
from application.quizzes.models import QuizQuestion, Quiz, Participation
from application.games.forms import QuizGameForm

@app.route("/play/", methods=["GET"])
def games_play():
	quizlist = []
	if current_user.is_authenticated:
		quizzes = Quiz.query.filter(Quiz.active == True, (Quiz.account_id != current_user.id) | (Quiz.automatic == True)).all()
	else:
		quizzes = Quiz.query.filter(Quiz.active == True)
	for q in quizzes:
		a = User.query.filter_by(id = q.account_id).first()
		creator = a.username
		if q.automatic == True:
			creator = "automatic"
		quizlist.append({"creator":creator, "name":q.name, "id":q.id, "category":q.category})

	return render_template("games/play.html", categories = Question.findAllCategoriesInUse(), quizlist = quizlist)

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
@login_required(role="USER")
def play_quiz(quiz_id, turn, answer):
	quiz = Quiz.query.get(quiz_id)
	if quiz.account_id == current_user.id and quiz.automatic == False:
		return login_manager.unauthorized()
	questions = Quiz.findAllQuestions(quiz_id)
	turn = int(turn)
	result = "Correct answer!"
	if answer == "False":
		result = "Wrong answer!"
	if answer == "-1":
		result = "Question was reported."
	if answer == "0":
		result = "Report was cancelled."
	if turn == 0:
		result = ""
		p = Participation()
		p.account_id = current_user.id
		p.quiz_id = quiz_id
		db.session().add(p)
		db.session().commit()
	if turn < len(questions):
		q = questions[turn]
		options = Option.query.filter_by(quest_id=q["id"]).all()
		random.shuffle(options)
		turn += 1
		return render_template("games/quiz.html", quiz = quiz, question = q, options = options, turn = turn, result = result)
	p = db.session.query(Participation).order_by(Participation.id.desc()).first()
	return redirect(url_for('quiz_results', quiz_id=quiz_id, participation_id=p.id, answer=answer))

@app.route("/play/quizzes/<quiz_id>/<turn>/<question_id>/<option_id>", methods=["POST"])
@login_required(role="USER")
def quiz_choose(quiz_id, turn, question_id, option_id):	
	c = UsersChoice()
	c.account_id = current_user.id
	c.option_id = option_id
	db.session().add(c)
	db.session().commit()
	
	q = Quiz.query.get(quiz_id)
	qn = Question.query.get(question_id)
	options = Option.query.filter_by(quest_id=qn.id).all()
	o = Option.query.get(option_id)
	if o.correct:
		return redirect(url_for('play_quiz', quiz_id=quiz_id, turn=turn, answer="True"))
	return redirect(url_for('play_quiz', quiz_id=quiz_id, turn=turn, answer="False"))

@app.route("/play/quizzes/<quiz_id>/<participation_id>/<answer>/results", methods=["GET"])
@login_required(role="USER")
def quiz_results(quiz_id, participation_id, answer):
	q = Quiz.query.get(quiz_id)
	p = Participation.query.get(participation_id)
	if p.account_id != current_user.id:
		return login_manager.unauthorized()
	p.quiz_id = quiz_id
	db.session().commit()

	qs = QuizQuestion.query.filter_by(quiz_id=q.id).count()
	correct = UsersChoice.countCorrectAnswersFromQuiz(current_user.id, participation_id)
	previous = Participation.query.filter_by(quiz_id=q.id, account_id=current_user.id).count() - 1
	result = "Correct answer!"
	if answer == "False":
		result = "Wrong answer!"
	if answer == "-1":
		result = "Question was reported."
	
	return render_template("games/quizresult.html", quiz = q, qs = qs, correct = correct, previous = previous, result = result)





