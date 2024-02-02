import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail



app = Flask(__name__)
app.config['SECRET_KEY'] = 'b56d7c1813909f6cd97db542a7759a2b0ec8efba'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres123@localhost:5433/blog_webapp'
db = SQLAlchemy(app) 
app.app_context().push()
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

"""Get your google credentials stored from the environment variable"""

app.config['MAIL_USERNAME'] = os.environ.get('ACCOUNT_EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('ACCOUNT_PASSWORD')
mail = Mail(app)


"""Import and register the modularized blueprints"""
from flask_webapp.users.routes import users
from flask_webapp.articles.routes import articles
from flask_webapp.main.routes import main


app.register_blueprint(users)
app.register_blueprint(articles)
app.register_blueprint(main)