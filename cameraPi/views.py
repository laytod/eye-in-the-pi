import datetime

from flask import url_for, render_template, jsonify, request, redirect
from cameraPi import app, login_manager, logger

# give alias to logger
# logger = app.logger

from flask.ext.login import current_user, login_required, login_user, logout_user
from forms import LoginForm
from models import User

from emails import send_alert


pins = {}


@login_manager.user_loader
def load_user(userID):
   return User.get(int(userID))

@login_manager.unauthorized_handler
def unauthorized():
   return redirect(url_for('login', next=request.path))

@app.route('/test')
def test():
   logger.info(current_user.username)
   return str(current_user.is_authenticated())

@app.route('/login', methods=['GET', 'POST'])
def login():
   form = LoginForm()

   if form.validate_on_submit():
      login_user(User.selectBy(username=form.user.data).getOne(), remember=form.rememberMe.data)
      logger.info('Logged in {user}'.format(user=current_user.username))
      return redirect(request.args.get('next') or url_for('index'))

   return render_template('login.html', form=form)

@app.route('/logout')
def logout():
   logger.info("Logging out {user}".format(user=current_user.username))
   logout_user()
   return redirect(url_for('index'))

@app.route("/")
@login_required
def index():
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

@app.route('/get_content')
@login_required
def get_content():

   buttonID = request.args.get('id', 'Button ID not found.')

   if buttonID == 'button1':
      templateData = {
         'pins' : pins
      }
      content = render_template('default.html', **templateData)
      f = open('test.out', 'w')
      f.write(content)
      f.close
   elif buttonID == 'button2':
      content = 'You clicked on button 2.  Good for you!'
   elif buttonID == 'button3':
      content = "This is the content area for button 3.  Isn't it spiffy?"
   else:
      content = buttonID

   return jsonify(result=content)


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/changePin")
@login_required
def action():
   action = request.args.get('action', None)
   pin = request.args.get('pin', None)
   pin = int(pin)

   try:
      result = True
   except:
      result = False

   logger.info('Turned pin {pin} {action}'.format(
         pin=pin,
         action=action))
   return jsonify(result=result)


@app.route("/mail")
def send_mail():
   recipients = ['laytod@gmail.com']
   send_alert(recipients)
   return "Sent"




