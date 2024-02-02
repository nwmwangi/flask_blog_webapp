from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, TextAreaField,SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_webapp.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
	username = StringField('username', validators=[DataRequired(), Length(min=2, max=25)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('user already exists, pick a different username!')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('user already exists, pick a different username!')



class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('remember me')
	
	submit = SubmitField('Login')


class UpdateForm(FlaskForm):
	username = StringField('username', validators=[DataRequired(), Length(min=2, max=25)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	picture = FileField('Update your profile picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update User')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('user already exists, pick a different username!')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('user already exists, pick a different username!')


class ResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Ask for Reset Password!')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('user does not exists, Please register to continue!')

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Reset Password!')