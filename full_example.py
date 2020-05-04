import sys
import os
from time import sleep

import pigpio as io
from ADS1256_definitions import *
from ADS1256_PiGPIO import ADS1256
from waveshare_definitions import *
from DAC8552_PiGPIO import DAC8552, DAC_A, DAC_B, MODE_POWER_DOWN_100K

from blessings import Terminal

term = Terminal()


def determine_led_bias_v():
    current_bias = 0x0
    step = 0x1fff
    print(term.blue('Determining LED forward bias. Press d to dim the LED, u to brighten, x when LED is barely lit.'))
    while True:
        print('Bias is', hex(current_bias))
        next = input('u/d/x?')
        if next == 'x':
            break
        if next == 'u':
            current_bias = current_bias + step
        if next == 'd':
            current_bias = current_bias - step
            # lazy man's binary search
            step = step >> 1
        if current_bias > 0xffff:
            current_bias = 0xffff
        if current_bias < 0:
            current_bias = 0
        dac.write_dac(DAC_A, current_bias - step)
    dac.write_dac(DAC_A, 0)
    return current_bias


def control_led_by_pot():
    try:
        while True:
            knob_val = adc.read_oneshot(POTI)
            print("Pot value is", hex(knob_val))
            pct_full_scale = min(1.0, knob_val / 0x4fffff)
            print("Pot % is", pct_full_scale)
            dac.write_dac(DAC_A, DEFAULT_LED_BIAS + int(LED_RANGE*pct_full_scale))

    except (KeyboardInterrupt):
        print("\n" * 8 + "User exit.\n")
    return


print(term.clear() + term.bold_red_on_bright_green(' Wavefront ADC/DAC Board with PiGPIO Demo '))
host = input('Raspberry Pi hostname (enter for localhost):')
hostName = host if host else 'localhost'
print(term.blue('Connecting to'), term.bold(hostName))

pi = io.pi(host)

if not pi.connected:
    print(term.white_on_red("Could not connect to PiGPIO target " + hostName + "!"))
    sys.exit(-1)

print(term.dim('...connection established'))
adc = ADS1256(pi=pi)
# calibrate
adc.cal_self()
dac = DAC8552(pi=pi)

led_bias = determine_led_bias_v()
print('Minimum LED forward bias is', hex(led_bias))
control_led_by_pot()
pi.stop()
