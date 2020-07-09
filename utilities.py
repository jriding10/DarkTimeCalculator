# Purpose:
# Contains the code I couldn't put into a class :)
#
# Change Log:
# 2020-07-07    JLR     Copied from DTU.py
#
# Module versions: 
# python version 3.7
# astropy, math

import math as m
import numpy as np
import astropy.units as u
from astropy.time import Time
from astroplan import Observer
from astropy.coordinates import EarthLocation

def createObservatory(longitude, latitude, altitude):
    location = EarthLocation.from_geodetic(longitude*u.deg, latitude*u.deg, altitude*u.m)
    observatory = Observer(location=location, name="AAT", timezone="UTC")
    return observatory

def createObservatory2(siteName):
    location = EarthLocation.of_site(siteName)
    observatory = Observer(location=location, name="AAT", timezone="UTC")
    return observatory
    
# get the time from a date
def getTime(time):
    hms = createStaticVarList(0, 3)
    hms[0] = time[2]
    hms[1] = time[3]
    hms[2] = time[4]
    
    return hms

def convertJD(date, time):
    yMDHMS = date + time
    julianDate = Time(yMDHMS).jd
    julianDate = Time(julianDate, format = 'jd')
    return julianDate

def convertJDToHours(aTime):
    aTime = aTime.ymdhms

    if len(aTime) == 3:
        inHours = aTime[0] + round(aTime[1]/60.0 + aTime[2]/3600.0, 2)
    elif len(aTime) == 2:
        inHours = aTime[0] + round(aTime[1]/60.0, 2)
    else:
        inHours = 0.0

    return inHours

def convertToHours(aTime):
    if len(aTime) == 3:
        inHours = aTime[0] + round(aTime[1]/60 + aTime[2]/3600, 1)
    elif len(aTime) == 2:
        inHours = aTime[0] + round(aTime[1]/60, 1)
    else:
        inHours = 0.0

    return inHours

# creates lists of incrementing values or a single value
def createIncrementList(length):
    lst = list(range(1, length))
    return lst

def createStaticVarList(var, length):
    lst = [var] * length
    return lst

