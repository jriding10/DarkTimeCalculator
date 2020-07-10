# Purpose:
# Contains the code for julian date
#
# Change Log:
# 2020-07-07    JLR     Copied from DTU.py
#
# Module versions: 
# python version 3.7
# astropy

import math as m
from astropy.time import Time

# Converts jd time into (hours, minutes, seconds)
class JDTime:
    def __init__(self, jdTime, convertFactor):
        self.jdTime = jdTime
        self.convertFactor = convertFactor
        self.whole = 0.0
        self.frac = 0.0
        self.newTime = 0.0

    def jdConversion(self):
        self.newTime = self.jdTime*self.convertFactor
        self.frac, self.whole = m.modf(self.newTime)
        self.jdTime = self.jdTime - self.whole

