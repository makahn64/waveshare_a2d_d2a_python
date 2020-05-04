# -*- coding: utf-8 -*-

import time
import struct
import pigpio as io
from ADS1256_definitions import *

# Change this to the local DNS name of your Pi (often raspberrypi.local, if you have changed it) or
# make it blank to connect to localhost.
PI_HOST = 'klabs.local'

SPI_CHANNEL = 1
SPI_FLAGS = 0b0000000000000011100001
SPI_FREQUENCY = 976563

# The RPI GPIOs used: All of these are optional and must be set to None if not
# used. See datasheet.
# CS_PIN = None
#CS_PIN      = 15
# pigpio uses different pin numbers!
CS_PIN      = 22

# This pin makes no sense. It should not have been 11!
#DRDY_PIN    = 11
# It should have been 7 per the soft mapping, but 17 per the schematic
#DRDY_PIN   = 7
DRDY_PIN    = 17

#RESET_PIN   = 12
RESET_PIN = 18

#PDWN_PIN    = 13
PDWN_PIN    = 27


DRDY_TIMEOUT    = 2
DRDY_DELAY      = 0.000001
CLKIN_FREQUENCY = 7680000

# Analog reference voltage at VREF pin
v_ref = 3.3

def usleep(x):
    time.sleep(x / 1000000.0)

def wait_DRDY():
    start = time.time()
    elapsed = time.time() - start

    drdy_level = pi.read(DRDY_PIN)
    print('DRDY is ', drdy_level, 'on initial read, we\'re good to go!')

    while (drdy_level == 1) and (elapsed < DRDY_TIMEOUT):
        elapsed = time.time() - start
        drdy_level = pi.read(DRDY_PIN)
        print('DRDY is ', drdy_level)
        # Delay in order to avoid busy wait and reduce CPU load.
        time.sleep(DRDY_DELAY)
    if elapsed >= DRDY_TIMEOUT:
        print("\nWarning: Timeout while polling configured DRDY pin!\n")

def chip_select(value):
    csval = 0 if value else 1
    print('Chip select on pin', CS_PIN, 'is now ', csval)
    pi.write(CS_PIN, csval)

def send_byte(register, value):
    pi.spi_write(spi_iface, bytes(value))


def reset():
    print('Issuing reset()')
    chip_select(True)
    usleep(2)
    pi.spi_write(spi_iface, bytes(CMD_RESET))
    wait_DRDY()
    chip_select(False)

def read_reg(register):
    print('Reading register ', register)
    chip_select(True)
    payload = [CMD_RREG | register, 0x0]
    print(bytes(payload))
    pi.spi_write(spi_iface, payload)
    usleep(2)
    (b,d) = pi.spi_read(spi_iface, 1)
    if b < 0:
        raise IOError("Can't read shit")
    chip_select(False)
    return d

pi = io.pi(PI_HOST)
if not pi.connected:
    raise IOError("Could not connect to hardware via pigpio library")

print('We are connected to klabs.local')

pi.set_mode(DRDY_PIN, io.INPUT)
print('=DRDY set to input')

pi.set_mode(CS_PIN, io.OUTPUT)
pi.write(CS_PIN, io.HIGH)
print('=CS set to output: ', io.HIGH)

pi.set_mode(RESET_PIN, io.OUTPUT)
pi.write(RESET_PIN, io.HIGH)
print('=RESET set to output: ', io.HIGH)

pi.set_mode(PDWN_PIN, io.OUTPUT)
pi.write(PDWN_PIN, io.HIGH)
print('=PDWN_PIN set to output: ', io.HIGH)

spi_iface = pi.spi_open(SPI_CHANNEL, SPI_FREQUENCY, SPI_FLAGS)

# 30ms settling
time.sleep(0.03)

print('Waiting on the DRDY pin...')
wait_DRDY()
reset()

time.sleep(0.03)
print(read_reg(0x4))
pi.stop()