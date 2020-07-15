#!/usr/bin/python
#################################################################################
#                                                                               #
#                               DTC.py                                          #
#                                                                               #
#################################################################################

# Purpose:
# Calculates the chiaroscuro - the fraction of time the night that is dark. 
# Completes this fraction for half nights to aid scheduling. This fraction is 
# calculated for the whole night and half night to aid with half-night programs.

# Instructions:
# The user needs to define a year and a month and the program will output the 
# night brightness for that time period. If month = 0, the program will output the
# night brightness over the whole year.

# Bright:       CH < 0.35
# Grey:         0.35 <= CH < 0.65
# Dark:         CH >= 0.65

# Change Log:
# 2020-06-28    JLR     Single day version complete
# 2020-07-07    JLR     Changed most time scenarios to JD
#                       Implemented classes
# 2020-07-10    JLR     Broke program into module files
# 2020-07-13    JLR     Calculates CH to some accuracy. Also calculates CH for
#                       the beginning and end halves of the night.

# Module Versions:
# python version 3.7
# nightTime.py, utilities.py, dateAndTime.py, DTC_GUI.py 
#################################################################################
# modules found in this directory
import utilities as util
import nightTime as nt
import dateAndTime as dnt

# standard libraries
import csv
from astropy.time import Time
import importlib as imp

# reload modules (for debugging purposes)
imp.reload(dnt)
imp.reload(util)
imp.reload(nt)

# run the next two lines occassionally for the most up-to-date rise/set times
# from astroplan import download_IERS_A   # Best precision data (arcseconds)
# download_IERS_A()

# Location of the AAT according to the Observer's Guide 1991. This concurs with 
# the location stored in astroplan library.
# longitude = 149deg 3min 58sec E
# latitude = 31deg 16min 37sec S
# altitude = 1165m - this is if the horizon is at sea level. Consider using 670m 
# with the local horizon. Difference in dark time under a minute. Difference in CH
# unnoticable.

#longitude = 149.0 + 3.0/60 + 58.0/3600
#latitude = -1*(31.0 + 16.0/60 + 37.0/3600)
#altitude = 1164
#aat = util.createObservatory(longitude, latitude, altitude)

siteName = "Anglo-Australian Observatory"
aat = util.createObservatory2(siteName)

# Dates will be left in julian format. Times in UTC.
# aest = utc + 10hours.
# aest = 6pm -> 8am utc (the previous day)
# aest = 6am -> 8pm utc (the previous day)
midday = ' 2:00:00'
midnight = ' 14:00:00'

# Obtain user input. Year, Month or Semester, CH or firstCH, secondCH and all.
year = 0
while year < 1900:
    year = input("Enter year (after 1900): ")
    try:
        year = int(year)
    except ValueError:
        print("Invalid year. Please enter an integer")
        year = 0

# coorect just checks user input.
correct = 0
while correct == 0:
    month = input("Enter month (1-12) or A/B for semesters: ")
    if month == 'A':
        monthStart = 2
        monthEnd = 7
        correct = 1
    elif month == 'B':
        monthStart = 8
        monthEnd = 1
        correct = 1
    else:
        try:
            month = int(month)
            monthStart = month
            monthEnd = month
            correct = 1
        except ValueError:
            print("Invalid month. Please enter an integer")

# numOutputs holds user value for whether they want CH, 1st or 2nd CH or all.
numOutputs = 4
while numOutputs < 0 or numOutputs > 1:
    numOutputs = input("Do you want the chiaroscuro for the whole night (0) or include half night versions(1)")
    try:
        numOutputs = int(numOutputs)
    except ValueError:
        print("Invalid choice. Pls try again.")
        numOutputs = 5

#################################################################################### 
i = 0
currentMonth = monthStart

# Initialise required dictionaries.
night = {}
if numOutputs == 1:
    firstHalf = {}
    secondHalf = {}

#This while loop cycles through the months requested.
while currentMonth >= monthStart and currentMonth <= monthEnd:
    # cover the fact semester B includes January of the next year
    if month == 'B':
        if currentMonth == 1:
            year += 1
    # compute the dates for this month.
    thisMonth = dnt.Dates(currentMonth, year)
    thisMonth.numDaysInMonth = thisMonth.numberOfDaysInMonth(currentMonth)
    thisMonth.createDate()
    dates = thisMonth.dates

    # This while loops over the days of the month and calculates CH
    j = 0
    while j < thisMonth.numDaysInMonth:
        # Create time object
        middayJD = util.convertJD(dates[j], midday)
        midnightJD = util.convertJD(dates[j], midnight)
        night[i] = nt.NightInfo(aat, dates[j], middayJD)

        # Calculate the various times to get CH
        night[i].getAstroTimes()
        night[i].getNauticalTimes()
        night[i].getNightLengths()
        night[i].getMoonTimes()
        night[i].moonUp()
        night[i].calculateChiaroscuro()
        
        # Repeat of above for 1st half of the night. Set end times to midnight.
        if numOutputs == 1:
            firstHalf[i] = nt.NightInfo(aat, dates[j], middayJD)
            firstHalf[i].getAstroTimes()
            firstHalf[i].getNauticalTimes()
            firstHalf[i].astroEnd = midnightJD
            firstHalf[i].nauticalEnd = midnightJD
            firstHalf[i].getNightLengths()
            firstHalf[i].getMoonTimes()
            firstHalf[i].moonUp()
            firstHalf[i].calculateChiaroscuro()

            # Repeat of above for 2nd half of the night. Set start times to midnight.
            secondHalf[i] = nt.NightInfo(aat, dates[j], middayJD)
            secondHalf[i].getAstroTimes()
            secondHalf[i].getNauticalTimes()
            secondHalf[i].astroStart = midnightJD
            secondHalf[i].nauticalStart = midnightJD
            secondHalf[i].getNightLengths()
            secondHalf[i].getMoonTimes()
            secondHalf[i].moonUp()
            secondHalf[i].calculateChiaroscuro()
    
        print(dates[j] + '      ' + str(round(night[i].chiaroscuro,3)))
   
        i+=1
        j+=1
    currentMonth+=1
   
numDays = len(night) 
CH = util.createStaticVarList(0.0, numDays)
dark = util.createStaticVarList(0.35, numDays)
grey = util.createStaticVarList(0.65, numDays)

if  numOutputs == 1:
    firstCH = util.createStaticVarList(0.0, numDays)
    secondCH = util.createStaticVarList(0.0, numDays)

i = 0
while i < numDays:
    CH[i] = night[i].chiaroscuro
    if  numOutputs == 1:
        firstCH[i] = firstHalf[i].chiaroscuro
        secondCH[i] = secondHalf[i].chiaroscuro
    i+=1 

if month == 'A':
    monthName = 'SemesterA'
elif month == 'B':
    monthName = 'SemesterB'
else:
    monthName = thisMonth.getMonthName()
    
filename = monthName + '_' + str(year)
filenameCSV = filename + '.csv'

if numOutputs == 0:
    util.readableTableCH(night, filename)
else:
    util.readableTableAllCH(night, firstCH, secondCH, filename)

#with open(filenameCSV, 'a+') as output:
#    wr = csv.writer(output, delimiter='\n')
#    wr.writerows([CH])



