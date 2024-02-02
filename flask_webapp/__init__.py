import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_webapp.config import Config
from flask import current_app




db = SQLAlchemy() 

bcrypt = Bcrypt()
 
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


mail = Mail()



"""create a configuration object function to modularize creation of apps"""
def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	app.app_context().push()
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	"""Import and register the modularized blueprints"""
	from flask_webapp.users.routes import users
	from flask_webapp.articles.routes import articles
	from flask_webapp.main.routes import main
	app.register_blueprint(users)
	app.register_blueprint(articles)
	app.register_blueprint(main)

	return app
