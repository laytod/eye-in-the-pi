#!/home/laytod/.virtualenvs/hogtrap/bin/python
import sys
from sqlobject import *
from werkzeug.security import generate_password_hash, check_password_hash


class User(SQLObject):
	username = StringCol()
	pwHash = StringCol()


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print "usage: ./addUser <username> <pw>"
		print '...is the virtualenv enabled?'
		sys.exit(2)

	try:
		sqlhub.processConnection = connectionForURI('mysql://root:root@localhost/flask')
		name = sys.argv[1]
		password = sys.argv[2]
		
		pwHash = generate_password_hash(password)
		User(username=name, pwHash=pwHash)

		print "User '{name}' successfully created.".format(name=name)

	except Exception as e:
		print "Error adding user '{name}': {e}".format(name=name, e=e)
		sys.exit(2)
