import json
import requests

from models import User
from forms import LoginForm
from emails import send_alert
from cameraPi import app, login_manager
from paths import TOGGLE_PIN_PATH, STATUS_PATH, TOGGLE_CAM_PATH, PROCESS_INFO_PATH, TOGGLE_MOTION_PATH

from flask import url_for, render_template, jsonify, request, redirect, abort
from flask.ext.login import current_user, login_required, login_user, logout_user

import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('/var/log/camserv/camserv.log')
formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

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
#    logger.info(current_user.username)
#    return str(current_user.is_authenticated())


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
    try:
        pin_status = get_status()

        supervisor_info = get_process_info()

        for process in supervisor_info:
            if process['name'] == 'cam':
                cam_status = process
            elif process['name'] == 'mjpg':
                mjpg_status = process
            elif process['name'] == 'pir':
                pir_status = process

        if cam_status['state'] > 0 and mjpg_status > 0:
            cam_state = True
        else:
            cam_state = False

        if pir_status['state'] > 0:
            pir_state = True
        else:
            pir_state = False

    except Exception as e:
        logger.exception(e)
        cam_state = False
        pin_status = dict()

        for pin in pins:
            pins[pin]['state'] = 0

    templateData = {
        'cam_state': cam_state,
        'pir_state': pir_state,
        'pins': pin_status
        }

    return render_template('main.html', **templateData)


@app.route("/toggle_pin", methods=['POST'])
@login_required
def toggle_pin():
    pin = request.form['pin']

    try:
        headers = {'api-key': app.api_key}
        r = requests.get(TOGGLE_PIN_PATH + '/{pin}'.format(
            pin=pin),
            headers=headers
        )

        if r.status_code == 200:
            logger.info('Toggled pin {pin}'.format(
                    pin=pin
            ))
            status = json.loads(r.content)
            return jsonify(status)
        else:
            logger.info('Toggling pin {pin} failed.'.format(
                pin=pin
            ))
            return render_template('error.html'), 500

    except Exception as e:
        logger.exception(e)
        return render_template('error.html'), 500


@app.route('/toggle_video')
@login_required
def toggle_video():

    # if not authenticate

    try:
        headers = {'api-key': app.api_key}
        r = requests.get(TOGGLE_CAM_PATH, headers=headers)

        if r.status_code == 200:
            logger.info('Toggled camera')
            return_val = json.loads(r.content)
            return jsonify(return_val)
        else:
            logger.info('Toggling camera failed.')
            return render_template('error.html'), 500

    except Exception as e:
        logger.exception(e)
        return render_template('error.html'), 500


@app.route('/toggle_motion')
@login_required
def toggle_motion():
    try:
        headers = {'api-key': app.api_key}
        r = requests.get(TOGGLE_MOTION_PATH, headers=headers)

        if r.status_code == 200:
            logger.info('turned on motion detection')
            return_val = json.loads(r.content)
            return jsonify(return_val)
        else:
            logger.info('failed attempting to turn on motion detection')
            abort(500)

    except Exception as e:
        logger.exception(e)
        abort(500)


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
        headers = {'api-key': app.api_key}
        r = requests.get(PROCESS_INFO_PATH + '/' + name, headers=headers)
        info = json.loads(r.content)
        if r.status_code == 200:
            return info
        else:
            return False

    except Exception as e:
        logger.exception(e)
        raise


def get_status():
    try:
        headers = {'api-key': app.api_key}
        r = requests.get(STATUS_PATH, headers=headers)
        r.headers['api_key'] = app.api_key
        status = json.loads(r.content)
        if r.status_code == 200:
            return status
        else:
            return False

    except Exception as e:
        logger.exception(e)
        raise
