# -*- coding: utf-8 -*-

# Digital to Analog Experiments

import time
import struct
import pigpio as io
from DAC8552_PiGPIO import DAC8552, DAC_A, DAC_B, MODE_POWER_DOWN_100K

SPI_CHANNEL = 1
SPI_FLAGS = 0b0000000000000011100001
SPI_FREQUENCY = 976563

# pigpio uses different pin numbers! See schematic and ref code.
CS_PIN = 23

# Analog reference voltage at VREF pin
v_ref = 3.3

LOAD_A = 0b00010000

def load_a_cmd(sixteenBitsOfVoltage):
    highbyte = sixteenBitsOfVoltage >> 8
    lowbyte = sixteenBitsOfVoltage & 0xFF
    barray = bytes([LOAD_A, highbyte, lowbyte])
    print(barray)
    return [LOAD_A, highbyte, lowbyte]



def usleep(x):
    time.sleep(x / 1000000.0)


def chip_select(value):
    csval: int = 0 if value else 1
    print('Setting chip select ', CS_PIN, ' to ', csval)
    pi.write(CS_PIN, csval)


def send_byte(register, value):
    pi.spi_write(spi_iface, bytes(value))


pi = io.pi('klabs.local')
if not pi.connected:
    raise IOError("Could not connect to hardware via pigpio library")

# dac = DAC8552(pi=pi)
# dac.write_dac(DAC_A, 0x9fff)
spi_iface = pi.spi_open(SPI_CHANNEL, SPI_FREQUENCY, SPI_FLAGS)
print('We are connected to klabs.local')

chip_select(True)
payload = load_a_cmd(0xfff)
pi.spi_write(spi_iface, payload)
chip_select(False)

time.sleep(0.03)
# pi.spi_close(spi_iface)
pi.stop()
