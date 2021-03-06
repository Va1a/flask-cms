# flask-cms
fork of @CoreyMSchafer 's flaskblog with added functionality (comments, likes, alerts, new theme, etc.)

# _how to run locally for development/modification_ #
0. clone the repository
1. set the following environment variables:
```ini
    flask-mail-user = (your gmail username) [or random gibberish if you do not want to use mail features, reset password will not work in this case]
    flask-mail-password = (gmail app specific password) [or random gibberish if you do not want to use mail features, reset password will not work in this case]
    flask-sqlalchemy-database-uri = sqlite:///site.db [or your custom database uri]
    flask-secret-key = (generate your own random secret key and put it here) [you can easily make one with os.urandom(24).hex()]
```
2. navigate to the root project directory (with run.py in it)
3. install requirements from the requirements.txt file `pip install -r requirements.txt`
3. ensure that an empty database is available at your database uri location. (if using default, simply create a file called "site.db" in the project directory)
4. open the python interpreter in the location from step 2.
5. run:
```py
   >>> from flaskblog import create_app, db
   >>> app = create_app()
   >>> ctx = app.app_context()
   >>> ctx.push()
   >>> db.create_all()
   >>> ctx.pop()
   >>> exit()
```
7. Finally, run `run.py`
