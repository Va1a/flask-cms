from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment, Like, Dislike, Alert, has_user_liked, has_user_disliked
from flaskblog.posts.forms import PostForm, CommentForm

posts = Blueprint('posts', __name__)

# MAKE NEW POST PAGE
@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash(f'Posted "{form.title.data}".', 'success')
		return redirect(url_for('main.home'))
	return render_template('newpost.html', title='New Post', form=form, legend='New Post', submit='post')

# VIEW EXISTING POST PAGE
@posts.route('/post/<int:post_id>', methods=["GET",'POST'])
def post(post_id):
	post = Post.query.get_or_404(post_id)
	page = request.args.get('page', 1, type=int)
	comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_commented.desc()).paginate(page=page, per_page=5)
	form = CommentForm()
	if form.validate_on_submit():
		if not current_user.is_authenticated: abort(403)
		comment = Comment(content=form.content.data, author=current_user, assoc_post=post)
		alert = Alert(assoc_user=post.author, type='comment', from_user=current_user.id, post_id=post.id)
		db.session.add(comment)
		db.session.add(alert)
		db.session.commit()
		flash(f'Commented on "{post.title}".', 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	return render_template('post.html', title=post.title, post=post, comments=comments, form=form, submit='comment', has_user_liked=has_user_liked, has_user_disliked=has_user_disliked)

# EDIT EXISTING POST PAGE
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Post updated.', 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('newpost.html', title='Update Post', form=form, legend='Edit Post', submit='update post')

# DELETE EXISTING POST PAGE
@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	commentsforpost = Comment.query.filter_by(post_id=post_id).all()
	likes = Like.query.filter_by(post_id=post_id).all()
	dislikes= Dislike.query.filter_by(post_id=post_id).all()
	for comment in commentsforpost:
		db.session.delete(comment)
	for like in likes: db.session.delete(like);
	for dislike in dislikes: db.session.delete(dislike);
	db.session.delete(post)
	db.session.commit()
	flash('Post deleted.', 'success')
	return redirect(url_for('main.home'))


#LIKE POSTS
@posts.route('/post/<int:post_id>/like', methods=['POST', 'GET'])
@login_required
def like_post(post_id):
	returnto = request.args.get('returnto')
	post = Post.query.get_or_404(post_id)
	like = Like.query.filter_by(post_id=post.id, user_id=current_user.id).first()
	dislike = Dislike.query.filter_by(post_id=post.id, user_id=current_user.id).first()
	if like:
		db.session.delete(like)
	else:
		if dislike: db.session.delete(dislike);
		like = Like(post_id=post.id, user_id=current_user.id)
		alert = Alert(assoc_user=post.author, type='like', from_user=current_user.id, post_id=post.id)
		db.session.add(like)
		db.session.add(alert)
	db.session.commit()
	if returnto == 'post':
		return redirect(url_for('posts.post', post_id=request.args.get('returnid')))
	elif returnto == 'userpage':
		return redirect(url_for('users.userpage', username=request.args.get('returnid')))
	elif returnto == 'home':
		return redirect(url_for('main.home'))
	else:
		abort(405)


#DISLIKE POSTS
@posts.route('/post/<int:post_id>/dislike', methods=['POST', 'GET'])
@login_required
def dislike_post(post_id):
	returnto = request.args.get('returnto')
	post = Post.query.get_or_404(post_id)
	like = Like.query.filter_by(post_id=post.id, user_id=current_user.id).first()
	dislike = Dislike.query.filter_by(post_id=post.id, user_id=current_user.id).first()
	if dislike:
		db.session.delete(dislike)
	else:
		if like: db.session.delete(like);
		alert = Alert(assoc_user=post.author, type='dislike', from_user=current_user.id, post_id=post.id)
		dislike = Dislike(post_id=post.id, user_id=current_user.id)
		db.session.add(dislike)
		db.session.add(alert)
	db.session.commit()
	if returnto == 'post':
		return redirect(url_for('posts.post', post_id=request.args.get('returnid')))
	elif returnto == 'userpage':
		return redirect(url_for('users.userpage', username=request.args.get('returnid')))
	elif returnto == 'home':
		return redirect(url_for('main.home'))
	else: abort(405)

@posts.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	if comment.author != current_user:
		abort(403)
	db.session.delete(comment)
	db.session.commit()
	flash('Comment deleted.', 'success')
	return redirect(url_for('posts.post', post_id=request.args.get('returnid')))