from flask import render_template, send_from_directory, request, Blueprint, abort, flash, redirect, url_for
from flaskblog.models import User, Post, Like, Dislike, Badge, has_user_liked, has_user_disliked
from flask_login import current_user
from flaskblog.main.forms import SearchForm, AssignBadgeForm, RevokeBadgeForm, PermissionsForm, ChangeEmailForm
from flaskblog import db

main = Blueprint('main', __name__)

# HOME PAGE
@main.route('/')
def home():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('home.html', posts=posts, has_user_liked=has_user_liked, has_user_disliked=has_user_disliked)

# ABOUT PAGE
@main.route('/about')
def about():
	return render_template('about.html', title='about')

@main.route('/robots.txt')
def robots():
	return send_from_directory('static', 'robots.txt')

@main.route('/search', methods=['GET', 'POST'])
def search():
	page = request.args.get('page', 1, type=int)
	form = SearchForm()
	view = request.args.get('view', 'posts', type=str)
	argSearch = request.args.get('query', '', type=str)
	if form.validate_on_submit() or argSearch:
		if not form.query.data: form.query.data = argSearch
		current_user.last_search = form.query.data
		db.session.commit()
		if argSearch != form.query.data:
			return redirect(url_for('main.search', view=view, query=form.query.data))
		if view == 'posts':
			result_posts = Post.query.filter(Post.title.like('%' + form.query.data + '%')).paginate(page=page, per_page=5)
			return render_template('search.html', title='search', form=form, legend='Search', view=view, search=True, posts=result_posts, query=argSearch, has_user_liked=has_user_liked, has_user_disliked=has_user_disliked)
		elif view == 'users':
			result_users = User.query.filter(User.username.like('%' + form.query.data + '%')).paginate(page=page, per_page=5)
			return render_template('search.html', title='search', form=form, legend='Search', view=view, search=True, users=result_users, query=argSearch)
	else:
		if request.method == 'GET' and current_user.is_authenticated:
			form.query.data = request.args.get('query', '', type=str)
		if view == 'posts':
			posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
			return render_template('search.html', title='search', form=form, legend='Search', view=view, posts=posts, query=argSearch, has_user_liked=has_user_liked, has_user_disliked=has_user_disliked)
		elif view == 'users':
			users = User.query.order_by(User.date_joined.desc()).paginate(page=page, per_page=5)
			return render_template('search.html', title='search', form=form, legend='Search', view=view, users=users, query=argSearch)

@main.route('/store')
def store():
	return render_template('store.html')

@main.route('/manage', methods=['GET', 'POST'])
def admin():
	if not current_user.is_authenticated or current_user.permission_level < 3:
		abort(404)
	badgeform = AssignBadgeForm()
	revokebadgeform = RevokeBadgeForm()
	permform = PermissionsForm()
	emailform = ChangeEmailForm()

	isAdmin = False
	if current_user.permission_level == 5: isAdmin = True;

	page = request.args.get('page', 1, type=int)
	users = User.query.order_by(User.date_joined.desc()).paginate(page=page, per_page=20)

	if badgeform.validate_on_submit():
		user = User.query.filter_by(username=badgeform.user.data).first()
		if user:
			badge = Badge(user_id=user.id, name=badgeform.badge_name.data, html=badgeform.badge_html.data)
			db.session.add(badge)
			db.session.commit()
			flash(f'Succesfully assigned "{badgeform.badge_name.data}" badge to user "{badgeform.user.data}".', 'success')
		else:
			flash(f'Could not find user "{badgeform.user.data}".', 'danger')
		return redirect(url_for('main.admin'))

	elif revokebadgeform.validate_on_submit():
		user = User.query.filter_by(username=revokebadgeform.user.data).first()
		if user: badge = Badge.query.filter_by(user_id=user.id, name=revokebadgeform.badge_name.data).first();
		if user and badge:
			db.session.delete(badge)
			db.session.commit()
			flash(f'Succesfully revoked "{revokebadgeform.badge_name.data}" badge from user "{revokebadgeform.user.data}".', 'success')
		else:
			flash(f'Could not find user "{revokebadgeform.user.data}" with badge "{revokebadgeform.badge_name.data}".', 'danger')
		return redirect(url_for('main.admin'))

	elif permform.validate_on_submit():
		user = User.query.filter_by(username=permform.user.data).first()
		formlevel = int(permform.level.data)
		if user and user != current_user:
			if isAdmin == False and formlevel >= current_user.permission_level:
				flash('You cannot set other\'s permission levels to values greater than or equal to your own.', 'danger')
			else:
				user.permission_level = formlevel
				db.session.commit()
				flash(f'Succesfully set "{permform.user.data}"\'s permission level to {formlevel}.', 'success')
		elif user == current_user: flash('You cannot manage your own permissions.', 'danger');
		else:
			flash(f'Could not find user "{permform.user.data}".', 'danger')
		return redirect(url_for('main.admin'))

	elif emailform.validate_on_submit():
		user = User.query.filter_by(email=emailform.user.data).first()
		if not user: user = User.query.filter_by(username=emailform.user.data).first();
		if user:
			if user.id == current_user.id:
				flash(f'To change your own email, please visit the profile page.', 'danger')
			elif user.permission_level >= current_user.permission_level and isAdmin == False:
				flash(f'You cannot change the email of a user with a permission level greater than or equal to yours.', 'danger')
			else:
				user.email = emailform.new_email.data
				db.session.commit()
				flash(f'Changed email for user "{emailform.user.data}".', 'success')
		else:
			flash(f'Could not find user with email/username "{emailform.user.data}".', 'danger')
		return redirect(url_for('main.admin'))
	
	return render_template('admin.html', title='admin', users=users, badgeform=badgeform, revokebadgeform=revokebadgeform, permform=permform, emailform=emailform)