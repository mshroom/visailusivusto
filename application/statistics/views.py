from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.questions.models import Question, Option, UsersChoice

@app.route("/statistics", methods=["GET"])
@login_required
def statistics_show():
	allAnswers = UsersChoice.countAllAnswers(current_user.id)
	correctAnswers = UsersChoice.countCorrectAnswers(current_user.id)
	percentageOfCorrectAnswers = 0
	if allAnswers > 0:
		percentageOfCorrectAnswers = correctAnswers/allAnswers*100

	return render_template("statistics/statistics.html", allAnswers = allAnswers, correctAnswers = correctAnswers, percentageOfCorrectAnswers = percentageOfCorrectAnswers)

