import os, re
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

# FUNCTION FOR SAVING PROFILE PICTURES
def savepic(form_pic, userid, oldfile):
	randomHex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_pic.filename)
	picture_fn = randomHex + '-' + str(userid) + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
	output_size = (125, 125)
	i = Image.open(form_pic)
	i.thumbnail(output_size)
	i.save(picture_path)
	if oldfile != 'default.jpeg':
		rmpath = os.path.join(current_app.root_path, 'static/profile_pics', oldfile)
		os.remove(rmpath)
	return picture_fn

# FUNCTION TO SEND RESET PASSWORD EMAIL
def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Reset Password Request for irony.club', sender='reset@irony.club', recipients=[user.email])
	msg.body = f'''
To reset your password, visit {url_for('users.resetPassword', token=token, _external=True)}

If you did not request a password reset then simply ignore this email and no changes will be made.
'''
	mail.send(msg)

# Ensures a user has the permissions to log in.
def verifyPerms(user):
	if user.permission_level >= 0:
		return True
	else:
		return False