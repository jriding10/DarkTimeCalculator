# class to handle information about start/rise and end/set times for 
# astronomical, nautical twilights and moon. Also contains lengths of
# time.

# ChangeLog:
# 2020-07-31    JLR     Created from the original nightTime.py

import CH_utilities as utils

class nightTime:
    def __init__(self, observatory, date):
        self.obs = observatory
        self.time = date
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

# get astronomical twilight times for date
    def getAstroTimes(self):
        self.astroStart = self.obs.twilight_evening_astronomical(self.time, which='next')
        self.astroEnd = self.obs.twilight_morning_astronomical(self.time, which='next')
        
# get nautical twilight times for date
    def getNauticalTimes(self):
        self.nauticalStart = self.obs.twilight_evening_nautical(self.time, which='next')
        self.nauticalEnd = self.obs.twilight_morning_nautical(self.time, which='next')

# get moon rise and set times for date
    def getMoonTimes(self):
        self.moonRise = self.obs.moon_rise_time(self.time, which = 'next', horizon = -1.75*u.deg)
        self.moonSet = self.obs.moon_set_time(self.time, which = 'next', horizon = -1.75*u.deg)
        moonPhase = self.obs.moon_phase(self.time)
        self.moonFraction = moonPhase/360.0

# compute the length of the twilights in hours
    def getNightLengths(self):
        self.astroLength = utils.convertJDtoHours(self.astroStart, self.astroEnd)
        self.nauticalLength = utils.convertJDtoHours(self.nauticalStart, self.nauticalEnd)

# compute the length of time the moon is up during astronimcal night
# case 1:   the moon rises either before or after the start of astro twilight, and sets either before
#           or after the end of astro twilight.
# case 2:   the moon sets before the start of astro twilight and does not rise during the night. Sets
#           moonAslept (sets) to astroEnd.
# case 3:   the moon rises after the end of astro twilight and is not up during the night. Sets moonArose
#           (rises) to astroEnd.
# case 4:   the moon sets first and then rises again later in the night. Adds the time it is up at the 
#           beginning of the night to the time up at the end.

    def moonUp(self):
        # case 1:
        moonArose = max(self.moonRise.jd, self.astroStart.jd)
        moonAslept = min(self.moonSet.jd, self.astroEnd.jd)
        
        # case 2:
        if self.moonSet.jd < self.astroStart.jd:
            moonAslept = self.astroEnd.jd
            
        # case 3:
        if moonArose > self.astroEnd.jd:
            moonArose = self.astroEnd.jd
        
        # case 4: 
        if moonAslept - moonArose < 0:
            if moonArose < self.astroEnd.jd:
                moonAslept += self.astroEnd.jd - moonArose
            else:  
                moonArose = self.astroStart.jd
            
        moonArose = Time(moonArose, format='jd')
        moonAslept = Time(moonAslept, format='jd')

        self.moonUpDuringNight = utils.convertJDtoHours(moonArose, moonAslept)