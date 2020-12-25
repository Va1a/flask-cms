from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
	title = StringField('Post Title', validators=[DataRequired(), Length(min=1, max=72)])
	content = TextAreaField('Post Content', validators=[DataRequired(), Length(min=1, max=10000)])
	submit = SubmitField('post')

class CommentForm(FlaskForm):
	content = TextAreaField('Add a Comment', validators=[DataRequired(), Length(min=1, max=1000)])
	submit = SubmitField('comment')