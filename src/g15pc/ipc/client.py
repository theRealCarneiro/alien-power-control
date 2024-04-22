import sys
import socket
import logging
from g15pc import settings
from . import common

LOG = logging.getLogger('generic')


def send_request(msg: str) -> str:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as conn:
        try:
            conn.connect(settings.SOCKET_PATH)
        except ConnectionRefusedError:
            LOG.critical('Daemon not running')
            sys.exit(1)

        common.send_message(conn, msg)
        res = common.get_message(conn)
        return res


def set_power_mode(power_mode):
    return send_request(f'set_power_mode {power_mode}')


def get_power_mode(_):
    powermode = send_request('get_power_mode')
    return powermode


def get_laptop_model(_):
    return send_request('get_laptop_model')


def get_g_mode(_):
    status = send_request('get_G_mode')
    return status == 'True'


def toggle_g_mode(_):
    return send_request('toggle_G_mode')


MESSAGE_TYPES = {
    'set_power_mode': set_power_mode,
    'get_power_mode': get_power_mode,
    'toggle_G_mode': toggle_g_mode,
    'get_G_mode': get_g_mode
}
