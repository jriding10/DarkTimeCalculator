# Purpose:
# Contains the class NightTime that holds all information pertaining to an
# object date. 

# Change Log:
# 2020-07-07    JLR     Created code from DTU.py
#
# Module versions: 
# python version 3.7

import utilities as util
import julianDate as jdt
from astropy.time import Time

class NightInfo:
    def __init__(self, observatory, date, jDate):
        self.obs = observatory
        self.date = date
        self.time = jDate
        self.midnight = ' 14:00:00.0'
        self.julianDate = 0.0
        self.astroStart = 0.0
        self.astroEnd = 0.0
        self.astroLength = 0.0
        self.nauticalStart = 0.0
        self.nauticalEnd = 0.0
        self.nauticalLength = 0.0
        self.moonRise = 0.0
        self.moonSet = 0.0
        self.moonFraction = 0.0
        self.moonUpDuringNight = 0.0
        self.chiaroscuro = 0.0

    def getAstroTimes(self):
        self.astroStart = self.obs.twilight_evening_astronomical(self.time)
        self.astroEnd = self.obs.twilight_morning_astronomical(self.time)
        self.astroLength = self.nightTime(self.astroStart, self.astroEnd)
        
    def getNauticalTimes(self):
        self.nauticalStart = self.obs.twilight_evening_nautical(self.time)
        self.nauticalEnd = self.obs.twilight_morning_nautical(self.time)
        self.nauticalLength = self.nightTime(self.nauticalStart, self.nauticalEnd)

    def getMoonTimes(self):
        self.moonRise = self.obs.moon_rise_time(self.time)
        self.moonSet = self.obs.moon_set_time(self.time, which = 'next')
        moonPhase = self.obs.moon_phase(time)
        self.moonFraction = moonPhase/360.0

# determines the length of night time in (hours, minutes, seconds)
    def nightTime(start, end):
        diffJD = end.jd - start.jd
        hour = jdt.JDTime(diffJD, 24)
        hour.jdConversion()
        hours = int(hour.whole)

        minute = jdt.JDTime(hour.frac, 60)
        minute.jdConversion()
        minutes = int(minute.whole)

        second = jdt.JDTime(minute.frac, 60)
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
       
    def calculateChiaroscuro(self):
        moonLengthInHours = util.convertToHours(self.moonUpDuringNight)
        astroLengthInHours = util.convertToHours(self.astroLength)
        naticalLengthInHours = util.convertToHours(self.nauticalLength)

        timeWOMoon = astroLengthInHours - moonLengthInHours
        
        try:
            self.chiaroscuro = timeWOMoon / nauticalLengthInHours
        except ZeroDivisionError:
            print("Nautical twilight has zero length")

        if self.chiaroscuro > 1.0:
            self.chiaroscuro = 1.0
            print("CH is too large again!")
        if self.chiaroscuro < 0.0:
            self.chiaroscuro = 0.0
            print("CH is too small!")         
