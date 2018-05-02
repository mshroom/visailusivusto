import os

from application import db
from application.models import Base

from sqlalchemy.sql import text

class Question(Base):
		
	name = db.Column(db.String(200), nullable=False)
	category = db.Column(db.String(20), nullable=False)
	difficulty = db.Column(db.String(10), nullable=False)
	active = db.Column(db.Boolean, nullable=False)
	
	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

	def __init__(self, name, category, difficulty):
		self.name = name
		self.category = category
		self.difficulty = difficulty
		self.active = False

	@staticmethod
	def findAllCategoriesInUse(active=True):
		stmt = text("SELECT DISTINCT Question.category from Question WHERE Question.active = :active ORDER BY Question.category").params(active=active)
		res = db.engine.execute(stmt)
		response = []
		for row in res:
			response.append(row[0])
		return response

class Option(Base):
		
	name = db.Column(db.String(200), nullable=False)
	correct = db.Column(db.Boolean, nullable=False)
	
	quest_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
	
	def __init__(self, name, correct):
		self.name = name
		self.correct = correct

class UsersChoice(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	
	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
	option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)
	
	@staticmethod	
	def countCorrectAnswers(user_id, correct=True):
		stmt = text("SELECT COUNT(Users_choice.id) FROM Users_choice, Option WHERE account_id = :user_id AND option_id = Option.id AND Option.correct = :correct").params(user_id=user_id, correct=correct)
		res = db.engine.execute(stmt)
		response = res.fetchone()[0]
		return response
	
	@staticmethod
	def countAllAnswers(user_id):
		stmt = text("SELECT COUNT(Users_choice.id) FROM Users_choice WHERE account_id = :user_id").params(user_id=user_id)
		res = db.engine.execute(stmt)
		response = res.fetchone()[0]
		return response

	@staticmethod
	def countAllAnswersByCategory(user_id, category):
		stmt = text("SELECT COUNT(Users_choice.id) FROM Users_choice, Option, Question WHERE Users_choice.account_id = :user_id AND Users_choice.option_id = Option.id AND Option.quest_id = Question.id AND Question.category = :category").params(user_id=user_id, category=category)
		res = db.engine.execute(stmt)
		response = res.fetchone()[0]
		return response

	@staticmethod
	def countCorrectAnswersByCategory(user_id, category, correct=True):
		stmt = text("SELECT COUNT(Users_choice.id) FROM Users_choice, Option, Question WHERE Users_choice.account_id = :user_id AND Users_choice.option_id = Option.id AND Option.quest_id = Question.id AND Option.correct = :correct AND Question.category = :category").params(user_id=user_id, category=category, correct=correct)
		res = db.engine.execute(stmt)
		response = res.fetchone()[0]
		return response

	@staticmethod
	def countCorrectAnswersFromQuiz(user_id, participation_id, correct=True):
		
		stmt = text("SELECT COUNT(Users_choice.id) FROM Users_Choice, Option, Question, Quiz_Question, Quiz, Participation WHERE Users_Choice.account_id = :user_id AND Users_Choice.option_id = Option.id AND Option.quest_id = Question.id AND Quiz_Question.question_id = Question.id AND Quiz_Question.quiz_id = Quiz.id AND Participation.quiz_id = Quiz.id AND Participation.account_id = Users_Choice.account_id AND Users_Choice.date_created >= Participation.date_created AND Users_Choice.date_created <= Participation.date_modified AND Participation.id = :participation_id AND Option.correct = :correct").params(user_id=user_id, participation_id=participation_id, correct=correct)
		res = db.engine.execute(stmt)
		response = res.fetchone()[0]
		return response

	@staticmethod
	def mostCorrectAnswers(correct=True):
		stmt = ""
		if os.environ.get("HEROKU"):
			stmt = text("SELECT Account.username, count(users_choice.id) AS answers FROM Account, Users_Choice, Option WHERE Users_Choice.date_created > DATE_TRUNC('week', CURRENT_TIMESTAMP - interval '1 week') AND Users_Choice.account_id = Account.id AND Users_Choice.option_id = Option.id AND Option.correct = :correct group by Account.id ORDER BY answers DESC LIMIT 10").params(correct=correct)
		else:
			stmt = text("SELECT Account.username, count(users_choice.id) AS answers FROM Account, Users_Choice, Option WHERE Users_Choice.date_created >= DATE(CURRENT_TIMESTAMP, '-6 DAY') AND Users_Choice.account_id = Account.id AND Users_Choice.option_id = Option.id AND Option.correct = :correct group by Account.id ORDER BY answers DESC LIMIT 10").params(correct=correct)
		res = db.engine.execute(stmt)
		response = []
		for row in res:
			response.append({"username":row[0], "answers":row[1]})
		return response


