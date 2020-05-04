# ADS1256 + DAC8552 Python Drivers

This project provides Python support for both the ADS1256 (A/D) and DAC8552 (D/A) chips on the Waveshare
ADC/DAC HAT board. It stands on the shoulders of two other projects that used disparate low-level
GPIO drivers.

- https://github.com/ul-gh/PiPyADC: ADS1256 driver, made use of the WiringPi low level library.
- https://github.com/adn05/dac8552: DAC8552 driver, made use of the PiGPIO low level library.

The original code for both of these projects (as of March 2020) are in their respective folders. This
code is not used in this project, it is simply there for reference. Check their respective repos for the latest code.

I decided to use the PiGPIO library, primarily because of the remote control capability. PiGPIO runs as a daemon
on the Pi and code using the daemon can run on a Mac/PC and connect over TCP. Works for me!

## Installing PiGPIO

PiGPIO needs to be installed on every Raspberry Pi you intend to run this code on,
or control remotely via TCP. Instructions can ba found here: http://abyz.me.uk/rpi/pigpio/download.html.

You can also install via `apt-get`. The whole process is explained here: https://gpiozero.readthedocs.io/en/stable/remote_gpio.html

You will likely want to make sure the PiGPIO daemon is launched on reboot:

- `sudo systemctl enable pigpiod`
- `systemctl start pigpiod`


## Python 3

Python 2.x is officially dead, so as a part of the project, I've moved everything to Python 3, though most of it already was.

## Running the Code

This code can be run two different ways:
1. Everything running on the Raspberry Pi.
2. Python runs on a PC/Mac/Linux controlling the Pi over TCP.

In both cases, you'll need to get the PiGPIO daemon installed and running as described above.

### Running on a PC/Mac/Linux with PiGPIO Daemon on a Target Pi

I find this to be the best way for development. You can use a real IDE like PyCharm and not
be subjected to painful performance issues.

1. Get the daemon running and enable remote access to the PiGPIO daemon as described above.
2. Make sure you can `ping` your Pi using local DNS. Raspian Pi devices normally have the default hostname `raspberrypi` so you can ping them with
`ping raspberrypi.local`. If you can't ping, check your networking setup. If you changed the hostname, you will need to ping `[hostname].local`.
3. Run any of the `example` applications. `full-example.py` prompts for a hostname. The others require you edit the file. Instructions are in the files.

### Running on the Target Pi with PiGPIO Daemon

If you want the application to run stand-alone on the target, do the following:
1. Get the daemon running as described above. You don't need to worry about enabling remote access.
2. Run any of the `example` applications. `full-example.py` prompts for a hostname. The others require you edit the file. Instructions are in the files. For
local operation, you can use a blank hostname and the code will use `localhost`.





