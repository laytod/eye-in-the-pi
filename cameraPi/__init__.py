import logging
import ConfigParser
from os import path
from sqlobject import *
from flask.ext.login import LoginManager
from logging.handlers import RotatingFileHandler

from flask import Flask
app = Flask(__name__)

# parse the config
config = ConfigParser.ConfigParser()
config_path = path.dirname(path.dirname(path.realpath(__file__))) + '/camserv.conf'
config.read(config_path)

app.api_key = config.get('api', 'key')

# create database connection
sqlhub.processConnection = connectionForURI('{adapter}://{user}:{pw}@{host}/{db}'.format(
	adapter=config.get('db', 'adapter'),
	user=config.get('db', 'user'),
	pw=config.get('db', 'pw'),
	host=config.get('db', 'host'),
	db=config.get('db', 'db')
))

# create LoginManager for Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Sessions variables are stored client side, on the users browser
# the content of the variables is encrypted, so users can't
# actually see it. They could edit it, but again, as the content
# wouldn't be signed with this hash key, it wouldn't be valid
# You need to set a scret key (random text) and keep it secret
app.secret_key = 'super secret key'

# Setup logging
# The logger will write to the same log file until it reaches
# maxBytes, and then will start a new log file and make a backup
# of the full log file.  A total of backupCount backup files
# will be made
app.logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(config.get('logs', 'main'),
 								maxBytes=10000,
 								backupCount=1)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s',
 								datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
app.logger.addHandler(handler)


api_key = config.get('api', 'key')

from cameraPi.views import *


