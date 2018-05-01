from application import db
from application.models import Base

from sqlalchemy.sql import text

class Quiz(Base):
		
	name = db.Column(db.String(200), nullable=False)
	category = db.Column(db.String(20), nullable=False)
	active = db.Column(db.Boolean, nullable=False)
	automatic = db.Column(db.Boolean, nullable=False)
	
	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

	def __init__(self, name, category):
		self.name = name
		self.category = category
		self.active = False
		self.automatic = False

	@staticmethod
	def findAllQuestions(quiz_id):
		stmt = text("SELECT Question.id, Question.name, Question.category, Question.difficulty, Question.active FROM Question, Quiz_question, Quiz WHERE Question.id = Quiz_question.question_id AND Quiz.id = Quiz_question.quiz_id AND Quiz.id = :quiz_id").params(quiz_id=quiz_id)
		res = db.engine.execute(stmt)
		response = []
		for row in res:
			response.append({"id":row[0], "name":row[1], "category":row[2], "difficulty":row[3], "active":row[4]})
		return response

	@staticmethod
	def findAllUsersUnusedQuestions(quiz_id):
		q = Quiz.query.get(quiz_id)
		stmt = text("SELECT Question.id, Question.name FROM QUESTION, ACCOUNT WHERE Question.account_id = Account.id AND Account.id = :account_id AND Question.id NOT IN (SELECT Question.id FROM Question, Quiz, Quiz_Question Where Quiz_Question.question_id = Question.id AND Quiz_Question.quiz_id = Quiz.id AND Quiz.id = :quiz_id)").params(account_id=q.account_id, quiz_id=quiz_id)
		res = db.engine.execute(stmt)
		response = []
		for row in res:
			response.append([row[0], row[1]])
		return response

class QuizQuestion(db.Model):
		
	id = db.Column(db.Integer, primary_key=True)
	
	quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
	question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
	
class Participation(Base):

	quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
