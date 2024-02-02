import os

"""Fetch sensitive information from the environment variable"""
class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True

	"""Get your google credentials stored from the environment variable"""

	MAIL_USERNAME = os.environ.get('ACCOUNT_EMAIL')
	MAIL_PASSWORD = os.environ.get('ACCOUNT_PASSWORD')