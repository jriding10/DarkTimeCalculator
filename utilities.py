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
import matplotlib.pyplot as plt
from astropy.time import Time
from datetime import datetime, timedelta
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

def createPlot(x, y, z):
    length = len(x)
    grey = createStaticVarList(0.35, length)
    dark = createStaticVarList(0.65, length)

    plt.plot(x, 'k')
    plt.plot(y, 'b*')
    plt.plot(z, 'r*')
    plt.plot(grey, 'k--')
    plt.plot(dark, 'k--')
    plt.show()

def readableTimes(night):
    delta = timedelta(hours=+10)
    
    astroStart = datetime.fromisoformat(night.astroStart.iso)
    astroStart += delta
    date = astroStart.isoformat()[0:10]
    astroStartTime = astroStart.isoformat()[11:16]
    astroEnd = datetime.fromisoformat(night.astroEnd.iso)
    astroEnd += delta
    astroEndTime = astroEnd.isoformat()[11:16]

    nautStart = datetime.fromisoformat(night.nauticalStart.iso)
    nautStart += delta
    nautStartTime = nautStart.isoformat()[11:16] 
    nautEnd = datetime.fromisoformat(night.nauticalEnd.iso)
    nautEnd += delta
    nautEndTime = nautEnd.isoformat()[11:16]

    moonRise = datetime.fromisoformat(night.moonRise.iso)
    moonRise += delta
    moonRiseDate = moonRise.isoformat()[0:10]
    moonRiseTime = moonRise.isoformat()[11:16]
    if moonRiseDate != date:
        moonRiseTime = '(' + moonRiseTime + ')'
    else: 
        moonRiseTime = ' ' + moonRiseTime + ' ' 
#    else:
#        moonRiseTime = ' ' + moonRiseTime + ' '
 
    moonSet = datetime.fromisoformat(night.moonSet.iso)
    moonSet += delta
    moonSetDate = moonSet.isoformat()[0:10]
    moonSetTime = moonSet.isoformat()[11:16]
    if moonSetDate != date:
        moonSetTime = '(' + moonSetTime + ')'
    else:
        moonRiseTime = ' ' + moonSetTime + '   '

    writeLine = date + '    '
    writeLine += astroStartTime + '    ' + astroEndTime + '   '
    writeLine += nautStartTime + '    ' + nautEndTime + '    '
    writeLine += moonRiseTime + '    ' + moonSetTime + '    '
    writeLine += str(round(night.chiaroscuro, 3)) + '    '
    
    return writeLine
# Create a human readable table of rise and set times as well as CH
def readableTableCH(night, filename):
    numDays = len(night)
    delta = timedelta(hours=+10)
    filename += '.txt'
    f = open(filename, 'a')    

    i = 0

    txt = '\n'
    txt = txt + filename + '\n'
    txt = txt + ' -----------------------------------------------------------------------------\n '
    txt = txt + '      |       AstroTwilight |  NautTwilight  |          Moon        | \n'
    txt = txt + ' Date |       Start     End |  Start     End |  ' + '   Rise        Set |   CH \n'
    txt = txt + '-------------------------------------------------------------------------------\n'

    f.write(txt)
    while i < numDays:
        writeLine = readableTimes(night[i]) + '\n'
        f.write(writeLine)
        i+=1

    f.close()

def readableTableAllCH(night, firstHalf, secondHalf, filename):
    numDays = len(night)
    delta = timedelta(hours=+10)
    filename += '_all.txt'
    f = open(filename, 'a')

    i = 0
    while i < numDays:
        CH1 = firstHalf[i].chiaroscuro
        CH2 = secondHalf[i].chiaroscuro
        writeLine = readableTimes(night[i])
        print(writeLine)
        print('\n' + str(round(CH1, 3)) + '\n')
        writeLine += str(round(CH1, 3)) + '    '
        writeLine += str(round(CH2, 3)) + '\n'
        f.write(writeLine)
        i+=1

    f.close()
        
