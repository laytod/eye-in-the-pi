# Server

### About

Flask server that serves an html/js/css front end for interaction with a raspberry pi's GPIO interface.

##### Requirements

##### Python packages
* sqlobject
* flask-login
* flask-wtf

### Database
* mysql

A database needs to be created and the name and user information should be added to the config file.  A script exists in `util/addUser.py` to create a user table and add a user to the table.  This must be done before you will be able to successfully login.

### Configuration

Requires a config file named `camserv.conf` located in the root directory of the repository.  An example config is shown below.

```
[api]
key=<api-key-must-match-clients-key>

[db]
adapter=mysql
user=<database-user>
pw=<database-password>
host=<database-host>
db=<database-name>

[logs]
main=<path-to-a-file-with-write-permissions>
```