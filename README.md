# ADS1256 + DAC8552 Python Drivers

This project provides Python support for both the ADS1256 (A/D) and DAC8552 (D/A) chips on the Waveshare
ADC/DAC HAT board. It stands on the shoulders of two other projects that used disparate low-level
GPIO drivers.

- https://github.com/ul-gh/PiPyADC: ADS1256 driver, made use of the WiringPi low level library.
- https://github.com/adn05/dac8552: DAC8552 driver, made use of the PiGPIO low level library.

The original code for both of these projects (as of March 2020) are in their respective folders. This
code is not used in this project, it is simply there for reference.

I decided to use the PiGPIO library, primarily because of the remote control capability. PiGPIO runs as a daemon
on the Pi and code using the daemon can connect over TCP. Works for me!

## Installing PiGPIO

PiGPIO needs to be installed on every Raspberry Pi you intend to run this code on,
or control remotely via TCP. Instructions can ba found here: http://abyz.me.uk/rpi/pigpio/download.html.

You will likely want to make sure the PiGPIO daemon is launched on reboot:

- `sudo systemctl enable pigpiod`
- `systemctl start pigpiod`

## Python 3

Python 2.x is officially dead, so as a part of the project, I've moved everything to Python 3.


