import os
import secrets
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from PIL import Image
from flask_webapp import app, db, bcrypt, mail
from flask_webapp.models import User, Article
from flask_webapp.forms import (RegistrationForm, LoginForm, UpdateForm, PostForm, ResetForm,ResetPasswordForm)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from flask_webapp import models

@app.route("/")
@app.route("/home")
def home():
	page = request.args.get('page', 1, type=int)
	posts = Article.query.order_by(Article.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('home.html', posts=posts)


@app.route("/about")
def about():
	return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Registered successfully, You can now Login!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')

			flash('You are now logged in!', 'success')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Invalid Username or password!', 'danger')
	return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	f_name, f_extension = os.path.splitext(form_picture.filename)
	picture_filename = random_hex + f_extension
	picture_path = os.path.join(app.root_path, 'static/profiles', picture_filename)

	"""resize the picture before saving it to file"""

	output_size = (125, 125)
	new_image = Image.open(form_picture)
	new_image.thumbnail(output_size)

	new_image.save(picture_path)
	return picture_filename


@app.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
	form = UpdateForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('update successful!')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename=f'profiles/{current_user.image_file}')
	return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/new", methods = ['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Article(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Article created successfully!', 'success')
		return redirect(url_for('home'))
	return render_template('create_post.html', title = 'New Post', form=form, legend='Create New Article')

@app.route("/post/<int:post_id>")
def article(post_id):
	post = Article.query.get_or_404(post_id)
	return render_template('article.html', title=Article.title, post=post, legend='New Article')


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_article(post_id):
	post = Article.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		flash('Update successful!', 'success')
		db.session.commit()
		return redirect(url_for('article', post_id = post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content

	return render_template('create_post.html', title='Update Article', legend = 'Update Article', form=form)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_article(post_id):
	post = Article.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)

	db.session.delete(post)
	db.session.commit()
	flash('Article deleted!', 'success')
	return redirect(url_for('home'))


@app.route("/")
@app.route("/user/<string:username>")
def user_article(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Article.query.filter_by(author=user)\
	.order_by(Article.date_posted.desc())\
	.paginate(page=page, per_page=2)
	return render_template('user_article.html', posts=posts, user=user)

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request',
					sender = os.environ.get('ACCOUNT_EMAIL'),
					recipients=[user.email])
	msg.body = f'''Follow this link to reset your password:
{url_for('reset_token', token=token, _external=True)} '''

	mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('home')) 
	form = ResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash("reset instructions send to your email!", 'info')
		return redirect(url_for('login'))
	return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('home')) 
	user = User.verify_reset_token(token)
	if user is None:
		flash("Expired token!", 'warning')
		return redirect(url_for('reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash(f'Password reset is successful! Login Now!', 'success')
		return redirect(url_for('login'))
	return render_template('reset_token.html', title='Reset Password', form=form)
