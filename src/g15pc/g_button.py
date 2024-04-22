import select
import threading
import evdev
from g15pc.ipc import client
from g15pc import settings

device = evdev.InputDevice(settings.KEYBOARD_DEV_PATH)

stop_event = threading.Event()


def main_loop():
    value = 0
    while True:
        r, _, _ = select.select([device], [], [], settings.KEYBOARD_PULL_RATE)
        if stop_event.is_set():
            break

        if r:
            for event in device.read_loop():
                if event.type == 4 and event.value == 104:
                    value += 1
                    if value >= 2:
                        value = 0
                        client.send_request('toggle_G_mode')
