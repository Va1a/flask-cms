from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class SearchForm(FlaskForm):
	query = StringField('Query', validators=[DataRequired(), Length(min=1, max=128)])
	submit = SubmitField('search')

class AssignBadgeForm(FlaskForm):
	user = StringField('Username', validators=[DataRequired(), Length(min=1, max=32)])
	badge_name = StringField('Badge Title', validators=[DataRequired(), Length(min=1, max=32)])
	badge_html = StringField('Badge Icon', validators=[DataRequired(), Length(min=1, max=56)])
	submit = SubmitField('assign')

class RevokeBadgeForm(FlaskForm):
	user = StringField('Username', validators=[DataRequired(), Length(min=1, max=32)])
	badge_name = StringField('Badge Title', validators=[DataRequired(), Length(min=1, max=32)])
	submit = SubmitField('revoke')

class PermissionsForm(FlaskForm):
	user = StringField('Username', validators=[DataRequired(), Length(min=1, max=32)])
	level = SelectField('Permission Level', choices=[('-1', '-1 - Locked Account, User blocked from logins [Locked].'), ('0', '0 - Default, User can manage own posts & comment, view profile, etc [Default].'),
	 ('1', '1 - User can flag posts, etc [Trusted].'), ('2', '2 - User can create and manage own Guilds [Guilder].'), ('3', '3 - User is Moderator (can delete posts, comments, lock accounts, and assign/revoke badges) [Moderator].'),
	 ('4', '4 - User has less than or equal to permission setting authority [Sr. Moderator].'), ('5', '5 - User has Administration privileges and access to all management features [Administrator].')])

class ChangeEmailForm(FlaskForm):
	user = StringField('User\'s Current Email or Username', validators=[DataRequired(), Length(min=1, max=256)])
	new_email = StringField('New Email', validators=[DataRequired(), Length(min=1, max=256), Email()])
	submit = SubmitField('Change Email')