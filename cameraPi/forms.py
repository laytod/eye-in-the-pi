from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SubmitField, validators, ValidationError, PasswordField
from models import User

class LoginForm(Form):
	user = TextField("Username", [validators.Required("Please enter your username.")])
	password = PasswordField('Password', [validators.Required("Please enter your password.")])
	rememberMe = BooleanField('Remember Me')
	submit = SubmitField("Sign In")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		users = User.selectBy(username = self.user.data)
		if users.count() > 0 and users.getOne().check_password(self.password.data):
			return True
		else:
			self.user.errors.append("Invalid username or password.")
			return False