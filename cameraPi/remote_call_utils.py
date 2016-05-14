import json
import requests

from cameraPi import app
from exceptions import RemoteCallFailed
from paths import TOGGLE_PIN_PATH, STATUS_PATH, TOGGLE_CAM_PATH, PROCESS_INFO_PATH, TOGGLE_MOTION_PATH

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


def get_pin_status():
    return remote_call('pins', 'status')


def get_task_status():
    task_status = remote_call('tasks', 'status')

    for task in task_status:
        if task['name'] == 'cam':
            cam_status = task
        elif task['name'] == 'mjpg':
            mjpg_status = task
        elif task['name'] == 'pir':
            pir_status = task

    if cam_status['state'] > 0 and mjpg_status > 0:
        cam_state = True
    else:
        cam_state = False

    if pir_status['state'] > 0:
        pir_state = True
    else:
        pir_state = False

    return {
        'cam_state': cam_state,
        'pir_state': pir_state,
    }


def remote_call(sensor_type='status', action='pin'):
    """ Valid argument values:
        sensor_type  ['pins', 'tasks']
        action       ['pin', 'cam', 'pir']
    """
    if action == 'status':
        if sensor_type == 'pins':
            path = STATUS_PATH
        else:
            # sensor_type == 'tasks'
            path = PROCESS_INFO_PATH
    else:
        if sensor_type == 'pin':
            path = TOGGLE_PIN_PATH
        elif sensor_type == 'cam':
            path = TOGGLE_CAM_PATH
        else:
            # sensor_type == 'pir'
            path = TOGGLE_MOTION_PATH

    try:
        headers = {'api-key': app.api_key}
        r = requests.get(path, headers=headers)
        if r.status_code == 200:
            return json.loads(r.content)
        else:
            raise RemoteCallFailed('Sensor unavailable.')
    except Exception:
        logger.info('Error when connecting to the sensor.')
        raise
