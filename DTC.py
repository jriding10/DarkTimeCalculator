# Purpose:
# Calculates the chiaroscuro - the fraction of time the night that is dark. 
# Completes this fraction for half nights to aid scheduling. This fraction is 
# calculated for the whole night and half night to aid with half-night programs.
# 
# Instructions:
# The user needs to define a year and a month and the program will output the 
# night brightness for that time period. If month = 0, the program will output the
# night brightness over the whole year.
#
# Bright:       CH < 0.35
# Grey:         0.35 <= CH < 0.65
# Dark:         CH >= 0.65
#
# Quick architecture:
# - setup AAT (lat, long, alt)
# - user input (year, month(s))
# - create date arrays

# Change Log:
# 2020-06-28    JLR     Single day version complete
# 2020-07-07    JLR     Changed most time scenarios to JD
#                       Implemented classes
# 2020-07-10    JLR     Broke program into module files

# Module Versions:
# python version 3.7
# nightTime.py, utilities.py, dateAndTime.py, DTC_GUI.py 
#################################################################################

import utilities as util
import nightTime as nt
import dateAndTime as dnt

import csv
from astropy.time import Time
import importlib as imp
import matplotlib.pyplot as plt

imp.reload(dnt)
imp.reload(util)
imp.reload(nt)

# run the next two lines occassionally for the most up-to-date rise/set times
# from astroplan import download_IERS_A   # Best precision data (arcseconds)
# download_IERS_A()

# Location of the AAT according to the Observer's Guide 1991
# longitude = 149deg 3min 58sec E
# latitude = 31deg 16min 37sec S
# altitude = 1165m - this is if the horizon is at sea level. Consider using 670m 
# with the local horizon. Difference in dark time under a minute.
# longitude = 149.0 + 3.0/60 + 58.0/3600
# latitude = -1*(31.0 + 16.0/60 + 37.0/3600)
# altitude = 1164
# aat = util.createObservatory(longitude, latitude, altitude)

siteName = "Anglo-Australian Observatory"
aat = util.createObservatory2(siteName)

# aest = utc + 10hours, so the variable time is set to local midnight the day before.
# aest = 6pm -> 8am utc (the previous day)
# aest = 6am -> 8pm utc (the previous day)
midnight = ' 2:00:00'

# Obtain user input
year = 0
while year < 1900:
    year = input("Enter year (after 1900): ")
    try:
        year = int(year)
    except ValueError:
        print("Invalid year. Please enter an integer")
        year = 0

month = 13
while month > 12 or month < -1:
    month = input("Enter month (1-12) or 0 for entire year's data: ")
    try:
        month = int(month)
    except ValueError:
        print("Invalid month. Please enter an integer")
        month = 13

#################################################################################### 
thisMonth = dnt.Dates(month, year)
thisMonth.numDaysInMonth = thisMonth.numberOfDaysInMonth(month)
thisMonth.createDate()
dates = thisMonth.dates

monthName = thisMonth.getMonthName()
filename = monthName + '_' + str(year) + '.csv'

CH = [0.0] * thisMonth.numDaysInMonth
dark = [0.0] * thisMonth.numDaysInMonth
grey = [0.0] * thisMonth.numDaysInMonth
night = {}
firstHalf = {}
secondHalf = {}

i = 0
while i < thisMonth.numDaysInMonth:
    # Create date object
    julianTime = util.convertJD(dates[i], midnight)
    night[i] = nt.NightInfo(aat, dates[i], julianTime)
#    firstHalf[i] = nt.FirstHalf(aat, dates[i], julianTime)
#    secondHalf[i] = nt.SecondHalf()

    night[i].getAstroTimes()
    night[i].getNauticalTimes()
    night[i].getNightLengths()
    night[i].getMoonTimes()

#    firstHalf[i].getAstroTimes()
#    firstHalf[i].getNauticalTimes()
#    firstHalf[i].getNightLengths()
#    firstHalf[i].getMoonTimes()

#    secondHalf[i].getAstroTimes()
#    secondHalf[i].getNauticalTimes()
#    secondHalf[i].getNightLengths()
#    secondHalf[i].getMoonTimes()
    
    astroStart = night[i].astroStart.ymdhms
    astroEnd = night[i].astroEnd.ymdhms
    moonStart = night[i].moonRise.ymdhms
    moonEnd = night[i].moonSet.ymdhms
   
    night[i].moonUp()
#    firstHalf[i].moonUp()
#    secondHalf[i].moonUp()
    
    night[i].calculateChiaroscuro()
#    firstHalf[i].calculateChiaroscuro()
#    secondHalf[i].calculateChiaroscuro()

    CH[i] = day[i].chiaroscuro 
    dark[i] = 0.65
    grey[i] = 0.35
    
    print(CH[i])
    i+=1

    
#with open(filename, 'a+') as output:
#    wr = csv.writer(output, delimiter='\n')
#    wr.writerows([CH])

#plt.plot(CH)
#plt.plot(dark)
#plt.plot(grey)
#plt.show()


