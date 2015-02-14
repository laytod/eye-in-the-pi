import json
import requests
import datetime

from models import User
from forms import LoginForm
from emails import send_alert
from cameraPi import app, login_manager, logger
from cameraPi.paths import TOGGLE_PATH, STATUS_PATH

from flask import url_for, render_template, jsonify, request, redirect
from flask.ext.login import current_user, login_required, login_user, logout_user



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
   status = get_status()

   templateData = {
      'pins' : status
      }

   return render_template('main.html', **templateData)


@app.route("/toggle_pin", methods=['POST'])
@login_required
def toggle_pin():
   pin = request.form['pin']

   try:
      r = requests.get(TOGGLE_PATH + '/{pin}'.format(
         pin=pin
      ))

      status = json.loads(r.content)

      if r.status_code == 200:
         logger.info('Toggled pin {pin}'.format(
               pin=pin
         ))
      else:
         logger.info('Toggling pin {pin} failed.'.format(
            pin=pin
         ))

      return jsonify(status)

   except Exception as e:
      logger.exception(e)
      return jsonify(dict(response=False))


@app.route("/mail")
def send_mail():
   recipients = ['laytod@gmail.com']
   send_alert(recipients)
   return "Sent"




def get_status():
   try:
      r = requests.get(STATUS_PATH)
      status = json.loads(r.content)
      if r.status_code == 200:
         return status
      else:
         return False

   except Exception as e:
      logger.exception(e)
      raise