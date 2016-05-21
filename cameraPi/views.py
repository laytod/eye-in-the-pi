from cameraPi import app
from remote_call_utils import remote_call

from flask import render_template, jsonify, request
from flask.ext.login import login_required

# need to import this or logins break
from login import load_user

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(app.log_path)
formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)


@app.route("/")
@login_required
def index():
    templateData = {
        'cam_state': False,
        'pir_state': False,
        'pins': dict(),
    }

    try:
        all_statuses = remote_call(action='status')

        for status in all_statuses['results']:
            if status['type'] == 'cam':
                templateData['cam_state'] = status['state']
            elif status['type'] == 'pir':
                templateData['pir_state'] = status['state']
            elif status['type'] == 'pin':
                pin_id = status['data']['pin_id']
                pin_name = status['data']['name']
                pin_state = status['state']
                templateData['pins'][pin_id] = {
                    'name': pin_name,
                    'state': pin_state,
                }

    except Exception as e:
        logger.info('Getting status failed')
        logger.exception(e)

    return render_template('main.html', **templateData)


@app.route("/toggle_pin", methods=['POST'])
@login_required
def toggle_pin():
    try:
        pin = request.form['pin']
        status = remote_call('pin', 'toggle', pin_id=pin)
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
