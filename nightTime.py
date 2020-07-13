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
import importlib as imp
import math as m
import astropy.units as u
from astropy.time import Time

imp.reload(jdt)

class NightInfo:
    def __init__(self, observatory, date, jDate):
        self.obs = observatory
        self.date = date
        self.time = jDate
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
        self.astroStart = self.obs.twilight_evening_astronomical(self.time, which='next')
        self.astroEnd = self.obs.twilight_morning_astronomical(self.time, which='next')
        
    def getNauticalTimes(self):
        self.nauticalStart = self.obs.twilight_evening_nautical(self.time, which='next')
        self.nauticalEnd = self.obs.twilight_morning_nautical(self.time, which='next')

    def getMoonTimes(self):
        self.moonRise = self.obs.moon_rise_time(self.time, which = 'next', horizon = -1.75*u.deg)
        self.moonSet = self.obs.moon_set_time(self.time, which = 'next', horizon = -1.75*u.deg)
        moonPhase = self.obs.moon_phase(self.time)
        self.moonFraction = moonPhase/360.0

    def getNightLengths(self):
        self.astroLength = self.nightTime(self.astroStart, self.astroEnd)
        self.nauticalLength = self.nightTime(self.nauticalStart, self.nauticalEnd)

# determines the length of night time in (hours, minutes, seconds)
    def nightTime(self, start, end):
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

    def moonUp(self):
        # covers the basic cases where the moon rises either before or after
        # the start of astro twilight. Similar, when it either sets before or
        # after the end of astro twilight.
        moonArose = max(self.moonRise.jd, self.astroStart.jd)
        moonAslept = min(self.moonSet.jd, self.astroEnd.jd)
        
        # covers the case the moon sets before night time. Setting it to
        # astroEnd ensures moonUp = astroEnd - astroEnd.
        if self.moonSet.jd < self.astroStart.jd:
            moonAslept = self.astroEnd.jd
            
        # covers the case the moon rises after the end of astro twilight. 
        # Setting it to astroEnd ensures moonUp = 0.
        if moonArose > self.astroEnd.jd:
            moonArose = self.astroEnd.jd
        
        # covers the case the moon sets at the start of the night but rises
        # again at the end. It takes the time up at the end of the night and
        # adds it to the start to get an acturate moonUp time.    
        if moonAslept - moonArose < 0:
            if moonArose < self.astroEnd.jd:
                moonAslept += self.astroEnd.jd - moonArose
            else:  
                moonArose = self.astroStart.jd
            
        moonArose = Time(moonArose, format='jd')
        moonAslept = Time(moonAslept, format='jd')

        self.moonUpDuringNight = self.nightTime(moonArose, moonAslept)
       
    def calculateChiaroscuro(self):
        moonLengthInHours = util.convertToHours(self.moonUpDuringNight)
        astroLengthInHours = util.convertToHours(self.astroLength)
        nauticalLengthInHours = util.convertToHours(self.nauticalLength)

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

#class FirstHalf(NightInfo):
#    def __init__(self, obs, date, jDate):
#        super().__init__(obs, date, jDate)
#        self.astroEnd = jDate
#        self.astroLength = 0.0
#        self.nauticalEnd = jDate
#        self.nauticalLength = 0.0
#        self.moonUpDuringNight = 0.0
#        self.chiaroscuro = 0.0

#    def getAT(self):
#        self.astroStart = super().getAstroTimes()
#        self.astroEnd = super().time

#    def getNT(self):
#        self.nauticalStart = super().getNauticalTimes()
#        self.nauticalEnd = super().time

#class SecondHalf(NightInfo):
#    def __init__(self):
#        self.astroStart = 0.0
#        self.astroLength = 0.0
#        self.nauticalStart = 0.0
#        self.nauticalLength = 0.0
#        self.moonUpDuringNight = 0.0
#        self.chiaroscuro = 0.0

#    def getAstroTimes(self):
#        self.astroStart = NightTime.time

#    def getNauticalTime(self):
#        self.nauticalStart = NightTime.time
