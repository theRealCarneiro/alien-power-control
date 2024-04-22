import logging
import sys
import pexpect

LOG = logging.getLogger('generic')


class Shell:

    def __init__(self):
        self.shell = None
        self.is_plugdev = None
        self.is_root = None

    def create_shell(self):

        # Create a shell subprocess
        self.shell = pexpect.spawn(
            'bash',
            encoding='utf-8',
            logfile=None,
            env=None,
            args=['--noprofile', '--norc']
        )

        self.shell.expect('[#$] ')
        self.exec(' export HISTFILE=/dev/null; history -c', silent=True)

        self.is_root = self.exec('whoami', silent=True)[1].find('root') != -1
        if self.is_root is True:
            LOG.debug('User is root')
            return

        # Check if user is member of plugdev
        self.is_plugdev = self.exec('groups')[1].find('plugdev') != -1
        if self.is_plugdev:
            LOG.debug('User is member of group of plugdev.')
        else:
            LOG.error('User is not a member of group plugdev')

        self.elevate_shell()

    def elevate_shell(self):
        LOG.debug('Attempting to create elevated bash subprocess...')

        # Elevate privileges (pkexec is needed)
        self.exec('pkexec bash --noprofile --norc')
        self.exec(' export HISTFILE=/dev/null; history -c')

        # Check if is root
        self.is_root = self.exec('whoami')[1].find('root') != -1
        if not self.is_root:
            LOG.critical('Shell is NOT root. Exiting...')
            sys.exit(1)

        LOG.debug('Shell is now root. ACPI methods now enabled')

    def exec(self, cmd: str, parse=False, silent=False):
        if silent is False:
            LOG.info('Executing: %s', cmd)
        self.shell.sendline(cmd)
        self.shell.expect('[#$] ')
        result = self.shell.before.split('\n')
        if parse:
            result = self.parse_shell_exec(result[1])

        return result

    def parse_shell_exec(self, line: str):
        return line[line.find('\r')+1:line.find('\x00')]
