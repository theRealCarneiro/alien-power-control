import logging
import threading
from g15pc import g_button
from g15pc.utils import arg_parser
from g15pc.ipc import server, client

LOG = logging.getLogger('generic')


def daemon(_):
    gbloop = threading.Thread(target=g_button.main_loop)
    gbloop.start()
    try:
        server.query_clients()

    except KeyboardInterrupt:
        pass

    finally:
        g_button.stop_event.set()


def tray(_):

    # avoid importing outside so gtk doesnt get included for nothing
    from g15pc.tray import create_indicator
    create_indicator()


ARG_FUNC = {
    'set_power_mode': client.set_power_mode,
    'get_power_mode': client.get_power_mode,
    'get_laptop_model': client.get_laptop_model,
    'get_g_mode': client.get_g_mode,
    'toggle_g_mode': client.toggle_g_mode,
    'daemon': daemon,
    'tray': tray
}


def main():
    args = arg_parser.parse_args()
    for arg, value in vars(args).items():
        if value is None:
            continue

        print(ARG_FUNC[arg](value))

    return 0


if __name__ == '__main__':
    main()
