from sqlobject import *
from werkzeug.security import generate_password_hash, check_password_hash

class User(SQLObject):
	username = StringCol()
	pwHash = StringCol()

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True

	def get_id(self):
		return self.id

	def set_password(self, password):
		self.pwHash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwHash, password)
