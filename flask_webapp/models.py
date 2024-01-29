from datetime import datetime
from flask_webapp import db



class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(25), unique=True, nullable=False)
	email = db.Column(db.String(130), unique=True, nullable=False)
	image_file = db.Column(db.String(30), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(125), nullable=False)
	date_posted = db.Column(db.String(130), unique=True, nullable=False)
	image_file = db.Column(db.DateTime(30), nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"User('{self.title}', '{self.date_posted}')"


