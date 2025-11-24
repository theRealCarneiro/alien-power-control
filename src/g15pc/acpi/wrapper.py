import logging
from g15pc.acpi.shell import Shell
from g15pc.acpi import calls

SHELL = Shell()
LOG = logging.getLogger('generic')


def create_shell():
    LOG.debug('Creating shell...')
    SHELL.create_shell()
    LOG.debug('Shell created')

    LOG.debug('Checking laptop model...')
    if check_laptop_model() is False:
        LOG.critical('System is not a Dell G15')
        raise RuntimeError('System is not a Dell G15')

    LOG.debug('Laptop model is G15 %d', calls.LAPTOP_MODEL)


def set_power_mode(power_mode) -> str:
    if calls.PowerModes.exists(power_mode):
        return SHELL.exec(calls.set_power_mode(power_mode), parse=True)

    return 'None'


def get_power_mode(_) -> str:
    power_mode_id = SHELL.exec(calls.get_power_mode(), parse=True)
    power_mode = calls.PowerModes(power_mode_id).name
    # power_mode = calls.REVERSE_POWER_MODES[reverse_power_mode]
    return power_mode


def get_laptop_model(_) -> str:
    return SHELL.exec(calls.get_laptop_model(), parse=True)


def get_g_mode(_) -> str:
    power_mode = SHELL.exec(calls.get_g_mode(), parse=True)
    return str(not power_mode == '0x0')


def toggle_g_mode(_) -> str:
    res = SHELL.exec(calls.toggle_g_mode(), parse=True)
    power_mode = 'G_Mode' if res == '0x1' else 'USTT_Balanced'
    SHELL.exec(calls.set_power_mode(power_mode))
    return power_mode


def check_laptop_model():
    is_g15 = False
    for calls.LAPTOP_MODEL in [5520, 5525]:
        if SHELL.exec(calls.get_laptop_model(), parse=True, silent=True) == "0x12c0":
            is_g15 = True
            # if patch:
            # patch(self)
            break

    return is_g15


def get_gpu_temp():
    res = SHELL.exec(calls.get_gpu_temp(), parse=True)
    return res


def get_cpu_temp():
    res = SHELL.exec(calls.get_cpu_temp(), parse=True)
    return res


def set_fan1_boost(speed):
    if 255 < speed < 0:
        LOG.error('Invalid Speed %d', speed)
        return
    res = SHELL.exec(calls.set_fan1_boost(speed), parse=True)
    return res


def set_fan2_boost(speed):
    if 255 < speed < 0:
        LOG.error('Invalid Speed %d', speed)
        return
    res = SHELL.exec(calls.set_fan2_boost(speed), parse=True)
    return res


def get_fan1_boost():
    res = SHELL.exec(calls.get_fan1_boost(), parse=True)
    return res


def get_fan2_boost():
    res = SHELL.exec(calls.get_fan2_boost(), parse=True)
    return res


def get_fan1_rpm():
    res = SHELL.exec(calls.get_fan1_rpm(), parse=True)
    return res


def get_fan2_rpm():
    res = SHELL.exec(calls.get_fan2_rpm(), parse=True)
    return res


MESSAGE_TYPES = {
    'set_power_mode': set_power_mode,
    'get_power_mode': get_power_mode,
    'get_laptop_model': get_laptop_model,
    'set_fan1_boost': get_fan1_boost,
    'get_fan1_boost': get_fan1_boost,
    'get_fan1_rpm': get_fan1_boost,
    'set_fan2_boost': get_fan2_boost,
    'get_fan2_boost': get_fan2_boost,
    'get_fan2_rpm': get_fan2_boost,
    'get_cpu_temp': get_cpu_temp,
    'get_gpu_temp': get_gpu_temp,
    'toggle_G_mode': toggle_g_mode,
    'get_G_mode': get_g_mode
}


if __name__ == '__main__':
    # create_shell()
    # print(int(get_cpu_temp(), 16))
    # print(int(get_gpu_temp(), 16))
