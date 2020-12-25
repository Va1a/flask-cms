import os


class Config:
	SECRET_KEY = os.environ.get('flask-secret-key')
	SQLALCHEMY_DATABASE_URI = os.environ.get('flask-sqlalchemy-database-uri')
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('flask-mail-user')
	MAIL_PASSWORD = os.environ.get('flask-mail-password')