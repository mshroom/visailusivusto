from application import db
from application.models import Base
from sqlalchemy.sql import text

class Report(Base):

	comment = db.Column(db.String(200), nullable=False)
	checked = db.Column(db.Boolean, nullable=False)
	
	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
	question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

	def __init__(self, comment):
		self.comment = comment
		self.checked = False

	@staticmethod
	def findAllReceivedReports(user_id, checked=False):
		stmt = text("SELECT Report.question_id, Report.comment, Report.date_created, Report.account_id FROM Report, Question WHERE Report.question_id = Question.id AND Question.account_id = :user_id AND Report.checked = :checked").params(user_id=user_id, checked=checked)
		res = db.engine.execute(stmt)
		response = []
		for row in res:
			response.append({"question_id":row[0], "comment":row[1], "date_created":row[2], "account_id":row[3]})
		return response

