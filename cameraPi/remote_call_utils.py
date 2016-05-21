import json
import requests

from cameraPi import app
from exceptions import RemoteCallFailed
from paths import TOGGLE_PIN_PATH, STATUS_PATH, TOGGLE_CAM_PATH, TOGGLE_MOTION_PATH

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


def remote_call(sensor_type='pin', action='status', pin_id=None):
    """ Valid argument values:
        sensor_type  ['pins', 'tasks']
        action       ['pin', 'cam', 'pir']
    """
    if action == 'toggle':
        if sensor_type == 'pin':
            if not pin_id:
                raise RemoteCallFailed('No pin_id given')

            path = TOGGLE_PIN_PATH + str(pin_id)
        elif sensor_type == 'cam':
            path = TOGGLE_CAM_PATH
        else:
            # sensor_type == 'pir'
            path = TOGGLE_MOTION_PATH
    else:
        path = STATUS_PATH

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
