from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[
		DataRequired(), Length(min=1, max=32),
		Regexp(r'^[a-zA-Z0-9_]*$', message='Usernames can contain only alphanumeric characters and _')
		])
	email = StringField('Email', validators=[
		DataRequired(), Email()
		])
	password = PasswordField('Password', validators=[
		DataRequired()
		])
	confirm_password = PasswordField('Confirm Password', validators=[
		DataRequired(), EqualTo('password')
		])

	submit = SubmitField('create account')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already in use.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already in use.')

class LoginForm(FlaskForm):
	usernameORemail = StringField('Username or Email', validators=[
		DataRequired(), Length(min=1, max=256)
		])
	password = PasswordField('Password', validators=[
		DataRequired()
		])
	remember = BooleanField('Stay logged in?')

	submit = SubmitField('log in')

class UpdateProfileForm(FlaskForm):
	username = StringField('Username', validators=[
		DataRequired(), Length(min=1, max=32),
		Regexp(r'^[a-zA-Z0-9_]*$', message='Usernames can contain only alphanumeric characters and _')])
	email = StringField('Email', validators=[
		DataRequired(), Email()
		])
	biography = TextAreaField('Biography', validators=[Length(min=0, max=75)])

	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

	submit = SubmitField('update profile')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username already in use.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email already in use.')

class UpdatePasswordForm(FlaskForm):
	oldpassword = PasswordField('Current Password', validators=[
		DataRequired()
		])
	newpassword = PasswordField('New Password', validators=[
		DataRequired()])
	confirmnewpassword = PasswordField('Confirm New Password', validators=[
		DataRequired(), EqualTo('newpassword')])

	submit = SubmitField('change password')

class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[
		DataRequired(), Email()])

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('No user exists with this email. Consider creating an account.')

	submit = SubmitField('request password reset')

class ResetPasswordForm(FlaskForm):
	newpassword = PasswordField('New Password', validators=[
		DataRequired()])
	confirmnewpassword = PasswordField('Confirm New Password', validators=[
		DataRequired(), EqualTo('newpassword')])

	submit = SubmitField('reset password')