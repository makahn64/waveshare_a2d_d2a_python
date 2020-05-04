import sys
from time import sleep
import pigpio as io
from DAC8552_PiGPIO import DAC8552, DAC_A, DAC_B, MODE_POWER_DOWN_100K
from ADS1256_definitions import *
from ADS1256_PiGPIO import ADS1256

# Change this to the local DNS name of your Pi (often raspberrypi.local, if you have changed it) or
# make it blank to connect to localhost.
PI_HOST = 'klabs.local'

POTI = POS_AIN0|NEG_AINCOM
# Light dependant resistor of the same board:
LDR  = POS_AIN1|NEG_AINCOM
# The other external input screw terminals of the Waveshare board:
EXT2, EXT3, EXT4 = POS_AIN2|NEG_AINCOM, POS_AIN3|NEG_AINCOM, POS_AIN4|NEG_AINCOM
EXT5, EXT6, EXT7 = POS_AIN5|NEG_AINCOM, POS_AIN6|NEG_AINCOM, POS_AIN7|NEG_AINCOM

# You can connect any pin as well to the positive as to the negative ADC input.
# The following reads the voltage of the potentiometer with negative polarity.
# The ADC reading should be identical to that of the POTI channel, but negative.
POTI_INVERTED = POS_AINCOM|NEG_AIN0

# For fun, connect both ADC inputs to the same physical input pin.
# The ADC should always read a value close to zero for this.
SHORT_CIRCUIT = POS_AIN0|NEG_AIN0

# Specify here an arbitrary length list (tuple) of arbitrary input channel pair
# eight-bit code values to scan sequentially from index 0 to last.
# Eight channels fit on the screen nicely for this example..
CH_SEQUENCE = (POTI, LDR, EXT2, EXT3, EXT4, EXT7, POTI_INVERTED, SHORT_CIRCUIT)

pi=io.pi(PI_HOST)

dac = DAC8552(pi=pi)
adc = ADS1256(pi=pi)

adc.cal_self()

def measurement_loop():
    while True:
        raw_channels = adc.read_sequence(CH_SEQUENCE)
        potval = raw_channels[0]>>7
        print(DAC_A, potval)
        dac.write_dac(DAC_A, potval)


try:
    print("\033[2J\033[H") # Clear screen
    print(__doc__)
    print("\nPress CTRL-C to exit.")
    measurement_loop()

except (KeyboardInterrupt):
    print("\n"*8 + "User exit.\n")
    pi.stop()
    sys.exit(0)

