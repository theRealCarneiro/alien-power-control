import os
import grp
import socket
import logging
from g15pc.acpi import wrapper
from g15pc import settings
from . import common

LOG = logging.getLogger('generic')
EXIT_FLAG = False


def query_clients() -> None:
    wrapper.create_shell()
    unlink_socket()
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        init_socket(sock)
        while not EXIT_FLAG:
            try:
                handle_connection(sock)
            except socket.timeout:
                if EXIT_FLAG:
                    break


def init_socket(sock):
    sock.settimeout(settings.LISTENER_TIMEOUT)
    sock.bind(settings.SOCKET_PATH)
    plugdevgid = grp.getgrnam('plugdev').gr_gid
    os.chmod(settings.SOCKET_PATH, 0o660)
    os.chown(settings.SOCKET_PATH, os.getuid(), plugdevgid)
    sock.listen()


def handle_connection(sock):
    conn, _ = sock.accept()
    LOG.debug('new client')
    msg = common.get_message(conn)
    LOG.info('Request: %s', msg)

    split_msg = msg.split(' ')
    message_type = split_msg[0]

    command = wrapper.MESSAGE_TYPES.get(message_type)
    if command is None:
        common.send_message(conn, f'ERROR: command not found: {message_type}')
        LOG.error('ERROR: command not found: %s', message_type)
        return

    args = None if len(split_msg) == 1 else split_msg[1]
    ret = command(args)
    LOG.info('Response: %s', ret)
    common.send_message(conn, ret)


def unlink_socket():
    try:
        os.unlink(settings.SOCKET_PATH)
    except OSError:
        if os.path.exists(settings.SOCKET_PATH):
            raise
