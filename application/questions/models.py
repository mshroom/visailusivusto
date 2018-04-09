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
	def findAllCategoriesInUse():
		stmt = text("SELECT DISTINCT Question.category from Question WHERE Question.active = 1 ORDER BY Question.category")
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
	
