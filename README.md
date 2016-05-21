# Server

## About

Flask server that serves an html/js/css front end for interaction with a raspberry pi's GPIO interface.

## Requirements

### Python packages
sqlobject
flask-login
flask-wtf

### Applications
mysql


## Configuration

Requires a config file named `camserv.conf` located in the root folder of the repository.  An example config is shown below.

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
main=/var/log/camserv/camserv.log
```