from application import app, db
from flask import redirect, render_template, request, url_for
from application.questions.models import Question

@app.route("/questions", methods=["GET"])
def questions_index():
	return render_template("questions/list.html", questions = Question.query.all())

@app.route("/questions/new/")
def questions_form():
	return render_template("questions/new.html")

@app.route("/questions/", methods=["POST"])
def questions_create():
	print(request.form.get("name"))
	
	q = Question(request.form.get("name"))
	
	db.session().add(q)
	db.session().commit()
	
	return redirect(url_for("questions_index"))
