from application import db

class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
	onupdate=db.func.current_timestamp())
	
	name = db.Column(db.String(200), nullable=False)
	category = db.Column(db.String(20), nullable=False)
	difficulty = db.Column(db.String(10), nullable=False)
	
	def __init__(self, name, category, difficulty):
		self.name = name
		self.category = category
		self.difficulty = difficulty
