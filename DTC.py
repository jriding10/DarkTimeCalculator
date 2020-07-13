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
midday = ' 2:00:00'
midnight = ' 14:00:00'

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

fraction = 4
while fraction < 0 or fraction > 3:
    fraction = input("Do you want the chiaroscuro for the whole night (0), first half (1), second half (2) or all (3)?")
    try:
        fraction = int(fraction)
    except ValueError:
        print("Invalid choice. Pls try again.")
        fraction = 5

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

if fraction == 1 or fraction == 3:
    firstCH = [0.0] * thisMonth.numDaysInMonth
    firstHalf = {}
if fraction == 2 or fraction == 3:
    secondCH = [0.0] * thisMonth.numDaysInMonth
    secondHalf = {}

i = 0
while i < thisMonth.numDaysInMonth:
    # Create date object
    middayJD = util.convertJD(dates[i], midday)
    midnightJD = util.convertJD(dates[i], midnight)
    night[i] = nt.NightInfo(aat, dates[i], middayJD)

    night[i].getAstroTimes()
    night[i].getNauticalTimes()
    night[i].getNightLengths()
    night[i].getMoonTimes()
    night[i].moonUp()
    night[i].calculateChiaroscuro()

    if fraction == 1 or fraction == 3:
        firstHalf[i] = nt.NightInfo(aat, dates[i], middayJD)
        firstHalf[i].getAstroTimes()
        firstHalf[i].getNauticalTimes()
        firstHalf[i].astroEnd = midnightJD
        firstHalf[i].nauticalEnd = midnightJD
        firstHalf[i].getNightLengths()
        firstHalf[i].getMoonTimes()
        firstHalf[i].moonUp()
        firstHalf[i].calculateChiaroscuro()
        firstCH[i] = firstHalf[i].chiaroscuro


    if fraction == 2 or fraction == 3:
        secondHalf[i] = nt.NightInfo(aat, dates[i], middayJD)
        secondHalf[i].getAstroTimes()
        secondHalf[i].getNauticalTimes()
        secondHalf[i].astroStart = midnightJD
        secondHalf[i].nauticalStart = midnightJD
        secondHalf[i].getNightLengths()
        secondHalf[i].getMoonTimes()
        secondHalf[i].moonUp()
        secondHalf[i].calculateChiaroscuro()
        secondCH[i] = secondHalf[i].chiaroscuro 
    
    astroStart = night[i].astroStart.ymdhms
    astroEnd = night[i].astroEnd.ymdhms
    moonStart = night[i].moonRise.ymdhms
    moonEnd = night[i].moonSet.ymdhms
   
    CH[i] = night[i].chiaroscuro
    dark[i] = 0.65
    grey[i] = 0.35
    
    print(CH[i])
    i+=1

    
#with open(filename, 'a+') as output:
#    wr = csv.writer(output, delimiter='\n')
#    wr.writerows([CH])



