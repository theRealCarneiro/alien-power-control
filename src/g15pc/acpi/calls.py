from enum import Enum

# Wrapper changes this in wrapper.check_laptop_model
LAPTOP_MODEL = 5525


class PowerEnum(Enum):

    @property
    def hex(self) -> str:
        return hex(self.value)

    @classmethod
    def _missing_(cls, value):
        try:

            # if an int is here, means value does not exist
            if isinstance(value, int):
                raise ValueError

            # check if value exists
            if value.upper() in cls.__members__:
                return cls[value.upper()]

            # check if hex value exist
            return cls(int(value, 16))

        except (KeyError, ValueError) as ex:
            raise ValueError(f"No such power mode: {value}") from ex

    @classmethod
    def exists(cls, value):
        try:
            cls(value)
        except ValueError:
            return False

        return True


class PowerModes(PowerEnum):
    MANUAL            =  0x0   # noqa: E222 E221
    USTT_BALANCED     =  0xa0  # noqa: E222 E221
    USTT_PERFORMANCE  =  0xa1  # noqa: E222 E221
    # USTT_COOL       =  0xa2  # noqa: E222 E221  # Does not work
    USTT_QUIET        =  0xa3  # noqa: E222 E221
    USTT_FULLSPEED    =  0xa4  # noqa: E222 E221
    USTT_BATTERYSAVER =  0xa5  # noqa: E222 E221
    G_MODE            =  0xab  # noqa: E222 E221


class CallTypes(PowerEnum):
    GET_LAPTOP_MODEL  =  ['0x1a', '0x02', '0x02']   # noqa: E222 E221
    GET_POWER_MODE    =  ['0x14', '0x0b', '0x00']   # noqa: E222 E221
    SET_POWER_MODE    =  ['0x15', '0x01']           # noqa: E222 E221  # Param
    TOGGLE_G_MODE     =  ['0x25', '0x01']           # noqa: E222 E221
    GET_G_MODE        =  ['0x25', '0x02']           # noqa: E222 E221
    SET_FAN1_BOOST    =  ['0x15', '0x02', '0x32']   # noqa: E222 E221  # Param
    GET_FAN1_BOOST    =  ['0x14', '0x0c', '0x32']   # noqa: E222 E221
    GET_FAN1_RPM      =  ['0x14', '0x05', '0x32']   # noqa: E222 E221
    GET_CPU_TEMP      =  ['0x14', '0x04', '0x01']   # noqa: E222 E221
    SET_FAN2_BOOST    =  ['0x15', '0x02', '0x33']   # noqa: E222 E221  # Param
    GET_FAN2_BOOST    =  ['0x14', '0x0c', '0x33']   # noqa: E222 E221
    GET_FAN2_RPM      =  ['0x14', '0x05', '0x33']   # noqa: E222 E221
    GET_GPU_TEMP      =  ['0x14', '0x04', '0x06']   # noqa: E222 E221


ACPI_COMMAND = 'echo "\\_SB.{}.WMAX 0 {} {{{}, {}, {}, 0x00}}" > /proc/acpi/call; cat /proc/acpi/call'

DEVICES = {5520: 'AMWW', 5525: 'AMW3'}

UNAVAILABLE_MODES = {
    5520: [],
    5525: [],
}

# COMMANDS = {
#     5520: ('echo "\\_SB.AMWW.WMAX 0 {} {{{}, {}, {}, 0x00}}" > /proc/acpi/call; cat /proc/acpi/call'),
#     5525: ('echo "\\_SB.AMW3.WMAX 0 {} {{{}, {}, {}, 0x00}}" > /proc/acpi/call; cat /proc/acpi/call'),
# }


def get_acpi_command(acpi_cmd=None):
    return DEVICES[LAPTOP_MODEL if acpi_cmd is None else acpi_cmd]


def format_acpi_cmd(arg0, arg1='0x00', arg2='0x00', arg3='0x00'):
    return ACPI_COMMAND.format(DEVICES[LAPTOP_MODEL], arg0, arg1, arg2, arg3)


def set_power_mode(power_mode):
    func = CallTypes('set_power_mode').value
    mode = PowerModes(power_mode).hex
    return format_acpi_cmd(*func, mode)


def get_power_mode():
    args = CallTypes('get_power_mode').value
    return format_acpi_cmd(*args)


def get_laptop_model():
    args = CallTypes('get_laptop_model').value
    return format_acpi_cmd(*args)


def get_g_mode():
    args = CallTypes('get_G_mode').value
    return format_acpi_cmd(*args)


def toggle_g_mode():
    args = CallTypes('toggle_G_mode').value
    return format_acpi_cmd(*args)


if __name__ == '__main__':
    print(get_g_mode())
    # print(format_acpi_cmd(*CallTypes('get_g_mode').value))
    # print(get_acpi_command())
    # print(PowerModes('0xa3').name)
    # print(CallTypes('get_g_mode').name)
