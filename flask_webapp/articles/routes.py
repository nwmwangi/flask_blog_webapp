from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from flask_webapp import db
from flask_webapp.models import  Article
from flask_webapp.articles.forms import  PostForm
import os


articles = Blueprint('articles', __name__)





@articles.route("/post/new", methods = ['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Article(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Article created successfully!', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html', title = 'New Post', form=form, legend='Create New Article')

@articles.route("/post/<int:post_id>")
def article(post_id):
	post = Article.query.get_or_404(post_id)
	return render_template('article.html', title=Article.title, post=post, legend='New Article')


@articles.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
		return redirect(url_for('articles.article', post_id = post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content

	return render_template('create_post.html', title='Update Article', legend = 'Update Article', form=form)


@articles.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_article(post_id):
	post = Article.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)

	db.session.delete(post)
	db.session.commit()
	flash('Article deleted!', 'success')
	return redirect(url_for('main.home'))

