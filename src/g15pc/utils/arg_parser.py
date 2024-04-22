import logging
import argparse
from g15pc.acpi import calls

LOG = logging.getLogger('generic')


def parse_args():
    LOG.debug('Parsing args...')
    parser = argparse.ArgumentParser(description='Dell G15 5525 Power Controller')
    group = parser.add_mutually_exclusive_group()

    power_modes = [i.name for i in calls.PowerModes]

    group.add_argument(
        '-s',
        '--set-power-mode',
        default=None,
        choices=power_modes,
        type=str.upper,
        help=f'Set the active powermode, available modes are: {power_modes}',
        metavar=''
    )

    group.add_argument(
        '-g',
        '--get-power-mode',
        default=None,
        action='store_true',
        help='Returns the active powermode'
    )

    group.add_argument(
        '-l',
        '--get-laptop-model',
        default=None,
        action='store_true',
        help='Returns laptop model'
    )

    group.add_argument(
        '-gg',
        '--get-g-mode',
        default=None,
        action='store_true',
        help='Returns gameshift state'
    )

    group.add_argument(
        '-t',
        '--toggle-g-mode',
        default=None,
        action='store_true',
        help='Toggles gameshift'
    )

    group.add_argument(
        '-d',
        '--daemon',
        default=None,
        action='store_true',
        help='Starts daemon'
    )

    group.add_argument(
        '--tray',
        action='store_true',
        default=None,
        help='Starts tray application'
    )

    return parser.parse_args()
