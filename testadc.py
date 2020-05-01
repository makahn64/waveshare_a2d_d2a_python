#!/usr/bin/python
"""Functional test/development code for ADS1256_PiGPIO port
"""
import sys
from time import sleep
import pigpio as io
from ADS1256_PiGPIO import ADS1256

# STEP 1: Initialise ADC object:
adc = ADS1256(pi=io.pi('klabs.local'))

try:
    print("\033[2J\033[H")  # Clear screen
    # print(__doc__)
    # print("\nPress CTRL-C to exit.")
    print(adc.status)

except KeyboardInterrupt:
    print("\nUser exit.\n")
    # STEP 3: Cleanup!

    sys.exit(0)