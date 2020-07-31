# CH_main.py is the main script that runs all other files.

import CH_nightTimes as nt
import CH_utilities as utils
import CH_daysAndDates as dnd

siteName = "Anglo-Australian Observatory"
aat = utils.createObservatory(siteName)

# Obtain user input. Year, Month or Semester, CH or firstCH, secondCH and all.
# Replaced by GUI (later).
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
    month = input("Enter month (1-12) or 13/14 for semesters A/B: ")
    if month == 13:
        monthStart = 2
        monthEnd = 7
        correct = 1
    elif month == 14:
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
        

i = 0
currentMonth = monthStart

night = {}
if numOutputs == 1:
    firstHalf = {}
    secondHalf = {}
    
while currentMonth >= monthStart and currentMonth <= monthEnd:
# cover the fact semester B includes January of the next year
    if month == 14:
        if currentMonth == 1:
            year += 1
# compute the dates for this month.
    thisMonth = dnd.daysAndDates(currentMonth, year)
    thisMonth.numDaysInMonth = thisMonth.numberOfDaysInMonth()
    thisMonth.createDate()
    thisMonth.createJDates()
    dates = thisMonth.jDates