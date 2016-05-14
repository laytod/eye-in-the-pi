from copy import deepcopy

from cameraPi import app
from remote_call_utils import get_task_status, get_pin_status, remote_call

from flask import render_template, jsonify, request
from flask.ext.login import login_required

# need to import this or logins break
from login import load_user

import logging
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


@app.route("/")
@login_required
def index():
    try:
        task_status = get_task_status()

        cam_state = task_status['cam_state']
        pin_status = get_pin_status()
        pir_state = task_status['pir_state']

    except Exception as e:
        logger.info('Getting status failed')
        logger.exception(e)
        cam_state = False
        pin_status = dict()
        pir_state = dict()

        for pin in pins:
            pin_status[pin] = deepcopy(pins[pin])
            pin_status[pin].update({'state': 0})

    templateData = {
        'cam_state': cam_state,
        'pir_state': pir_state,
        'pins': pin_status
    }

    return render_template('main.html', **templateData)


@app.route("/toggle_pin", methods=['POST'])
@login_required
def toggle_pin():
    try:
        pin = request.form['pin']
        status = remote_call('pin', 'toggle')
        logger.info('Toggled pin {pin}'.format(
            pin=pin
        ))
        return jsonify(status)

    except Exception as e:
        logger.info('Toggling pin {pin} failed.'.format(
            pin=pin
        ))
        logger.exception(e)
        return render_template('error.html'), 500


@app.route('/toggle_video')
@login_required
def toggle_video():
    try:
        status = remote_call('cam', 'toggle')
        logger.info('Toggled camera')
        return jsonify(status)

    except Exception as e:
        logger.info('Toggling camera failed.')
        logger.exception(e)
        return render_template('error.html'), 500


@app.route('/toggle_motion')
@login_required
def toggle_motion():
    try:
        status = remote_call('pir', 'toggle')
        logger.info('turned on motion detection')
        return jsonify(status)

    except Exception as e:
        logger.info('failed attempting to turn on motion detection')
        logger.exception(e)
        return render_template('error.html'), 500


# @app.route("/mail")
# def send_mail():
#     recipients = ['laytod@gmail.com']
#     send_alert(recipients)
#     return "Sent"
