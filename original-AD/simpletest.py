import sys
import os
from ADS1256_definitions import *
from pipyadc import ADS1256

ads = ADS1256()

print(ads.status)