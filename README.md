# Alien Power Control
WORK IN PROGRESS, INSTALL NOT WORKING YET

This is a fork/rewrite of [@cemkaya-mpi](https://github.com/cemkaya-mpi) [Dell-G15-Controller](https://github.com/cemkaya-mpi/Dell-G15-Controller).

Daemon and tray application to control power modes (with G button support) for the Dell G15 5525 laptops.
Might work on other models but I have not tested.

USE AT YOUR OWN RISK.

# Features
- Change power modes
- G button for toggling Gameshift mode.
- Daemon (can run as a systemd unit)
- Tray application
- CLI application

## Features not available that are available in the original app
- Manual fan control
- Lights

# Requirements
- Polkit (for raising shell privileges)
- Python3

## Python requirements
- evdev (for gbutton support)
- pexpect (to run the acpi calls)
- pygobject (for tray application)
- setuptools (installation)

## plugdev 

Make sure the user is part of the plugdev group, this is needed for accessing the socket.

```
/etc/udev/rules.d/00-aw-elc.rules

SUBSYSTEM=="usb", ATTRS{idVendor}=="187c", ATTRS{idProduct}=="0550", MODE="0660", GROUP="plugdev", SYMLINK+="awelc"
```

# installation
NOT DONE YET

# How to

## CLI
```
options:
  -h, --help            show this help message and exit
  -s , --set-power-mode Set the active powermode, available modes are: [
                            'MANUAL', 'USTT_BALANCED', 'USTT_PERFORMANCE', 'USTT_QUIET',
                            'USTT_FULLSPEED', 'USTT_BATTERYSAVER', 'G_MODE'
                        ]
  -g, --get-power-mode  Returns the active powermode
  -l, --get-laptop-model
                        Returns laptop model
  -gg, --get-g-mode     Returns gameshift state
  -t, --toggle-g-mode   Toggles gameshift
  -d, --daemon          Starts daemon
  --tray                Starts tray application
```

## Daemon

### Systemd service PROVIDED UNIT NOT WORKING YET, I NEED TO FIX THE INSTALL FIRST TO ADD THE CORRECT EXEC
Install and run the provided unit 

### CLI
Just pass `--daemon` as argument. The daemon needs root access, it will run polkit to elevate the shell if run by a normal user, but will work just fine by running as root.

DON'T RUN THE TRAY APPLICATION AS ROOT

## Tray
Just pass `--tray` as argument. Will create an indicator that can toggle Gameshift and change power modes.


# Acknowledgements
This is basically a rewrite of [@cemkaya-mpi](https://github.com/cemkaya-mpi) [Dell-G15-Controller](https://github.com/cemkaya-mpi/Dell-G15-Controller), I used all the core functions for changing power modes and toggling G mode.
