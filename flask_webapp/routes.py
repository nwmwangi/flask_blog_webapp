from flask import render_template, url_for, flash, redirect

from flask_webapp import app
# from flask_webapp.forms import RegistrationForm, LoginForm
from flask_webapp.models import User, Post

posts = [
	{
	'author': 'Wangui',
	'title': 'Post 1',
	'content': 'My very first post',
	'date_posted': 'January 28, 2024'
	},
	{
	'author': 'Kinyanjui',
	'title': 'Post 2',
	'content': 'Kinyanjui\'s very first post',
	'date_posted': 'January 28, 2024'
	}

]

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', posts=posts)


@app.route("/about")
def about():
	return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'{form.username.data} registered successfully!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('You are now logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Invalid Username or password!', 'danger')
	return render_template('login.html', title='Login', form=form)
