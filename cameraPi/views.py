import json
import requests

from models import User
from forms import LoginForm
from emails import send_alert
from cameraPi import app, login_manager
from paths import TOGGLE_PIN_PATH, STATUS_PATH, TOGGLE_CAM_PATH, PROCESS_INFO_PATH

from flask import url_for, render_template, jsonify, request, redirect
from flask.ext.login import current_user, login_required, login_user, logout_user

pins = {
    17: {'name': 'green'},
    22: {'name': 'yellow'},
    23: {'name': 'red'}
}


@login_manager.user_loader
def load_user(userID):
    return User.get(int(userID))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login', next=request.path))


# @app.route('/test')
# def test():
#    app.logger.info(current_user.username)
#    return str(current_user.is_authenticated())


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        login_user(User.selectBy(username=form.user.data).getOne(), remember=form.rememberMe.data)
        app.logger.info('Logged in {user}'.format(user=current_user.username))
        return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    app.logger.info("Logging out {user}".format(user=current_user.username))
    logout_user()
    return redirect(url_for('index'))


@app.route("/")
@login_required
def index():
    try:
        pin_status = get_status()

        cam_status = get_process_info('cam')
        mjpg_status = get_process_info('mjpg')

        if cam_status['state'] > 0 and mjpg_status > 0:
            cam_state = True
        else:
            cam_state = False

    except Exception as e:
        app.logger.exception(e)
        cam_state = False
        pin_status = dict()

        for pin in pins:
            pins[pin]['state'] = 0

    templateData = {
        'cam_state': cam_state,
        'pins': pin_status
        }

    return render_template('main.html', **templateData)


@app.route("/toggle_pin", methods=['POST'])
@login_required
def toggle_pin():
    pin = request.form['pin']

    try:
        r = requests.get(TOGGLE_PIN_PATH + '/{pin}'.format(
            pin=pin
        ))
        r.headers['api_key'] = app.api_key

        if r.status_code == 200:
            app.logger.info('Toggled pin {pin}'.format(
                    pin=pin
            ))
            status = json.loads(r.content)
            return jsonify(status)
        else:
            app.logger.info('Toggling pin {pin} failed.'.format(
                pin=pin
            ))
            return render_template('error.html'), 500

    except Exception as e:
        app.logger.exception(e)
        return render_template('error.html'), 500


@app.route('/toggle_video')
@login_required
def toggle_video():

    # if not authenticate

    try:
        r = requests.get(TOGGLE_CAM_PATH)
        r.headers['api_key'] = app.api_key

        if r.status_code == 200:
            app.logger.info('Toggled camera')
            return_val = json.loads(r.content)
            app.logger.info(return_val)
            app.logger.info('--')
            return jsonify(return_val)
        else:
            app.logger.info('Toggling camera failed.')
            return render_template('error.html'), 500

    except Exception as e:
        app.logger.exception(e)
        return render_template('error.html'), 500


@app.route("/mail")
def send_mail():
    recipients = ['laytod@gmail.com']
    send_alert(recipients)
    return "Sent"


def get_cam_status():
    process_info = get_process_info()
    return process_info


def get_process_info(name='all'):
    try:
        r = requests.get(PROCESS_INFO_PATH + '/' + name)
        r.headers['api_key'] = app.api_key
        info = json.loads(r.content)
        if r.status_code == 200:
            return info
        else:
            return False

    except Exception as e:
        app.logger.exception(e)
        raise


def get_status():
    try:
        r = requests.get(STATUS_PATH)
        r.headers['api_key'] = app.api_key
        status = json.loads(r.content)
        if r.status_code == 200:
            return status
        else:
            return False

    except Exception as e:
        app.logger.exception(e)
        raise
