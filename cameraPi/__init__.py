# from sqlobject import *
# from flask.ext.login import LoginManager


from flask import Flask
app = Flask(__name__)

# create database connection
# sqlhub.processConnection = connectionForURI('mysql://root:root@localhost/flask')

# create LoginManager for Flask-Login
# login_manager = LoginManager()
# login_manager.init_app(app)

# Sessions variables are stored client side, on the users browser
# the content of the variables is encrypted, so users can't
# actually see it. They could edit it, but again, as the content
# wouldn't be signed with this hash key, it wouldn't be valid
# You need to set a scret key (random text) and keep it secret
# app.secret_key = 'super secret key'


import cameraPi.views