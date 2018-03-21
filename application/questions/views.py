from application import app, db
from flask import redirect, render_template, request, url_for
from application.questions.models import Question

@app.route("/questions", methods=["GET"])
def questions_index():
	return render_template("questions/list.html", questions = Question.query.all())

@app.route("/questions/new/")
def questions_form():
	return render_template("questions/new.html")

@app.route("/questions/<question_id>/", methods=["POST"])
def questions_delete(question_id):
	q = Question.query.get(question_id)
	db.session().delete(q)
	db.session().commit()
	
	return redirect(url_for("questions_index"))

@app.route("/questions/", methods=["POST"])
def questions_create():
	print(request.form.get("name"))
	print(request.form.get("category"))
	print(request.form.get("difficulty"))
	
	q = Question(request.form.get("name"), request.form.get("category"), request.form.get("difficulty"))
	
	db.session().add(q)
	db.session().commit()
	
	return redirect(url_for("questions_index"))
