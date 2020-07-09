# Purpose:
# Contains the code for julian date
#
# Classes:
# JDTime - converts jd time into hhmmss
# 
# Functions:
# nightTime - determines the length of night from jd to hhmmss
# laterTime - determines the later of two dates/times
# earilerTime - determines the eariler of two dates/times
#
# Change Log:
# 2020-06-28    JLR     First working version completed
#
# Module versions: 
# python version 3.7
# astropy, math

import math as m
import numpy as np
import astropy.unimts as u
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

class NightInfo:
    def __init__(self, observatory, date):
        self.obs = observatory
        self.date = date
        self.midnight = ' 14:00:00.0'
        self.julianDate = 0.0
        self.astronomicalStart = 0.0
        self.astronomicalEnd = 0.0
        self.astronomicalLength = 0.0
        self.nauticalStart = 0.0
        self.nauticalEnd = 0.0
        self.nauticalLength = 0.0
        self.moonRise = 0.0
        self.moonSet = 0.0
        self.moonFraction = 0.0
        self.moonUpDuringNight = 0.0
        self.chiaroscuro = 0.0

    def getAstroTimes(self):
        self.astronomicalStart = self.obs.twilight_evening_astronomical(self.time)
        self.astronomicalEnd = self.obs.twilight_morning_astronomical(self.time)
        self.astronomicalLength = self.nightTime(astronomicalStart, astronomicalEnd)
        
    def getNauticalTimes(self):
        self.nauticalStart = self.obs.twilight_evening_nautical(self.time)
        self.nauticalEnd = self.obs.twilight_morning_nautical(self.time)
        self.nauticalLength = self.nightTime(nauticalStart, nauticalEnd)

    def getMoonTimes(self):
        self.moonRise = self.obs.moon_rise_time(self.time)
        self.moonSet = self.obs.moon_set_time(self.time, which = 'next')
        moonPhase = self.obs.moon_phase(time)
        self.moonFraction = moonPhase/360.0

# determines the length of night time in (hours, minutes, seconds)
    def nightTime(start, end):
        diffJD = end.jd - start.jd
        hour = JDTime(diffJD, 24)
        hour.jdConversion()
        hours = int(hour.whole)

        minute = JDTime(hour.frac, 60)
        minute.jdConversion()
        minutes = int(minute.whole)

        second = JDTime(minute.frac, 60)
        second.jdConversion()
        seconds = round(second.newTime)
    
        return hours, minutes, seconds

    def createJD(self):
        timeAndDate = self.date + self.midnight
        self.julianDate = Time(timeAndDate)
         
    def moonUp(self):
        if self.moonRise.jd > self.astronomicalEnd.jd:
            moonArose = self.astronomicalEnd.jd
        else:
            moonArose = max(self.moonRise.jd, self.astronomicalStart.jd)

        if self.moonSet < self.astronomicalStart.jd:
            moonAslept = self.astronomicalEnd.jd
        else:
            moonAslept = min(self.moonSet.jd, self.astronomicalEnd.jd)

        moonArose = Time(moonArose, format='jd')
        moonAslept = Time(moonAslept, format='jd')

        self.moonUpDuringNight = self.nightTime(moonArose, moonAslept)
        
        
        
class Dates:
    def __init__ (self, month, year):
        self.month = month
        self.year = year
        self.numDaysInMonth = 31
        self.numDaysLastMonth = 0
        self.dates = [None]

    def numberOfDaysInMonth(self):
        thirty = [4, 6, 9, 11]
        thirtyOne = [1, 3, 5, 7, 8, 10, 12]

        if self.month in thirty:
            self.numDaysInMonth = 30
        elif numMonth in thirtyOne:
            self.numDaysInMonth = 31
        else:       
            if year % 4 == 0:
                if year % 100 != 0 or year % 400 == 0:
                    self.numDaysInMonth = 29
            else:
                self.numDaysInMonth = 28

    def createDate(self):
        days = list(range(1, self.numDaysInMonth))
        days.insert(0, self.numDaysLastMonth)
        
        months = [self.month] * self.numDaysInMonth
        if self.month == 1:
            lastMonth = 12
            lastYear = self.year - 1
        else:
            lastMonth = self.month - 1
            lastYear = self.year
        months.insert(0, lastMonth)

        years = [self.year] * self.numDaysInMonth
        years.insert(0, lastYear)
    
        self.dates = [None] * numDaysInMonth
        i = 0
        while i < self.numDaysInMonth:
            self.dates[i] = str(years[i]) + '-' + str(months[i]) + '-' + str(days[i])
            i+=1

         

    
# get the time from a date
def getTime(time):
    hms = createStaticVarList(0, 3)
    hms[0] = time[2]
    hms[1] = time[3]
    hms[2] = time[4]
    
    return hms

def convertJDToHours(aTime):
    aTime = aTime.ymdhms

    if len(aTime) == 3:
        inHours = aTime[0] + round(aTime[1]/60.0 + aTime[2]/3600.0, 2)
    elif len(aTime) == 2:
        inHours = aTime[0] + round(aTime[1]/60.0, 2)
    else:
        inHours = 0.0

    return inHours

def convertMinutesToHours(aTime):
    inHours = round(aTime/60,5)
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

def createJDList(dates, midnight):
    numDates = len(dates)
    julianDates = [0] * numDates
    i = 0
    while i < numDates:
        date = dates[i]
        dt = date + midnight
        julianDates[i] = Time(dt)
        i+=1

    return julianDates

def createDateList(day, month, year):
    numDates = len(day)
    dates = [None] * numDates
    i = 0
    while i < numDates:
        dates[i] = str(year[i]) + '-' + str(month[i]) + '-' + str(day[i])
        i+=1
    
    return dates
        
