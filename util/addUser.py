#!/usr/bin/python
import sys
from os import path
import ConfigParser
from sqlobject import *
from werkzeug.security import generate_password_hash, check_password_hash


# parse the config
config = ConfigParser.ConfigParser()
config_path = path.dirname(path.dirname(path.realpath(__file__))) + '/camserv.conf'
config.read(config_path)


class User(SQLObject):
    username = StringCol()
    pwHash = StringCol()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "usage: ./addUser <username> <pw>"
        print '...is the virtualenv enabled?'
        sys.exit(2)

    try:
        name = sys.argv[1]
        password = sys.argv[2]
        sqlhub.processConnection = connectionForURI('{adapter}://{user}:{pw}@{host}/{db}'.format(
            adapter=config.get('db', 'adapter'),
            user=config.get('db', 'user'),
            pw=config.get('db', 'pw'),
            host=config.get('db', 'host'),
            db=config.get('db', 'db')
        ))

        pwHash = generate_password_hash(password)

        if not User.tableExists():
            User.createTable()

        User(username=name, pwHash=pwHash)

        print "User '{name}' successfully created.".format(name=name)

    except Exception as e:
        print "Error adding user '{name}': {e}".format(name=name, e=e)
        raise
