# Utilities file for CH_calculator.py. Contains random functions.

# ChangeLog:
# 2020-07-31    JLR     Created from original utilities.py
import astropy.time as Time
from astroplan import Observer


# converts a julian date fraction (ie. less than a day) into hours.
def convertJDtoHours(start, end):
    jdLength = end.jd - start.jd
    hours = jdLength*24.0
    return hours

# takes the site name and creates a class object. A location can be given instead of 
# a site (see utilities.py).
def createObservatory(siteName):
    location = EarthLocation.of_site(siteName)
    observatory = Observer(location=location, name="AAT", timezone="UTC")
    return observatory

# list of the months
def monthsList():
    optionsList = { 1: 'January', 
                    2: 'Febuary', 
                    3: 'March',
                    4: 'April',
                    5: 'May',
                    6: 'June',
                    7: 'July',
                    8: 'August',
                    9: 'September',
                    10: 'October',
                    11: 'November',
                    12: 'December',
                    13: 'Semester A',
                    14: 'Semester B'}