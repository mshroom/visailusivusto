from application import db
from application.models import Base

class User(Base):
	
	__tablename__ = "account"
	
	name = db.Column(db.String(50), nullable=False)
	username = db.Column(db.String(50), nullable=False)
	password = db.Column(db.String(50), nullable=False)
	role = db.Column(db.String(50))
	
	questions = db.relationship("Question", backref='account', lazy=True)
	
	def __init__(self, name, username, password):
		self.name = name
		self.username = username
		self.password = password
		self.role = "USER"
	
	def get_id(self):
		return self.id
	
	def is_active(self):
		return True
	
	def is_anonymous(self):
		return False
	
	def is_authenticated(self):
		return True

	def get_role(self):
		return self.role
