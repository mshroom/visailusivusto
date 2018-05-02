from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.questions.models import Question, Option, UsersChoice
from application.quizzes.models import Quiz, Participation

@app.route("/statistics", methods=["GET"])
@login_required
def statistics_show():
	allAnswers = UsersChoice.countAllAnswers(current_user.id)
	correctAnswers = UsersChoice.countCorrectAnswers(current_user.id)
	percentageOfCorrectAnswers = 0
	if allAnswers > 0:
		percentageOfCorrectAnswers = correctAnswers/allAnswers*100

	categories = Question.findAllCategoriesInUse()

	answersByCategories = []
	for c in categories:
		category = c
		categoryAnswers = UsersChoice.countAllAnswersByCategory(current_user.id, c)
		categoryCorrect = UsersChoice.countCorrectAnswersByCategory(current_user.id, c)
		categoryPercentage = 0
		if categoryAnswers > 0:
			categoryPercentage = categoryCorrect/categoryAnswers*100
		answersByCategories.append({"category":category, "answers":categoryAnswers, "correct":categoryCorrect, "percentage":categoryPercentage})

	return render_template("statistics/statistics.html", allAnswers = allAnswers, correctAnswers = correctAnswers, percentageOfCorrectAnswers = percentageOfCorrectAnswers, answersByCategories = answersByCategories)

@app.route("/index", methods=["GET"])
def highscores_create():
	mostCorrectAnswersWeek = UsersChoice.mostCorrectAnswers(week=True)
	mostAddedQuestionsWeek = Question.mostAddedQuestions(week=True)
	mostQuizPlaysWeek = Participation.mostQuizPlays(week=True)
	mostCorrectAnswers = UsersChoice.mostCorrectAnswers(week=False)
	mostAddedQuestions = Question.mostAddedQuestions(week=False)
	mostQuizPlays = Participation.mostQuizPlays(week=False)
	
	return render_template("index.html", mostCorrectAnswersWeek = mostCorrectAnswersWeek, mostAddedQuestionsWeek = mostAddedQuestionsWeek, mostQuizPlaysWeek = mostQuizPlaysWeek, mostCorrectAnswers = mostCorrectAnswers, mostAddedQuestions = mostAddedQuestions, mostQuizPlays = mostQuizPlays)
