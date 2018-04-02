from application import db

class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
	onupdate=db.func.current_timestamp())
	
	name = db.Column(db.String(200), nullable=False)
	category = db.Column(db.String(20), nullable=False)
	difficulty = db.Column(db.String(10), nullable=False)
	active = db.Column(db.Boolean, nullable=False)
	
	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
	
	def __init__(self, name, category, difficulty, active):
		self.name = name
		self.category = category
		self.difficulty = difficulty
		self.active = active

class Option(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
	onupdate=db.func.current_timestamp())
	
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
	
